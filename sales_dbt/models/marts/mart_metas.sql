{{ config(materialized='external', location='../output/parquet/mart_metas.parquet') }}

WITH receita_semanal AS (
    SELECT
        id_store,
        year,
        week,
        SUM(price) AS revenue_actual
    FROM {{ ref('stg_vendas') }}
    GROUP BY id_store, year, week
)
SELECT
    m.date,
    m.year,
    m.quarter,
    m.month,
    m.week,
    m.id_store,
    l.store_name,
    l.state,
    l.size                                              AS store_size,
    m.revenue_target,
    COALESCE(r.revenue_actual, 0)                       AS revenue_actual,
    COALESCE(r.revenue_actual, 0) - m.revenue_target   AS revenue_gap,
    ROUND(
        COALESCE(r.revenue_actual, 0) / NULLIF(m.revenue_target, 0) * 100,
        2
    )                                                   AS pct_achievement
FROM {{ ref('stg_metas') }} m
LEFT JOIN {{ ref('stg_lojas') }}         l ON m.id_store = l.id_store
LEFT JOIN receita_semanal   r ON m.id_store = r.id_store
                             AND m.year     = r.year
                             AND m.week     = r.week
