-- Schema for the GridSignal database.
-- Raw hourly measurements are stored once; calendar fields and groupings
-- are derived in a view, so every tool uses the same definitions.

DROP VIEW IF EXISTS market_hours_local;
DROP TABLE IF EXISTS market_hours;

CREATE TABLE market_hours (
    start_time_utc    timestamptz      PRIMARY KEY,  -- one row per hour, unambiguous
    price_eur_mwh     double precision NOT NULL,     -- day-ahead price
    wind_offshore_mwh double precision NOT NULL,
    wind_onshore_mwh  double precision NOT NULL,
    solar_mwh         double precision NOT NULL,
    grid_load_mwh     double precision NOT NULL,
    residual_load_mwh double precision NOT NULL,     -- grid load - wind - solar
    -- Negative means strictly below zero, computed by the database itself.
    is_negative_price boolean GENERATED ALWAYS AS (price_eur_mwh < 0) STORED
);

-- Local German time, calendar fields, weekday/weekend and residual-load bands.
CREATE VIEW market_hours_local AS
WITH base AS (
    SELECT
        m.*,
        m.start_time_utc AT TIME ZONE 'Europe/Berlin' AS start_time_local
    FROM market_hours AS m
)
SELECT
    b.*,
    EXTRACT(YEAR  FROM b.start_time_local)::int AS year,
    EXTRACT(MONTH FROM b.start_time_local)::int AS month,
    EXTRACT(HOUR  FROM b.start_time_local)::int AS hour,
    to_char(b.start_time_local, 'Mon')          AS month_name,
    CASE WHEN EXTRACT(ISODOW FROM b.start_time_local) IN (6, 7)
         THEN 'Weekend' ELSE 'Weekday' END      AS day_type,
    CASE
        WHEN b.residual_load_mwh <= 0     THEN '<= 0 GW'
        WHEN b.residual_load_mwh <= 5000  THEN '0-5 GW'
        WHEN b.residual_load_mwh <= 10000 THEN '5-10 GW'
        WHEN b.residual_load_mwh <= 15000 THEN '10-15 GW'
        WHEN b.residual_load_mwh <= 20000 THEN '15-20 GW'
        WHEN b.residual_load_mwh <= 30000 THEN '20-30 GW'
        ELSE '> 30 GW'
    END                                         AS residual_load_band,
    CASE
        WHEN b.residual_load_mwh <= 0     THEN 1
        WHEN b.residual_load_mwh <= 5000  THEN 2
        WHEN b.residual_load_mwh <= 10000 THEN 3
        WHEN b.residual_load_mwh <= 15000 THEN 4
        WHEN b.residual_load_mwh <= 20000 THEN 5
        WHEN b.residual_load_mwh <= 30000 THEN 6
        ELSE 7
    END                                         AS residual_load_band_order
FROM base AS b;