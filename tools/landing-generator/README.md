# 랜딩페이지 생성기

고객 정보 JSON 하나로 소상공인 랜딩페이지를 자동 생성한다. **외부 의존성 없음** (Python 표준 라이브러리만).

## 사용법

```bash
cd tools/landing-generator
python3 generate.py configs/dental-clinic.json            # 하나
python3 generate.py configs/*.json                        # 전부
```

config의 `output` 경로(설정 파일 기준 상대경로)에 `index.html`이 생성된다.

## 새 고객 페이지 만들기 (10분 워크플로)

1. 기존 config 중 업종이 가까운 것을 복사: `cp configs/cafe.json configs/새고객.json`
2. 업체명·카피·가격·후기·주소·연락처를 고객 정보로 수정
3. `output`을 원하는 폴더로 지정 (예: `"../../clients/새고객"`)
4. `python3 generate.py configs/새고객.json`
5. 결과 확인 후 Netlify Drop 등에 배포 → 링크를 영업 메시지에 첨부

## config 구조

| 키 | 내용 |
|---|---|
| `output` | 출력 폴더 (config 파일 기준 상대경로) |
| `brand` | `name`(상호), `mark`(로고 원 안의 글자 1자) |
| `meta` | 브라우저 제목·검색 설명 |
| `theme` | 색상 9종 — `cream/cream_deep`(배경), `ink/ink_soft`(글자), `primary/primary_light`(메인색), `accent/accent_deep`(포인트색), `muted` |
| `nav` | 메뉴 라벨 (`why`, `price`, `cta`) |
| `hero` | 헤드라인(`<em>`, `<br>` 허용), 리드문, CTA 문구, 신뢰 지표, 카드 글리프(한자/한글 1자) |
| `marquee` | 흐르는 키워드 목록 |
| `why` | 강점 3카드 — `icon`은 프리셋 이름 |
| `pricing` | 가격 플랜 3개 — `featured: true`가 강조 카드 |
| `reviews` | 후기 3개 |
| `location` | 오시는 길 정보 행 |
| `contact` | 전화(`tel`은 숫자만), 카카오 URL, 예약 URL, 영업시간 |

**아이콘 프리셋:** `person` `heart` `align` `shield` `star` `clock` `sparkle` `coffee` `scissors` `cross` `leaf` `chat`

## 포함된 예시 config

| config | 업체 (가상) | 테마 |
|---|---|---|
| `dental-clinic.json` | 밝은미소 치과 (마포) | 틸 그린 + 코랄 |
| `hair-salon.json` | 살롱 드 온 (연남) | 플럼 + 골드 |
| `cafe.json` | 카페 향 (망원) | 에스프레소 + 카라멜 |

생성 결과는 [`demo/`](../../demo/) 폴더에 있다. 원조 수제 데모는 [`demo/pilates-studio`](../../demo/pilates-studio/).

## 템플릿 특징

- 모바일 하단 고정 CTA 바 (전화·카톡·예약) — 소상공인 전환의 핵심
- 외부 이미지 0개 (SVG·그라디언트 자체 완결) → 어디 올려도 항상 렌더링
- 스크롤 리빌 애니메이션, 반응형, `prefers-reduced-motion` 대응
- 치환 누락 시 생성기가 오류로 알려줌 (빈 페이지 배포 사고 방지)
