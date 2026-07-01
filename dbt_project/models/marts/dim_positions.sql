SELECT DISTINCT
    position
FROM {{ ref('stg_players') }}
WHERE position IS NOT NULL
