# DETOUR Project Specification

> **Shortest isn't always best.**  
> **가장 빠른 길이 아니라, 나에게 맞는 길.**

- 문서 목적: Codex와 개발자가 이 파일만 읽고 주차별 구현을 시작할 수 있는 단일 명세
- 구현 기간: 6주 × 주 3시간, 총 18시간
- 제품 형태: Mobile-first responsive web
- 우선순위: 작동하는 추천 MVP → 모바일 UX 완성 → 선택적 확장

---

## 1. 프로젝트 한 줄 정의

**DETOUR는 출발지와 목적지 사이에서 사용자의 남은 시간, 예산, 하고 싶은 활동을 고려해 ‘가장 빠른 길’ 대신 ‘지금 나에게 맞는 작은 우회’를 추천하는 데이터 기반 모바일 웹서비스다.**

## 2. 문제 정의

기존 지도 서비스는 주로 최단 시간과 최단 거리를 최적화한다. 그러나 사용자가 원하는 좋은 이동은 상황에 따라 다르다. 누군가는 약속 전 90분 동안 공원을 걷고 싶고, 누군가는 예산 안에서 카페에 들르고 싶으며, 누군가는 평소 지나치던 동네를 새롭게 경험하고 싶다.

DETOUR가 답할 핵심 질문은 다음과 같다.

> 제한된 시간과 예산 안에서 사용자의 현재 취향에 가장 잘 맞는 경유지와 우회 경로를 설명 가능한 방식으로 추천할 수 있는가?

### 해결하려는 핵심 사용자 경험

1. 사용자가 현재 이동 조건을 짧게 입력한다.
2. 서비스가 실제 장소와 경로 후보를 만든다.
3. 조건 적합도를 계산해 Detour TOP 3를 보여준다.
4. 사용자는 점수뿐 아니라 추천 이유, 예상 시간·비용·추가 거리, 지도와 경유지를 함께 확인한다.

### 프로젝트 성공의 정의

- 입력 조건을 바꾸면 TOP 3 순위가 실제로 달라진다.
- 각 추천 결과가 왜 선택됐는지 사람이 이해할 수 있다.
- 휴대폰 브라우저에서 입력부터 결과 확인까지 막힘 없이 작동한다.
- 제한된 테스트 지역의 실제 장소 데이터를 사용한다.

---

## 3. 제품 범위

### 3.1 MVP — 반드시 구현

#### 핵심 입력

- 출발지
- 목적지
- 남은 시간(분)
- 예산(원)
- 하고 싶은 활동: 예) 산책, 카페, 구경/문화

#### 핵심 출력

- 추천 Detour TOP 3
- 각 코스의 match score
- 총 예상 시간
- 총 예상 비용
- 최단 경로 대비 추가 거리 또는 추가 시간
- 추천 이유 2~3개
- 지도 위 경로 및 경유지
- 출발지 → 경유지 → 목적지 순서

#### 필수 화면 및 상태

1. 홈/조건 입력 화면
2. 추천 결과 목록 화면 또는 섹션
3. 선택한 Detour 상세 화면
4. 로딩 상태
5. 입력 오류 상태
6. 추천 후보 없음/API 오류 상태

### 3.2 확장 기능 — MVP 완료 후에만

- **상황 반영 추천**: 날씨(맑음·비 등)에 따라 실내/실외 장소 선호도를 조정하고, 현재 위치를 바탕으로 각 후보까지의 예상 이동 시간을 반영
- **After 6**: 현재 시각과 귀가 예정 시각 사이의 남은 시간을 자동 계산해 코스 추천
- **Barrier-free Detour**: 계단, 경사, 엘리베이터 등 이동 조건 반영
- **City Quest / Mini Quest**: 경로 중 작은 발견 미션이나 빙고 제공
- 이용 기록, 저장, 공유, 리뷰
- 사용자 행동 기반 가중치 학습
- 다양한 도시 및 실시간 혼잡도 확장

Week 5에 시간이 남는 경우 확장 기능은 **After 6 하나만** 우선 검토한다. 기존 시간 제약 추천 로직을 재사용할 수 있기 때문이다. Barrier-free 데이터는 정확성과 책임 문제가 있으므로 충분한 데이터 검증 없이 안전 경로라고 표현하지 않는다.

현재 위치와 날씨는 5주차 지도·모바일 UX 작업에서 우선 검토한다. 위치는 사용자 동의를 받은 경우에만 사용하고, 권한을 거부해도 출발지를 직접 입력해 추천을 받을 수 있어야 한다. 날씨는 추천 후보를 완전히 제외하기보다 실내/실외 적합도 점수와 추천 이유에 반영한다.

### 3.3 이번 MVP에서 하지 않는 것

- 네이티브 iOS/Android 앱
- 복잡한 회원가입 및 소셜 기능
- 결제
- 딥러닝 모델
- 서울 전역 또는 전국 규모 데이터 수집
- 완전한 실시간 경로 최적화 엔진
- 확장 기능을 위한 핵심 추천 일정 지연

---

## 4. UI/UX 방향

### 4.1 제품 인상

밝고 발랄한 MZ 감성의 editorial/UI 스타일을 지향한다. 일반적인 지도 앱처럼 기능적으로만 보이기보다, 잡지의 큰 제목과 라이프스타일 카드가 결합된 느낌을 만든다.

### 4.2 시각 원칙

- 첫 화면에 큰 소문자 `detour` 타이포를 브랜드 앵커로 사용
- lime/green을 핵심 accent color로 사용
- 주요 CTA는 black background + high-contrast text
- 추천 코스는 서로 다른 pastel route cards로 구분
- 넉넉한 여백, 큰 제목, 짧은 카피, 선명한 정보 위계
- 둥근 카드와 pill/chip을 사용하되 장식이 정보보다 앞서지 않게 함
- Mini Quest는 재미 요소로 보이되 MVP 핵심 흐름과 분리
- 지도는 결과 이해를 돕는 핵심 정보이며 장식용 배경으로 취급하지 않음

### 4.3 주요 카피 예시

- `Shortest isn't always best.`
- `가장 빠른 길이 아니라, 나에게 맞는 길.`
- `늘 가던 길 말고, 오늘은 나를 위한 우회로 어때?`
- CTA: `detour me! →`
- 결과: `Today's Detour`, `91% Match`

### 4.4 Mobile-first 반응형 기준

- 360~430px 폭을 먼저 설계하고 터치 영역은 최소 44px 수준을 확보한다.
- 작은 화면에서는 입력과 결과를 한 열로 배치한다.
- 넓은 화면에서는 입력 패널과 지도/결과를 2열로 확장할 수 있다.
- 모바일 브라우저의 위치 권한 거부, 느린 네트워크, 긴 장소명도 고려한다.
- 키보드만으로 주요 입력과 CTA를 사용할 수 있게 하고 색상만으로 상태를 구분하지 않는다.

### 4.5 Week 1 화면 구성

```text
detour

늘 가던 길 말고,
오늘은 나를 위한 우회로 어때?

[ 출발지                    ]
[ 목적지                    ]

[ 남은 시간 90분 ] [ 예산 20,000원 ]

하고 싶은 것
[ 🌳 산책 ] [ ☕ 카페 ] [ 📚 구경 ]

[          detour me! →          ]
```

Week 1 결과 화면은 mock data로 TOP 3 카드, match score, 시간/비용/추가 거리, 추천 이유를 보여주면 된다. 지도는 정적 placeholder여도 된다.

---

## 5. 데이터사이언스 설계

### 5.1 전체 파이프라인

```text
사용자 조건
  → 후보 장소/경로 생성
  → 장소·경로 feature engineering
  → feature normalization
  → user preference weights 적용
  → constraint filtering + score 계산
  → ranking
  → TOP 3 + 추천 이유 생성
```

### 5.2 초기 데이터 범위

- 테스트 지역 1곳
- 장소 20~50개
- 초기에는 CSV 또는 JSON 사용 가능
- DB는 조회/관리 필요가 생길 때 최소 수준으로 도입

### 5.3 장소 데이터 예시

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | string | 장소 고유 ID |
| `name` | string | 장소명 |
| `category` | enum/string | park, cafe, culture 등 |
| `latitude`, `longitude` | number | 좌표 |
| `estimated_price` | number | 1인 예상 비용 |
| `stay_minutes` | number | 권장 체류 시간 |
| `rating` | number/null | 평점, 없을 수 있음 |
| `opening_hours` | object/null | 영업 시간 |
| `tags` | string[] | 산책, 조용함, 사진 등 |
| `source` | string | 데이터 출처 |

### 5.4 경로 후보 feature 예시

- 총 예상 시간
- 총 예상 비용
- 최단 경로 대비 추가 거리/시간
- 활동 선호 일치도
- 장소 평점 또는 품질 점수
- 영업 여부
- 경유지 수
- 데이터 신뢰도/결측 여부

### 5.5 점수 계산 초안

먼저 시간·예산 같은 절대 제약을 넘는 후보를 제거하거나 큰 패널티를 적용한다. 이후 각 feature를 0~1로 정규화하고 가중합을 계산한다.

```text
score =
  w_time     × time_fit
+ w_budget   × budget_fit
+ w_activity × activity_fit
+ w_distance × distance_fit
+ w_quality  × quality_fit
```

초기 기본 가중치 예시:

```text
w_time     = 0.30
w_budget   = 0.25
w_activity = 0.30
w_distance = 0.10
w_quality  = 0.05
```

가중치 합은 1로 유지한다. 이 값은 정답이 아니라 명시적으로 기록하고 테스트할 가설이다. 사용자가 활동을 선택하면 관련 category/tag의 `activity_fit`과 필요 시 가중치를 조정한다.

### 5.6 정규화 예시

- `time_fit = max(0, 1 - abs(route_minutes - target_minutes) / target_minutes)`
- 예산 이내이면 여유 비율을 반영하고 초과하면 0 또는 강한 패널티
- 추가 거리는 후보 집합 내 min-max normalization 후 역방향 점수 사용
- 활동은 category/tag 일치 비율 또는 규칙 기반 점수 사용
- 평점 결측치는 무조건 0으로 두지 말고 중립값 또는 별도 결측 정책 사용

0분, 0원, 동일한 최솟값/최댓값 등 0으로 나누는 경계 조건을 테스트해야 한다.

### 5.7 추천 이유 생성

점수 기여도가 높은 feature와 제약 충족 정보를 자연어 템플릿에 연결한다.

- `예산의 82%만 사용해요.`
- `원한 산책 장소를 포함했어요.`
- `남은 90분 안에 도착할 수 있어요.`
- `최단 경로보다 1.2km만 더 걸어요.`

추천 이유는 LLM이 임의 생성하기보다 실제 계산값에서 파생해야 한다.

### 5.8 최소 검증

- 같은 입력은 같은 순위를 반환한다.
- 활동을 산책에서 카페로 바꾸면 관련 코스의 순위가 상승한다.
- 예산을 낮추면 비싼 코스가 제외되거나 하락한다.
- 남은 시간을 줄이면 긴 코스가 제외되거나 하락한다.
- match score와 추천 이유가 같은 계산 근거를 사용한다.

---

## 6. 기술 구조

```text
Mobile/Web Browser
        ↓
Next.js / React frontend
        ↓ REST + JSON
Python FastAPI backend
  ├─ place/route data adapter
  ├─ feature pipeline
  ├─ recommendation engine
  └─ explanation builder
        ↓
최소 DB 또는 CSV/JSON + 지도/장소 API
```

### 6.1 권장 기술

- Frontend: Next.js + React + TypeScript
- Styling: CSS Modules, Tailwind CSS 등 한 가지 방식만 선택
- Backend: Python + FastAPI + Pydantic
- API: REST/JSON
- Data: 초기 CSV/JSON, 필요 시 SQLite/PostgreSQL
- Map/Place: 하나의 지도·장소 API를 선정해 adapter 뒤에 격리
- Deploy: frontend는 Vercel, backend는 FastAPI를 지원하는 배포 서비스
- Test: frontend의 핵심 컴포넌트/흐름 테스트 + backend scoring 단위 테스트

지도·장소 API는 지역 커버리지, 무료 할당량, 경로 API 제공 여부, 브라우저 사용 조건을 확인한 뒤 Week 3에 확정한다. API key는 `.env`에 두고 Git에 커밋하지 않는다.

### 6.2 API 계약 초안

`POST /api/recommend`

Request:

```json
{
  "origin": { "name": "동대문역", "lat": 37.5714, "lng": 127.0095 },
  "destination": { "name": "서울숲", "lat": 37.5444, "lng": 127.0374 },
  "available_minutes": 90,
  "budget_krw": 20000,
  "activities": ["walk", "cafe"]
}
```

Response:

```json
{
  "recommendations": [
    {
      "id": "detour-001",
      "rank": 1,
      "title": "Green Pause",
      "match_score": 0.91,
      "total_minutes": 85,
      "estimated_cost_krw": 16500,
      "extra_distance_km": 1.2,
      "waypoints": [{ "id": "place-01", "name": "서울숲", "lat": 37.5444, "lng": 127.0374 }],
      "reasons": ["남은 시간 안에 가능해요", "원한 산책 장소를 포함했어요"],
      "route_geometry": null
    }
  ]
}
```

초기 버전에서는 출발지/목적지를 문자열로 받고 backend나 mock adapter가 좌표로 변환해도 된다. 단, frontend와 backend가 공유하는 계약은 문서화한다.

---

## 7. 6주 구현 로드맵

매주 권장 루틴은 `개념 30~45분 → 구현 90~120분 → 코드 읽기/테스트 30분 → 기록 15분`이다.

### Week 1 — Frontend prototype

**목표:** DETOUR의 가치와 전체 입력→결과 흐름을 브라우저에서 보여준다.

- 현재 저장소 구조 확인 또는 Next.js frontend 생성
- 디자인 토큰과 mobile-first 기본 레이아웃 설정
- 핵심 입력 폼 구현
- 활동 chip 선택 상태 구현
- `detour me!` 클릭 시 mock TOP 3 결과 표시/이동
- 결과 카드에 score, 시간, 비용, 추가 거리, 이유 표시
- 최소 입력 검증
- README에 실행법과 Week 1 범위 기록

**완료 조건:** 모바일 크기 브라우저에서 값을 입력하고 버튼을 누르면 mock 추천 TOP 3를 볼 수 있으며 새로고침/기본 오류 없이 실행된다.

### Week 2 — Backend/API + first deploy

**목표:** frontend 입력이 실제 FastAPI를 거쳐 JSON 결과로 돌아온다.

- FastAPI 앱과 `/health`, `/api/recommend` 생성
- Pydantic request/response schema 작성
- frontend의 mock 호출을 실제 API 호출로 교체
- CORS와 환경변수 구성
- API 실패/로딩 UI 추가
- frontend 첫 배포, 가능하면 backend도 배포

**완료 조건:** 버튼 클릭 시 Python backend가 입력을 받고 응답하며 frontend가 이를 표시한다. 배포 URL 또는 재현 가능한 로컬 실행 절차가 있다.

### Week 3 — Real place data / data pipeline

**목표:** 하드코딩된 추천 결과를 제한된 실제 장소 데이터로 교체한다.

- 테스트 지역과 지도/장소 데이터 소스 확정
- 실제 장소 20~50개 수집
- 원본/정제 데이터 분리
- 중복, 결측, 좌표, category/tag 정리
- 전처리 및 feature 생성 코드 작성
- 장소 마커 표시
- 데이터 출처와 한계 기록

**완료 조건:** 결과의 장소가 정제 데이터셋에서 조회되며, 원본→정제→feature 생성 과정을 다시 실행할 수 있다.

### Week 4 — Recommendation engine

**목표:** 사용자 조건에 따라 설명 가능한 TOP 3 순위가 실제로 달라진다.

- 절대 제약 filtering/penalty 구현
- normalization 함수 구현
- preference weight와 score 구현
- 안정적인 정렬 및 TOP 3 반환
- 계산값 기반 추천 이유 생성
- scoring 단위 테스트와 입력 변화 시나리오 테스트

**완료 조건:** 활동·시간·예산을 변경하면 예상 방향으로 추천 순위가 변하고, 점수와 이유가 계산 근거와 일치한다.

### Week 5 — Map + mobile UX + optional After 6

**목표:** 분석 결과를 실제 모바일 서비스처럼 이해하고 사용할 수 있게 만든다.

- 선택 코스 경로와 waypoint를 지도에 표시
- 모바일 레이아웃, touch target, 긴 텍스트 점검
- 로딩 skeleton, empty/error, 위치 권한 거부 처리
- 실제 휴대폰 테스트
- 시간이 남을 때만 After 6 추가

**완료 조건:** 휴대폰에서 입력→추천→지도/경유지 확인이 가능하고, 주요 실패 상태가 사용자에게 이해 가능한 문장으로 표시된다.

### Week 6 — Deploy / user test / portfolio

**목표:** 다른 사람이 설명 없이 사용하고 프로젝트 과정을 검토할 수 있게 한다. 새 기능은 추가하지 않는다.

- production 배포와 환경변수/HTTPS 확인
- 3~5명 무설명 사용자 테스트
- 반복되는 핵심 문제 1~2개 수정
- README, architecture, algorithm, limitations 정리
- 대표 화면과 데모 흐름 준비
- DEVLOG와 이슈 정리

**완료 조건:** 공개 URL에서 핵심 흐름이 작동하고, 사용자 테스트 결과와 반영 사항이 기록되며, README만으로 설치·실행·프로젝트 이해가 가능하다.

---

## 8. 권장 저장소 구조

```text
detour/
├─ README.md
├─ DETOUR_PROJECT_SPEC.md
├─ .gitignore
├─ .env.example
├─ docs/
│  ├─ DEVLOG.md
│  ├─ architecture.md
│  ├─ recommendation.md
│  ├─ data-sources.md
│  └─ screenshots/
├─ frontend/
│  ├─ app/
│  ├─ components/
│  ├─ lib/
│  ├─ types/
│  └─ public/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ api/
│  │  ├─ schemas/
│  │  ├─ services/
│  │  │  ├─ data_service.py
│  │  │  ├─ feature_engineering.py
│  │  │  ├─ recommender.py
│  │  │  └─ explanations.py
│  │  └─ core/
│  ├─ tests/
│  └─ requirements.txt 또는 pyproject.toml
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ sample/
└─ scripts/
   └─ prepare_places.py
```

기존 저장소가 이미 있다면 이 구조로 강제 이동하지 않는다. 현재 구조를 먼저 읽고 최소 변경으로 필요한 책임만 분리한다.

---

## 9. GitHub 기록 전략

### 9.1 README 권장 구성

1. 프로젝트 한 줄 소개와 핵심 문구
2. 문제와 해결 방식
3. 대표 스크린샷/GIF 및 배포 URL
4. 핵심 기능
5. 기술 구조
6. 추천 알고리즘 요약
7. 로컬 실행법
8. 데이터 출처
9. 테스트 방법
10. 한계와 향후 확장

### 9.2 DEVLOG

`docs/DEVLOG.md` 하나에 주차별 기록을 누적하거나 `docs/weekly/week-01.md` 형태로 분리한다. 작은 프로젝트에는 단일 DEVLOG를 권장한다.

매주 다음 템플릿을 사용한다.

```markdown
## Week N — 주제

- 목표:
- 완료한 것:
- 핵심 코드/개념:
- 막힌 문제와 원인:
- 해결 또는 남은 가설:
- 테스트한 것:
- 스크린샷/배포 주소:
- 다음 주 할 일:
- 이번 주 배운 점 한 줄:
```

### 9.3 Commit convention

작고 설명 가능한 단위로 커밋한다.

- `feat: add detour preference form`
- `feat(api): connect recommendation endpoint`
- `data: add processed places for seongsu`
- `fix: handle zero-minute recommendation request`
- `test: cover activity-weight ranking`
- `docs: record week 3 data pipeline`
- `style: refine mobile route cards`
- `chore: add environment variable example`

생성된 코드를 한 번에 `final` 같은 메시지로 커밋하지 않는다. 비밀키, `.env`, 대용량 원본 데이터는 커밋하지 않는다.

### 9.4 Issues와 milestones

- Milestone: `Week 1` ~ `Week 6`
- 각 issue는 30~90분 안에 끝낼 수 있는 크기로 작성
- Issue 예: `Create mobile input form`, `Define recommend API schema`, `Normalize time feature`
- label 권장: `frontend`, `backend`, `data`, `recommendation`, `design`, `docs`, `bug`, `stretch`
- 확장 기능은 `stretch` label과 별도 milestone로 격리
- issue 본문에 완료조건(acceptance criteria)을 반드시 작성

---

## 10. Codex 작업 원칙

Codex는 다음 규칙을 모든 주차에 따른다.

1. **전체 프로젝트를 한 번에 만들지 않는다.** 현재 주차의 작은 task 하나씩 구현한다.
2. 작업 전 저장소 구조, 기존 코드, 실행 방식, 변경 중인 파일을 먼저 확인한다.
3. 기존 구조와 사용자 변경을 최대한 유지하고 필요한 파일만 수정한다.
4. 구현 전 이번 task에서 바꿀 내용과 바꾸지 않을 내용을 짧게 설명한다.
5. 새 라이브러리는 필요성과 대안을 설명하고 최소한만 추가한다.
6. 모든 변경 후 실행·테스트·검증 명령과 실제 결과를 제공한다.
7. 오류가 나면 증상만 고치지 말고 원인을 쉬운 말로 설명한다.
8. 사용자가 학습할 핵심 코드는 Component, State, Event, API, schema, feature, normalization, weight, score, ranking 관점에서 설명한다.
9. 점수식과 데이터 가정은 코드 속 magic number로 숨기지 말고 이름과 문서로 남긴다.
10. API key와 비밀값은 `.env`로 관리하고 `.env.example`에는 이름만 기록한다.
11. 실제 데이터의 출처, 수집일, 라이선스/사용 조건, 결측 처리와 한계를 기록한다.
12. UI 변경 시 모바일 화면을 먼저 확인하고 loading/empty/error 상태를 함께 고려한다.
13. 테스트가 실패한 상태를 완료라고 말하지 않는다. 실행하지 못했다면 이유와 사용자가 실행할 명령을 분명히 적는다.
14. 매 task 종료 시 `무엇을 변경했는지 / 어떻게 확인하는지 / 무엇을 배울지 / 다음 작은 task`를 정리한다.
15. Barrier-free, After 6, City Quest가 MVP 완료를 늦추면 구현하지 않는다.

---

## 11. MVP 완료 체크리스트

- [ ] Mobile-first 반응형 입력 화면이 있다.
- [ ] 다섯 핵심 입력을 받을 수 있다.
- [ ] frontend와 FastAPI가 REST/JSON으로 통신한다.
- [ ] 제한된 지역의 실제 장소 데이터를 사용한다.
- [ ] feature engineering과 normalization 과정이 코드로 분리되어 있다.
- [ ] 사용자 선호 가중치로 score를 계산한다.
- [ ] TOP 3가 안정적으로 정렬된다.
- [ ] 입력을 바꾸면 결과가 합리적으로 변한다.
- [ ] match score, 시간, 비용, 추가 거리, 추천 이유가 보인다.
- [ ] 지도와 경유지가 보인다.
- [ ] loading, invalid input, empty result, API error 상태가 있다.
- [ ] 핵심 scoring 테스트가 통과한다.
- [ ] 공개 URL이 작동한다.
- [ ] README와 DEVLOG가 최신 상태다.
- [ ] 데이터와 추천 방식의 한계를 명시한다.

---

## 12. Week 1 Codex 첫 작업 프롬프트

아래 프롬프트를 새 Codex 작업에 그대로 사용한다.

```text
DETOUR 프로젝트의 Week 1 frontend prototype을 시작해 주세요.

먼저 저장소 전체 구조와 기존 파일, 실행 방법, 사용 중인 패키지, Git 상태를 읽기 전용으로 확인하세요. DETOUR_PROJECT_SPEC.md를 요구사항의 기준으로 사용하되, 기존 구조가 있다면 최대한 유지하세요. 아직 backend, 실제 지도 API, DB, 추천 알고리즘은 만들지 마세요.

이번 작업의 범위:
1. Next.js/React/TypeScript 기반의 mobile-first 홈 입력 화면
2. 입력: 출발지, 목적지, 남은 시간, 예산, 하고 싶은 활동
3. 활동 chip: 산책, 카페, 구경/문화
4. 큰 detour 타이포, lime/green accent, black CTA, 밝은 editorial 스타일
5. detour me! 버튼을 누르면 mock data 기반 추천 TOP 3 표시
6. 결과 카드에 match score, 시간, 비용, 추가 거리, 추천 이유 표시
7. 기본 필수 입력 검증과 접근 가능한 label/button 처리
8. 데스크톱에서도 깨지지 않는 반응형 레이아웃

진행 방식:
- 구현 전에 현재 구조와 수정 예정 파일을 짧게 설명하세요.
- task를 작은 단계로 나누고 한 단계씩 구현하세요.
- 기존 사용자 변경은 덮어쓰지 마세요.
- 필요한 의존성만 추가하고 이유를 설명하세요.
- 구현 후 lint/test/build 등 가능한 검증을 실제로 실행하세요.
- 실행 명령을 제공하세요.
- 마지막에는 Component, State, Event가 이번 코드 어디에 있는지 초보자도 이해할 수 있게 설명하세요.
- 변경 파일, 검증 결과, 남은 문제, 다음 추천 task를 정리하세요.

Week 1 완료조건:
모바일 크기의 브라우저에서 사용자가 값을 입력하고 detour me!를 누르면 mock 추천 TOP 3를 볼 수 있어야 합니다.
```

---

## 13. 최종 포트폴리오 스토리

1. **Problem:** 지도는 대부분 가장 빠른 길을 추천한다.
2. **Insight:** 사용자가 원하는 좋은 길은 시간, 예산, 취향에 따라 달라진다.
3. **Solution:** 현재 조건에 맞는 작은 우회 경험 TOP 3를 추천한다.
4. **Data:** 장소와 경로를 비교 가능한 feature로 가공했다.
5. **Algorithm:** `Feature → Normalization → Weight → Score → Ranking`을 구현했다.
6. **Explanation:** 추천 점수와 이유를 같은 계산 근거에서 만들었다.
7. **Product:** 모바일 우선 웹과 지도에서 결과를 확인할 수 있다.
8. **Validation:** 입력 변화 테스트와 사용자 테스트로 결과를 점검했다.
9. **Limitations:** 데이터 지역, API 정확도, 규칙 기반 가중치의 한계를 공개한다.
10. **Future:** After 6, Barrier-free, City Quest로 확장할 수 있다.

DETOUR의 포트폴리오 가치는 복잡한 모델 사용 여부가 아니라, 실제 문제를 작은 범위로 정의하고 데이터를 feature로 바꾸며 설명 가능한 추천 결과를 웹서비스로 전달한 전 과정에 있다.
