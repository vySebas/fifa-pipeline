SELECT DISTINCT
    player_id,
    player_name,
    age,
    height_cm
FROM {{ ref('stg_players') }}
