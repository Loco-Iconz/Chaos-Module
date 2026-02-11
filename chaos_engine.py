from fastapi import APIRouter
from models import LiveInput, LiveOutput

router = APIRouter(prefix="", tags=["chaos-engine"])


def compute_live_state(payload: LiveInput) -> LiveOutput:
    # Core score diff
    score_diff = payload.home_score - payload.away_score

    total_points = payload.home_score + payload.away_score
    total_fouls = payload.home_fouls + payload.away_fouls
    total_turnovers = payload.home_turnovers + payload.away_turnovers

    # Pace
    pace_status = "fast" if total_points >= 120 else "slow"

    # Efficiency (simple)
    efficiency_status = "high" if total_points >= 100 else "low"

    # Whistle
    if total_fouls >= 18:
        whistle_status = "tight"
    elif total_fouls <= 8:
        whistle_status = "loose"
    else:
        whistle_status = "normal"

    # Turnovers
    if total_turnovers >= 24:
        turnover_status = "sloppy"
    elif total_turnovers <= 10:
        turnover_status = "clean"
    else:
        turnover_status = "average"

    # Volatility
    volatility_score_v2 = (
        abs(score_diff) * 0.4
        + total_turnovers * 0.3
        + (payload.star_multiplier * 10 if payload.star_override else 0)
        + (5 if payload.trap_flag else 0)
        + (5 if payload.deception_flag else 0)
    )

    # Collapse / comeback
    collapse_probability = min(0.95, max(0.05, abs(score_diff) / 30.0))
    comeback_probability = 1.0 - collapse_probability

    # Live edge
    live_edge_v2 = score_diff * (1 + (volatility_score_v2 / 100.0))

    # Run ceilings
    run_ceiling_home = max(5.0, 10.0 + volatility_score_v2 / 5.0)
    run_ceiling_away = max(5.0, 10.0 + volatility_score_v2 / 5.0)

    # Avalanche
    avalanche_flag_v2 = volatility_score_v2 >= 25.0

    # Momentum / drive
    momentum_score = score_diff - (total_turnovers * 0.5)
    drive_score = total_points / 2.0

    # Chaos vs stability
    chaos_probability = min(0.95, volatility_score_v2 / 40.0)
    stability_probability = 1.0 - chaos_probability

    # Half ratings (simple)
    first_half_team_rating = score_diff - (total_fouls * 0.2)
    second_half_team_rating = score_diff - (total_turnovers * 0.3)

    return LiveOutput(
        score_diff=score_diff,
        pace_status=pace_status,
        efficiency_status=efficiency_status,
        whistle_status=whistle_status,
        turnover_status=turnover_status,
        volatility_score_v2=volatility_score_v2,
        collapse_probability=collapse_probability,
        comeback_probability=comeback_probability,
        live_edge_v2=live_edge_v2,
        run_ceiling_home=run_ceiling_home,
        run_ceiling_away=run_ceiling_away,
        avalanche_flag_v2=avalanche_flag_v2,
        momentum_score=momentum_score,
        drive_score=drive_score,
        chaos_probability=chaos_probability,
        stability_probability=stability_probability,
        first_half_team_rating=first_half_team_rating,
        second_half_team_rating=second_half_team_rating,
    )


@router.get("/live")
def live_status():
    return {"status": "online", "service": "chaos-engine"}


@router.post("/compute", response_model=LiveOutput)
def compute_structured(payload: LiveInput):
    return compute_live_state(payload)


@router.post("/compute/raw")
def compute_raw(payload: LiveInput):
    result = compute_live_state(payload)
    return {
        "status": "processed",
        "engine_output": result.dict(),
    }
