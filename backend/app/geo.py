"""좌표 계산. 카카오 API 없이 할 수 있는 부분."""
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0

# 도보 속도. 신호 대기와 길 찾는 시간을 감안해 보수적으로 잡는다.
WALK_KM_PER_HOUR = 4.0


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """두 좌표 사이의 직선 거리(km).

    지구가 둥글기 때문에 평면 거리 공식을 쓰면 틀린다.
    haversine은 구면 위의 최단 거리를 구하는 공식이다.
    """
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def walk_minutes(distance_km: float) -> int:
    """직선 거리를 도보 분으로 어림한다.

    실제 길은 직선이 아니므로 1.3배를 곱한다(우회 계수).
    정확한 값은 카카오 경로 API가 주며, 그때 이 함수는 대체된다.
    """
    return max(1, round(distance_km * 1.3 / WALK_KM_PER_HOUR * 60))


def detour_minutes(
    origin: tuple[float, float],
    place: tuple[float, float],
    destination: tuple[float, float],
) -> int:
    """우회에 드는 추가 이동 시간.

    출발지에서 목적지로 바로 가는 대신 중간에 들렀을 때
    늘어나는 시간만 계산한다. 어차피 가야 할 길은 빼는 것이다.

        직행:  출발 → 목적지
        우회:  출발 → 후보 → 목적지
        추가:  우회 - 직행
    """
    direct = haversine_km(*origin, *destination)
    via = haversine_km(*origin, *place) + haversine_km(*place, *destination)
    return walk_minutes(max(0.0, via - direct))
