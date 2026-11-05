# GridSignal AI

**German Electricity Market Analytics · Python · pandas · matplotlib · pytest**

Negative day-ahead electricity prices in Germany appear when wind and solar cover almost all of demand. This project turns hourly SMARD data for 2024–2025 into validated datasets, controlled comparisons and charts that show when negative prices happen and what separates those hours from the rest.

Despite the name, there is no machine-learning component yet. Forecasting and AI-assisted explanations are ideas for later, not implemented features.

## In plain terms

- **Negative price:** producers pay to deliver electricity instead of being paid. It happens when more power is on offer than buyers want at a normal price, and some plants find it cheaper to keep running than to shut down.
- **Residual load:** demand minus wind and solar, the amount other power plants (gas, coal, hydro) still have to supply. When it is near zero, wind and solar cover almost everything.

## Key Findings

These are descriptive results from two years of hourly data. They show associations, not causes.

### 1. Negative prices appear when residual load is low

![Share of hours with a negative price, by residual load](docs/negative_price_share_by_residual_load_2024_2025.png)

- When wind and solar covered all of demand (residual load of 0 GW or below), 239 of 261 hours (92%) had a negative price.
- Across the 13,296 hours with residual load above 20 GW, none did.
- 89% of all negative-price hours (918 of 1,030) happened when residual load was below 10 GW.
- Residual load has a correlation of 0.83 with price (Spearman 0.87), far stronger than demand alone (0.31).

### 2. Solar alone is a weak explanation

Average solar output is 4.55× higher in negative-price hours than in other hours (2025), but most of that gap comes from *when* negative prices happen: at midday, in the sunny months. Comparing like with like shrinks it step by step.

| 2025 comparison | Negative-price hours | Other hours | Ratio |
|---|---|---|---|
| All hours | 573 hours, 31.3 GW | 8,187 hours, 6.9 GW | 4.55× |
| Midday only (11:00–14:59) | 342 hours, 36.4 GW | 1,118 hours, 21.8 GW | 1.67× |
| Midday, April–September | 302 hours, 37.8 GW | 430 hours, 32.1 GW | 1.18× |

In 2024 the same steps give 4.11×, 1.72× and 1.16×. Values are average solar output per hour, in GW.

### 3. Negative prices cluster around midday

![Hour-of-day pattern of negative prices and solar output](docs/hour_of_day_analysis_2024_2025.png)

- 84% of negative-price hours fell between 10:00 and 17:00 German local time.
- The peak hour was 14:00 in 2024 (20.49% of those hours) and 13:00 in 2025 (27.12%).

### 4. Negative prices became more frequent in 2025, mostly in spring

![Monthly frequency of negative prices](docs/negative_price_frequency_2024_2025.png)

- Negative-price hours rose from 457 in 2024 to 573 in 2025 (+116, or +25.4%).
- April to June added 153 hours, partly offset by July, which fell from 81 hours to 12. The July drop is not yet explained.
- February, November and December 2025 had no negative-price hours.

### 5. Most negative prices are mild

![Severity of negative prices](docs/negative_price_severity_2024_2025.png)

- 70.0% of negative-price hours in 2024 and 76.4% in 2025 were between −10 and 0 €/MWh.
- Hours below −100 €/MWh rose from 5 to 13, but remain rare. The lowest price was −250.32 €/MWh (2025).

See [detailed findings](docs/findings.md) for tables, method notes and limitations.

## Limitations

- Two years of data; the results describe associations, not causes.
- Residual load subtracts only wind and solar, not hydro, biomass or imports.
- Time of day and season are controlled in the solar comparison. Demand, wind, power-plant flexibility, cross-border flows and subsidy rules are not.
- Negative means strictly below €0/MWh. Counting zero-price hours as well would give 519 (2024) and 655 (2025) hours.
- From 1 October 2025 the market uses 15-minute products; hourly values after that date average four quarter-hours.

The full list is in [docs/findings.md](docs/findings.md).

## Data and Method

**Source:** [SMARD](https://www.smard.de/en), Germany/Luxembourg bidding zone, hourly data for 2024–2025: day-ahead prices, actual offshore wind, onshore wind and solar generation, and actual grid consumption. The selected generation measures are not total supply.

1. **Clean** timestamps and numeric values for each source file.
2. **Validate** required columns, duplicate timestamps and interval continuity.
3. **Combine** prices, generation and consumption on UTC timestamps (17,544 matched hourly rows: 8,784 in 2024 and 8,760 in 2025).
4. **Analyze** with grouped, controlled comparisons and fixed residual-load bands.
5. **Visualize** each finding with one chart whose numbers are computed from the data.

Calendar analysis uses `Europe/Berlin` local time. All scripts read data through one shared loader, and `run_pipeline.py` runs the whole workflow in order.

## Repository Structure

```text
GridSignal_AI/
├── data/
│   ├── raw/                  # Local source data; not tracked
│   └── processed/            # Generated datasets; not tracked
├── docs/
│   ├── findings.md
│   ├── negative_price_frequency_2024_2025.png
│   ├── negative_price_severity_2024_2025.png
│   ├── negative_price_share_by_residual_load_2024_2025.png
│   ├── hour_of_day_analysis_2024_2025.png
│   ├── negative_price_comparison_2024_2025.csv
│   ├── price_by_residual_load_band_2024_2025.csv
│   ├── price_correlations_2024_2025.csv
│   ├── solar_comparison_controls_2024_2025.csv
│   ├── hourly_negative_price_frequency_2024_2025.csv
│   └── hourly_solar_by_price_category_2024_2025.csv
├── src/
│   └── gridsignal/
│       ├── __init__.py
│       ├── config.py
│       ├── data_loader.py
│       ├── data_validation.py
│       ├── clean_data.py
│       ├── clean_generation.py
│       ├── combine_data.py
│       ├── prepare_consumption_data.py
│       ├── analyze_solar_controls.py
│       ├── analyze_residual_load.py
│       ├── analyze_negative_price_hours.py
│       ├── analyze_hour_of_day.py
│       ├── plot_negative_price_frequency.py
│       ├── plot_negative_price_severity.py
│       ├── plot_residual_load_bands.py
│       ├── plot_hour_of_day_analysis.py
│       ├── inspect_dst_consumption_alignment.py
│       ├── inspect_raw_dst_rows.py
│       └── run_pipeline.py
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

Raw and processed datasets and local notes are excluded from version control.

## Run Locally

Instructions describe the Windows PowerShell workflow.

### Requirements

- Python 3.14 or later, as specified in the current project configuration
- pip
- Git

### 1. Clone

```powershell
git clone https://github.com/aliakbarse/GridSignal-AI.git
cd GridSignal-AI
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, consult the Python documentation for your environment's execution-policy settings.

### 3. Install the project and development dependencies

```powershell
python -m pip install -e ".[dev]"
```

### 4. Download source data

Download the hourly day-ahead prices, actual generation and actual consumption CSV files from [SMARD](https://www.smard.de/en) and place them in `data/raw/` with these names:

```text
data/raw/
├── Day-ahead_prices_202312312100_202512312100_Hour.csv
├── Actual_generation_202312312100_202512312100_Hour.csv
└── Actual_consumption_202312312100_202512312100_Hour.csv
```

These are local inputs and are not tracked in Git. Check the applicable source terms before redistributing downloaded data.

### 5. Run the full pipeline

From the repository root:

```powershell
python -m gridsignal.run_pipeline
```

This cleans and combines the data, runs every analysis and regenerates every chart. Processed datasets are written to `data/processed/` and analysis outputs and charts to `docs/`. Each stage can also be run on its own, for example `python -m gridsignal.analyze_residual_load`.

### 6. Run tests

```powershell
python -m pytest -v
```

The tests cover key data-pipeline rules, including negative-price classification, timestamp validation and matching price and generation records. Passing tests verify the tested rules; they do not validate every analytical conclusion.

### 7. Optional timestamp and DST diagnostics

```powershell
python -m gridsignal.inspect_dst_consumption_alignment
python -m gridsignal.inspect_raw_dst_rows
```

These are diagnostic tools, not required stages of a normal run.

## Next Steps

Planned, not yet implemented: weekend, holiday and night-time analysis, an explanation of the July 2025 drop, a business view of solar capture rates, a SQL layer and automated checks on every commit.

## License

A license has not yet been selected. Project code and third-party data remain subject to their applicable terms until licensing and redistribution permissions are confirmed.