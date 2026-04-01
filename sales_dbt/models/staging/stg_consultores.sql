WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_consultores') }}
),
renamed AS (
    SELECT
        IdSeller AS id_seller,
        Seller AS seller_name,
        IdStore AS id_store,
        TRIM(Role) AS role,
        CAST(Wage AS BIGINT) AS wage
    FROM source
),
prioritized AS (
    SELECT
        *,
        CASE
            WHEN role = 'Sales Manager' THEN 1
            WHEN role = 'Sales consultant' THEN 2
            ELSE 3
        END AS _priority
    FROM renamed
),
deduplicated AS (
    SELECT
        id_seller,
        seller_name,
        id_store,
        role,
        wage
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER(PARTITION BY id_seller ORDER BY _priority ASC) as rn
        FROM prioritized
    )
    WHERE rn = 1
)
SELECT * FROM deduplicated
