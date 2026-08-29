# Week 1 — Frontend와 웹 구조

## 목표

DETOUR의 입력 화면을 읽고, 사용자의 입력이 화면에 반영되는 과정을 설명할 수 있다.

## 공부할 개념

- HTML: 화면의 구조
- CSS: 색상, 크기, 간격, 반응형 레이아웃
- JavaScript: 값, 함수, 조건문, 이벤트
- DOM: HTML 요소를 JavaScript로 찾아 바꾸는 방법
- Event: 버튼 클릭 같은 사용자 행동에 반응하는 방법
- CDN: 인터넷의 CSS/JavaScript 파일을 주소 한 줄로 가져오는 방법
- Pico.css: 기본 버튼·입력창을 정돈해 주는 CSS 라이브러리

이번 주에는 React와 Next.js를 설치하지 않는다. 빌드 도구 없이 `index.html` 한 파일로 화면과 동작을 먼저 완성한다.

## 작은 실습

현재 위치·도착 위치·남은 시간·활동을 입력하고 버튼을 누르면 예시 DETOUR 카드 2개를 표시한다.

React 없이 하면 이렇게 된다. 값을 기억하는 곳이 `useState`가 아니라 **입력칸 자신**이다.

```html
<input id="origin" />
<button id="go">확인</button>

<script>
  document.querySelector("#go").addEventListener("click", () => {
    const origin = document.querySelector("#origin").value;
    alert(`${origin}에서 출발하는군요`);
  });
</script>
```

## DETOUR 적용

- 목적지
- 남은 시간
- 예산
- 하고 싶은 활동
- 추천 결과를 보여주는 버튼

## 개념을 내 말로 설명하기

### Component

화면을 이루는 **부품 하나**. React에서는 함수 하나가 부품이지만, `index.html`에는 React가 없으므로
HTML 태그 묶음이 그 역할을 한다. DETOUR에서는 입력 폼(`<form id="detour-form">`), 안내 문구
(`<section id="message">`), 결과 영역(`<section id="result">`)이 각각 하나의 부품이다.
카드 한 장을 만들어 내는 `renderCards()` 함수가 "카드 Component"에 가장 가깝다.

### State

화면이 **지금 기억하고 있는 값**. React는 `useState`에 넣어 두지만, `index.html`에서는
입력칸 자체가 값을 들고 있다. `document.querySelector("#time").value`를 읽으면 사용자가 고른
시간이 나온다. 그래서 이번 주 코드에는 State를 따로 저장하는 변수가 없고, 버튼을 누르는 순간
입력칸에서 값을 한 번에 꺼내 온다.

State가 화면에 반영되는 방식도 다르다. React는 State가 바뀌면 알아서 다시 그리지만,
`index.html`에서는 내가 직접 `cards.innerHTML = ...`으로 다시 그려야 한다.

### Event

사용자가 뭔가 했을 때 **실행되는 함수를 미리 등록해 두는 것**. DETOUR에서는
`form.addEventListener("submit", ...)` 한 곳뿐이다. 버튼을 누르면 이 함수가 실행된다.
`event.preventDefault()`는 "폼을 제출하고 페이지를 새로고침하는" 브라우저 기본 동작을 막는다.
이걸 빼면 결과를 보여주기도 전에 화면이 새로고침된다.

## 코드 읽기 기록

- 읽은 파일: `index.html`
- 찾은 Component: `#detour-form`(입력), `#message`(안내), `#result`(결과), `renderCards()`(카드)
- 찾은 State: 별도 변수 없음. `#origin` `#destination` `#time` `#budget` `#activity` 입력칸이 값을 가진다
- 찾은 Event: `form.addEventListener("submit", ...)` 한 개
- 이해한 흐름:

```text
버튼 클릭
→ submit Event 실행
→ preventDefault()로 새로고침 막기
→ 입력칸 5개에서 값 꺼내기
→ 값이 비었는지 검사 (아니면 안내 문구)
→ places 20개를 filter로 걸러내기
→ sort로 순서 정하고 slice(0, 2)로 2개만
→ innerHTML로 카드 그리기
```

## 장소 데이터의 필수 필드 (Day 3)

`index.html`의 `places` 배열이 쓰는 필드다. Week 3에서 데이터베이스로, Week 4에서 점수 계산으로
그대로 이어지도록 이름을 정했다.

| 필드 | 뜻 | 왜 필요한가 | 다음 주 계획 |
| --- | --- | --- | --- |
| `id` | 고유 키 | 같은 이름의 장소를 구분한다 | Week 3 DB의 primary key |
| `name` | 장소 이름 | 카드 제목 | 그대로 |
| `area` | 지역 묶음 | 테스트 지역을 한 곳으로 좁힌다 | Week 3에서 서울 1개 지역 확정 |
| `activity` | 산책·카페·구경·문화 | 사용자의 활동 선택과 맞춘다 | Week 4 활동 가중치의 입력 |
| `stayMinutes` | 머무는 시간(분) | 시간 조건 계산 | 그대로 |
| `travelMinutes` | 왕복 이동 시간(분) | 시간 조건 계산 | Week 4에 카카오 길찾기 값으로 교체 |
| `cost` | 1인 예상 비용(원) | 예산 조건 계산 | 그대로 |
| `tags` | 키워드 | 추천 이유를 뒷받침 | Week 4 추천 이유 문장의 재료 |
| `reason` | 추천 이유 문장 | 왜 이 장소인지 설명 | Week 4에 점수 근거로 자동 생성 |

핵심 규칙 하나: **총 소요 시간 = `stayMinutes` + `travelMinutes`**, 이 값이 남은 시간 이하여야 한다.

처음에는 `minutes`(총 시간)와 `distance`(사실은 이동 분)라는 두 필드였는데, `distance`라는
이름에 분 단위 값이 들어 있어 카드가 `78분`과 `예시 이동 시간 13분`을 나란히 보여주었다.
사용자가 91분으로 잘못 읽을 수 있는 표시였다. 이름이 값의 뜻과 맞아야 한다는 걸 배웠다.

넣지 않기로 한 필드: `indoor`(날씨용), `crowd`(혼잡도용). `docs/MVP_DECISION_RULES.md`에서
확장 기능으로 분류된 것들이라 필드만 미리 만들어 두지 않는다.

## 실습 결과

- 실행한 날짜: 2026-08-29
- 작동한 것: 입력 5개 → 조건에 맞는 장소 필터링 → 카드 2개 표시. Loading·안내·결과 세 상태 전환
- 막힌 것: 없음
- 다음에 확인할 것: `fetch()`로 서버에서 값을 받아오는 방법 (Week 2)

## GitHub 기록

- 관련 커밋: `1a4f856` 수업 기준 정적 프로토타입, `812c4d5` 장소 필드·시간 표시 정리

## Day 2 — React와 Next.js 구조

> 이 절은 `frontend/`에 만들어 둔 Next.js 실험본에 대한 기록이다.
> 이번 주 수업 제출본은 `index.html`이며, 두 파일은 서로 다른 트랙이다.

### 이 프로젝트에서의 Component

- `frontend/src/app/page.tsx`: 제목, 소개, 추천 기준처럼 정적인 첫 화면을 배치한다.
- `frontend/src/app/detour-planner.tsx`: 사용자의 입력과 버튼 클릭에 반응하는 추천 입력·결과 영역이다.

### 이 프로젝트에서의 State

`DetourPlanner`의 `form` State는 현재 위치, 도착 위치, 시간, 예산, 날씨, 활동, 혼잡도 선호를 기억한다. 사용자가 값을 바꾸면 `updateField()`가 State를 새 값으로 갱신한다.

### 이 프로젝트에서의 Event

- `onChange`: 사용자가 입력칸이나 선택 메뉴의 값을 바꿀 때 실행된다.
- `onSubmit`: 사용자가 `작은 Detour 받아보기` 버튼을 눌렀을 때 실행된다.

### 왜 Client Component인가

Next.js의 `page.tsx`는 기본적으로 Server Component다. 반면 `useState`, `onChange`, `onSubmit`처럼 브라우저에서 반응해야 하는 `detour-planner.tsx` 파일 맨 위에는 `"use client"`를 선언한다.

### 두 방식을 비교하며 배운 것

| | `index.html` (이번 주) | `frontend/` (실험) |
| --- | --- | --- |
| 값을 기억하는 곳 | 입력칸 자체 (`.value`) | `useState` |
| 화면 다시 그리기 | 내가 `innerHTML`로 직접 | React가 알아서 |
| 실행 방법 | 파일을 더블클릭 | `npm run dev` |
| 설치할 것 | 없음 | Node.js, 패키지 수백 개 |

작은 화면 하나에는 React가 없어도 충분하다는 걸 직접 비교해서 확인했다.
