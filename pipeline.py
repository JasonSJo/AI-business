#!/usr/bin/env python3
"""Jason's Consulting — 수익화 파이프라인 (원커맨드).

영상 기반 수익화 워크플로 전체를 한 번에 실행한다:

  1. 랜딩페이지 데모 재생성   (tools/landing-generator)
  2. 배포용 사이트 빌드       (tools/build-site.py → _site/, 푸시하면 Pages 자동 배포)
  3. 아웃리치 메시지 생성     (tools/cold-email-generator → 발송센터.html 포함)
  4. 다음 액션 안내

사용법:
    python3 pipeline.py                                    # 데모 + 사이트만
    python3 pipeline.py --leads my-leads.csv --sender 제이슨   # 아웃리치까지
    python3 pipeline.py --leads my-leads.csv --sender 제이슨 \
        --base-url https://jasons-consulting.com/

외부 의존성 없음.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES_URL = "https://jasons-consulting.com/"


def run(title: str, cmd: list[str], cwd: Path) -> bool:
    print(f"\n━━ {title}")
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode != 0:
        print(f"[실패] {title} — 위 출력을 확인하세요")
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="수익화 파이프라인")
    ap.add_argument("--leads", help="리드 CSV 경로 (지정하면 아웃리치 생성까지 실행)")
    ap.add_argument("--sender", default="제이슨", help="발신자 이름 (기본: 제이슨)")
    ap.add_argument("--base-url", default=PAGES_URL,
                    help=f"배포된 사이트 루트 (기본: {PAGES_URL})")
    ap.add_argument("--skip-demos", action="store_true", help="데모 재생성 건너뛰기")
    args = ap.parse_args()

    ok = True

    if not args.skip_demos:
        gen = ROOT / "tools/landing-generator"
        configs = sorted(str(p) for p in (gen / "configs").glob("*.json"))
        ok &= run("1/3 랜딩페이지 데모 재생성",
                  [sys.executable, "generate.py", *configs], gen)

    ok &= run("2/3 배포용 사이트 빌드 (_site/)",
              [sys.executable, "tools/build-site.py"], ROOT)

    if args.leads:
        leads = Path(args.leads).resolve()
        if not leads.exists():
            print(f"[실패] 리드 파일이 없습니다: {leads}")
            ok = False
        else:
            ok &= run("3/3 아웃리치 메시지 + 발송 센터 생성",
                      [sys.executable, "generate.py", str(leads),
                       "--sender", args.sender, "--base-url", args.base_url],
                      ROOT / "tools/cold-email-generator")
    else:
        print("\n━━ 3/3 아웃리치 생성 건너뜀 (--leads 미지정)")

    print("\n" + "═" * 52)
    if not ok:
        sys.exit("일부 단계가 실패했습니다. 위 로그를 확인하세요.")
    print("파이프라인 완료. 다음 액션:")
    print(f"  1. git push → GitHub Actions가 데모를 자동 배포 ({args.base_url})")
    if args.leads:
        print("  2. tools/cold-email-generator/out/발송센터.html 을 브라우저로 열어 발송")
        print("  3. 발송 후 '완료분 KPI JSON 내보내기' → 대시보드 'JSON 가져오기'로 기록")
    else:
        print("  2. 리드 CSV를 만들고 다시 실행: python3 pipeline.py --leads 파일.csv")
    print("  · tools/kpi-dashboard/index.html 에서 주간 병목 확인")


if __name__ == "__main__":
    main()
