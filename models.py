from pydantic import BaseModel


class LiveInput(BaseModel):
    game_id: str
    time: str

    home_score: int
    away_score: int

    home_fouls: int
    away_fouls: int

    home_turnovers: int
    away_turnovers: int

    star_override: bool = False
    star_multiplier: float = 1.0

    trap_flag: bool = False
    deception_flag: bool = False


class LiveOutput(BaseModel):
    score_diff: int

    pace_status: str
    efficiency_status: str
    whistle_status: str
    turnover_status: str

    volatility_score_v2: float

    collapse_probability: float
    comeback_probability: float

    live_edge_v2: float

    run_ceiling_home: float
    run_ceiling_away: float

    avalanche_flag_v2: bool

    momentum_score: float
    drive_score: float

    chaos_probability: float
    stability_probability: float

    first_half_team_rating: float
    second_half_team_rating: float
