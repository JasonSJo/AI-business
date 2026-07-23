#!/usr/bin/env python3
"""Jason's Consulting — 배포용 사이트 빌더 (글로벌판).

demo/ 를 _site/ 로 모으고, 언어별 포트폴리오 허브를 생성한다:
  /        영어 허브 (미국 아웃바운드 착륙)
  /ja/     일본어 허브
  /kr/     한국어 허브
사용법:  python3 tools/build-site.py   (저장소 루트에서 실행 → _site/ 생성)
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"

CONTACT_EMAIL = "wheldfo23@gmail.com"
GOATCOUNTER_CODE = ""
CUSTOM_DOMAIN = ""  # DNS 전환 확인 후 "jasons-consulting.com" 으로 복원
SITE_URL = f"https://{CUSTOM_DOMAIN}" if CUSTOM_DOMAIN else "https://jasonsjo.github.io/AI-business"

DEMOS = [
    {"slug": "studio-en", "glyph": "W", "grad": "linear-gradient(150deg,#3F5138,#5E7351)",
     "en": ("Willow Pilates", "Pilates · Austin, TX", "1-on-1 studio — built to convert intro bookings"),
     "kr": ("Willow Pilates", "필라테스 · 오스틴(미국형)", "미국 시장용 영어 데모")},
    {"slug": "pilates-studio", "glyph": "高", "grad": "linear-gradient(150deg,#3F5138,#5E7351)",
     "en": ("Goyo Pilates", "Pilates · Seoul", "Korean-market sample — private studio"),
     "kr": ("고요 필라테스", "필라테스 · 성수", "1:1 프라이빗 스튜디오 — 체험 예약 전환 중심")},
    {"slug": "dental-clinic", "glyph": "笑", "grad": "linear-gradient(150deg,#1F5F55,#35796D)",
     "en": ("Bright Smile Dental", "Dental clinic · Seoul", "Korean-market sample — free checkup offer"),
     "kr": ("밝은미소 치과", "치과 · 마포", "무료 검진 오퍼와 정직 진료 포지셔닝")},
    {"slug": "hair-salon", "glyph": "溫", "grad": "linear-gradient(150deg,#6E3B4F,#8A5468)",
     "en": ("Salon de On", "Hair salon · Seoul", "Korean-market sample — booking-first salon"),
     "kr": ("살롱 드 온", "헤어살롱 · 연남", "얼굴형 진단 커트 — 첫 방문 할인 전환")},
    {"slug": "cafe", "glyph": "香", "grad": "linear-gradient(150deg,#4E342A,#6B4A3B)",
     "en": ("Cafe Hyang", "Cafe · Seoul", "Korean-market sample — subscriptions & bookings"),
     "kr": ("카페 향", "카페 · 망원", "원두 구독·단체석 대관 — 반복 매출 설계")},
]

LOCALES = {
    "en": {
        "path": "", "lang": "en", "demo_key": "en",
        "title": "Jason's Consulting — Booking-ready landing pages in 48 hours",
        "desc": "We build booking-ready landing pages for local businesses in 48 hours. Free sample first — pay only if you love it.",
        "eyebrow": "JASON'S CONSULTING",
        "h1": "A booking-ready page,<br>in 48 hours.",
        "lede": "Live demos below. We'll build a free sample with your business name — if you don't love it, you don't pay.",
        "pitch_h": "Want one with your name on it?",
        "pitch_p": "Send your business name and city. A free sample lands in your inbox within 48 hours.",
        "cta": "Request a free sample",
        "mail_subject": "Free%20sample%20request",
        "mail_body": "Business%20name%3A%20%0ACity%3A%20%0AWebsite%2FInstagram%3A%20",
        "email_note": "Email: __EMAIL__ · just your business name and city is enough",
        "foot": "© 2026 Jason's Consulting · Demo businesses are fictional",
        "switch": '<a href="ja/">日本語</a> · <a href="kr/">한국어</a>',
    },
    "ja": {
        "path": "ja/", "lang": "ja", "demo_key": "en",
        "title": "Jason's Consulting — 予約が入るLPを48時間で",
        "desc": "地域ビジネスのための予約特化ランディングページを48時間で制作。まず無料サンプル、気に入らなければ費用はかかりません。",
        "eyebrow": "JASON'S CONSULTING",
        "h1": "予約が入るページを、<br>48時間で。",
        "lede": "下記はデモです。貴店の名前で無料サンプルをお作りします — 気に入らなければ、お支払いは不要です。",
        "pitch_h": "貴店バージョンをご覧になりますか？",
        "pitch_p": "店名と所在地をお送りください。48時間以内に無料サンプルをお届けします。",
        "cta": "無料サンプルを依頼する",
        "mail_subject": "%E7%84%A1%E6%96%99%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%E4%BE%9D%E9%A0%BC",
        "mail_body": "%E5%BA%97%E5%90%8D%3A%20%0A%E6%89%80%E5%9C%A8%E5%9C%B0%3A%20%0AWeb%2FInstagram%3A%20",
        "email_note": "メール: __EMAIL__ · 店名と所在地だけで結構です",
        "foot": "© 2026 Jason's Consulting · デモの店舗は架空です",
        "switch": '<a href="../">English</a> · <a href="../kr/">한국어</a>',
    },
    "kr": {
        "path": "kr/", "lang": "ko", "demo_key": "kr",
        "title": "Jason's Consulting — 예약받는 랜딩페이지, 48시간",
        "desc": "예약·문의를 받는 랜딩페이지를 48시간 안에. 무료 샘플 먼저, 결제는 나중에.",
        "eyebrow": "JASON'S CONSULTING",
        "h1": "예약받는 랜딩페이지,<br>48시간 안에.",
        "lede": "아래는 업종별 데모입니다(가상 업체). 사장님 가게 이름으로 만든 샘플을 무료로 보여드립니다 — 마음에 안 들면 안 쓰셔도 됩니다.",
        "pitch_h": "내 가게 버전이 궁금하다면",
        "pitch_p": "업체명과 연락처만 알려주세요. 48시간 안에 샘플을 만들어 보내드립니다.",
        "cta": "무료 샘플 요청하기",
        "mail_subject": "%EB%9E%9C%EB%94%A9%ED%8E%98%EC%9D%B4%EC%A7%80%20%EC%83%98%ED%94%8C%20%EC%9A%94%EC%B2%AD",
        "mail_body": "%EC%97%85%EC%B2%B4%EB%AA%85%3A%20%0A%EC%97%85%EC%A2%85%3A%20%0A%EC%97%B0%EB%9D%BD%EC%B2%98%3A%20",
        "email_note": "이메일: __EMAIL__ · 업체명·업종만 보내주시면 됩니다",
        "foot": "© 2026 Jason's Consulting · 데모의 업체는 모두 가상입니다",
        "switch": '<a href="../">English</a> · <a href="../ja/">日本語</a>',
    },
}

HUB = """<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>__TITLE__</title>
<meta name="description" content="__DESC__" />
<meta property="og:type" content="website" />
<meta property="og:title" content="__TITLE__" />
<meta property="og:description" content="__DESC__" />
<meta property="og:image" content="__SITEURL__/assets/og-1200x630.png" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/png" href="__REL__assets/favicon-192.png" />
<link rel="apple-touch-icon" href="__REL__assets/favicon-192.png" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap" rel="stylesheet" />
<style>
  :root{--cream:#F4EFE6;--ink:#23281F;--soft:#4B4E42;--muted:#8A8474;--clay:#C0784F;--clay-d:#A5603A;--line:rgba(35,40,31,.12)}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Pretendard',sans-serif;background:var(--cream);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}
  .serif{font-family:'Gowun Batang',serif}
  .wrap{max-width:1020px;margin:0 auto;padding:0 22px}
  header{padding:70px 0 40px;text-align:center;position:relative}
  .lang{position:absolute;top:24px;right:22px;font-size:13px;color:var(--muted)}
  .lang a{color:var(--soft);text-decoration:none;font-weight:600}
  .lang a:hover{color:var(--clay-d)}
  .eyebrow{font-size:12.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--clay);font-weight:600}
  h1{font-size:clamp(30px,5vw,50px);line-height:1.15;margin-top:14px;letter-spacing:-.01em}
  .lede{margin:18px auto 0;max-width:56ch;color:var(--soft);font-size:16.5px}
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
  .mailnote{margin-top:14px;font-size:13px;color:var(--muted)}
  footer{text-align:center;color:var(--muted);font-size:12.5px;padding:0 0 46px}
</style>
</head>
<body>
<header class="wrap">
  <div class="lang">__SWITCH__</div>
  <div class="eyebrow">__EYEBROW__</div>
  <h1 class="serif">__H1__</h1>
  <p class="lede">__LEDE__</p>
</header>
<main class="wrap">
  <div class="grid">
__CARDS__
  </div>
  <div class="pitch">
    <h3 class="serif">__PITCH_H__</h3>
    <p>__PITCH_P__</p>
    <a class="cta" href="mailto:__EMAIL__?subject=__MSUBJ__&body=__MBODY__">__CTA__</a>
    <p class="mailnote">__EMAIL_NOTE__</p>
  </div>
</main>
<footer>__FOOT__</footer>
</body>
</html>
"""

CARD = """    <a class="card" href="__REL__{slug}/">
      <span class="thumb serif" style="background:{grad}">{glyph}</span>
      <span>
        <span class="ind">{ind}</span>
        <h2>{name}</h2>
        <p>{desc}</p>
      </span>
      <span class="go">→</span>
    </a>"""


def analytics_snippet() -> str:
    if not GOATCOUNTER_CODE:
        return ""
    return (f'<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count" '
            'async src="//gc.zgo.at/count.js"></script>')


def build_hub(loc: dict, missing: set, snippet: str) -> str:
    rel = "../" if loc["path"] else ""
    key = loc["demo_key"]
    cards = "\n".join(
        CARD.replace("__REL__", rel).format(slug=d["slug"], grad=d["grad"], glyph=d["glyph"],
                                            name=d[key][0], ind=d[key][1], desc=d[key][2])
        for d in DEMOS if d["slug"] not in missing)
    html = (HUB.replace("__LANG__", loc["lang"]).replace("__TITLE__", loc["title"])
            .replace("__DESC__", loc["desc"]).replace("__SITEURL__", SITE_URL)
            .replace("__REL__", rel).replace("__SWITCH__", loc["switch"])
            .replace("__EYEBROW__", loc["eyebrow"]).replace("__H1__", loc["h1"])
            .replace("__LEDE__", loc["lede"]).replace("__CARDS__", cards)
            .replace("__PITCH_H__", loc["pitch_h"]).replace("__PITCH_P__", loc["pitch_p"])
            .replace("__MSUBJ__", loc["mail_subject"]).replace("__MBODY__", loc["mail_body"])
            .replace("__CTA__", loc["cta"]).replace("__EMAIL_NOTE__", loc["email_note"])
            .replace("__EMAIL__", CONTACT_EMAIL).replace("__FOOT__", loc["foot"]))
    if snippet:
        html = html.replace("</body>", snippet + "\n</body>")
    return html


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / ".nojekyll").write_text("")
    if CUSTOM_DOMAIN:
        (SITE / "CNAME").write_text(CUSTOM_DOMAIN + "\n")

    snippet = analytics_snippet()
    missing = set()
    for d in DEMOS:
        src = ROOT / "demo" / d["slug"]
        if not (src / "index.html").exists():
            missing.add(d["slug"])
            continue
        shutil.copytree(src, SITE / d["slug"])
        if snippet:
            page = SITE / d["slug"] / "index.html"
            page.write_text(page.read_text(encoding="utf-8").replace(
                "</body>", snippet + "\n</body>"), encoding="utf-8")

    for name, loc in LOCALES.items():
        out = SITE / loc["path"] if loc["path"] else SITE
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(build_hub(loc, missing, snippet), encoding="utf-8")

    ad_video = ROOT / "tools/video-ad/jasons-ad-15s.mp4"
    if ad_video.exists():
        (SITE / "ad").mkdir(exist_ok=True)
        shutil.copy2(ad_video, SITE / "ad" / "jasons-ad-15s.mp4")

    brand = ROOT / "assets/brand"
    (SITE / "assets").mkdir(exist_ok=True)
    for n in ("og-1200x630.png", "favicon-192.png", "profile-1080.png"):
        if (brand / n).exists():
            shutil.copy2(brand / n, SITE / "assets" / n)

    print(f"빌드 완료: {SITE} (데모 {len(DEMOS) - len(missing)}종 + 허브 EN/JA/KR)")
    if missing:
        print(f"[경고] 누락 데모: {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
