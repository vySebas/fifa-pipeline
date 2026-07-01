SELECT
    player_id,
    player_name,
    nationality,
    position,
    CAST(age AS INTEGER) AS age,
    CAST(height_cm AS INTEGER) AS height_cm,
    CAST(goals AS INTEGER) AS goals,
    CAST(shots_on_target AS INTEGER) AS shots_on_target,
    CAST(expected_goals_xg AS DOUBLE) AS expected_goals_xg,
    CAST(yellow_cards AS INTEGER) AS yellow_cards
FROM {{ source('raw', 'raw_player_performance') }}
