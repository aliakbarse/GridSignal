-- Schema for the GridSignal database.
-- Raw hourly measurements are stored once; calendar fields are derived in a view.

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

-- Local German time and calendar fields, derived from the UTC timestamp.
CREATE VIEW market_hours_local AS
SELECT
    m.*,
    m.start_time_utc AT TIME ZONE 'Europe/Berlin'                     AS start_time_local,
    EXTRACT(YEAR  FROM m.start_time_utc AT TIME ZONE 'Europe/Berlin')::int AS year,
    EXTRACT(MONTH FROM m.start_time_utc AT TIME ZONE 'Europe/Berlin')::int AS month,
    EXTRACT(HOUR  FROM m.start_time_utc AT TIME ZONE 'Europe/Berlin')::int AS hour
FROM market_hours AS m;