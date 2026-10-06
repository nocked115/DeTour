"""성수동 실제 장소를 카카오 카테고리 검색으로 수집한다.

카카오맵이 켜지면 이 스크립트가 예시 20개를 진짜 장소로 교체한다.

    .venv/bin/python scripts_collect.py           # 후보를 보기만 함
    .venv/bin/python scripts_collect.py --write   # data/places.json 에 저장

체류 시간과 비용은 카카오가 주지 않는다. docs/PLACE_RULES.md 의 규칙표로 채운다.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

import kakao  # noqa: E402

CENTER = {"name": "성수·서울숲", "lat": 37.5445, "lng": 127.0465, "radius": 1200}

# 규칙표(docs/PLACE_RULES.md)
RULES = {
    "cafe-takeout": {"activity": "카페", "stayMinutes": 10, "cost": 4500},
    "cafe-sit":     {"activity": "카페", "stayMinutes": 40, "cost": 7000},
    "bakery":       {"activity": "카페", "stayMinutes": 30, "cost": 8000},
    "bookstore":    {"activity": "구경", "stayMinutes": 25, "cost": 2000},
    "giftshop":     {"activity": "구경", "stayMinutes": 25, "cost": 3000},
    "market":       {"activity": "구경", "stayMinutes": 45, "cost": 5000},
    "gallery":      {"activity": "문화", "stayMinutes": 40, "cost": 5000},
    "exhibition":   {"activity": "문화", "stayMinutes": 40, "cost": 3000},
    "library":      {"activity": "문화", "stayMinutes": 35, "cost": 0},
    "park":         {"activity": "산책", "stayMinutes": 30, "cost": 0},
    "riverside":    {"activity": "산책", "stayMinutes": 45, "cost": 0},
    "street":       {"activity": "산책", "stayMinutes": 30, "cost": 0},
}

# 카카오 카테고리 이름에서 placeType 을 고른다.
# 사람이 최종 확인해야 하는 부분이다 — 이 분류는 어림짐작이다.
def guess_type(doc: dict) -> str | None:
    cat = doc.get("category", "")
    name = doc.get("name", "")
    if "도서관" in cat or "도서관" in name:
        return "library"
    if "미술관" in cat or "갤러리" in name:
        return "gallery"
    if "전시" in cat or "전시" in name:
        return "exhibition"
    if "서점" in cat or "책방" in name:
        return "bookstore"
    if "공원" in cat:
        return "park"
    if "베이커리" in cat or "제과" in cat or "빵" in name:
        return "bakery"
    if "카페" in cat:
        return "cafe-takeout" if re.search(r"(테이크아웃|то고|TO GO)", name, re.I) else "cafe-sit"
    return None


TAGS_BY_TYPE = {
    "cafe-takeout": ["빠름", "가까움"], "cafe-sit": ["실내", "앉아서 쉬기"],
    "bakery": ["실내", "간단한 식사"], "bookstore": ["실내", "조용함"],
    "giftshop": ["실내", "저예산"], "market": ["야외", "활기참"],
    "gallery": ["실내", "여유"], "exhibition": ["실내", "짧은 관람"],
    "library": ["실내", "무료"], "park": ["야외", "무료"],
    "riverside": ["야외", "조용함"], "street": ["야외", "구경 겸용"],
}


def slugify(name: str, kakao_id: str) -> str:
    base = re.sub(r"[^0-9a-zA-Z가-힣]+", "-", name).strip("-").lower()
    return f"{base}-{kakao_id}"[:60]


def collect() -> list[dict]:
    seen, out = set(), []
    for code in ("CE7", "CT1", "AT4"):
        for page in (1, 2, 3):
            try:
                docs = kakao.search_category(
                    code, str(CENTER["lng"]), str(CENTER["lat"]),
                    radius=CENTER["radius"], size=15, page=page,
                )
            except kakao.KakaoError as exc:
                print(f"❌ {exc.message}\n   → {exc.hint}")
                return []
            if not docs:
                break
            for doc in docs:
                p = kakao.to_place_summary(doc)
                if p["kakaoId"] in seen:
                    continue
                seen.add(p["kakaoId"])
                ptype = guess_type(p)
                if not ptype:
                    continue
                rule = RULES[ptype]
                out.append({
                    "id": slugify(p["name"], p["kakaoId"]),
                    "name": p["name"],
                    "area": CENTER["name"],
                    "address": p["address"],
                    "activity": rule["activity"],
                    "placeType": ptype,
                    "stayMinutes": rule["stayMinutes"],
                    "cost": rule["cost"],
                    "lat": p["lat"], "lng": p["lng"],
                    "tags": TAGS_BY_TYPE[ptype],
                    "reason": "",          # Week 4부터는 점수 근거로 자동 생성한다
                    "url": p["url"],
                    "isReal": True,
                })
    return out


if __name__ == "__main__":
    places = collect()
    if not places:
        sys.exit(1)

    by_activity = {}
    for p in places:
        by_activity.setdefault(p["activity"], []).append(p)
    print(f"수집 {len(places)}개")
    for act, items in sorted(by_activity.items()):
        print(f"  {act}: {len(items)}개 — {', '.join(i['name'] for i in items[:3])} ...")

    if "--write" in sys.argv:
        # 활동별로 고르게 남긴다. 한 활동만 많으면 추천이 치우친다.
        picked = [p for items in by_activity.values() for p in items[:8]]
        json.dump(
            {"area": CENTER["name"],
             "source": "카카오맵 카테고리 검색 (CE7/CT1/AT4), 반경 %dm" % CENTER["radius"],
             "collectedAt": datetime.now(timezone.utc).isoformat(),
             "isReal": True,
             "note": "체류 시간과 비용은 docs/PLACE_RULES.md 규칙표로 채운 추정치다.",
             "places": picked},
            open(Path(__file__).parent / "data" / "places.json", "w", encoding="utf-8"),
            ensure_ascii=False, indent=2,
        )
        print(f"\n✅ data/places.json 에 {len(picked)}개 저장")
    else:
        print("\n저장하려면 --write 를 붙이세요.")
