# DETOUR Backend

FastAPI 서버. 브라우저가 보낸 조건으로 우회 코스 TOP 3를 점수 순으로 돌려준다.

## 실행

```bash
cd backend
.venv/bin/uvicorn main:app --reload --port 8000 --app-dir app
```

`http://127.0.0.1:8000/docs`에서 직접 호출해볼 수 있다.

## 처음 받았다면

```bash
cd backend
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env     # 그리고 카카오 REST API key를 넣는다
```

## 화면과 함께 띄우기

`index.html`을 `file://`로 열면 브라우저가 출처를 `null`로 보고 서버 호출을 막는다.
정적 서버로 띄워야 한다.

```bash
python3.12 -m http.server 5500      # 저장소 루트에서
```

그다음 `http://127.0.0.1:5500/index.html`로 연다.

## 구조

| 파일 | 하는 일 |
| --- | --- |
| `app/main.py` | Endpoint와 요청·응답 모양 |
| `app/config.py` | `.env` 읽기, 허용 출처 |
| `app/kakao.py` | 카카오 로컬 API 호출, 오류를 사람 말로 변환 |
| `app/geo.py` | haversine 거리, 우회 추가 시간 — 카카오 없이 동작 |
| `app/scoring.py` | 정규화 → 가중치 → 점수 → 순위 → 이유 |
| `data/places.json` | 장소 데이터 |
| `scripts_collect.py` | 카카오로 실제 장소 수집 |

Endpoint 상세는 [`../docs/API.md`](../docs/API.md)에 있다.

## 실제 장소로 교체하기

지금 `data/places.json`은 직접 지어낸 예시다 (`isReal: false`).
카카오맵이 켜지면 아래로 교체한다.

```bash
.venv/bin/python scripts_collect.py           # 후보만 본다
.venv/bin/python scripts_collect.py --write   # data/places.json 에 저장
```

체류 시간과 비용은 카카오가 주지 않으므로 [`../docs/PLACE_RULES.md`](../docs/PLACE_RULES.md)의
규칙표로 채운다. `placeType` 분류는 어림짐작이라 사람이 확인해야 한다.

## 배포할 때

- `KAKAO_REST_API_KEY`를 환경변수로 넣는다. `.env` 파일은 올리지 않는다.
- `app/config.py`의 `ALLOWED_ORIGINS`에 배포된 화면 주소를 넣는다.
- `index.html`의 `API_BASE`를 배포된 서버 주소로 바꾼다.
