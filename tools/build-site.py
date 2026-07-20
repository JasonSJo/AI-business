#!/usr/bin/env python3
"""Jason's Consulting — 배포용 사이트 빌더 (Pages 자동 배포용).

demo/ 폴더의 데모들을 _site/로 모으고, 포트폴리오 허브(index.html)를 생성한다.
GitHub Actions(Pages 배포)와 로컬 미리보기 양쪽에서 쓴다.

사용법:
    python3 tools/build-site.py            # 저장소 루트에서 실행 → _site/ 생성 (Pages 워크플로가 사용)
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"

DEMOS = [
    {"slug": "pilates-studio", "name": "고요 필라테스", "industry": "필라테스 · 성수", "glyph": "高",
     "grad": "linear-gradient(150deg,#3F5138,#5E7351)", "desc": "1:1 프라이빗 스튜디오 — 체험 예약 전환 중심"},
    {"slug": "dental-clinic", "name": "밝은미소 치과", "industry": "치과 · 마포", "glyph": "笑",
     "grad": "linear-gradient(150deg,#1F5F55,#35796D)", "desc": "무료 검진 오퍼와 정직 진료 포지셔닝"},
    {"slug": "hair-salon", "name": "살롱 드 온", "industry": "헤어살롱 · 연남", "glyph": "溫",
     "grad": "linear-gradient(150deg,#6E3B4F,#8A5468)", "desc": "얼굴형 진단 커트 — 첫 방문 할인 전환"},
    {"slug": "cafe", "name": "카페 향", "industry": "카페 · 망원", "glyph": "香",
     "grad": "linear-gradient(150deg,#4E342A,#6B4A3B)", "desc": "원두 구독·단체석 대관 — 반복 매출 설계"},
]

HUB = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Jason's Consulting — 소상공인 랜딩페이지 포트폴리오</title>
<meta name="description" content="예약·문의를 받는 랜딩페이지를 48시간 안에. 업종별 실제 데모를 확인하세요." />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap" rel="stylesheet" />
<style>
  :root{--cream:#F4EFE6;--ink:#23281F;--soft:#4B4E42;--muted:#8A8474;--clay:#C0784F;--clay-d:#A5603A;--line:rgba(35,40,31,.12)}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Pretendard',sans-serif;background:var(--cream);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}
  .serif{font-family:'Gowun Batang',serif}
  .wrap{max-width:1020px;margin:0 auto;padding:0 22px}
  header{padding:80px 0 40px;text-align:center}
  .eyebrow{font-size:12.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--clay);font-weight:600}
  h1{font-size:clamp(30px,5vw,50px);line-height:1.15;margin-top:14px;letter-spacing:-.01em}
  .lede{margin:18px auto 0;max-width:52ch;color:var(--soft);font-size:16.5px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:30px 0 10px}
  @media(max-width:760px){.grid{grid-template-columns:1fr}}
  a.card{display:flex;gap:18px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;
    text-decoration:none;color:inherit;transition:.3s;box-shadow:0 14px 40px -22px rgba(35,40,31,.25)}
  a.card:hover{transform:translateY(-4px);box-shadow:0 22px 50px -22px rgba(35,40,31,.35)}
  .thumb{width:76px;height:96px;border-radius:12px;flex-shrink:0;display:grid;place-items:center;color:rgba(255,255,255,.85);
    font-family:'Gowun Batang',serif;font-size:34px}
  .card h2{font-family:'Gowun Batang',serif;font-size:20px}
  .card .ind{font-size:12.5px;color:var(--clay);font-weight:600;letter-spacing:.06em;margin-bottom:4px}
  .card p{font-size:13.5px;color:var(--muted);margin-top:6px}
  .card .go{margin-left:auto;color:var(--muted);font-size:20px}
  .pitch{background:#fff;border:1px solid var(--line);border-radius:20px;padding:34px;margin:26px 0 60px;text-align:center}
  .pitch h3{font-family:'Gowun Batang',serif;font-size:24px}
  .pitch p{color:var(--soft);margin-top:10px;font-size:15px}
  .cta{display:inline-block;margin-top:20px;background:var(--clay);color:#fff;font-weight:600;padding:14px 30px;border-radius:100px;text-decoration:none;transition:.25s}
  .cta:hover{background:var(--clay-d)}
  footer{text-align:center;color:var(--muted);font-size:12.5px;padding:0 0 46px}
</style>
</head>
<body>
<header class="wrap">
  <div class="eyebrow">Jason's Consulting</div>
  <h1 class="serif">예약받는 랜딩페이지,<br>48시간 안에.</h1>
  <p class="lede">아래는 업종별 데모입니다(가상 업체). 사장님 가게 이름으로 만든 샘플을 무료로 보여드립니다 — 마음에 안 들면 안 쓰셔도 됩니다.</p>
</header>
<main class="wrap">
  <div class="grid">
__CARDS__
  </div>
  <div class="pitch">
    <h3 class="serif">내 가게 버전이 궁금하다면</h3>
    <p>업체명과 연락처만 알려주세요. 48시간 안에 샘플을 만들어 보내드립니다.</p>
    <a class="cta" href="mailto:hello@example.com?subject=%EB%9E%9C%EB%94%A9%ED%8E%98%EC%9D%B4%EC%A7%80%20%EC%83%98%ED%94%8C%20%EC%9A%94%EC%B2%AD">무료 샘플 요청하기</a>
  </div>
</main>
<footer>© 2026 Jason's Consulting · 데모의 업체는 모두 가상입니다</footer>
</body>
</html>
"""

CARD = """    <a class="card" href="{slug}/">
      <span class="thumb serif" style="background:{grad}">{glyph}</span>
      <span>
        <span class="ind">{industry}</span>
        <h2>{name}</h2>
        <p>{desc}</p>
      </span>
      <span class="go">→</span>
    </a>"""


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / ".nojekyll").write_text("")

    missing = []
    for d in DEMOS:
        src = ROOT / "demo" / d["slug"]
        if not (src / "index.html").exists():
            missing.append(d["slug"])
            continue
        shutil.copytree(src, SITE / d["slug"])

    cards = "\n".join(CARD.format(**d) for d in DEMOS if d["slug"] not in missing)
    (SITE / "index.html").write_text(HUB.replace("__CARDS__", cards), encoding="utf-8")

    print(f"빌드 완료: {SITE} (데모 {len(DEMOS) - len(missing)}종 + 허브)")
    if missing:
        print(f"[경고] 누락된 데모: {', '.join(missing)} — tools/landing-generator로 먼저 생성하세요")


if __name__ == "__main__":
    main()
