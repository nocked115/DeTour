# DETOUR 5주 실행 계획

이 문서는 DETOUR를 5주 동안 학습하면서 실제 서비스로 완성하기 위한 기준 계획입니다.

## 사용 방법

- 주차가 시작되면 해당 주의 일일 체크리스트를 기준으로 진행합니다.
- 완료한 항목은 `- [x]`로 표시합니다.
- 주차 회고가 끝나면 완료한 체크 항목은 삭제하고, 주간 회고 문서에 결과를 보존합니다.
- 사용자가 “시작하자”라고 하면 그날의 작업 문서와 구체적인 일일 체크리스트를 만듭니다.
- 사용자가 “일주일이 끝났어”라고 하면 공부·구현·GitHub 기록을 점검합니다.

## Week 1 — Frontend와 첫 화면

목표: 사용자가 목적지, 남은 시간, 예산, 활동을 입력하고 결과 화면까지 이동한다.

- [ ] Day 1: 현재 랜딩 페이지 읽기, HTML/CSS/JavaScript 역할 확인
- [ ] Day 2: React/Next.js 프로젝트 구조와 Component 이해
- [ ] Day 3: 입력값과 State 연결
- [ ] Day 4: 활동 선택 Event와 기본 검증 구현
- [ ] Day 5: 결과 화면과 mock 추천 카드 구현
- [ ] Day 6: 모바일 화면 점검과 코드 읽기
- [ ] Day 7: Week 1 공부·구현 점검, 회고, GitHub 기록

완료 기준: 입력 후 버튼을 누르면 mock 추천 결과가 보인다.

## Week 2 — Frontend ↔ Backend

목표: Frontend가 FastAPI에 추천 요청을 보내고 JSON 응답을 화면에 표시한다.

- [ ] Day 1: HTTP, Request, Response, JSON 공부
- [ ] Day 2: FastAPI 설치와 `/health` Endpoint 구현
- [ ] Day 3: Pydantic Request/Response Model 작성
- [ ] Day 4: `POST /recommend` 구현
- [ ] Day 5: Frontend `fetch()` 연결
- [ ] Day 6: Loading, Error 상태와 Swagger `/docs` 확인
- [ ] Day 7: Week 2 공부·구현 점검, 첫 API 배포 검토, 회고

완료 기준: 브라우저 입력이 FastAPI를 거쳐 JSON 결과로 돌아온다.

## Week 3 — 장소 데이터와 파이프라인

목표: 장소 데이터를 저장하고 추천에 사용할 수 있는 형태로 정제한다.

- [ ] Day 1: 장소 데이터 구조와 CSV/JSON/DB 비교
- [ ] Day 2: 테스트 지역과 장소 데이터 범위 결정
- [ ] Day 3: 장소 데이터 20개 이상 수집·작성
- [ ] Day 4: 결측값·중복·잘못된 값 정리
- [ ] Day 5: Feature Engineering 코드 작성
- [ ] Day 6: 원본 → 정제 → Feature 생성 흐름 재실행
- [ ] Day 7: Dataset 점검, 출처·한계 기록, 회고

완료 기준: 정제된 장소 데이터에서 추천 후보를 조회할 수 있다.

## Week 4 — 추천 Engine과 지도

목표: 사용자 조건에 따라 설명 가능한 TOP 3 추천과 지도 표시를 제공한다.

- [ ] Day 1: Feature, Normalization, Weight, Score, Ranking 공부
- [ ] Day 2: 시간·예산·거리 Feature를 0~1로 정규화
- [ ] Day 3: 사용자 Weight와 최종 Score 계산
- [ ] Day 4: Ranking과 TOP 3 응답 구현
- [ ] Day 5: 점수 근거 기반 추천 이유 생성
- [ ] Day 6: 지도 API, 위도·경도, Marker 연결
- [ ] Day 7: 조건 변화 테스트, 추천·지도 통합 점검, 회고

완료 기준: 입력 조건을 바꾸면 순위가 합리적으로 바뀌고 지도에서 장소를 확인할 수 있다.

## Week 5 — 모바일 UX, 배포, 사용자 테스트

목표: 처음 보는 사람이 설명 없이 사용하고, 실제 URL에서 핵심 흐름을 완료한다.

- [ ] Day 1: 환경변수와 API key 보안 점검
- [ ] Day 2: 모바일 레이아웃과 Touch Target 점검
- [ ] Day 3: Loading, Empty, Error, 위치 권한 거부 상태 개선
- [ ] Day 4: Production Build와 배포
- [ ] Day 5: 3~5명 사용자 테스트
- [ ] Day 6: 반복되는 문제 1~2개 수정
- [ ] Day 7: README·DEVLOG·포트폴리오 정리와 최종 회고

완료 기준: 배포된 웹에서 입력 → 추천 → 지도 확인이 막힘 없이 가능하다.

## 핵심 추천 파이프라인

```text
장소·경로 데이터
→ Feature Engineering
→ Normalization
→ 사용자 Weight
→ Score
→ Ranking
→ 추천 이유
```

