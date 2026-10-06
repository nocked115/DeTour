"""추천 점수 계산.

파이프라인은 AGENTS.md에 적힌 그대로다.

    Feature Engineering → Normalization → Weight → Score → Ranking → 추천 이유

모든 Feature는 0~1로 정규화하고, 1에 가까울수록 좋다.
단위가 서로 다른 값(분, 원, km)을 그대로 더할 수 없기 때문이다.
"""
from dataclasses import dataclass

# 가중치. 합이 1이 되게 둔다.
#
# 시간을 가장 크게 본 이유: DETOUR는 "남은 시간"에서 출발한 서비스다.
# 우회 시간이 그다음인 이유: 목적지에서 많이 벗어나면 애초에 우회로가 아니다.
# 예산이 가장 작은 이유: 조건을 넘지 않으면 대체로 받아들일 수 있는 값이다.
WEIGHTS = {
    "time": 0.45,
    "detour": 0.30,
    "budget": 0.25,
}

# 남은 시간의 몇 %를 쓰는 것이 가장 좋은가.
# 1.0(꽉 채움)은 늦을까 불안하고, 0.2(거의 안 씀)는 시간이 아깝다.
IDEAL_TIME_USAGE = 0.75

# 우회 시간이 이만큼이면 적합도가 절반이 된다.
DETOUR_HALF_LIFE_MINUTES = 10.0


@dataclass
class Scored:
    place: dict
    score: float
    features: dict      # 정규화된 0~1 값
    total_minutes: int
    detour_minutes: int
    spare_minutes: int
    reason: str


def time_fit(total_minutes: int, available_minutes: int) -> float:
    """남은 시간을 얼마나 알맞게 쓰는가.

    짧아도 감점이고 빠듯해도 감점이다. 0.75 근처가 가장 높다.
    """
    if available_minutes <= 0:
        return 0.0
    usage = total_minutes / available_minutes
    gap = abs(usage - IDEAL_TIME_USAGE)
    return max(0.0, 1.0 - gap / IDEAL_TIME_USAGE)


def budget_fit(cost: int, budget: int) -> float:
    """예산 대비 비용.

    쌀수록 좋지만, 예산 안에 들어오기만 하면 0.5 아래로는 내려가지 않는다.
    "싼 것이 항상 좋다"로 만들면 무료 장소만 추천하게 된다.
    """
    if budget <= 0:
        return 1.0 if cost <= 0 else 0.0
    return max(0.0, 1.0 - (cost / budget) * 0.5)


def detour_fit(extra_minutes: int) -> float:
    """목적지에서 벗어나는 정도.

    0분이면 1.0, 10분이면 0.5, 20분이면 0.33으로 완만하게 떨어진다.
    """
    return 1.0 / (1.0 + extra_minutes / DETOUR_HALF_LIFE_MINUTES)


def build_reason(place: dict, features: dict, spare: int, extra: int) -> str:
    """점수의 근거로 문장을 만든다.

    가장 높은 Feature 두 개를 골라 설명한다.
    순위만 보여주는 대신 "왜"를 함께 주는 것이 이 서비스의 목표다.
    """
    ranked = sorted(features.items(), key=lambda kv: kv[1], reverse=True)
    parts = []
    for name, value in ranked[:2]:
        if value < 0.4:
            continue
        if name == "time":
            parts.append(f"남은 시간에 알맞게 들어가요 ({spare}분 여유)")
        elif name == "detour":
            parts.append(
                "가는 길에서 거의 벗어나지 않아요" if extra <= 3
                else f"목적지 방향이라 {extra}분만 더 걸어요"
            )
        elif name == "budget":
            parts.append("예산이 넉넉해요" if place["cost"] == 0 else "예산 안에서 여유 있어요")
    if not parts:
        parts.append("지금 조건에 들어오는 선택지예요")
    return " · ".join(parts)


def score_places(
    places: list[dict],
    available_minutes: int,
    budget: int,
    activity: str,
    detour_lookup=None,
) -> list[Scored]:
    """조건에 맞는 후보를 걸러 점수를 매기고 순위를 낸다.

    detour_lookup(place) -> 추가 이동 분. 좌표가 없으면 None을 넘겨
    장소에 적힌 travelMinutes를 그대로 쓴다.
    """
    results: list[Scored] = []

    for place in places:
        if place["activity"] != activity:
            continue
        if place["cost"] > budget:
            continue

        extra = (
            detour_lookup(place) if detour_lookup else place.get("travelMinutes", 0)
        )
        total = place["stayMinutes"] + extra
        if total > available_minutes:
            continue

        features = {
            "time": time_fit(total, available_minutes),
            "detour": detour_fit(extra),
            "budget": budget_fit(place["cost"], budget),
        }
        score = sum(WEIGHTS[k] * v for k, v in features.items())
        spare = available_minutes - total

        results.append(
            Scored(
                place=place,
                score=round(score, 4),
                features={k: round(v, 3) for k, v in features.items()},
                total_minutes=total,
                detour_minutes=extra,
                spare_minutes=spare,
                reason=build_reason(place, features, spare, extra),
            )
        )

    results.sort(key=lambda s: s.score, reverse=True)
    return results
