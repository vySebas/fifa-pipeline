SELECT DISTINCT
    nationality
FROM {{ ref('stg_players') }}
WHERE nationality IS NOT NULL
