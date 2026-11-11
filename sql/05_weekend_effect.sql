-- Do weekends have more negative-price hours than weekdays?
-- Query 1 uses all hours; query 2 holds time of day and season constant
-- (midday 11:00-14:59, April-September), the same control as in Finding Two.
-- Weekends only: public holidays are not in the data and are not covered.

-- Query 1: all hours
SELECT
    CASE WHEN EXTRACT(ISODOW FROM start_time_local) IN (6, 7)
         THEN 'weekend' ELSE 'weekday' END                    AS day_type,
    count(*)                                                   AS hours,
    round(100.0 * count(*) / sum(count(*)) OVER (), 1)         AS share_of_hours_pct,
    count(*) FILTER (WHERE is_negative_price)                  AS negative_hours,
    round(100.0 * count(*) FILTER (WHERE is_negative_price) / count(*), 1)
                                                               AS negative_rate_pct
FROM market_hours_local
GROUP BY 1
ORDER BY 1 DESC;

-- Query 2: midday hours, April-September
SELECT
    CASE WHEN EXTRACT(ISODOW FROM start_time_local) IN (6, 7)
         THEN 'weekend' ELSE 'weekday' END                    AS day_type,
    count(*)                                                   AS hours,
    round(100.0 * count(*) / sum(count(*)) OVER (), 1)         AS share_of_hours_pct,
    count(*) FILTER (WHERE is_negative_price)                  AS negative_hours,
    round(100.0 * count(*) FILTER (WHERE is_negative_price) / count(*), 1)
                                                               AS negative_rate_pct
FROM market_hours_local
WHERE hour BETWEEN 11 AND 14
  AND month BETWEEN 4 AND 9
GROUP BY 1
ORDER BY 1 DESC;