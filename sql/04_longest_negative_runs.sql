-- Longest unbroken runs of negative-price hours ("gaps and islands").
-- Assumes one row per hour with no gaps (checked when the data were validated).

WITH numbered AS (
    SELECT
        start_time_utc,
        price_eur_mwh,
        is_negative_price,
        row_number() OVER (ORDER BY start_time_utc)                              AS rn_all,
        row_number() OVER (PARTITION BY is_negative_price ORDER BY start_time_utc) AS rn_same_status
    FROM market_hours
),
runs AS (
    SELECT
        rn_all - rn_same_status          AS run_id,   -- constant within one unbroken run
        count(*)                         AS hours,
        min(start_time_utc)              AS first_hour_utc,
        max(start_time_utc)              AS last_hour_utc,
        round(avg(price_eur_mwh)::numeric, 1) AS avg_price_eur_mwh,
        round(min(price_eur_mwh)::numeric, 1) AS lowest_price_eur_mwh
    FROM numbered
    WHERE is_negative_price
    GROUP BY rn_all - rn_same_status
)
SELECT
    hours,
    first_hour_utc AT TIME ZONE 'Europe/Berlin' AS first_hour_local,
    last_hour_utc  AT TIME ZONE 'Europe/Berlin' AS last_hour_local,
    avg_price_eur_mwh,
    lowest_price_eur_mwh
FROM runs
ORDER BY hours DESC, first_hour_utc
LIMIT 10;