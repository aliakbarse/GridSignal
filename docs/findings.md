# GridSignal AI — Key Findings

## 1. Research Question

How did negative electricity prices in the German day-ahead market vary between 2024 and 2025, and how did renewable generation differ between negative-price and non-negative-price hours?

## 2. Finding One: Negative Prices Increased in May and June 2025

Negative-price hours became substantially more frequent in May and June 2025 compared with the same months in 2024.

| Month | 2024 negative-price hours | 2024 frequency | 2025 negative-price hours | 2025 frequency |
|---|---:|---:|---:|---:|
| May | 78 | 10.48% | 129 | 17.34% |
| June | 64 | 8.89% | 141 | 19.58% |

The frequency increased by 6.86 percentage points in May and 10.69 percentage points in June.

**Interpretation:** These results identify late spring and early summer 2025 as periods worth investigating further. They do not establish the underlying causes of the increase.

**Visualization:** `negative_price_frequency_2024_2025.png`

## 3. Finding Two: Negative-Price Frequency and Severity Tell Different Stories

### Negative-price severity

Negative-price hours were grouped into five severity bands and compared as a share of all negative-price hours in each year.

| Negative-price range | 2024 hours | 2024 share | 2025 hours | 2025 share |
|---|---:|---:|---:|---:|
| Below -100 EUR/MWh | 5 | 1.1% | 13 | 2.3% |
| -100 to -50 EUR/MWh | 22 | 4.8% | 17 | 3.0% |
| -50 to -20 EUR/MWh | 61 | 13.3% | 54 | 9.4% |
| -20 to -10 EUR/MWh | 49 | 10.7% | 51 | 8.9% |
| -10 to 0 EUR/MWh | 320 | 70.0% | 438 | 76.4% |
| **Total negative-price hours** | **457** | **100.0%** | **573** | **100.0%** |

Mild negative prices, between -10 and 0 EUR/MWh, represented 70.0% of negative-price hours in 2024 and 76.4% in 2025. This is an increase of 6.4 percentage points.

The number of hours below -100 EUR/MWh increased from 5 in 2024 to 13 in 2025. The observed share of negative-price hours in this band rose from 1.1% to 2.3%, although the counts remain small.

The annual minimum price was also more extreme in 2025 (-250.32 EUR/MWh versus -135.45 EUR/MWh in 2024). However, this single extreme does not mean negative prices were generally more severe. The mean negative price was -11.50 EUR/MWh in 2024 and -10.95 EUR/MWh in 2025, while the median was approximately -2.01 EUR/MWh and -2.02 EUR/MWh, respectively.

**Interpretation:** Negative prices became more frequent in 2025, and their distribution shifted toward the mildest negative-price band. At the same time, the dataset recorded more hours below -100 EUR/MWh. These patterns show why frequency and severity should be examined separately.

**Visualization:** `negative_price_severity_2024_2025.png`

## 4. Finding Three: Higher Solar Generation Coincided With Negative Prices

### Monthly comparisons

In May 2025, average solar generation was approximately 34,775 MWh during negative-price hours, compared with 9,415 MWh during non-negative-price hours.

In June 2025, the corresponding averages were approximately 35,296 MWh and 9,713 MWh.

These figures represent average generation per observed hourly interval, not monthly generation totals.

**Interpretation:** The observed data show an association between higher solar generation and negative prices in these months. Other factors, including electricity demand, wind generation, conventional power-plant operations, cross-border electricity flows, and broader market conditions, may also contribute. This analysis does not establish causation.

### Monthly consistency

A monthly consistency analysis compared average solar generation during negative-price hours with average solar generation during non-negative-price hours. To reduce reliance on months with very few negative-price observations, the analysis used a screening threshold of at least 30 negative-price hours per month.

Across the 2024–2025 dataset:

- **13 year-month combinations** met the 30-hour threshold.
- In all 13 eligible combinations, average solar generation was higher during negative-price hours.
- The mean monthly difference was 20,334.1 MWh, while the median monthly difference was 19,167.5 MWh.
- The median relative difference was 245.8%.
- The smallest eligible monthly difference was 1,818.9 MWh, and the largest was 29,726.7 MWh.

The mean monthly difference remained positive when any single eligible month was excluded. In this leave-one-month-out sensitivity check, the mean ranged from 19,551.4 to 21,877.0 MWh.

These comparisons use averages across observed hourly intervals within each price category. The differences are not monthly generation totals.

**Interpretation:** The positive association between solar generation and negative prices was consistent across the eligible year-month combinations, and the direction of the average difference did not depend on any single month. This supports treating the relationship as a priority for further investigation.

However, the 30-hour threshold is a practical screening rule, not a formal statistical significance test. The eligible months are not independent experimental observations, and the analysis does not isolate solar generation from other potential influences. In particular, it does not control for time of day, demand, wind generation, conventional generation, or cross-border electricity flows.

**Supporting analysis:** `monthly_solar_consistency_2024_2025.csv`

**Visualization:** `monthly_solar_comparison_2024_2025.png`

### Hourly timing

An hourly analysis examined the proportion of observed intervals with negative prices at each German local hour. The rate was calculated separately for 2024 and 2025 using the observed intervals for each hour as the denominator.

| Year | Hour of peak rate (German local time) | Negative-price hours | Observed hours | Negative-price rate |
|---|---:|---:|---:|---:|
| 2024 | 14:00 | 75 | 366 | 20.49% |
| 2025 | 13:00 | 99 | 365 | 27.12% |

The highest observed hourly rate increased by approximately 6.63 percentage points between these two annual peaks. The peak shifted from 14:00 in 2024 to 13:00 in 2025.

The hourly profiles show that negative prices were substantially more frequent during the middle of the day than overnight, particularly in 2025.

**Interpretation:** Negative-price frequency varied considerably by time of day. The midday concentration is consistent with a potential relationship between periods of high solar generation and negative prices, but the hourly frequency pattern alone cannot establish the mechanism behind it.

**Visualization:** `hour_of_day_analysis_2024_2025.png`

### Solar generation by hour

The hourly solar analysis compared average solar generation during negative-price and non-negative-price intervals at each hour, separately for 2024 and 2025.

The results show that average solar generation was generally higher during negative-price hours through much of the daytime in both years. For example, at 11:00 in 2025:

- Average solar generation during negative-price hours was approximately 35,216 MWh.
- Average solar generation during non-negative-price hours was approximately 22,946 MWh.

The difference was approximately 12,270 MWh per observed hourly interval, or about 53% relative to the non-negative-price average.

The daytime comparison is descriptive. It does not show that high solar generation independently caused negative prices. The observed differences may also reflect other factors associated with the timing of negative-price intervals, including electricity demand, wind generation, conventional generation, and cross-border electricity flows.

Some overnight hour-and-price-category combinations contain very few observations. In particular, the hourly averages based on fewer than 30 negative-price intervals should be treated cautiously. The 30-observation threshold is a practical warning, not a statistical significance test.

**Interpretation:** The hourly analysis adds a time-of-day perspective to the monthly findings. It shows that the association between solar generation and negative prices is particularly visible during daytime hours, while also demonstrating why hourly sample sizes and other market factors matter when interpreting the relationship.

**Supporting analyses:**

- `hourly_negative_price_frequency_2024_2025.csv`
- `hourly_solar_by_price_category_2024_2025.csv`
- `seasonal_price_and_solar_summary_2024_2025.csv`

**Visualization:** `hour_of_day_analysis_2024_2025.png`

## 5. Finding Four: Residual Load Was Strongly Associated With Price

### Negative-price versus non-negative-price hours

A comparison of negative-price and non-negative-price intervals examined electricity prices, grid load, selected renewable generation, and residual load across the combined 2024–2025 dataset.

The analysis contained **17,544 hourly observations**:

| Price category | Observed hours | Average price (EUR/MWh) | Average grid load (MWh) | Average selected renewables (MWh) | Average residual load (MWh) |
|---|---:|---:|---:|---:|---:|
| Negative price | 1,030 | -11.19 | 49,459.16 | 45,724.73 | 3,734.43 |
| Non-negative price | 16,514 | 89.84 | 53,900.70 | 21,962.50 | 31,938.20 |

Negative-price intervals represented **5.87%** of the combined observations, while non-negative-price intervals represented **94.13%**.

During negative-price intervals, average selected renewable generation was approximately **23,762.23 MWh higher** than during non-negative-price intervals. Average grid load was approximately **4,441.54 MWh lower**, and average residual load was approximately **28,203.77 MWh lower**.

Residual load represents grid load after subtracting the selected wind and solar generation components. The observed comparison therefore shows that negative-price intervals coincided with substantially higher selected renewable generation relative to grid load.

### Correlation analysis

The correlation analysis across the combined dataset also showed:

| Variable pair | Correlation |
|---|---:|
| Price and grid load | 0.308 |
| Price and selected renewables | -0.651 |
| Price and residual load | 0.827 |
| Grid load and selected renewables | 0.280 |
| Grid load and residual load | 0.370 |
| Selected renewables and residual load | -0.788 |

These correlations describe linear relationships across the combined observations. They do not measure causal effects and may reflect common patterns in time, demand, generation, or market conditions.

### Price across demand and residual-load quintiles

A demand-price analysis examined how electricity prices varied across grid-load and residual-load levels. The analysis divided observations into five quintiles, from very low to very high values, and compared the average and median prices within each group.

#### Price by grid-load quintile

| Grid-load quintile | Observed hours | Average grid load (MWh) | Average price (EUR/MWh) | Median price (EUR/MWh) | Negative-price hours |
|---|---:|---:|---:|---:|---:|
| Very Low | 3,509 | 41,149.66 | 67.72 | 82.22 | 285 |
| Low | 3,509 | 47,428.25 | 68.16 | 78.87 | 346 |
| Medium | 3,508 | 53,607.20 | 85.90 | 90.05 | 190 |
| High | 3,509 | 59,225.90 | 85.28 | 85.43 | 183 |
| Very High | 3,509 | 66,788.68 | 112.49 | 101.33 | 26 |

Average prices were substantially higher in the very-high-grid-load quintile than in the lower-load groups. However, the average price did not increase strictly at every quintile, and negative-price hours were observed across the grid-load distribution.

#### Price by residual-load quintile

| Residual-load quintile | Observed hours | Average residual load (MWh) | Average price (EUR/MWh) | Median price (EUR/MWh) | Negative-price hours |
|---|---:|---:|---:|---:|---:|
| Very Low | 3,509 | 9,371.06 | 18.25 | 8.38 | 1,026 |
| Low | 3,509 | 22,753.62 | 68.65 | 71.11 | 4 |
| Medium | 3,508 | 30,983.46 | 88.80 | 88.56 | 0 |
| High | 3,509 | 38,337.50 | 103.07 | 101.89 | 0 |
| Very High | 3,509 | 49,966.40 | 140.78 | 128.56 | 0 |

The average price increased from 18.25 EUR/MWh in the very-low-residual-load quintile to 140.78 EUR/MWh in the very-high-residual-load quintile.

Negative-price intervals were concentrated in the very-low-residual-load group: **1,026 of its 3,509 observations** had negative prices. The remaining residual-load quintiles contained very few or no negative-price observations.

**Interpretation:** Residual load showed a strong positive relationship with price across the observed quintiles. Negative prices were concentrated in intervals with very low residual load, while higher residual-load groups had progressively higher average prices.

This is consistent with residual load being an important descriptive indicator of market conditions. However, the quintile analysis does not isolate residual load from time of day, seasonality, demand patterns, generation availability, cross-border flows, or other market factors. It does not establish a causal relationship.

**Supporting analyses:**

- `negative_price_comparison_2024_2025.csv`
- `demand_price_analysis_2024_2025.csv`

## 6. Data Coverage and Limitations

- The combined dataset contains **17,544 matched hourly records** for 2024 and 2025.
- The 2024 dataset contains 8,784 records, covering the leap year.
- The 2025 dataset contains 8,760 records.
- The combined dataset has no duplicate UTC timestamps.
- The UTC timeline is continuous, with every consecutive timestamp separated by exactly one hour.
- The spring daylight-saving transitions in 2024 and 2025 show continuous UTC time while local time moves from 01:00 to 03:00. The local 02:00 hour is absent on those transition dates.
- The autumn daylight-saving transitions contain repeated local 02:00 labels. The inspected raw consumption records for both years matched the merged records in source chronological order and in their observed values. Because the raw source timestamps do not independently distinguish the two repeated local hours, this check should not be interpreted as independent verification of every source row.
- The timestamp validation establishes continuity of the merged UTC timeline and checks the inspected daylight-saving records. It does not independently verify every original source row.
- February, November, and December 2025 had no observed negative-price hours, so negative-versus-non-negative generation comparisons are unavailable for those months.
- The severity-band percentages describe the distribution of observed negative-price hours, not the share of all hours in a year.
- The solar-consistency analysis includes 13 year-month combinations meeting the 30-negative-hour screening threshold. The threshold is a practical rule, not a statistical significance criterion.
- Hourly frequency rates use observed intervals as their denominators. Local daylight-saving transitions can result in different observation counts for certain hours.
- Some hourly solar averages during negative-price intervals are based on fewer than 30 observations and should be interpreted cautiously.
- The demand-price quintile analysis is descriptive. Quintiles group observations by their measured grid load or residual load; they do not represent independent experiments or causal comparisons.
- The analysis is descriptive. It does not control for imports and exports, conventional generation, storage, time of day in the monthly comparisons, or other factors that can influence electricity prices.
- The selected renewable-generation measure includes the wind and solar components available in this dataset; it should not be interpreted as a complete measure of every renewable energy source.
- Before publication, verify the original SMARD field definitions and units for generation data. The numerical differences reported here are preserved from the analysis output and should not be interpreted as monthly totals.
- The dataset covers 2024–2025 and should not automatically be assumed to represent future market conditions.

## 7. Conclusion

The analysis identifies a clear increase in negative-price frequency during May and June 2025, alongside higher average solar generation during negative-price hours in those months.

The severity analysis shows that mild negative prices accounted for a larger share of negative-price events in 2025, while the observed number of hours below -100 EUR/MWh also increased. These findings demonstrate that negative-price frequency and severity provide different perspectives on market conditions.

The monthly consistency analysis adds evidence that higher solar generation coincided with negative prices in all 13 year-month combinations meeting the screening threshold. The direction of the average difference remained positive when any one eligible month was excluded.

The hourly analysis adds a temporal dimension: negative prices peaked around midday in both years, and average solar generation was generally higher during daytime negative-price intervals. These patterns are consistent with a relationship worth investigating further, but they do not establish causation or isolate the effects of individual market factors.

The demand-price analysis adds a broader market perspective. Negative-price intervals were associated with higher selected renewable generation and substantially lower residual load. Across residual-load quintiles, average prices increased from the very-low-residual-load group to the very-high-residual-load group, while negative-price observations were concentrated in the very-low-residual-load group.

Together, the findings provide a foundation for deeper investigation into the relationship between renewable generation, residual load, and electricity-market prices. Further work should examine additional market variables and account for time-of-day effects before drawing conclusions about causes or implications for market participants.
