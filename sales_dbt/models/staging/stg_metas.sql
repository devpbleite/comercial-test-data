WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_metas') }}
)
SELECT
    IdStore AS id_store,
    CAST(Date AS DATE) AS date,
    EXTRACT(year FROM CAST(Date AS DATE))::INT AS year,
    EXTRACT(quarter FROM CAST(Date AS DATE))::INT AS quarter,
    EXTRACT(month FROM CAST(Date AS DATE))::INT AS month,
    CAST(Week AS INTEGER) AS week,
    CAST(RevenueTarget AS DOUBLE) AS revenue_target
FROM source
