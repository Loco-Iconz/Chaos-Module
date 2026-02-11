from fastapi import APIRouter
from app.models import MLFeatureSnapshot
from app.chaos_engine import (
    compute_live_state,
    compute_first_half_team_rating,
    compute_second_half_team_rating,
    compute_foul_rating,
    compute_turnover_rating
)

router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/snapshot")
def ml_snapshot(payload: MLFeatureSnapshot):
    """
    ML Snapshot Pipeline (v2.5)
    - Extracts full live engine metrics
    - Extracts all identity ratings
    - Packages everything into a training-ready feature vector
    """

    # Run the full live engine to get volatility, momentum, chaos, etc.
    live_state = compute_live_state(payload)

    # Compute identity ratings
    first_half_rating = compute_first_half_team_rating(payload)
    second_half_rating = compute_second_half_team_rating(payload)
    foul_rating = compute_foul_rating(payload)
    turnover_rating = compute_turnover_rating(payload)

    # Build ML feature vector
    feature_vector = {
        "game_id": payload.game_id,
        "snapshot_time": payload.snapshot_time,

        # Full live engine output
        "live_state": live_state,

        # Identity ratings
        "first_half_team_rating": first_half_rating,
        "second_half_team_rating": second_half_rating,
        "foul_rating": foul_rating,
        "turnover_rating": turnover_rating,

        # Optional supervised labels
        "label_outcome": payload.label_outcome,
        "label_margin": payload.label_margin,
        "label_covered_flag": payload.label_covered_flag
    }

    return {
        "status": "logged",
        "game_id": payload
