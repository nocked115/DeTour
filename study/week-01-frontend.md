# Week 1 — Frontend와 웹 구조

## 목표

DETOUR의 입력 화면을 읽고, 사용자의 입력이 화면에 반영되는 과정을 설명할 수 있다.

## 공부할 개념

- HTML: 화면의 구조
- CSS: 색상, 크기, 간격, 반응형 레이아웃
- JavaScript: 값, 함수, 조건문, 이벤트
- React: Component, Props, State, Event
- Next.js: 페이지와 프로젝트 구조

## 작은 실습

이름을 입력하고 버튼을 누르면 화면에 인사말을 표시한다.

```jsx
const [name, setName] = useState("");

<input value={name} onChange={(event) => setName(event.target.value)} />
<button onClick={() => alert(`안녕하세요, ${name}님`)}>확인</button>
```

## DETOUR 적용

- 목적지
- 남은 시간
- 예산
- 하고 싶은 활동
- 추천 결과를 보여주는 버튼

## 개념을 내 말로 설명하기

### Component

내 설명:

### State

내 설명:

### Event

내 설명:

## 코드 읽기 기록

- 읽은 파일:
- 찾은 Component:
- 찾은 State:
- 찾은 Event:
- 이해한 흐름:

## 실습 결과

- 실행한 날짜:
- 작동한 것:
- 막힌 것:
- 다음에 확인할 것:

## GitHub 기록

- 관련 커밋:
- 관련 Issue:

