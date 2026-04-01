WITH source_1t AS (
    SELECT * FROM {{ source('raw', 'raw_vendas_1t') }}
),
source_2t AS (
    SELECT * FROM {{ source('raw', 'raw_vendas_2t') }}
),
unioned AS (
    SELECT * FROM source_1t
    UNION ALL
    SELECT * FROM source_2t
)
SELECT
    IdStore AS id_store,
    CAST(Date AS DATE) AS date,
    EXTRACT(year FROM CAST(Date AS DATE))::INT AS year,
    EXTRACT(quarter FROM CAST(Date AS DATE))::INT AS quarter,
    EXTRACT(month FROM CAST(Date AS DATE))::INT AS month,
    EXTRACT(week FROM CAST(Date AS DATE))::INT AS week,
    IdPurchase AS id_purchase,
    IdSeller AS id_seller,
    CAST(Quantity AS INTEGER) AS quantity,
    CAST(Price AS DOUBLE) AS price
FROM unioned
