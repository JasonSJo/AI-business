#!/usr/bin/env python3
"""Jason's Consulting — 광고 런처.

config.json의 값으로 유튜브(구글 애즈)·인스타(메타) 캠페인 실행 문서를 생성한다.
계정 로그인·결제는 본인만 할 수 있으므로, 그 외 전부(구조·타겟·예산·문구·소재·UTM)를
"열고 붙여넣기만 하면 되는" 상태로 만들어 두는 것이 이 도구의 역할이다.

사용법:
    python3 generate.py          # launch/ 폴더에 실행 문서 생성

외부 의존성 없음.
"""
import json
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent


def utm(url: str, source: str) -> str:
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={source}&utm_medium=cpc&utm_campaign=landing-v1"


def main() -> None:
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    out = BASE / "launch"
    out.mkdir(exist_ok=True)

    url = cfg["landing_url"]
    budget = f'{cfg["daily_budget_krw"]:,}'
    tg = cfg["targeting"]
    g, m = cfg["google"], cfg["meta"]

    # ── 1) 유튜브 (구글 애즈) ──────────────────────────────
    yt = f"""# 유튜브 광고 실행 시트 — {g["campaign_name"]}

> 아래 값을 화면에 그대로 붙여넣는다. 걸리는 시간: 계정 첫 생성 15분 + 캠페인 10분.

## A. 계정 만들기 (최초 1회, 본인만 가능)
1. ads.google.com → 구글 계정(유튜브와 같은 계정)으로 로그인 → "새 Google Ads 계정"
2. ⚠ 첫 화면의 "스마트 캠페인"은 건너뛰기 — 하단 "전문가 모드로 전환" 클릭
3. "캠페인 없이 계정 만들기" 선택 → 국가 대한민국 / 통화 KRW
4. 결제: 도구·설정 → 청구 → 결제 수단에 카드 등록
5. 유튜브 채널 연결: 도구·설정 → 연결된 계정 → YouTube → 내 채널 연결

## B. 소재 준비 (5분)
1. `{cfg["video_file"]}` 을 유튜브 채널에 업로드 — 공개 설정: **일부 공개(미등록)** 이면 충분
2. 업로드된 영상 URL을 `config.json` 의 `youtube_video_url` 에 기록
   - 현재 값: {cfg["youtube_video_url"]}

## C. 캠페인 만들기 (붙여넣기)
새 캠페인 → 목표 **"안내 없이 캠페인 만들기"** → 유형 **동영상** → 하위유형 **동영상 조회수 확보**

| 항목 | 값 |
|---|---|
| 캠페인 이름 | `{g["campaign_name"]}` |
| 입찰 | CPV (조회당비용) |
| 일일예산 | ₩{budget} |
| 네트워크 | YouTube 동영상 (검색·파트너 해제) |
| 위치 | {tg["location"]} |
| 언어 | {tg["language"]} |
| 잠재고객 · 연령 | {tg["age"]} |
| 관심분야 | {", ".join(tg["interests"])} |
| 게재 위치(선택) | YouTube Shorts 우선 노출 원하면 "Shorts" 게재면 선택 |

**광고 만들기**

| 항목 | 값 |
|---|---|
| 동영상 | (B에서 만든 유튜브 URL) |
| 최종 URL | `{utm(url, "youtube")}` |
| 클릭 유도 문구 | `{g["cta_button"]}` |
| 광고 제목 | `{g["headline"]}` |
| 긴 광고 제목 | `{g["long_headline"]}` |
| 설명 | `{g["description"]}` |

게시 → 심사는 보통 1영업일 이내.

## D. 게시 직후 할 일
- [ ] KPI 대시보드 메모 규칙: 유튜브발 문의 = 응답+1, 메모 "광고-유튜브"
- [ ] 2주 뒤 판단 (CPL 룰): 문의당 3만원 이하 → 증액 / 5만원 초과 지속 → 중단
"""

    # ── 2) 인스타그램 (메타) ──────────────────────────────
    ig = f"""# 인스타그램 광고 실행 시트 — {m["campaign_name"]}

> 아래 값을 화면에 그대로 붙여넣는다. 걸리는 시간: 계정 첫 생성 15분 + 캠페인 10분.

## A. 계정 만들기 (최초 1회, 본인만 가능)
1. 인스타그램 앱 → 설정 → 계정 유형 → **프로페셔널(비즈니스) 계정으로 전환**
2. business.facebook.com → 비즈니스 포트폴리오 만들기 → 인스타그램 계정 연결
3. 광고 관리자 (adsmanager.facebook.com) → 결제 수단에 카드 등록
4. 프로필 링크를 `{utm(url, "instagram-bio")}` 로 설정

## B. 소재 준비 (2분)
- 영상: `{cfg["video_file"]}` (1080×1920 · 15초 — 릴스 규격 그대로, 변환 불필요)

## C-1. 가장 쉬운 시작 — 릴스 부스트 (앱에서 3분)
1. 릴스로 영상 업로드 (캡션은 숏폼 가이드의 복붙 캡션 사용)
2. 게시물 하단 **"게시물 홍보하기"** → 목표 "웹사이트 방문 늘리기"
3. URL: `{utm(url, "instagram")}` / 버튼: {m["cta_button"]}
4. 타겟: 자동 또는 직접(연령 {tg["age"]}, 관심사 {", ".join(tg["interests"])})
5. 예산: 일 ₩{budget} × 7일

## C-2. 정식 캠페인 — 광고 관리자 (성과 확인 후 전환)

| 항목 | 값 |
|---|---|
| 캠페인 이름 | `{m["campaign_name"]}` |
| 목표 | 트래픽 (문의 잡히면 → 판매/리드로 전환) |
| 일일예산 | ₩{budget} |
| 위치 | {tg["location"]} |
| 연령 | {tg["age"]} |
| 관심사 | {", ".join(tg["interests"])} |
| 노출 위치 | 어드밴티지+ (자동) |

**광고 소재**

| 항목 | 값 |
|---|---|
| 형식 | 단일 동영상 (릴스 규격) |
| 영상 | jasons-ad-15s.mp4 업로드 |
| 기본 문구 | {m["primary_text"].replace(chr(10), " / ")} |
| 제목 | `{m["headline"]}` |
| 랜딩 URL | `{utm(url, "instagram")}` |
| 버튼 | {m["cta_button"]} |

## D. 게시 직후 할 일
- [ ] KPI 대시보드 메모 규칙: 인스타발 문의 = 응답+1, 메모 "광고-인스타"
- [ ] 2주 뒤 판단 (CPL 룰): 문의당 3만원 이하 → 증액 / 5만원 초과 지속 → 중단
"""

    # ── 3) 요약 체크리스트 ──────────────────────────────
    idx = f"""# 광고 런치 체크리스트

생성 기준 config: 일예산 ₩{budget} · 착륙 {url}

| 순서 | 할 일 | 소요 | 문서 |
|---|---|---|---|
| 1 | 구글 애즈 계정 생성 + 카드 등록 (본인) | 15분 | [유튜브 시트](youtube-google-ads.md) A |
| 2 | 15초 영상 유튜브 업로드(미등록) → config에 URL 기록 | 5분 | 〃 B |
| 3 | 유튜브 동영상 캠페인 붙여넣기 생성 | 10분 | 〃 C |
| 4 | 인스타 프로페셔널 전환 + 광고 계정 + 카드 (본인) | 15분 | [인스타 시트](instagram-meta.md) A |
| 5 | 릴스 업로드 → "게시물 홍보하기" 부스트 | 5분 | 〃 C-1 |
| 6 | 문의 오면 KPI 대시보드 기록 (광고-유튜브 / 광고-인스타) | 매일 | — |
| 7 | 2주 뒤 CPL 판단 → 증액/교체/중단 | 10분 | [광고 가이드](../../../docs/광고-세팅-가이드.md) |

값 수정 후 재생성: `python3 tools/ads-launcher/generate.py`
"""

    (out / "youtube-google-ads.md").write_text(yt, encoding="utf-8")
    (out / "instagram-meta.md").write_text(ig, encoding="utf-8")
    (out / "README.md").write_text(idx, encoding="utf-8")
    print(f"생성 완료: {out}/ (youtube-google-ads.md, instagram-meta.md, README.md)")


if __name__ == "__main__":
    main()
