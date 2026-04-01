{{ config(materialized='external', location='../output/parquet/mart_faturamento.parquet') }}

SELECT
    v.date,
    v.year,
    v.quarter,
    v.month,
    v.week,
    v.id_store,
    l.store_name,
    l.state,
    l.size                                  AS store_size,
    v.id_seller,
    c.seller_name,
    c.role,
    v.id_purchase,
    v.quantity,
    v.price                                 AS revenue,
    v.price / NULLIF(v.quantity, 0)         AS avg_price_per_unit
FROM {{ ref('stg_vendas') }} v
LEFT JOIN {{ ref('stg_lojas') }}       l ON v.id_store  = l.id_store
LEFT JOIN {{ ref('stg_consultores') }} c ON v.id_seller = c.id_seller
