# Jason's Consulting

AI auto business service tool

## 프로젝트 목표

**Jason's Consulting** — Claude를 활용한 1인 AI 비즈니스를 실제 수익으로 연결한다.
기반 자료: [Start a 1-Person Business with Claude (4 HOUR COURSE 2026)](https://www.youtube.com/watch?v=mKyaNr3jK-E)

## 상품

**소상공인 "예약받는 랜딩페이지" 제작** — 동네 병원·미용실·필라테스 등에게 48시간 안에 예약/문의를 받는 모바일 랜딩페이지를 만들어 준다.

## 빠른 시작 — 파이프라인 한 번에 실행

```bash
# 데모 재생성 + 배포용 사이트 빌드 + 아웃리치 메시지·발송센터 생성
python3 pipeline.py --leads tools/cold-email-generator/leads.sample.csv --sender 제이슨
```

`git push` 하면 GitHub Actions가 데모 4종 + 포트폴리오 허브를 GitHub Pages에 자동 배포한다
(최초 1회 저장소 Settings → Pages → Source를 **GitHub Actions**로 설정).
배포 URL: `https://jasonsjo.github.io/AI-business/`

**매일 루틴 (자동화 후 남는 일):**
1. 리드 CSV에 오늘 연락할 업체 추가 (개인화 한 줄 필수)
2. `python3 pipeline.py --leads 내리드.csv` 실행
3. `out/발송센터.html` 열고 클릭 발송 → 완료 체크
4. "KPI JSON 내보내기" → 대시보드 "가져오기" → 병목 확인

## 문서

- **[30일 첫 수익 실행 로드맵](docs/30일-수익-실행-로드맵.md)** — 무엇을 팔지, 누구에게, 얼마에, 어디서 찾을지 + 일별 실행 계획과 복붙 템플릿.
- **[결제 세팅 가이드](docs/결제-세팅-가이드.md)** — 사업자등록·계좌 분리·현금영수증·카드 링크결제·세금 달력 + 입금 요청 메시지 템플릿.
- **[광고 세팅 가이드](docs/광고-세팅-가이드.md)** — 네이버 검색광고·메타 광고 세팅 순서, 키워드·광고 문구(복붙용), 예산·CPL 판단 기준, UTM 추적.

## 영업용 데모 (4종)

| 데모 | 업종 | 테마 | 비고 |
|---|---|---|---|
| [고요 필라테스](demo/pilates-studio/) | 필라테스 (성수) | 크림 + 파인그린 | 수제 원본 · [가이드](demo/pilates-studio/README.md) |
| [밝은미소 치과](demo/dental-clinic/) | 치과 (마포) | 틸그린 + 코랄 | 생성기로 제작 |
| [살롱 드 온](demo/hair-salon/) | 헤어살롱 (연남) | 플럼 + 골드 | 생성기로 제작 |
| [카페 향](demo/cafe/) | 카페 (망원) | 에스프레소 + 카라멜 | 생성기로 제작 |

모두 반응형 + 모바일 하단 고정 CTA(전화·카톡·예약), 외부 이미지 0개(어디 올려도 렌더링 보장).

## 도구

- **[랜딩페이지 생성기](tools/landing-generator/)** — 고객 정보 JSON → 랜딩페이지 자동 생성. 새 고객 페이지 10분 컷.
- **[콜드 아웃리치 생성기](tools/cold-email-generator/)** — 리드 CSV → 업종·채널별 개인화 메시지 대량 생성 + 발송 체크리스트. 한국어 조사 자동 처리.
- **[KPI 대시보드](tools/kpi-dashboard/)** — 발송→응답→미팅→계약 퍼널을 매일 기록, 병목 자동 진단 + 처방. 단일 HTML(브라우저에서 바로 열기).
- **[견적서·청구서](tools/invoice/청구서.html)** — 클릭해서 수정 → 인쇄/PDF. 부가세 자동 계산, 계좌·사업자 정보 자동 저장, 견적서↔청구서 전환.

## 로드맵

1. ✅ **실행 로드맵** — 30일 안에 첫 수익 내는 계획서
2. ✅ **데모 상품** — 영업에 쓸 랜딩페이지 데모 4종 (필라테스·치과·헤어살롱·카페)
3. ✅ **랜딩페이지 생성기** — 고객 정보 입력 → 사이트 자동 생성
4. ✅ **콜드 아웃리치 생성기** — 리드 CSV → 개인화 메시지 대량 생성
5. ✅ **KPI 대시보드** — 발송/응답/미팅/계약 추적 + 병목 진단
6. ✅ **전 과정 자동화** — Pages 자동 배포 + 발송 센터(클릭 발송) + KPI 자동 기록 + `pipeline.py`
7. ⬜ **첫 발송** — 리드 20곳 리스트업 후 실행 (사람이 하는 일: 리드 발굴 + 클릭)
