WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_lojas') }}
)
SELECT
    IdStore AS id_store,
    Store AS store_name,
    CASE TRIM(Size)
        WHEN 'LRGE' THEN 'LARGE'
        WHEN 'MID' THEN 'MEDIUM'
        WHEN 'MEDIUN' THEN 'MEDIUM'
        WHEN 'SMAL' THEN 'SMALL'
        ELSE TRIM(Size)
    END AS size,
    State AS state
FROM source
