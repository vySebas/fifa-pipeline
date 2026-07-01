SELECT
    player_id,
    nationality,
    position,
    goals,
    shots_on_target,
    expected_goals_xg,
    yellow_cards
FROM {{ ref('stg_players') }}
