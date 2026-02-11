from math import exp

# ---------------------------------------------------------
# NEW RATING FUNCTIONS
# ---------------------------------------------------------

def compute_first_half_team_rating(payload):
    score_diff = payload.away_score - payload.home_score
    pace_factor = 1 if payload.time.startswith("1H") else 0.5
    foul_penalty = (payload.away_fouls + payload.home_fouls) * 0.3
    turnover_penalty = (payload.away_turnovers + payload.home_turnovers) * 0.4

    return max(0, 50 + score_diff * 1.2 + pace_factor * 10 - foul_penalty - turnover_penalty)


def compute_second_half_team_rating(payload):
    score_diff = payload.away_score - payload.home_score
    pressure_factor = 1.5 if payload.time.startswith("2H") else 0.7
    foul_penalty = (payload.away_fouls + payload.home_fouls) * 0.5
    turnover_penalty = (payload.away_turnovers + payload.home_turnovers) * 0.6

    return max(0, 50 + score_diff * 1.5 + pressure_factor * 12 - foul_penalty - turnover_penalty)


def compute_foul_rating(payload):
    total_fouls = payload.away_fouls + payload.home_fouls
    return max(0, 100 - total_fouls * 4)


def compute_turnover_rating(payload):
    total_turnovers = payload.away_turnovers + payload.home_turnovers
    return max(0, 100 - total_turnovers * 5)


# ---------------------------------------------------------
# CORE CHAOS ENGINE v2.0
# ---------------------------------------------------------

def compute_live_state(payload):

    # Basic score diff
    score_diff = payload.away_score - payload.home_score

    # Pace status
    if score_diff > 12:
        pace_status = "fast"
    elif score_diff < -12:
        pace_status = "slow"
    else:
        pace_status = "neutral"

    # Efficiency status
    efficiency_status = "high" if abs(score_diff) > 8 else "balanced"

    # Whistle status
    total_fouls = payload.away_fouls + payload.home_fouls
    whistle_status = "tight" if total_fouls >= 12 else "normal"

    # Turnover status
    total_turnovers = payload.away_turnovers + payload.home_turnovers
    turnover_status = "sloppy" if total_turnovers >= 10 else "controlled"

    # Volatility Score v2
    volatility_score_v2 = (
        abs(score_diff) * 0.8 +
        total_fouls * 0.6 +
        total_turnovers * 0.7
    )

    # Collapse / Comeback probabilities
    collapse_prob_away_v2 = min(1.0, exp(-score_diff / 10))
    collapse_prob_home_v2 = min(1.0, exp(score_diff / 10))
    comeback_prob_away_v2 = 1 - collapse_prob_away_v2
    comeback_prob_home_v2 = 1 - collapse_prob_home_v2

    # Live edge
    live_edge_v2 = (comeback_prob_away_v2 - collapse_prob_home_v2) * 100

    # Run ceilings
    away_run_ceiling_v2 = max(0, 15 - total_turnovers * 0.5)
    home_run_ceiling_v2 = max(0, 15 - total_fouls * 0.4)

    # Avalanche flag
    avalanche_flag_v2 = (
        abs(score_diff) >= 18 and
        total_turnovers >= 8
    )

    # Momentum & Drive
    momentum_score = max(0, 50 + score_diff * 1.1 - total_turnovers * 0.8)
    drive_score = max(0, 50 - score_diff * 1.1 - total_fouls * 0.7)

    # Chaos / Stability
    chaos_probability = min(1.0, volatility_score_v2 / 100)
    stability_probability = 1 - chaos_probability

    # ---------------------------------------------------------
    # NEW RATINGS (wired into engine output)
    # ---------------------------------------------------------

    first_half_rating = compute_first_half_team_rating(payload)
    second_half_rating = compute_second_half_team_rating(payload)
    foul_rating = compute_foul_rating(payload)
    turnover_rating = compute_turnover_rating(payload)

    # ---------------------------------------------------------
    # RETURN BLOCK
    # ---------------------------------------------------------

    return {
        "game_id": payload.game_id,
        "score_diff": score_diff,
        "pace_status": pace_status,
        "efficiency_status": efficiency_status,
        "whistle_status": whistle_status,
        "turnover_status": turnover_status,
        "volatility_score_v2": volatility_score_v2,
        "collapse_prob_away_v2": collapse_prob_away_v2,
        "collapse_prob_home_v2": collapse_prob_home_v2,
        "comeback_prob_away_v2": comeback_prob_away_v2,
        "comeback_prob_home_v2": comeback_prob_home_v2,
        "live_edge_v2": live_edge_v2,
        "away_run_ceiling_v2": away_run_ceiling_v2,
        "home_run_ceiling_v2": home_run_ceiling_v2,
        "avalanche_flag_v2": avalanche_flag_v2,
        "momentum_score": momentum_score,
        "drive_score": drive_score,
        "chaos_probability": chaos_probability,
        "stability_probability": stability_probability,

        # NEW RATINGS
        "first_half_team_rating": first_half_rating,
        "second_half_team_rating": second_half_rating,
        "foul_rating": foul_rating,
        "turnover_rating": turnover_rating
    }
