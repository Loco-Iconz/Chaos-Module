from pydantic import BaseModel
from typing import Optional


# ---------------------------------------------------------
# LIVE ENGINE INPUT
# ---------------------------------------------------------

class LiveInput(BaseModel):
    game_id: str
    time: str
    away_score: int
    home_score: int
    away_fouls: int
    home_fouls: int
    away_turnovers: int
    home_turnovers: int
    star_override: bool = False
    star_multiplier: float = 1.0
    trap_flag: bool = False
    deception_flag: bool = False


# ---------------------------------------------------------
# LIVE ENGINE OUTPUT (FULL v2.5)
# ---------------------------------------------------------

class LiveOutput(BaseModel):
    game_id: str
    score_diff: int
    pace_status: str
    efficiency_status: str
    whistle_status: str
    turnover_status: str

    volatility_score_v2: float

    collapse_prob_away_v2: float
    collapse_prob_home_v2: float
    comeback_prob_away_v2: float
    comeback_prob_home_v2: float

    live_edge_v2: float

    away_run_ceiling_v2: float
    home_run_ceiling_v2: float

    avalanche_flag_v2: bool

    momentum_score: float
    drive_score: float

    chaos_probability: float
    stability_probability: float

    # -----------------------------------------------------
    # NEW RATINGS (IDENTITY METRICS)
    # -----------------------------------------------------
    first_half_team_rating: float
    second_half_team_rating: float
    foul_rating: float
    turnover_rating: float


# ---------------------------------------------------------
# RULE ENGINE
# ---------------------------------------------------------

class RuleEvent(BaseModel):
    game_id: str
    rule_name: str
    rule_weight: float = 1.0
    trigger_count: int = 1


class RuleScoreOutput(BaseModel):
    game_id: str
    rule_name: str
    rule_weight: float
    trigger_count: int
    rule_score: float
    adaptive_weight: float


# ---------------------------------------------------------
# OUTCOME HINT ENGINE
# ---------------------------------------------------------

class OutcomeHintInput(BaseModel):
    probability_value: float


class OutcomeHintOutput(BaseModel):
    probability_tier: str
    chaos_probability_hint: str


# ---------------------------------------------------------
# ML SNAPSHOT PIPELINE
# ---------------------------------------------------------

class MLFeatureSnapshot(BaseModel):
    game_id: str
    snapshot_time: str
    feature_vector: Optional[str] = None

    # Optional labels for supervised learning
    label_outcome: Optional[str] = None
    label_margin: Optional[float] = None
    label_covered_flag: Optional[bool] = None
