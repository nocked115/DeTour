# DETOUR API

FastAPI 서버의 Endpoint 네 개. 요청·응답 형식은 여기를 기준으로 한다.

실행 중이면 `http://127.0.0.1:8000/docs`에서 직접 호출해볼 수 있다.

## 키가 필요한가

| Endpoint | 카카오 키 | 비고 |
| --- | --- | --- |
| `GET /health` | 불필요 | |
| `GET /places` | 불필요 | |
| `POST /recommend` | 선택 | 키가 있으면 실제 거리로 계산, 없으면 예시 값 |
| `POST /geocode` | **필요** | |

키는 `backend/.env`의 `KAKAO_REST_API_KEY`에서만 읽는다. 브라우저로 내보내지 않는다.

---

## GET /health

```json
{
  "status": "ok",
  "places": 20,
  "placesAreReal": false,
  "kakaoKeyConfigured": true
}
```

`placesAreReal`이 `false`면 장소가 아직 직접 지어낸 예시라는 뜻이다.
화면은 이 값을 보고 "장소는 아직 예시입니다"를 표시한다.

---

## POST /geocode

주소나 장소명을 좌표로 바꾼다.

```json
{ "query": "서울숲역" }
```

**찾았을 때**

```json
{
  "query": "서울숲역",
  "found": true,
  "place": {
    "kakaoId": "8502125",
    "name": "서울숲역 5호선",
    "address": "서울 성동구 성수동1가",
    "category": "교통,수송 > 지하철,전철",
    "lat": 37.5444, "lng": 127.0374,
    "url": "http://place.map.kakao.com/8502125"
  }
}
```

**찾지 못했을 때** — 사용자가 다시 입력하면 된다

```json
{
  "query": "ㅁㄴㅇㄹ",
  "found": false,
  "message": "‘ㅁㄴㅇㄹ’ 이라는 장소를 찾지 못했어요.",
  "retryable": false
}
```

**카카오 쪽 문제** — 사용자가 고칠 수 없다

```json
{
  "query": "서울숲역",
  "found": false,
  "error": "이 앱에서 카카오맵(로컬) 서비스가 꺼져 있습니다.",
  "hint": "developers.kakao.com → 내 애플리케이션 → 카카오맵 → 사용 설정 → 상태 ON",
  "retryable": true
}
```

**둘을 나눈 이유**: 화면에서 할 일이 다르다. 전자는 "다시 입력해 주세요",
후자는 "다시 시도하기" 버튼을 줘야 한다. 하나로 합치면 사용자가
고칠 수 없는 걸 고치라고 하게 된다.

---

## POST /recommend

```json
{
  "origin": "서울숲역",
  "destination": "성수역",
  "time": 60,
  "budget": 10000,
  "activity": "카페",
  "limit": 3
}
```

| 필드 | 제약 |
| --- | --- |
| `time` | 1~600 (분) |
| `budget` | 0 이상 (원) |
| `activity` | `산책` / `카페` / `구경` / `문화` |
| `limit` | 1~10, 기본 3 |

제약을 어기면 **422**와 함께 어느 필드가 왜 틀렸는지 돌아온다. Pydantic이 처리한다.

**응답**

```json
{
  "origin": "서울숲역",
  "destination": "성수역",
  "time": 60,
  "distanceSource": "example",
  "placesAreReal": false,
  "notice": null,
  "results": [
    {
      "id": "seongsu-roastery",
      "name": "성수 로스터리 카페",
      "activity": "카페",
      "placeType": "cafe-sit",
      "lat": 37.5447, "lng": 127.051,
      "stayMinutes": 41,
      "travelMinutes": 7,
      "totalMinutes": 48,
      "spareMinutes": 12,
      "cost": 7000,
      "tags": ["실내", "앉아서 쉬기"],
      "score": 0.759,
      "features": { "time": 0.933, "detour": 0.588, "budget": 0.65 },
      "reason": "남은 시간에 알맞게 들어가요 (12분 여유) · 예산 안에서 여유 있어요"
    }
  ]
}
```

### `distanceSource`

| 값 | 뜻 |
| --- | --- |
| `kakao` | 출발지·도착지 좌표를 찾아 **실제 우회 거리**로 계산했다 |
| `example` | 좌표를 못 구해 장소에 적힌 **예시 이동 시간**을 썼다 |

화면은 `example`일 때 "이동 시간은 예시 값이에요"를 표시한다.
숫자의 출처를 숨기지 않는 것이 이 서비스의 원칙이다.

### `features` — 점수의 근거

0~1로 정규화된 값이며, 셋을 가중치로 합한 것이 `score`다.

```
score = 0.45 × time  +  0.30 × detour  +  0.25 × budget
```

| Feature | 뜻 | 1.0에 가까우려면 |
| --- | --- | --- |
| `time` | 남은 시간을 알맞게 쓰는가 | 남은 시간의 75%쯤 사용 |
| `detour` | 목적지에서 얼마나 벗어나는가 | 추가 이동 0분 |
| `budget` | 예산 대비 비용 | 비용 0원 |

가중치의 근거는 `backend/app/scoring.py`의 주석에 적혀 있다.
화면은 이 값을 막대로 그려서 **왜 1등인지 눈으로 확인할 수 있게** 한다.

**결과가 없을 때**는 `results: []`다. 오류가 아니며 HTTP 200이다.
