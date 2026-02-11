from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import MLFeatureSnapshot
from chaos_engine import (
    compute_live_state,
    compute_first_half_team_rating,
    compute_second_half_team_rating,
    compute_foul_rating,
    compute_turnover_rating
)

app = FastAPI(
    title="Chaos Engine API",
    version="2.5",
    description="Live volatility engine + ML snapshot pipeline"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# ML Snapshot endpoint
@app.post("/ml/snapshot")
def ml_snapshot(payload: MLFeatureSnapshot):

    live_state = compute_live_state(payload)

    first_half_rating = compute_first_half_team_rating(payload)
    second_half_rating = compute_second_half_team_rating(payload)
    foul_rating = compute_foul_rating(payload)
    turnover_rating = compute_turnover_rating(payload)

    feature_vector = {
        "game_id": payload.game_id,
        "snapshot_time": payload.snapshot_time,
        "live_state": live_state,
        "first_half_rating": first_half_rating,
        "second_half_rating": second_half_rating,
        "foul_rating": foul_rating,
        "turnover_rating": turnover_rating
    }

    return feature_vector
