WITH staging AS (
    SELECT * FROM {{ ref('stg_players') }}
)

SELECT
    nationality,
    position,
    COUNT(player_id) AS total_players,
    AVG(age) AS average_age,
    AVG(height_cm) AS average_height,
    SUM(goals) AS total_goals,
    SUM(shots_on_target) AS total_shots_on_target,
    SUM(expected_goals_xg) AS total_expected_goals_xg,
    SUM(yellow_cards) AS total_yellow_cards
FROM staging
GROUP BY nationality, position
