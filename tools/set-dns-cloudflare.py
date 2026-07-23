#!/usr/bin/env python3
"""Cloudflare DNS를 GitHub Pages로 자동 전환하는 스크립트.

jasons-consulting.com 존에서 @/www의 기존 A·AAAA·CNAME 레코드를 지우고
GitHub Pages용 레코드 5개(A×4 + CNAME www)를 DNS only로 생성한다.

사용법:
    export CF_API_TOKEN="..."   # Edit zone DNS 권한, 해당 존 한정 토큰
    python3 tools/set-dns-cloudflare.py            # 실제 적용
    python3 tools/set-dns-cloudflare.py --dry-run  # 삭제/생성 계획만 출력

토큰은 절대 파일로 저장하지 말 것 (환경변수로만 전달).
외부 의존성 없음 (표준 라이브러리만 사용).
"""
import json
import os
import sys
import urllib.request

ZONE_NAME = "jasons-consulting.com"
PAGES_A = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]
WWW_TARGET = "jasonsjo.github.io"
API = "https://api.cloudflare.com/client/v4"


def call(method: str, path: str, token: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if not data.get("success"):
        sys.exit(f"[오류] {method} {path}: {data.get('errors')}")
    return data


def main() -> None:
    dry = "--dry-run" in sys.argv
    token = os.environ.get("CF_API_TOKEN", "").strip()
    if not token:
        sys.exit("[오류] CF_API_TOKEN 환경변수가 비어 있습니다.\n"
                 "Cloudflare → My Profile → API Tokens → 'Edit zone DNS' 템플릿으로 만들어 주세요.")

    zones = call("GET", f"/zones?name={ZONE_NAME}", token)["result"]
    if not zones:
        sys.exit(f"[오류] 이 토큰으로 '{ZONE_NAME}' 존을 찾을 수 없습니다 (Zone Resources 확인).")
    zone_id = zones[0]["id"]
    print(f"존 확인: {ZONE_NAME} ({zone_id})")

    records = call("GET", f"/zones/{zone_id}/dns_records?per_page=100", token)["result"]
    targets = {ZONE_NAME, f"www.{ZONE_NAME}"}
    stale = [r for r in records if r["type"] in ("A", "AAAA", "CNAME") and r["name"] in targets]
    for r in stale:
        tag = "삭제 예정" if dry else "삭제"
        print(f"  {tag}: {r['type']:5} {r['name']} → {r['content']} "
              f"({'Proxied' if r.get('proxied') else 'DNS only'})")
        if not dry:
            call("DELETE", f"/zones/{zone_id}/dns_records/{r['id']}", token)

    new = [{"type": "A", "name": "@", "content": ip, "ttl": 1, "proxied": False} for ip in PAGES_A]
    new.append({"type": "CNAME", "name": "www", "content": WWW_TARGET, "ttl": 1, "proxied": False})
    for rec in new:
        tag = "생성 예정" if dry else "생성"
        print(f"  {tag}: {rec['type']:5} {rec['name']} → {rec['content']} (DNS only)")
        if not dry:
            call("POST", f"/zones/{zone_id}/dns_records", token, rec)

    if dry:
        print("dry-run 완료 — 실제 변경 없음.")
    else:
        print("전환 완료. 1~5분 후 dig/브라우저로 185.199.108~111.153 확인 → "
              "GitHub Settings→Pages에서 Custom domain 저장 + Enforce HTTPS.")


if __name__ == "__main__":
    main()
