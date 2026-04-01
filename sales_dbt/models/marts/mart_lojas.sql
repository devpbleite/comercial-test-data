{{ config(materialized='external', location='../output/parquet/mart_lojas.parquet') }}

WITH vendas_loja AS (
    SELECT
        id_store,
        year,
        quarter,
        month,
        COUNT(DISTINCT id_purchase)                             AS total_purchases,
        SUM(quantity)                                           AS total_units,
        SUM(price)                                              AS total_revenue,
        ROUND(SUM(price) / NULLIF(COUNT(DISTINCT id_purchase), 0), 2)
                                                                AS ticket_medio
    FROM {{ ref('stg_vendas') }}
    GROUP BY id_store, year, quarter, month
),
folha_loja AS (
    SELECT
        id_store,
        COUNT(*)        AS total_sellers,
        SUM(wage)       AS total_wage_bill,
        AVG(wage)       AS avg_wage
    FROM {{ ref('stg_consultores') }}
    GROUP BY id_store
)
SELECT
    vl.id_store,
    l.store_name,
    l.state,
    l.size                  AS store_size,
    vl.year,
    vl.quarter,
    vl.month,
    vl.total_purchases,
    vl.total_units,
    vl.total_revenue,
    vl.ticket_medio,
    fl.total_sellers,
    fl.total_wage_bill,
    ROUND(fl.avg_wage, 2)   AS avg_wage,
    ROUND(
        vl.total_revenue / NULLIF(fl.total_wage_bill, 0), 2
    )                       AS revenue_per_wage_ratio
FROM vendas_loja vl
LEFT JOIN {{ ref('stg_lojas') }}   l  ON vl.id_store = l.id_store
LEFT JOIN folha_loja               fl ON vl.id_store = fl.id_store
