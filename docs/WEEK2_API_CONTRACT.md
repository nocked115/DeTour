# Week 2 API 계약 (초안)

Week 1에서는 API를 연결하지 않기로 결정했다. 대신 다음 주 FastAPI가 그대로 구현할 수 있도록
요청·응답 형식만 여기서 확정한다. 이 문서에는 코드가 없다.

## 왜 이번 주에 브라우저에서 직접 부르지 않는가

`index.html`은 빌드 도구 없이 브라우저가 직접 여는 파일이다. 여기에 카카오 REST API key를 적으면
페이지 소스 보기만으로 누구나 key를 가져갈 수 있다. 도메인 제한을 걸 수 있는 JavaScript key와 달리
REST key에는 그런 보호 장치를 쓰기 어렵고, 카카오 로컬 REST API는 브라우저에서 직접 호출하면
CORS로 막히는 경우가 많다.

그래서 key는 FastAPI 서버의 `.env`에만 두고, 브라우저는 우리 서버에만 요청한다.

```text
브라우저(index.html) → FastAPI(.env에 key 보관) → 카카오 API
```

## 지금 `index.html`이 가진 값

현재 화면이 이미 아래 값을 가지고 있다. Week 2의 요청 본문은 이 값을 그대로 옮긴 것이다.

| 화면 요소 | id | 값의 예 |
| --- | --- | --- |
| 출발 위치 | `origin` | `"서울숲역"` |
| 도착 위치 | `destination` | `"성수역"` |
| 남은 시간 | `time` | `60` (분) |
| 예산 | `budget` | `10000` (원) |
| 하고 싶은 것 | `activity` | `"카페"` |

## POST /geocode

주소나 장소명을 좌표로 바꾼다. Week 2 Day 4 항목.

요청

```json
{ "query": "서울숲역" }
```

응답 (성공)

```json
{
  "query": "서울숲역",
  "found": true,
  "place": {
    "name": "서울숲역 5호선",
    "address": "서울 성동구 성수동1가",
    "latitude": 37.5444,
    "longitude": 127.0374
  }
}
```

응답 (주소를 찾지 못함) — HTTP 200, `found: false`

```json
{ "query": "없는역", "found": false, "message": "입력한 장소를 찾지 못했어요." }
```

응답 (외부 API 오류) — HTTP 502

```json
{ "detail": "장소 정보를 가져오지 못했어요. 잠시 후 다시 시도해 주세요." }
```

주소를 못 찾은 것은 사용자가 고칠 수 있는 상황이라 200으로, 카카오 쪽 장애는 사용자가 고칠 수 없어
502로 구분한다. 화면에서도 각각 다른 안내 문구를 띄운다.

## POST /recommend

추천 후보를 돌려준다. Week 2에는 서버가 아직 더미 데이터를 쓰고, Week 3~4에 실제 장소 데이터와
경로 시간으로 교체한다.

요청

```json
{
  "origin": "서울숲역",
  "destination": "성수역",
  "time": 60,
  "budget": 10000,
  "activity": "카페"
}
```

- `activity`는 `산책 | 카페 | 구경 | 문화` 중 하나
- `time`은 분, `budget`은 원

응답

```json
{
  "origin": "서울숲역",
  "destination": "성수역",
  "time": 60,
  "results": [
    {
      "id": "seongsu-roastery",
      "name": "성수 로스터리 카페",
      "area": "성수·서울숲",
      "activity": "카페",
      "stayMinutes": 41,
      "travelMinutes": 7,
      "cost": 7000,
      "tags": ["실내", "앉아서 쉬기"],
      "reason": "잠깐 앉아 쉬기 좋고, 목적지와도 멀지 않은 선택이에요."
    }
  ]
}
```

`results`의 항목은 `index.html`의 `places` 배열 원소와 **필드 이름이 같다.** 그래서 Week 2에는
`places` 상수를 지우고 `fetch()` 결과를 그대로 넣으면 카드 렌더링 코드는 바꾸지 않아도 된다.
이번 주에 필드 이름을 정확히 잡아둔 이유가 이것이다.

응답 (조건에 맞는 후보 없음) — HTTP 200, 빈 배열

```json
{ "origin": "서울숲역", "destination": "성수역", "time": 60, "results": [] }
```

빈 배열은 오류가 아니다. 화면은 지금과 같이 "조건에 맞는 예시 코스가 없어요" 안내를 띄운다.

## Week 2에 `index.html`이 바뀌는 지점

지금 submit 핸들러에는 아래 주석이 달린 자리가 있다.

```text
// 지금은 브라우저 안에서 바로 계산하지만,
// Week 2에는 이 자리에 FastAPI로 보내는 fetch()가 들어갑니다.
```

`window.setTimeout` 자리에 `fetch()`가 들어가고, 이미 만들어 둔 Loading·Empty·Error 화면을
그대로 쓴다. 그래서 Week 2에 새로 만들 UI는 없다.

## 아직 정하지 않은 것

- 응답 개수: 이번 주 화면은 2개, 최종 MVP는 TOP 3다. Week 4에 정한다.
- `results` 정렬 기준: 지금은 남은 시간을 알차게 쓰는 순. Week 4에 정규화·가중치 기반 점수로 바꾼다.
- CORS 허용 도메인: 배포 주소가 정해지는 Week 5에 확정한다.
