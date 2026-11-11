-- Share of negative-price hours by residual-load band (compare with Finding One).
-- Execution order: FROM -> GROUP BY (bands) -> aggregates -> ORDER BY.

SELECT
    CASE
        WHEN residual_load_mwh <= 0     THEN '1: <= 0 GW'
        WHEN residual_load_mwh <= 5000  THEN '2: 0-5 GW'
        WHEN residual_load_mwh <= 10000 THEN '3: 5-10 GW'
        WHEN residual_load_mwh <= 15000 THEN '4: 10-15 GW'
        WHEN residual_load_mwh <= 20000 THEN '5: 15-20 GW'
        WHEN residual_load_mwh <= 30000 THEN '6: 20-30 GW'
        ELSE                                 '7: > 30 GW'
    END AS residual_load_band,
    count(*)                                              AS hours,
    count(*) FILTER (WHERE is_negative_price)             AS negative_hours,
    round(100.0 * count(*) FILTER (WHERE is_negative_price) / count(*), 1)
                                                          AS share_negative_pct,
    round(avg(price_eur_mwh)::numeric, 1)                 AS avg_price_eur_mwh,
    round((percentile_cont(0.5) WITHIN GROUP (ORDER BY price_eur_mwh))::numeric, 1)
                                                          AS median_price_eur_mwh
FROM market_hours
GROUP BY 1
ORDER BY 1;