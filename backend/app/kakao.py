"""카카오 로컬 API 클라이언트.

key는 이 서버 안에만 있다. 브라우저로 내보내지 않는다.
"""
import httpx

from config import KAKAO_REST_API_KEY

BASE = "https://dapi.kakao.com/v2/local"
TIMEOUT = 5.0


class KakaoError(Exception):
    """카카오 쪽 문제. 사용자가 고칠 수 없는 상황."""

    def __init__(self, message: str, hint: str = ""):
        super().__init__(message)
        self.message = message
        self.hint = hint


def _headers() -> dict:
    if not KAKAO_REST_API_KEY:
        raise KakaoError(
            "카카오 API key가 설정되지 않았습니다.",
            "backend/.env 에 KAKAO_REST_API_KEY 를 넣으세요.",
        )
    return {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}


def _get(path: str, params: dict) -> dict:
    try:
        response = httpx.get(
            f"{BASE}{path}", headers=_headers(), params=params, timeout=TIMEOUT
        )
    except httpx.RequestError as exc:
        raise KakaoError("카카오에 연결하지 못했습니다.", str(exc)) from exc

    if response.status_code == 401:
        raise KakaoError("카카오 API key가 올바르지 않습니다.", "키를 다시 확인하세요.")
    if response.status_code == 403:
        # 가장 흔한 실수. 키는 맞는데 앱에서 카카오맵을 안 켠 경우다.
        raise KakaoError(
            "이 앱에서 카카오맵(로컬) 서비스가 꺼져 있습니다.",
            "developers.kakao.com → 내 애플리케이션 → 카카오맵 → 사용 설정 → 상태 ON",
        )
    if response.status_code == 429:
        raise KakaoError("카카오 API 사용량을 초과했습니다.", "잠시 후 다시 시도하세요.")
    if response.status_code >= 400:
        raise KakaoError(f"카카오 응답 오류 ({response.status_code})", response.text[:200])

    return response.json()


def search_keyword(query: str, size: int = 5, x: str = "", y: str = "", radius: int = 0) -> list[dict]:
    """장소명·주소로 검색한다."""
    params = {"query": query, "size": size}
    if x and y:
        params.update({"x": x, "y": y, "radius": radius, "sort": "distance"})
    return _get("/search/keyword.json", params).get("documents", [])


def search_category(code: str, x: str, y: str, radius: int = 1000, size: int = 15, page: int = 1) -> list[dict]:
    """카테고리 코드로 주변을 검색한다.

    CE7 카페 · FD6 음식점 · CT1 문화시설 · AT4 관광명소
    """
    return _get(
        "/search/category.json",
        {"category_group_code": code, "x": x, "y": y, "radius": radius,
         "size": size, "page": page, "sort": "distance"},
    ).get("documents", [])


def to_place_summary(doc: dict) -> dict:
    """카카오 응답에서 우리가 쓰는 부분만 꺼낸다."""
    return {
        "kakaoId": doc.get("id"),
        "name": doc.get("place_name"),
        "address": doc.get("road_address_name") or doc.get("address_name"),
        "category": doc.get("category_name"),
        "lat": float(doc["y"]),
        "lng": float(doc["x"]),
        "url": doc.get("place_url"),
    }
