#!/usr/bin/env python3
"""커스텀 도메인 전환 스크립트.

새 도메인 하나만 넣으면 저장소 전체의 사이트 URL을 일괄 교체하고,
배포 빌드에 CNAME을 포함시킨다. 이후 push 하면 새 도메인으로 서비스된다.

사용법 (저장소 루트에서):
    python3 tools/set-domain.py jasonsconsulting.kr

교체 범위:
    - tools/build-site.py         (CUSTOM_DOMAIN + og/파비콘 절대 URL)
    - tools/landing-generator/template.html  (데모 og:image)
    - tools/ads-launcher/config.json         (광고 착륙 URL)
    - tools/youtube-uploader/upload.py       (영상 설명 링크)
    - docs/*.md, README.md, pipeline.py      (문서·UTM 링크)
그 후: 데모 재생성 + 사이트 재빌드까지 자동 실행.

되돌리기: python3 tools/set-domain.py jasonsjo.github.io/AI-business
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_HOSTS = [
    "jasonsjo.github.io/AI-business",  # 기본 Pages 주소
]

TARGETS = [
    "tools/build-site.py",
    "tools/landing-generator/template.html",
    "tools/ads-launcher/config.json",
    "tools/youtube-uploader/upload.py",
    "tools/cold-email-generator/README.md",
    "tools/lead-collector/index.html",
    "README.md",
    "pipeline.py",
] + [str(p.relative_to(ROOT)) for p in (ROOT / "docs").glob("*.md")]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    domain = sys.argv[1].strip().rstrip("/")
    domain = re.sub(r"^https?://", "", domain)
    is_pages_default = domain.startswith("jasonsjo.github.io")

    # 이전에 설정된 커스텀 도메인도 교체 대상에 포함
    m = re.search(r'CUSTOM_DOMAIN = "([^"]*)"', (ROOT / "tools/build-site.py").read_text())
    if m and m.group(1):
        OLD_HOSTS.append(m.group(1))

    changed = 0
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            continue
        text = orig = p.read_text(encoding="utf-8")
        for old in OLD_HOSTS:
            if old == domain:
                continue
            text = text.replace(f"https://{old}/", f"https://{domain}/")
            text = text.replace(f"https://{old}", f"https://{domain}")
            text = text.replace(old, domain)
        if text != orig:
            p.write_text(text, encoding="utf-8")
            changed += 1
            print(f"교체: {rel}")

    # build-site.py 의 CUSTOM_DOMAIN 설정 (기본 Pages 주소면 비움)
    bs = ROOT / "tools/build-site.py"
    val = "" if is_pages_default else domain
    bs.write_text(re.sub(r'CUSTOM_DOMAIN = "[^"]*"', f'CUSTOM_DOMAIN = "{val}"',
                         bs.read_text(encoding="utf-8")), encoding="utf-8")

    print(f"\n{changed}개 파일 교체 완료. 데모·사이트 재생성 중...")
    gen = ROOT / "tools/landing-generator"
    configs = sorted(str(c) for c in (gen / "configs").glob("*.json"))
    subprocess.run([sys.executable, "generate.py", *configs], cwd=gen, check=True)
    subprocess.run([sys.executable, "tools/build-site.py"], cwd=ROOT, check=True)

    print(f"""
완료. 다음 순서:
  1. git add -A && git commit && git push  → 자동 배포
  2. GitHub Settings → Pages → Custom domain 에 `{domain}` 입력 → Save
  3. 도메인 구매처 DNS 에 레코드 입력:
     A     @    185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153
     CNAME www  jasonsjo.github.io
  4. 인증서 발급(최대 24시간) 후 Settings → Pages 에서 "Enforce HTTPS" 체크
  5. 유튜브 영상 설명·인스타 프로필 링크도 새 도메인으로 수동 갱신
""")


if __name__ == "__main__":
    main()
