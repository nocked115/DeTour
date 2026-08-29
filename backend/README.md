# DETOUR Backend

FastAPI 서버. 브라우저가 보낸 조건으로 추천 후보를 돌려준다.

## 실행

```bash
cd backend
.venv/bin/uvicorn app.main:app --reload --port 8000
```

`http://127.0.0.1:8000/docs`에서 직접 호출해볼 수 있다.

## 처음 받았다면

```bash
cd backend
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Endpoint

| 주소 | 방식 | 하는 일 | 카카오 키 |
| --- | --- | --- | --- |
| `/health` | GET | 서버가 살아있는지 | 불필요 |
| `/places` | GET | 장소 20개 전부 | 불필요 |
| `/recommend` | POST | 조건에 맞는 후보 2개 | 불필요 |
| `/geocode` | POST | 주소 → 좌표 (아직 없음) | **필요** |

요청·응답 형식은 [`../docs/WEEK2_API_CONTRACT.md`](../docs/WEEK2_API_CONTRACT.md)를 따른다.

## 화면과 함께 띄우기

`index.html`을 `file://`로 열면 브라우저가 출처를 `null`로 보고 서버 호출을 막는다.
정적 서버로 띄워야 한다.

```bash
python3.12 -m http.server 5500      # 저장소 루트에서
```

그다음 `http://127.0.0.1:5500/index.html`로 연다.

## 아직 남은 것

- `allow_origins=["*"]`는 개발용이다. 배포 시 실제 도메인으로 좁힌다.
- 서버 배포는 Week 3 Session 3. 배포하면 `index.html`의 `API_BASE`를 바꾼다.
