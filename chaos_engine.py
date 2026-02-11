from fastapi import APIRouter
from pydantic import BaseModel

# ---------------------------------------------------------
# FASTAPI ROUTER
# ---------------------------------------------------------
router = APIRouter()

# ---------------------------------------------------------
# PAYLOAD MODEL (matches your engine logic)
# ---------------------------------------------------------
class ChaosPayload(BaseModel):
    home_score: int
    away_score: int
    home_pace: float
    away_pace: float
    home_efficiency: float
    away_efficiency: float
    home_fouls: int
    away_fouls: int
    home_turnovers: int
    away_turnovers: int


# ---------------------------------------------------------
# RATING FUNCTIONS (your original logic)
# ---------------------------------------------------------
def compute_first_half_team_rating(score_diff, pace, efficiency):
    return (score_diff * 0.4) + (pace * 0.3) + (efficiency * 0.3)


def compute_second_half_team_rating(score_diff, pace, efficiency):
    return (score_diff * 0.5) + (pace * 0.2) + (efficiency * 0.3)


def compute_foul_rating(fouls):
    if fouls <= 5:
        return 1.0
    elif fouls <= 8:
        return 0.8
    else:
        return 0.6


def compute_turnover_rating(turnovers):
    if turnovers <= 5:
        return 1.0
    elif turnovers <= 10:
        return 0.8
    else:
        return 0.6


# ---------------------------------------------------------
# CORE CHAOS ENGINE v2.0 (your logic)
# ---------------------------------------------------------
def compute_live_state(payload: ChaosPayload):
    score_diff = payload.home_score - payload.away_score
    pace_status = "fast" if (payload.home_pace + payload.away_pace) / 2 > 70 else "slow"
    efficiency_status = "high" if (payload.home_efficiency + payload.away_efficiency) / 2 > 1.05 else "low"

    total_fouls = payload.home_fouls + payload.away_fouls
    whistle_status = "tight" if total_fouls > 12 else "normal"

    total_turnovers = payload.home_turnovers + payload.away_turnovers
    turnover_status = "clean" if total_turnovers < 10 else "sloppy"

    return {
        "score_diff": score_diff,
        "pace_status": pace_status,
        "efficiency_status": efficiency_status,
        "whistle_status": whistle_status,
        "turnover_status": turnover_status,
    }


# ---------------------------------------------------------
# FASTAPI ENDPOINTS
# ---------------------------------------------------------
@router.get("/live")
def live_check():
    return {"status": "ok", "engine": "chaos-engine-online"}


@router.post("/compute")
def compute(payload: ChaosPayload):
    result = compute_live_state(payload)
    return {
        "status": "processed",
        "engine_output": result
    }
