#!/usr/bin/env python3
"""Jason's Consulting — 콜드 아웃리치 메시지 생성기.

리드 CSV를 읽어 업종·채널별 템플릿에 개인화 정보를 채워
발송 준비된 메시지를 대량 생성한다.

사용법:
    python3 generate.py leads.sample.csv --sender 제이슨
    python3 generate.py my-leads.csv --sender 제이슨 --demo-url https://demo.example.com

CSV 컬럼 (헤더 필수):
    business  업체명 (필수)
    owner     호칭 (비우면 "대표님")
    industry  dental | salon | cafe | pilates | 그 외 → default 템플릿
    channel   email | dm (비우면 email)
    observation  개인화 한 줄 — "리뷰가 200개인데 예약 링크가 없어서요" (필수에 가깝게 권장)
    contact   이메일/인스타 핸들 등 (출력에 메모로 표시)
    demo_url  이 리드에게 보여줄 데모 URL (비우면 --demo-url 값)

출력:
    out/NNN-업체명.txt  리드별 발송용 메시지
    out/전체목록.md     발송 체크리스트 (업체·채널·연락처·파일)

외부 의존성 없음 (표준 라이브러리만 사용).
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

# 업종 → 배포된 데모 경로 (--base-url 사용 시 자동 매핑)
DEMO_PATHS = {
    "dental": "dental-clinic/",
    "salon": "hair-salon/",
    "cafe": "cafe/",
    "pilates": "pilates-studio/",
    "us": "studio-en/",
    "jp": "studio-en/",
}


def safe_name(text: str) -> str:
    return re.sub(r'[\\/:*?"<>|\s]+', "-", text).strip("-") or "무제"


def josa(word: str, with_batchim: str, without_batchim: str) -> str:
    """단어 끝 받침 유무로 조사를 고른다 (한글이 아니면 병기)."""
    ch = word[-1] if word else ""
    if "가" <= ch <= "힣":
        return with_batchim if (ord(ch) - 0xAC00) % 28 else without_batchim
    return f"{with_batchim}({without_batchim})"


def pick_template(templates: dict, channel: str, industry: str) -> dict:
    ch = templates.get(channel) or templates["email"]
    return ch.get(industry) or ch.get("default") or templates["email"]["default"]


def fill(text: str, lead: dict, sender: str, demo_url: str) -> str:
    biz = lead["business"]
    mapping = {
        "업체명을": biz + josa(biz, "을", "를"),
        "업체명이": biz + josa(biz, "이", "가"),
        "업체명은": biz + josa(biz, "은", "는"),
        "업체명": biz,
        "대표님": lead.get("owner") or "대표님",
        "관찰": lead.get("observation") or "",
        "데모링크": lead.get("demo_url") or demo_url,
        "이름": sender,
    }
    # 긴 키부터 치환해 {업체명을}이 {업체명}보다 먼저 잡히게 한다
    for key in sorted(mapping, key=len, reverse=True):
        text = text.replace("{" + key + "}", mapping[key])
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description="콜드 아웃리치 메시지 생성기")
    ap.add_argument("csv_file", help="리드 CSV 파일")
    ap.add_argument("--sender", required=True, help="발신자 이름 (서명에 들어감)")
    ap.add_argument("--demo-url", default="(데모 URL을 넣으세요)",
                    help="기본 데모 링크 (리드별 demo_url 컬럼이 우선)")
    ap.add_argument("--base-url", default=None,
                    help="배포 사이트 루트 URL — 업종별 데모 경로를 자동으로 붙인다 "
                         "(예: https://jasonsjo.github.io/AI-business/)")
    ap.add_argument("--out", default=str(BASE / "out"), help="출력 폴더 (기본: out/)")
    args = ap.parse_args()

    templates = json.loads((BASE / "templates.json").read_text(encoding="utf-8"))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(open(args.csv_file, encoding="utf-8-sig")))
    if not rows:
        sys.exit("[오류] CSV에 리드가 없습니다.")

    index_lines = [
        "# 발송 체크리스트",
        "",
        "| # | 업체 | 채널 | 연락처 | 파일 | 발송 | 응답 |",
        "|---|---|---|---|---|---|---|",
    ]
    center_leads = []
    skipped = 0
    for i, lead in enumerate(rows, 1):
        business = (lead.get("business") or "").strip()
        if not business:
            skipped += 1
            continue
        lead = {k: (v or "").strip() for k, v in lead.items()}
        channel = lead.get("channel") or "email"
        industry = lead.get("industry") or "default"
        tpl = pick_template(templates, channel, industry)

        # 데모 링크 우선순위: 리드별 demo_url > base_url+업종경로 > --demo-url
        demo_url = args.demo_url
        if args.base_url:
            demo_url = args.base_url.rstrip("/") + "/" + DEMO_PATHS.get(industry, "")

        subject = fill(tpl.get("subject", ""), lead, args.sender, demo_url)
        body = fill(tpl["body"], lead, args.sender, demo_url)

        parts = [f"[받는 곳] {lead.get('contact') or '(연락처 미입력)'}",
                 f"[채널] {channel} / [업종 템플릿] {industry}"]
        if not lead.get("observation"):
            parts.append("[주의] observation(개인화 한 줄)이 비어 있습니다 — 채워서 보내세요!")
        if subject:
            parts.append(f"\n제목: {subject}")
        parts.append(f"\n{body}")

        fname = f"{i:03d}-{safe_name(business)}.txt"
        (out_dir / fname).write_text("\n".join(parts), encoding="utf-8")
        index_lines.append(
            f"| {i} | {business} | {channel} | {lead.get('contact') or '-'} | {fname} | ☐ | ☐ |"
        )
        center_leads.append({
            "business": business,
            "contact": lead.get("contact") or "",
            "channel": channel,
            "subject": subject,
            "body": body,
            "warn": not lead.get("observation"),
        })

    (out_dir / "전체목록.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # 발송 센터 HTML — 클릭 발송(mailto)/복사 + 완료 체크 + KPI 내보내기
    center_tpl = (BASE / "send-center-template.html").read_text(encoding="utf-8")
    today = __import__("datetime").date.today().isoformat()
    center = (center_tpl
              .replace("__DATA__", json.dumps(center_leads, ensure_ascii=False))
              .replace("__DATE__", today))
    (out_dir / "발송센터.html").write_text(center, encoding="utf-8")

    made = len(rows) - skipped
    print(f"생성 완료: {made}건 → {out_dir}/")
    if skipped:
        print(f"건너뜀: 업체명 없는 행 {skipped}건")
    print(f"발송 체크리스트: {out_dir / '전체목록.md'}")
    print(f"발송 센터:      {out_dir / '발송센터.html'}  ← 브라우저로 여세요")


if __name__ == "__main__":
    main()
