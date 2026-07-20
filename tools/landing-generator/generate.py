#!/usr/bin/env python3
"""Jason's Consulting — 랜딩페이지 생성기.

고객 정보 JSON config를 읽어 template.html에서 랜딩페이지를 생성한다.

사용법:
    python3 generate.py configs/dental-clinic.json
    python3 generate.py configs/*.json          # 여러 개 한 번에

외부 의존성 없음 (표준 라이브러리만 사용).
"""
import json
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent

# why 카드에서 쓸 수 있는 아이콘 프리셋 (24x24 stroke SVG)
ICONS = {
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "heart": '<path d="M12 21s-7-4.35-9.5-8.5C.5 9 2.5 5 6 5c2 0 3.5 1.5 6 4 2.5-2.5 4-4 6-4 3.5 0 5.5 4 3.5 7.5C19 16.65 12 21 12 21z"/>',
    "align": '<path d="M12 3v18M5 8l7-5 7 5M5 8v8l7 5 7-5V8"/>',
    "shield": '<path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z"/>',
    "star": '<path d="M12 2l3 6.5 7 .8-5.2 4.8 1.4 7L12 17.5 5.8 21l1.4-7L2 9.3l7-.8L12 2z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "sparkle": '<path d="M12 2l2 7 7 3-7 3-2 7-2-7-7-3 7-3 2-7z"/>',
    "coffee": '<path d="M4 8h13v7a5 5 0 01-5 5H9a5 5 0 01-5-5V8z"/><path d="M17 9h2a2.5 2.5 0 010 5h-2M8 2v3M12 2v3"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.2 7.8L21 20M8.2 16.2L21 4"/>',
    "cross": '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6V3z"/>',
    "leaf": '<path d="M4 20C4 9 10 4 21 4c0 11-5 17-16 17"/><path d="M4 20c4-6 8-9 13-11"/>',
    "chat": '<path d="M21 12a8 8 0 01-8 8H4l2-3.5A8 8 0 1121 12z"/>',
}

ICON_WRAP = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" '
             'stroke="currentColor" stroke-width="1.8">{body}</svg>')


def icon(name: str) -> str:
    body = ICONS.get(name, ICONS["star"])
    return ICON_WRAP.format(body=body)


def render_marquee(items: list[str]) -> str:
    spans = "".join(f"<span>· {escape(t)}</span>" for t in items)
    # 무한 슬라이드용으로 두 번 반복
    return f"    {spans}\n    {spans}"


def render_why_cards(cards: list[dict]) -> str:
    out = []
    for i, c in enumerate(cards):
        delay = f' style="transition-delay:.{i * 8:02d}s"' if i else ""
        out.append(f'''      <div class="why-card reveal"{delay}>
        <span class="num serif">{i + 1:02d}</span>
        <div class="ico">{icon(c.get("icon", "star"))}</div>
        <h3>{escape(c["title"])}</h3>
        <p>{escape(c["desc"])}</p>
      </div>''')
    return "\n".join(out)


def render_plans(plans: list[dict]) -> str:
    out = []
    for i, p in enumerate(plans):
        cls = "plan featured" if p.get("featured") else "plan"
        delay = f' style="transition-delay:.{i * 8:02d}s"' if i else ""
        pill = f'<span class="pill">{escape(p["pill"])}</span>\n            ' if p.get("pill") else ""
        items = "\n              ".join(f"<li>{escape(x)}</li>" for x in p["items"])
        out.append(f'''          <div class="{cls} reveal"{delay}>
            {pill}<div class="tier">{escape(p["tier"])}</div>
            <div class="plan-price serif">{escape(p["price"])}<span class="per"> {escape(p["per"])}</span></div>
            <ul>
              {items}
            </ul>
            <a href="#location" class="btn btn-plan">{escape(p["cta"])}</a>
          </div>''')
    return "\n".join(out)


def render_reviews(items: list[dict]) -> str:
    out = []
    for i, r in enumerate(items):
        delay = f' style="transition-delay:.{i * 8:02d}s"' if i else ""
        out.append(f'''      <div class="rev reveal"{delay}>
        <div class="stars">★★★★★</div>
        <p class="q">“{escape(r["quote"])}”</p>
        <div class="who"><span class="av serif">{escape(r["initial"])}</span>
          <div><div class="nm">{escape(r["name"])}</div><div class="mt">{escape(r["meta"])}</div></div>
        </div>
      </div>''')
    return "\n".join(out)


def render_loc_rows(rows: list[dict]) -> str:
    return "\n".join(
        f'      <div class="loc-row"><span class="k">{escape(r["k"])}</span>'
        f'<span class="v">{escape(r["v"])}</span></div>'
        for r in rows
    )


def build(cfg_path: Path) -> Path:
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    tpl = (BASE / "template.html").read_text(encoding="utf-8")

    theme = cfg["theme"]
    hero = cfg["hero"]
    contact = cfg["contact"]

    mapping = {
        "TITLE": cfg["meta"]["title"],
        "META_DESC": cfg["meta"]["description"],
        "BRAND_NAME": cfg["brand"]["name"],
        "BRAND_MARK": cfg["brand"]["mark"],
        "NAV_WHY": cfg.get("nav", {}).get("why", "소개"),
        "NAV_PRICE": cfg.get("nav", {}).get("price", "가격"),
        "NAV_CTA": cfg.get("nav", {}).get("cta", "예약하기"),
        "C_CREAM": theme["cream"],
        "C_CREAM_DEEP": theme["cream_deep"],
        "C_INK": theme["ink"],
        "C_INK_SOFT": theme["ink_soft"],
        "C_PRIMARY": theme["primary"],
        "C_PRIMARY_LIGHT": theme["primary_light"],
        "C_ACCENT": theme["accent"],
        "C_ACCENT_DEEP": theme["accent_deep"],
        "C_MUTED": theme["muted"],
        "HERO_EYEBROW": hero["eyebrow"],
        "HERO_HEADLINE": hero["headline"],  # <em>·<br> 허용 (escape 안 함)
        "HERO_LEDE": hero["lede"],
        "HERO_CTA_PRIMARY": hero["cta_primary"],
        "HERO_CTA_SECONDARY": hero.get("cta_secondary", "둘러보기"),
        "HERO_TRUST": hero["trust"],  # <strong> 허용
        "BADGE1_N": hero["badge1_n"],
        "BADGE1_T": hero["badge1_t"],
        "BADGE2_T": hero.get("badge2", "오늘 예약 가능"),
        "CARD_GLYPH": hero["card_glyph"],
        "CARD_SM": hero["card_sm"],
        "CARD_LG": hero["card_lg"],
        "MARQUEE_ITEMS": render_marquee(cfg["marquee"]),
        "WHY_TAG": cfg["why"]["tag"],
        "WHY_TITLE": cfg["why"]["title"],
        "WHY_SUB": cfg["why"]["sub"],
        "WHY_CARDS": render_why_cards(cfg["why"]["cards"]),
        "PRICE_TAG": cfg["pricing"]["tag"],
        "PRICE_TITLE": cfg["pricing"]["title"],
        "PLANS": render_plans(cfg["pricing"]["plans"]),
        "REVIEWS_TAG": cfg["reviews"].get("tag", "Reviews"),
        "REVIEWS_TITLE": cfg["reviews"]["title"],
        "REVIEWS_SUB": cfg["reviews"]["sub"],
        "REVIEWS": render_reviews(cfg["reviews"]["items"]),
        "LOC_TITLE": cfg["location"]["title"],
        "LOC_ROWS": render_loc_rows(cfg["location"]["rows"]),
        "PHONE": contact["phone"],
        "PHONE_TEL": contact["tel"],
        "KAKAO_URL": contact.get("kakao_url", "#"),
        "KAKAO_LABEL": contact.get("kakao_label", ""),
        "BOOK_URL": contact.get("book_url", "#price"),
        "HOURS": contact.get("hours", ""),
        "CTA_BAR_BOOK": cfg.get("cta_bar_book", "예약하기"),
        "FOOT_NOTE": cfg["footer"]["note"],
    }

    html = tpl
    for key, val in mapping.items():
        html = html.replace("{{" + key + "}}", str(val))

    leftovers = [t for t in html.split("{{")[1:] if "}}" in t]
    if leftovers:
        names = ", ".join(t.split("}}")[0] for t in leftovers)
        raise SystemExit(f"[오류] 치환되지 않은 플레이스홀더: {names}")

    out_dir = (cfg_path.parent / cfg["output"]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")
    return out_file


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for arg in sys.argv[1:]:
        out = build(Path(arg))
        print(f"생성 완료: {out}")


if __name__ == "__main__":
    main()
