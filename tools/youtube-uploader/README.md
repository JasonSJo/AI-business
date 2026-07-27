# 유튜브 자동 업로더

구글이 공식 허용하는 방식(OAuth 기기 인증 + YouTube Data API)으로 영상을 자동 업로드한다.
**비밀번호를 절대 사용하지 않는다** — 최초 1회 화면에서 코드를 승인하면 이후는 명령 한 줄로 업로드된다.

## ⚠ 먼저 알아야 할 제약

유튜브 정책상 **검증(audit)받지 않은 API 프로젝트로 올린 영상은 자동으로 "비공개"로 잠긴다.**
→ 올린 직후 유튜브 스튜디오에서 수동으로 "일부 공개/공개"로 바꾸거나(클릭 2번),
   [API 감사](https://support.google.com/youtube/contact/yt_api_form)를 신청해 잠금을 풀 수 있다(수일 소요).

그래서 **"오늘 첫 영상 하나"는 폰 업로드(3분)가 가장 빠르고**, 이 도구는
앞으로 영상을 반복 게시할 때(업종별 변형, 주 3회 콘텐츠) 진가를 발휘한다.

## 최초 1회 준비 (약 10분, 본인 계정으로)

1. [console.cloud.google.com](https://console.cloud.google.com) → 새 프로젝트 (이름: jasons-consulting)
2. "API 및 서비스" → 라이브러리 → **YouTube Data API v3** → 사용 설정
3. "OAuth 동의 화면" → 외부 → 앱 이름/이메일만 입력 → 테스트 사용자에 본인 지메일 추가
4. "사용자 인증 정보" → 사용자 인증 정보 만들기 → **OAuth 클라이언트 ID** → 유형: **"TV 및 제한된 입력 장치"**
5. 생성된 client_id / client_secret 을 이 폴더에 `client_secret.json` 으로 저장:

```json
{ "client_id": "xxx.apps.googleusercontent.com", "client_secret": "xxx" }
```

(구글이 주는 JSON 파일을 그대로 저장해도 된다 — `installed` 형태 지원)

## 업로드

```bash
cd tools/youtube-uploader
python3 upload.py
```

- 처음 실행하면 화면에 **주소 + 코드**가 뜬다 → 폰이나 브라우저에서 열어 코드 입력 → 본인 계정으로 승인
- 이후에는 저장된 토큰(`token.json`)으로 **묻지 않고 바로 업로드**된다
- 제목/설명/공개범위 변경: `python3 upload.py --title "..." --privacy unlisted`
- 기본값: 15초 광고 영상 + 쇼츠용 제목/설명/태그/UTM 링크 자동 포함

## 보안

- `client_secret.json` / `token.json` 은 `.gitignore` 처리되어 커밋되지 않는다
- 권한 범위는 `youtube.upload` 하나뿐 — 이 토큰으로는 업로드 외 어떤 것도 할 수 없다
- 연결 해제: [myaccount.google.com/permissions](https://myaccount.google.com/permissions) 에서 언제든 회수
