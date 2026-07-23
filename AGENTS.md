# AGENTS.md — AI 에이전트 작업 안내

이 저장소는 **Jason's Consulting**(1인 랜딩페이지 제작 사업)의 수익화 시스템 전체다.
데모 생성 → 사이트 배포 → 콜드 아웃리치 → KPI 추적이 모두 코드로 관리된다.
여기서 작업하는 모든 AI 에이전트(Claude, Codex 등)는 아래 규칙을 지킨다.

## 절대 규칙 (어기면 실제 피해 발생)

1. **비밀·개인정보 커밋 금지.** `.gitignore`에 있는 것들은 이유가 있다:
   - `tools/cold-email-generator/*.csv` — 실제 영업 리드(개인정보). `leads.sample.csv`만 커밋 가능
   - `tools/cold-email-generator/out/` — 생성된 발송 메시지
   - `tools/youtube-uploader/client_secret.json`, `token.json` — Google OAuth 자격증명
   - API 토큰·비밀번호는 어떤 파일에도 저장하지 않는다 (환경변수로만)
2. **`demo/**` 또는 `tools/build-site.py`를 건드리는 push는 실서비스 배포를 트리거한다**
   (`.github/workflows/deploy-demos.yml` → GitHub Pages). 확신 없으면 해당 경로를 커밋에서 빼라.
3. **`tools/build-site.py`의 `CUSTOM_DOMAIN`** 은 도메인 전환 상태와 연동된다.
   빈 문자열이면 github.io로, `"jasons-consulting.com"`이면 커스텀 도메인으로 배포된다.
   DNS가 GitHub Pages(185.199.108~111.153)를 가리키기 전에 값을 채우면 **발송된 링크가 전부 깨진다.**
4. 데모 페이지의 업체는 전부 **가상**이다. 실존 업체명·전화번호·주소를 데모에 넣지 마라.
5. 콜드메일 템플릿(`tools/cold-email-generator/templates.json`)의 **수신거부 문구를 지우지 마라**
   (미국 CAN-SPAM, 일본 特定電子メール法 준수 문구다).

## 구조와 명령어

```bash
# 랜딩페이지 데모 생성 (config JSON → demo/<slug>/index.html)
python3 tools/landing-generator/generate.py tools/landing-generator/configs/<name>.json

# 사이트 전체 빌드 (demo/* + 3개 국어 허브 → _site/)
python3 tools/build-site.py

# 콜드 아웃리치 메시지 생성 (리드 CSV → out/…/발송센터.html)
cd tools/cold-email-generator && python3 generate.py <leads.csv> --sender Jason \
  --base-url https://jasons-consulting.com/ --out out/global

# 전체 파이프라인 (데모 → 빌드 → 아웃리치)
python3 pipeline.py

# 도메인 일괄 교체 (구 host → 신 host 치환 + CUSTOM_DOMAIN 설정 + 재생성)
python3 tools/set-domain.py <new-domain>
```

- `tools/landing-generator/` — `template.html`의 `{{PLACEHOLDER}}`를 config 값으로 치환.
  **치환되지 않은 플레이스홀더가 남으면 생성기가 에러로 멈춘다** — 템플릿에 플레이스홀더를
  추가하면 `generate.py`의 mapping과 모든 config에 함께 추가할 것.
- `tools/build-site.py` — `DEMOS`(데모 목록)와 `LOCALES`(en/ja/kr 허브 문자열).
  데모 추가 시 두 곳 모두 갱신. ja 로케일은 `d.get("ja") or d["en"]` 폴백을 쓴다.
- `demo/` — 생성 결과물. **직접 수정하지 말고** config를 고쳐 재생성하라.
- `docs/` — 운영 가이드(로드맵, 결제, 광고, 글로벌 아웃바운드 등). 한국어.
- `tools/kpi-dashboard/`, `tools/lead-collector/`, `tools/invoice/` — localStorage 기반 단일 HTML 도구.

## Git 규칙

- 현재 작업 브랜치: `claude/video-content-monetization-idjfzc` (Claude 전용).
  **다른 에이전트는 자기 브랜치를 새로 만들어 작업**하고, 같은 브랜치에 섞어 푸시하지 마라.
- push 전 반드시 `git pull --rebase origin <branch>` — 여러 에이전트가 병행 작업 중이다.
- 커밋 메시지는 영어 제목 + 필요시 본문. 데모/사이트 변경은 배포됨을 감안해 검증 후 커밋.

## 관련 외부 자산

- Codex(ChatGPT Sites)로 제작한 메인 사이트(OpenAI 호스팅, 삭제 금지):
  https://jasons-consulting-ai.rsr8f9vz55.chatgpt.site/
  — 사용자 결정(2026-07-23): **두 사이트를 함께 사용한다.**
  `jasons-consulting.com` = Codex 사이트 (Porkbun DNS: A @ 162.159.143.30 / 172.66.3.26,
  ChatGPT Sites 커스텀 도메인 값), 데모 포트폴리오 = github.io 기본 주소로 서비스.
  `CUSTOM_DOMAIN`은 빈 문자열로 유지한다 — 사용자 지시 없이 바꾸지 마라.

## 현재 상태 (2026-07-23)

- 데모 포트폴리오(3개 국어 허브 + 데모 6종)는 https://jasonsjo.github.io/AI-business
  로 서비스한다. 메인 도메인은 Codex 사이트(위 "관련 외부 자산" 참고).
- 아웃리치 메시지의 데모 링크는 github.io, 회사 소개 링크는 jasons-consulting.com 을 쓴다.
- 아웃바운드: 국내 인스타 DM 진행 중, 미국·일본 이메일은 리드 12건 생성 완료(발송 전).

## 디자인 시스템

"온기 기하학": cream `#F4EFE6`, ink `#23281F`, pine `#3F5138`, clay `#C0784F`.
서체 Gowun Batang(제목 serif) + Pretendard(본문) + DM Mono(숫자/코드).
새 페이지·자산을 만들 때 이 팔레트를 벗어나지 마라. 상세: `tools/brand-assets/design-philosophy.md`
