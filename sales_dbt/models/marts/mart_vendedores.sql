{{ config(materialized='external', location='../output/parquet/mart_vendedores.parquet') }}

SELECT
    v.year,
    v.quarter,
    v.month,
    v.week,
    v.date,
    v.id_seller,
    c.seller_name,
    c.role,
    c.wage,
    v.id_store,
    l.store_name,
    l.state,
    l.size                                          AS store_size,
    COUNT(DISTINCT v.id_purchase)                  AS total_purchases,
    SUM(v.quantity)                                AS total_units,
    SUM(v.price)                                   AS total_revenue,
    ROUND(SUM(v.price) / NULLIF(COUNT(DISTINCT v.id_purchase), 0), 2)
                                                   AS ticket_medio
FROM {{ ref('stg_vendas') }} v
LEFT JOIN {{ ref('stg_consultores') }} c ON v.id_seller = c.id_seller
LEFT JOIN {{ ref('stg_lojas') }}       l ON v.id_store  = l.id_store
GROUP BY
    v.year, v.quarter, v.month, v.week, v.date,
    v.id_seller, c.seller_name, c.role, c.wage,
    v.id_store, l.store_name, l.state, l.size
