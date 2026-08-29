# DETOUR 작업 지침

이 파일은 DETOUR 저장소에서 작업하는 Codex 및 협업자를 위한 프로젝트 기준 문서다. 작업을 시작하기 전에 `README.md`, `PLAN.md`, 이 파일을 읽는다.

## 프로젝트 한 줄 정의

DETOUR는 사용자의 현재 조건(목적지, 남은 시간, 예산, 원하는 활동)을 바탕으로 지금 바로 갈 만한 장소와 코스 TOP 3를 추천하는 반응형 웹 서비스다.

핵심 문제는 “갈 곳이 없다”가 아니라 “지금 내 조건에서 무엇을 선택해야 할지 어렵다”는 것이다. 추천 결과에는 순위뿐 아니라 왜 추천하는지도 설명해야 한다.

## 5주 목표

1. Frontend + 웹 구조 — 첫 화면 만들기
2. Backend + REST API — Frontend ↔ FastAPI 연결
3. DB 설계 + 데이터 파이프라인 — 장소 데이터 저장·가공
4. 추천 시스템 + 서비스 통합 — 개인화 DETOUR 추천
5. 서버 + 배포 + 운영 기초 — 지도·모바일 UX·실제 서비스 배포

상세한 일일 체크리스트는 `PLAN.md`를 기준으로 한다. 전체 기능을 한 번에 구현하지 말고, 현재 주차의 작은 작업 하나씩 진행한다.

## 추천 파이프라인

```text
장소·경로 데이터
→ Feature Engineering
→ Normalization
→ 사용자 Weight
→ Score
→ Ranking
→ 추천 이유
```

초기 추천은 복잡한 머신러닝이 아닌 설명 가능한 규칙 기반 점수 계산으로 구현한다.

## 기술 방향

- Week 1 Frontend: 빌드 도구 없이 `index.html` 한 파일. React·Next 설치 금지, 필요하면 Pico.css CDN 사용
- 이후 Frontend: Week 1 완료 후 구조가 복잡해질 때 React/Next 도입 여부를 결정
- Backend: Python + FastAPI + Pydantic
- Data: 초기 CSV/JSON, 필요 시 SQLite 또는 PostgreSQL
- Map: 국내 장소 데이터와 호환되는 지도 API 하나만 선정
- Deployment: Frontend와 Backend를 배포하고 환경변수로 API key를 관리

API key, `.env` 파일, 실제 개인 정보는 커밋하지 않는다.

## 이번 주 수업 우선 규칙

이번 주에는 실제 AI 키, 실제 장소 API, 크롤링, React/Next를 시작하지 않는다. 직접 만든 장소 20개와 예시 결과 카드 2개로 “입력 폼 → 결과 카드”를 먼저 완성한다. 자세한 수업 정리는 `docs/COURSE_WEEK1_BRIEF.md`를 따른다.

## 작업 방식

- 사용자가 “시작하자”라고 하면 해당 일차의 작은 구현/학습 단위를 만든다.
- 사용자가 “오늘은 끝나자”라고 하면 `journal/`에 날짜·시간, 공부, 구현, 고민, 다음 작업을 기록한다.
- 사용자가 “일주일이 끝났어”라고 하면 공부와 구현의 완료 조건을 점검하고 주간 회고를 작성한다.
- 완료된 체크박스는 주간 회고에 결과를 남긴 뒤 `PLAN.md`에서 삭제한다.
- 구현 변경 후에는 테스트 가능한 범위에서 확인하고 의미 있는 Git 커밋으로 남긴다.

## 학습 원칙

코드를 단순히 생성하는 데 그치지 않는다. 매주 다음 질문에 답할 수 있게 `study/`에 기록한다.

1. 이 개념을 한 문장으로 설명하면?
2. DETOUR에서 어디에 쓰는가?
3. 실제 코드의 어느 파일 또는 함수에 있는가?

사용자가 학습 중이므로 Component, State, Event, API, schema, feature, normalization, weight, score, ranking을 쉬운 언어로 설명한다.

## 기준 문서

- `README.md`: GitHub 방문자용 프로젝트 소개
- `PLAN.md`: 5주·일일 실행 계획
- `DETOUR_PROJECT_SPEC.md`: 제품·기술 상세 명세
- `DETOUR_5WEEK_HANDOFF.md`: 기존 인수인계 및 학습 맥락
- `study/`: 학습 자료 및 실습 기록
- `journal/`: 날짜별 고민·결정·회고
- `docs/PROJECT_CONTEXT.md`: 새 세션과 협업자를 위한 빠른 시작 안내

## GitHub

- Repository: `nocked115/DeTour`
- Default branch: `main`
- 원격 저장소: `https://github.com/nocked115/DeTour.git`
