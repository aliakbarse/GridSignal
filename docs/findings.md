# GridSignal — Key Findings

## 1. Research Question

When do negative electricity prices occur in the German day-ahead market in 2024–2025, and what separates negative-price hours from all other hours?

All results are descriptive associations in two years of hourly data. They do not establish causation.

## 2. Finding One: Residual Load Separates Negative-Price Hours Best

Residual load is grid load minus wind and solar generation: the amount other power plants still have to supply. The table groups all 17,544 hours into fixed residual-load bands.

| Residual load | Hours | Negative-price hours | Share negative | Average price (€/MWh) | Median price (€/MWh) |
|---|---:|---:|---:|---:|---:|
| ≤ 0 GW | 261 | 239 | 91.6% | −24.0 | −10.2 |
| 0–5 GW | 621 | 399 | 64.3% | −4.6 | −0.1 |
| 5–10 GW | 812 | 280 | 34.5% | 8.3 | 1.0 |
| 10–15 GW | 1,097 | 98 | 8.9% | 29.8 | 26.4 |
| 15–20 GW | 1,457 | 14 | 1.0% | 51.9 | 55.1 |
| 20–30 GW | 4,050 | 0 | 0.0% | 75.7 | 78.0 |
| > 30 GW | 9,246 | 0 | 0.0% | 114.6 | 106.0 |

The share column answers "in this band, how often is the price negative?" A different question gives a different number: 918 of the 1,030 negative-price hours (89%) fell in the three lowest bands, below 10 GW.

![Share of hours with a negative price, by residual load](negative_price_share_by_residual_load_2024_2025.png)

### Negative-price hours compared with all other hours

| Hours | Count | Average price (€/MWh) | Average grid load (GW) | Average wind and solar (GW) | Average residual load (GW) |
|---|---:|---:|---:|---:|---:|
| Negative price | 1,030 | −11.19 | 49.5 | 45.7 | 3.7 |
| Non-negative price | 16,514 | 89.84 | 53.9 | 22.0 | 31.9 |

Negative-price hours made up 5.87% of all hours. Their residual load was 28.2 GW lower. About 84% of that gap comes from higher wind and solar output (23.8 GW) and about 16% from lower demand (4.4 GW).

### Correlation with price

| Variable | Pearson | Spearman |
|---|---:|---:|
| Grid load | 0.308 | 0.279 |
| Wind and solar | −0.651 | −0.695 |
| Residual load | 0.827 | 0.869 |

Pearson measures how close the relationship is to a straight line, Spearman how consistently the two variables rise and fall together.

**Interpretation:** Negative prices almost never occur once other plants must supply 20 GW or more, and become the norm when wind and solar cover all of demand. The relationship is partly mechanical, because residual load is built from demand and generation, so it is a strong descriptor of market conditions rather than proof of a cause.

**Caveats:** The middle bands are mixed (34.5% negative at 5–10 GW), so other factors matter there. Residual load subtracts only wind and solar, and it is an hourly national average that can hide short or regional surpluses.

**Supporting files:** `price_by_residual_load_band_2024_2025.csv`, `price_correlations_2024_2025.csv`, `negative_price_comparison_2024_2025.csv`

## 3. Finding Two: Solar Alone Is a Weak Explanation

Average solar output is much higher in negative-price hours, but the raw comparison is misleading. Negative prices occur mostly at midday in the sunny months, so the negative-price group contains mainly midday summer hours, while the other group contains every night hour. The comparison below holds time of day and season constant step by step. Solar output is the average per hour, in GW.

| Year | Comparison | Negative-price hours | Other hours | Ratio |
|---|---|---|---|---|
| 2024 | All hours | 457 hours, 25.5 GW | 8,327 hours, 6.2 GW | 4.11× |
| 2024 | Midday (11:00–14:59) | 237 hours, 33.3 GW | 1,227 hours, 19.4 GW | 1.72× |
| 2024 | Midday, April–September | 218 hours, 34.4 GW | 514 hours, 29.5 GW | 1.16× |
| 2024 | …on weekdays | 87 hours, 34.9 GW | 437 hours, 29.5 GW | 1.19× |
| 2024 | …on weekends | 131 hours, 34.0 GW | 77 hours, 29.8 GW | 1.14× |
| 2025 | All hours | 573 hours, 31.3 GW | 8,187 hours, 6.9 GW | 4.55× |
| 2025 | Midday (11:00–14:59) | 342 hours, 36.4 GW | 1,118 hours, 21.8 GW | 1.67× |
| 2025 | Midday, April–September | 302 hours, 37.8 GW | 430 hours, 32.1 GW | 1.18× |
| 2025 | …on weekdays | 152 hours, 39.6 GW | 372 hours, 32.3 GW | 1.23× |
| 2025 | …on weekends | 150 hours, 35.9 GW | 58 hours, 30.8 GW | 1.17× |

**Interpretation:** Most of the raw gap reflects when negative prices happen, not solar output alone. Within midday hours of April–September, negative-price hours still have about 16–18% more solar output, so a small association remains. Weekends do not explain it: the weekday and weekend ratios are similar, although the weekend samples are small.

**Caveats:** Demand, wind, power-plant flexibility and cross-border flows are not controlled.

**Supporting file:** `solar_comparison_controls_2024_2025.csv`

## 4. Finding Three: Negative Prices Cluster Around Midday

84% of negative-price hours (863 of 1,030) fell between 10:00 and 17:00 German local time.

| Year | Peak hour (local time) | Negative-price hours | Observed hours | Negative-price rate |
|---|---:|---:|---:|---:|
| 2024 | 14:00 | 75 | 366 | 20.49% |
| 2025 | 13:00 | 99 | 365 | 27.12% |

The peak rate was about 6.63 percentage points higher in 2025. Overnight rates stayed in the low single digits in 2024 and below 2% in 2025.

Comparing hours at the same time of day removes the daily solar cycle. At 11:00 in 2025, average solar output was about 35.2 GW in negative-price hours and 22.9 GW in other hours, a difference of about 12.3 GW (53%). Seasons are not controlled in this comparison. Averages for hours with fewer than 30 negative-price observations, mostly overnight and at the edges of the day, are flagged on the chart and should be read cautiously.

![Hour-of-day pattern of negative prices and solar output](hour_of_day_analysis_2024_2025.png)

**Supporting files:** `hourly_negative_price_frequency_2024_2025.csv`, `hourly_solar_by_price_category_2024_2025.csv`

## 5. Finding Four: Negative Prices Became More Frequent in 2025, Mostly in Spring

Negative-price hours rose from 457 in 2024 to 573 in 2025 (+116, or +25.4%).

| Month | 2024 hours | 2024 frequency | 2025 hours | 2025 frequency |
|---|---:|---:|---:|---:|
| January | 16 | 2.15% | 14 | 1.88% |
| February | 4 | 0.57% | 0 | 0.00% |
| March | 12 | 1.62% | 30 | 4.04% |
| April | 50 | 6.94% | 75 | 10.42% |
| May | 78 | 10.48% | 129 | 17.34% |
| June | 64 | 8.89% | 141 | 19.58% |
| July | 81 | 10.89% | 12 | 1.61% |
| August | 68 | 9.14% | 64 | 8.60% |
| September | 40 | 5.56% | 60 | 8.33% |
| October | 25 | 3.36% | 48 | 6.44% |
| November | 11 | 1.53% | 0 | 0.00% |
| December | 8 | 1.08% | 0 | 0.00% |

April to June added 153 hours (192 in 2024, 345 in 2025). July 2025 fell by 69 hours compared with July 2024, which offsets part of that gain; the other months net to +32. June 2025 had the highest monthly frequency in the dataset (19.58%). The July drop is examined in the next section.

![Monthly frequency of negative prices](negative_price_frequency_2024_2025.png)

## 6. Finding Four, Follow-Up: The July 2025 Drop Is Only Partly Explained

Residual load was the best separator of negative-price hours (Finding One), so the first question is whether July 2025 simply had fewer low-residual hours. It did, but that is a small part of the story. The table below keeps only hours with residual load below 10 GW, April–October, and compares them with the average day-ahead price of the neighbouring zones in the same hours. "Spread" is the neighbours' median price minus Germany's median price.

| Month | Year | Low-residual hours | Negative hours | Share negative | Germany median (€/MWh) | Neighbours median (€/MWh) | Spread (€/MWh) |
|---|---:|---:|---:|---:|---:|---:|---:|
| April | 2024 | 79 | 42 | 53.2% | −0.1 | 7.0 | 11.1 |
| April | 2025 | 93 | 74 | 79.6% | −3.0 | 1.0 | 7.3 |
| May | 2024 | 82 | 63 | 76.8% | −1.6 | 3.0 | 8.4 |
| May | 2025 | 163 | 119 | 73.0% | −1.1 | 8.9 | 13.5 |
| June | 2024 | 68 | 52 | 76.5% | −3.6 | 0.6 | 7.9 |
| June | 2025 | 185 | 131 | 70.8% | −1.0 | 4.9 | 8.5 |
| July | 2024 | 82 | 64 | 78.0% | −3.1 | −0.1 | 5.3 |
| July | 2025 | 61 | 12 | 19.7% | 2.4 | 17.0 | 8.0 |
| August | 2024 | 76 | 59 | 77.6% | −4.2 | 3.3 | 6.9 |
| August | 2025 | 132 | 59 | 44.7% | 0.0 | 7.8 | 6.9 |
| September | 2024 | 59 | 31 | 52.5% | −0.0 | 5.0 | 3.7 |
| September | 2025 | 113 | 60 | 53.1% | −0.0 | 22.7 | 18.4 |
| October | 2024 | 19 | 18 | 94.7% | −0.4 | 0.5 | 5.2 |
| October | 2025 | 142 | 48 | 33.8% | 1.6 | 29.9 | 22.5 |

**What the data show:**

- In July 2024, 64 of 82 low-residual hours (78.0%) had a negative price. In July 2025 it was 12 of 61 (19.7%).
- Of the 69-hour fall in July negative-price hours (81 to 12), 52 hours came from low-residual hours (64 to 12) and 17 from other hours (17 to 0). Low-residual hours were also fewer (82 to 61).
- In July 2025 the neighbouring zones' median price in those hours was 17.0 €/MWh, against −0.1 in July 2024. Germany's own median rose from −3.1 to +2.4.
- The gap between Germany and its neighbours did not widen much in July (5.3 to 8.0 €/MWh). This does not support the idea that German surplus was being absorbed by exports.

**Interpretation:** When German residual load was low in July 2025, the surrounding markets did not have a matching surplus, and German prices stayed positive with them. A plausible reading is that negative prices need a surplus across the coupled market, not only in Germany.

**Caveats:**

- The pattern is not consistent. In September 2025 the neighbours' median was far higher than in 2024 (22.7 against 5.0) but the negative share was unchanged (53.1% against 52.5%), and May and June 2025 do not fit either. This is a hint, not an explanation.
- The data contain prices of neighbouring zones but no cross-border flows, outages or fuel prices, so the reason for the higher prices is not tested.
- October 2025 is affected by the switch to 15-minute products, and October 2024 has only 19 low-residual hours.
- Residual load below 10 GW is an hourly national average; negative means strictly below €0/MWh.

**Supporting file:** `low_residual_hours_by_month_2024_2025.csv`

## 7. Finding Five: Solar Earned About Half the Average Price in 2025

The capture rate is the average price solar output earned, weighted by hourly solar output, divided by the simple average price of all hours. A value below 1 means solar produces when prices are lower than average.

| Year | Average price (€/MWh) | Solar-weighted price (€/MWh) | Capture rate | Solar output in negative-price hours | Value of that output (million €) |
|---|---:|---:|---:|---:|---:|
| 2024 | 78.5 | 46.2 | 0.589 | 18.4% | −178.0 |
| 2025 | 89.3 | 46.1 | 0.516 | 24.1% | −244.0 |

Monthly capture rates for the main solar months:

| Month | Capture rate 2024 | Capture rate 2025 | Solar-weighted price 2025 (€/MWh) | Average price 2025 (€/MWh) | Solar output in negative-price hours 2025 |
|---|---:|---:|---:|---:|---:|
| March | 0.765 | 0.537 | 50.8 | 94.7 | 13.4% |
| April | 0.621 | 0.402 | 31.3 | 77.9 | 32.6% |
| May | 0.488 | 0.322 | 21.7 | 67.3 | 43.7% |
| June | 0.610 | 0.313 | 20.1 | 64.0 | 46.9% |
| July | 0.529 | 0.681 | 59.8 | 87.8 | 5.2% |
| August | 0.526 | 0.507 | 39.1 | 77.0 | 22.2% |
| September | 0.577 | 0.530 | 44.3 | 83.5 | 24.5% |
| October | 0.783 | 0.850 | 71.7 | 84.4 | 8.7% |

**What the data show:**

- Solar's own weighted price was almost unchanged (46.2 and 46.1 €/MWh). The capture rate fell because the average price of all hours rose, partly through high winter prices (January 2025 114.1 and February 128.5 €/MWh) when solar produces little.
- April to June 2025 had the lowest capture rates (0.31–0.40, against 0.49–0.62 in 2024). These three months account for −212.5 of the −244.0 million € value at negative prices (about 87%), against about 63% in 2024.
- July 2025 is the one summer month where the capture rate improved (0.68 against 0.53), the same month in which negative prices dropped (Finding Four, follow-up).
- Between November and February the capture rate is 0.86–1.03, so most of the loss of value is a spring and summer effect.

**Caveats:** The euro values are the market value of all solar output at day-ahead prices. They are not actual plant revenue, because feed-in tariffs, direct-marketing contracts and curtailment rules are not modelled. Solar output is the SMARD actual generation figure. Month-level figures rest on 24 months of data.

**Supporting files:** `solar_capture_rate_2024_2025.csv`, `solar_capture_rate_by_month_2024_2025.csv`

## 8. Finding Six: Most Negative Prices Are Mild

| Negative-price range | 2024 hours | 2024 share | 2025 hours | 2025 share |
|---|---:|---:|---:|---:|
| Below −100 €/MWh | 5 | 1.1% | 13 | 2.3% |
| −100 to −50 €/MWh | 22 | 4.8% | 17 | 3.0% |
| −50 to −20 €/MWh | 61 | 13.3% | 54 | 9.4% |
| −20 to −10 €/MWh | 49 | 10.7% | 51 | 8.9% |
| −10 to 0 €/MWh | 320 | 70.0% | 438 | 76.4% |
| **Total** | **457** | **100.0%** | **573** | **100.0%** |

Percentages describe negative-price hours only, not all hours. Mild prices between −10 and 0 €/MWh made up 70.0% of negative-price hours in 2024 and 76.4% in 2025. Hours below −100 €/MWh rose from 5 to 13, but the counts are small. The lowest price was −250.32 €/MWh in 2025 (−135.45 in 2024), yet that single extreme does not mean prices were generally more severe: the mean negative price was −11.50 €/MWh in 2024 and −10.95 €/MWh in 2025, and the median was about −2.0 €/MWh in both years.

![Severity of negative prices](negative_price_severity_2024_2025.png)

## 9. Finding Seven: Negative Prices Are About Three Times as Common on Weekends

These results come from SQL queries on the PostgreSQL layer (`sql/05_weekend_effect.sql` and `sql/04_longest_negative_runs.sql`). Weekend means Saturday or Sunday in German local time. Public holidays are not in the data and are not analysed.

| Hours compared | Day type | Hours | Share of hours | Negative hours | Negative rate |
|---|---|---:|---:|---:|---:|
| All hours | Weekend | 4,992 | 28.5% | 604 | 12.1% |
| All hours | Weekday | 12,552 | 71.5% | 426 | 3.4% |
| Midday (11:00–14:59), April–September | Weekend | 416 | 28.4% | 281 | 67.5% |
| Midday (11:00–14:59), April–September | Weekday | 1,048 | 71.6% | 239 | 22.8% |

The midday April–September counts (281 and 239 negative hours) match the weekend and weekday counts in Finding Two, which is a check on the SQL. Finding Two asks a different question, whether solar output differs within negative-price hours, and found no weekend effect there. Finding Seven asks how often negative prices occur, and the answer is much more often on weekends.

### Longest unbroken runs of negative prices

| Hours | Start (local) | End (local) | Average price (€/MWh) | Lowest price (€/MWh) |
|---:|---|---|---:|---:|
| 20 | 2025-10-04 21:00 | 2025-10-05 16:00 | −2.3 | −5.0 |
| 18 | 2024-07-07 00:00 | 2024-07-07 17:00 | −5.9 | −22.4 |
| 17 | 2025-10-04 01:00 | 2025-10-04 17:00 | −0.7 | −2.6 |
| 16 | 2024-08-25 01:00 | 2024-08-25 16:00 | −5.7 | −20.0 |
| 16 | 2024-10-13 01:00 | 2024-10-13 16:00 | −3.1 | −15.7 |
| 14 | 2025-01-01 03:00 | 2025-01-01 16:00 | −0.1 | −1.0 |
| 10 | 2024-04-28 08:00 | 2024-04-28 17:00 | −31.6 | −65.1 |
| 10 | 2024-06-09 08:00 | 2024-06-09 17:00 | −15.5 | −37.1 |
| 10 | 2024-06-15 09:00 | 2024-06-15 18:00 | −32.0 | −80.0 |
| 10 | 2024-06-16 08:00 | 2024-06-16 17:00 | −15.2 | −35.7 |

All ten runs started on a Saturday, a Sunday or New Year's Day. The longest runs are mild and the deepest are short. Several long runs start at 01:00, so they are not only a solar effect.

**Interpretation:** Weekends hold 28.5% of hours but 58.6% of negative-price hours, and the difference remains when time of day and season are held constant. Lower weekend demand is a plausible explanation, but demand is not tested in these queries.

**Caveats:** A run ends at any hour with a price of zero or above, so zero-price hours split runs. The 4–5 October 2025 run falls after the switch to 15-minute products, so its hourly values are averages. The top ten runs are a small set of examples.

**Supporting files:** `sql/04_longest_negative_runs.sql`, `sql/05_weekend_effect.sql`

## 10. What This Means for a Solar Plant Owner

Written for an owner who sells at market prices; owners on fixed feed-in tariffs are affected differently. These are conclusions from descriptive data, not forecasts.

| # | Recommendation | Evidence |
|---|---|---|
| 1 | Forecast revenue month by month, not with a yearly average. | Capture rate 0.31–0.40 in April–June 2025, against 0.52 for the year. |
| 2 | Use residual load as a warning signal for negative prices. | Below 5 GW, 638 of 882 hours (72%) were negative; above 20 GW, none were. |
| 3 | Treat negative-price hours as a contract and curtailment question. | 24.1% of 2025 solar output (46.9% in June) was produced in negative-price hours, valued at −244 million €. |
| 4 | Do not plan on July 2025 repeating. | Capture rate was 0.68, the only summer improvement, and its cause is only partly explained. |
| 5 | Plan weekends separately. | In April–September middays, 67.5% of weekend hours had a negative price against 22.8% of weekday hours. |

**Not yet analysed:** whether storage could capture the midday-to-evening price gap. This needs a separate analysis of price spreads within the day.

## 11. Data Coverage and Limitations

- The combined dataset has 17,544 matched hourly records: 8,784 in 2024 (a leap year) and 8,760 in 2025.
- Prices, generation and consumption are matched on UTC timestamps. The UTC timeline has no duplicates and no gaps. Calendar analysis uses `Europe/Berlin` local time.
- At the spring daylight-saving change the local 02:00 hour is absent; in autumn the local 02:00 label repeats. The raw source timestamps do not distinguish the two repeated hours. The inspected raw consumption records matched the merged records in source order and in value, but this does not independently verify every source row.
- Negative means strictly below €0/MWh. Counting zero-price hours as well would give 519 hours in 2024 and 655 in 2025.
- From 1 October 2025 the day-ahead market uses 15-minute products, and hourly values after that date average four quarter-hours.
- Residual load subtracts only wind and solar. Hydro, biomass, imports and exports are not included, and the generation measures are not total supply.
- The controlled solar comparisons hold time of day and season constant. They do not control for demand, wind, conventional generation, storage, cross-border flows or subsidy rules.
- The July 2025 analysis uses the SMARD average price of neighbouring zones. It has no flow, outage or fuel-price data, so it cannot show why neighbouring prices differed.
- The capture rate and euro values apply day-ahead prices to all solar output. They are not plant revenue, because feed-in tariffs, direct-marketing contracts, curtailment and intraday trading are not modelled.
- The weekend comparison covers Saturdays and Sundays only. Public holidays are not analysed, and the reason for the weekend effect (demand, wind or both) is not tested.
- Some groups are small, such as the weekend comparisons (58 and 77 other hours), overnight hours with few negative prices and October 2024 (19 low-residual hours).
- February, November and December 2025 had no negative-price hours, so no negative-versus-other comparison exists for those months.
- Before commercial use, check the original SMARD field definitions and units.
- Two years of data should not be assumed to represent future market conditions.

## 12. Conclusion

Negative prices in 2024–2025 occurred almost entirely when wind and solar covered most of demand: 89% of negative-price hours had a residual load below 10 GW, and none occurred above 20 GW. Solar output alone explains much less than the raw comparison suggests, because most of its apparent effect comes from timing at midday in spring and summer. Negative prices cluster between 10:00 and 17:00, rose in spring 2025 and remained mostly mild.

The sharp drop in July 2025 is only partly explained: at the same low residual load, far fewer hours had negative prices, and neighbouring zones' prices in those hours were much higher. That is consistent with negative prices needing a market-wide surplus, but September 2025 and the spring months do not follow the same pattern, and no flow data were available to test it.

For a solar plant owner selling at market prices, the cost is concentrated in spring: the capture rate fell from 0.59 to 0.52 over the year and to 0.31–0.40 in April–June 2025, and 24% of 2025 solar output was produced in negative-price hours.

Negative prices are also about three times as common on weekends (12.1% of hours against 3.4%), and all ten of the longest unbroken runs started on a weekend or public holiday.

These findings describe associations in two years of hourly data. Next steps are to examine public holidays and night-time wind, and to analyse the midday-to-evening price gap for storage.
