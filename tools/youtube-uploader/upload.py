#!/usr/bin/env python3
"""Jason's Consulting — 유튜브 자동 업로더.

구글 공식 OAuth 기기 인증(Device Flow)으로 로그인하고, YouTube Data API로
영상을 업로드한다. 비밀번호를 절대 다루지 않는다 — 최초 1회 화면에서
코드를 승인하면 토큰이 저장되어 이후 업로드는 완전 자동이다.

준비 (최초 1회, 약 10분 — README.md 참고):
  1. console.cloud.google.com 에서 프로젝트 생성
  2. "YouTube Data API v3" 사용 설정
  3. OAuth 클라이언트 ID 생성 — 유형: "TV 및 제한된 입력 장치"
  4. client_id / client_secret 을 이 폴더의 client_secret.json 에 저장:
     {"client_id": "...", "client_secret": "..."}

사용법:
  python3 upload.py                          # 기본: 15초 광고 영상 업로드
  python3 upload.py --video 경로 --title "제목" --privacy unlisted

토큰은 token.json 에 저장된다 (client_secret.json / token.json 은 gitignore 됨).
"""
import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
SCOPE = "https://www.googleapis.com/auth/youtube.upload"
DEVICE_CODE_URL = "https://oauth2.googleapis.com/device/code"
TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = ("https://www.googleapis.com/upload/youtube/v3/videos"
              "?uploadType=resumable&part=snippet,status")

DEFAULTS = {
    "video": str(ROOT / "tools/video-ad/jasons-ad-15s.mp4"),
    "title": "사장님 가게, 검색하면 뭐가 나오나요? #shorts",
    "description": (
        "검색해도 안 나오는 가게는, 없는 가게랑 같습니다.\n"
        "예약 버튼 달린 한 페이지 — 48시간이면 됩니다.\n"
        "내 가게 이름으로 무료 샘플부터 받아보세요:\n"
        "https://jasons-consulting.com/?utm_source=youtube&utm_medium=cpc&utm_campaign=landing-v1\n\n"
        "#소상공인 #자영업 #홈페이지제작 #랜딩페이지"
    ),
    "tags": ["소상공인", "자영업", "홈페이지제작", "랜딩페이지", "마케팅"],
    "privacy": "unlisted",
}


def die(msg: str) -> None:
    sys.exit(f"[중단] {msg}")


def load_client() -> dict:
    p = BASE / "client_secret.json"
    if not p.exists():
        die("client_secret.json 이 없습니다. README.md의 최초 1회 준비를 먼저 하세요.")
    c = json.loads(p.read_text())
    # 구글 콘솔에서 받은 원본 JSON({"installed": {...}}) 형태도 허용
    if "installed" in c:
        c = c["installed"]
    if not c.get("client_id") or not c.get("client_secret"):
        die("client_secret.json 에 client_id / client_secret 이 필요합니다.")
    return c


def device_flow_login(client: dict) -> dict:
    r = requests.post(DEVICE_CODE_URL, data={
        "client_id": client["client_id"], "scope": SCOPE}, timeout=30)
    if r.status_code != 200:
        die(f"기기 코드 발급 실패: {r.status_code} {r.text[:300]}")
    d = r.json()
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  브라우저에서 열기 : {d['verification_url']}")
    print(f"  입력할 코드      : {d['user_code']}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("위 주소에서 코드를 입력하고 이 계정으로 승인하세요. 대기 중...")

    deadline = time.time() + d["expires_in"]
    while time.time() < deadline:
        time.sleep(d.get("interval", 5))
        t = requests.post(TOKEN_URL, data={
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "device_code": d["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }, timeout=30)
        body = t.json()
        if t.status_code == 200:
            print("승인 완료. 토큰 저장.")
            return body
        if body.get("error") in ("authorization_pending", "slow_down"):
            continue
        die(f"승인 실패: {body.get('error')} — {body.get('error_description','')}")
    die("승인 시간 초과. 다시 실행하세요.")


def get_access_token(client: dict) -> str:
    tp = BASE / "token.json"
    if tp.exists():
        tok = json.loads(tp.read_text())
        if tok.get("refresh_token"):
            r = requests.post(TOKEN_URL, data={
                "client_id": client["client_id"],
                "client_secret": client["client_secret"],
                "refresh_token": tok["refresh_token"],
                "grant_type": "refresh_token"}, timeout=30)
            if r.status_code == 200:
                return r.json()["access_token"]
            print("저장된 토큰 만료 — 재로그인합니다.")
    tok = device_flow_login(client)
    tp.write_text(json.dumps(tok, indent=2))
    return tok["access_token"]


def upload(access_token: str, video: Path, title: str, desc: str,
           tags: list, privacy: str) -> None:
    meta = {
        "snippet": {"title": title, "description": desc, "tags": tags,
                    "categoryId": "22"},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    init = requests.post(UPLOAD_URL, headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(video.stat().st_size),
    }, json=meta, timeout=60)
    if init.status_code != 200:
        die(f"업로드 세션 생성 실패: {init.status_code} {init.text[:400]}")
    session_url = init.headers["Location"]

    print(f"업로드 중… ({video.stat().st_size/1e6:.1f} MB)")
    up = requests.put(session_url, headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "video/mp4",
    }, data=video.read_bytes(), timeout=600)
    if up.status_code not in (200, 201):
        die(f"업로드 실패: {up.status_code} {up.text[:400]}")
    v = up.json()
    vid = v["id"]
    status = v.get("status", {}).get("privacyStatus", "?")
    print("\n업로드 완료 ✓")
    print(f"  영상 URL   : https://youtu.be/{vid}")
    print(f"  공개 상태  : {status}")
    if status == "private" and DEFAULTS["privacy"] != "private":
        print("  [안내] 미검증 API 프로젝트의 업로드는 유튜브가 비공개로 잠급니다.")
        print("         스튜디오에서 수동으로 공개 전환하거나, API 감사(audit)를 신청하세요.")
    print("\n다음: 이 URL을 tools/ads-launcher/config.json 의 youtube_video_url 에 넣고")
    print("      launch/youtube-google-ads.md 시트대로 광고 캠페인에 연결하세요.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=DEFAULTS["video"])
    ap.add_argument("--title", default=DEFAULTS["title"])
    ap.add_argument("--description", default=DEFAULTS["description"])
    ap.add_argument("--privacy", default=DEFAULTS["privacy"],
                    choices=["public", "unlisted", "private"])
    args = ap.parse_args()

    video = Path(args.video)
    if not video.exists():
        die(f"영상 파일이 없습니다: {video}")

    client = load_client()
    token = get_access_token(client)
    upload(token, video, args.title, args.description,
           DEFAULTS["tags"], args.privacy)


if __name__ == "__main__":
    main()
