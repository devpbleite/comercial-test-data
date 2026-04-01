{{ config(materialized='external', location='../output/parquet/mart_calendario.parquet') }}

WITH dates AS (
    SELECT UNNEST(
        generate_series(
            DATE '2024-01-01',
            DATE '2024-06-30',
            INTERVAL '1 day'
        )
    )::DATE AS date
)
SELECT
    date,
    EXTRACT(year    FROM date)::INT  AS year,
    EXTRACT(quarter FROM date)::INT  AS quarter,
    EXTRACT(month   FROM date)::INT  AS month,
    EXTRACT(week    FROM date)::INT  AS week,
    EXTRACT(dow     FROM date)::INT  AS day_of_week,
    EXTRACT(day     FROM date)::INT  AS day,
    CASE EXTRACT(quarter FROM date)
        WHEN 1 THEN '1T-2024'
        WHEN 2 THEN '2T-2024'
    END                              AS quarter_label,
    STRFTIME(date, '%b/%Y')          AS month_label
FROM dates
