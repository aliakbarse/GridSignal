-- Solar capture rate by year (compare with solar_capture_rate_2024_2025.csv).
-- Simple average price: every hour counts the same.
-- Solar-weighted price: each hour counts in proportion to how much solar produced.
-- Capture rate = solar-weighted price / simple average price.

SELECT
    year,
    round(avg(price_eur_mwh)::numeric, 3)                          AS average_price_eur_mwh,
    round((sum(price_eur_mwh * solar_mwh) / sum(solar_mwh))::numeric, 3)
                                                                   AS solar_weighted_price_eur_mwh,
    round((sum(price_eur_mwh * solar_mwh) / sum(solar_mwh) / avg(price_eur_mwh))::numeric, 3)
                                                                   AS capture_rate,
    round((100 * sum(solar_mwh) FILTER (WHERE is_negative_price) / sum(solar_mwh))::numeric, 3)
                                                                   AS solar_share_at_negative_prices_pct,
    round((sum(price_eur_mwh * solar_mwh) FILTER (WHERE is_negative_price) / 1e6)::numeric, 3)
                                                                   AS value_at_negative_prices_eur_million
FROM market_hours_local
GROUP BY year
ORDER BY year;