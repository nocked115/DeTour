"""DETOUR 추천 서버.

브라우저가 보낸 조건으로 우회 코스 TOP 3를 돌려준다.
순위뿐 아니라 왜 추천하는지도 함께 보낸다.
"""
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import kakao
from config import ALLOWED_ORIGINS, DATA_FILE, kakao_ready
from geo import detour_minutes
from scoring import score_places

app = FastAPI(
    title="DETOUR API",
    description="남은 시간·예산·활동에 맞는 작은 우회로를 추천한다.",
)

# 브라우저가 다른 출처의 서버를 부르려면 서버가 먼저 허락해야 한다.
# 개발 중에는 "*"였지만, 실제로 부르는 곳만 남겼다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.github\.io",
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

with open(DATA_FILE, encoding="utf-8") as f:
    DATA = json.load(f)
PLACES = DATA["places"]


# ---------- 주고받는 데이터의 모양 ----------

class GeocodeRequest(BaseModel):
    query: str = Field(min_length=1, description="주소 또는 장소명")


class RecommendRequest(BaseModel):
    origin: str = Field(min_length=1)
    destination: str = Field(min_length=1)
    time: int = Field(gt=0, le=600, description="남은 시간(분)")
    budget: int = Field(ge=0, description="예산(원)")
    activity: str = Field(description="산책 | 카페 | 구경 | 문화")
    limit: int = Field(default=3, ge=1, le=10)


# ---------- Endpoint ----------

@app.get("/health")
def health():
    """서버가 살아있는지, 카카오를 쓸 준비가 됐는지."""
    return {
        "status": "ok",
        "places": len(PLACES),
        "placesAreReal": DATA.get("isReal", False),
        "kakaoKeyConfigured": kakao_ready(),
    }


@app.get("/places")
def list_places():
    return {"count": len(PLACES), "source": DATA.get("source"), "places": PLACES}


@app.post("/geocode")
def geocode(req: GeocodeRequest):
    """주소·장소명을 좌표로 바꾼다.

    실패를 두 가지로 나눈다.
      찾지 못함  → 200 + found:false  (사용자가 다시 입력하면 된다)
      카카오 문제 → 200 + error       (사용자가 고칠 수 없다)
    둘을 섞으면 화면에서 같은 안내를 띄우게 되는데, 사용자가 할 일이 다르다.
    """
    try:
        docs = kakao.search_keyword(req.query, size=1)
    except kakao.KakaoError as exc:
        return {
            "query": req.query,
            "found": False,
            "error": exc.message,
            "hint": exc.hint,
            "retryable": True,
        }

    if not docs:
        return {
            "query": req.query,
            "found": False,
            "message": f"‘{req.query}’ 이라는 장소를 찾지 못했어요.",
            "retryable": False,
        }

    return {"query": req.query, "found": True, "place": kakao.to_place_summary(docs[0])}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    """조건에 맞는 우회 코스를 점수 순으로 돌려준다.

    출발지·도착지의 좌표를 찾을 수 있으면 실제 우회 거리를 계산하고,
    못 찾으면 장소에 적힌 예시 이동 시간을 쓴다. 어느 쪽인지 응답에 밝힌다.
    """
    coords, notice = {}, None
    if kakao_ready():
        try:
            for role, query in (("origin", req.origin), ("destination", req.destination)):
                docs = kakao.search_keyword(query, size=1)
                if docs:
                    p = kakao.to_place_summary(docs[0])
                    coords[role] = (p["lat"], p["lng"])
        except kakao.KakaoError as exc:
            notice = exc.message

    use_real_distance = len(coords) == 2
    lookup = None
    if use_real_distance:
        def lookup(place):
            if place.get("lat") is None:
                return place.get("travelMinutes", 0)
            return detour_minutes(
                coords["origin"], (place["lat"], place["lng"]), coords["destination"]
            )

    scored = score_places(PLACES, req.time, req.budget, req.activity, lookup)[: req.limit]

    return {
        "origin": req.origin,
        "destination": req.destination,
        "time": req.time,
        "budget": req.budget,
        "activity": req.activity,
        "distanceSource": "kakao" if use_real_distance else "example",
        "placesAreReal": DATA.get("isReal", False),
        "notice": notice,
        "results": [
            {
                "id": s.place["id"],
                "name": s.place["name"],
                "area": s.place.get("area"),
                "activity": s.place["activity"],
                "placeType": s.place.get("placeType"),
                "lat": s.place.get("lat"),
                "lng": s.place.get("lng"),
                "stayMinutes": s.place["stayMinutes"],
                "travelMinutes": s.detour_minutes,
                "totalMinutes": s.total_minutes,
                "spareMinutes": s.spare_minutes,
                "cost": s.place["cost"],
                "tags": s.place.get("tags", []),
                "score": s.score,
                "features": s.features,     # 점수의 근거를 그대로 보낸다
                "reason": s.reason,
                "placeReason": s.place.get("reason"),
            }
            for s in scored
        ],
    }
