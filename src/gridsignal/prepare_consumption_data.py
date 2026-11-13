"""Add grid consumption and residual load to the combined dataset.

Reads the combined market file and the raw SMARD consumption CSV, and
keeps the consumption intervals that fall inside the market data's local
time range. Before joining, it checks row by row that the local start and
end times match, so the two repeated hours at the autumn clock change stay
separate. The columns are then joined by row order. Raises an error if the
row counts or timestamps do not match, instead of merging anyway.

Writes data/processed/germany_market_consumption_combined_2024_2025.csv,
which the analysis scripts read.

Run with: python -m gridsignal.prepare_consumption_data
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MARKET_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_combined_2024_2025.csv"
)

CONSUMPTION_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Actual_consumption_202312312100_202512312100_Hour.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_consumption_combined_2024_2025.csv"
)

CONSUMPTION_COLUMNS = {
    "grid load [MWh] Calculated resolutions": "grid_load_mwh",
    "Grid load incl. hydro pumped storage [MWh] Calculated resolutions": (
        "grid_load_incl_pumped_storage_mwh"
    ),
    "Hydro pumped storage [MWh] Calculated resolutions": (
        "hydro_pumped_storage_mwh"
    ),
    "Residual load [MWh] Calculated resolutions": "residual_load_mwh",
}


def load_market_data():
    if not MARKET_FILE.exists():
        raise FileNotFoundError(
            f"Market dataset not found:\n{MARKET_FILE}"
        )

    market = pd.read_csv(MARKET_FILE)

    required_columns = {
        "start_time_utc",
        "start_time_local",
        "end_time_local",
    }

    missing_columns = required_columns - set(market.columns)

    if missing_columns:
        raise ValueError(
            f"Market dataset is missing columns: {missing_columns}"
        )

    market["start_time_utc"] = pd.to_datetime(
        market["start_time_utc"],
        utc=True,
        errors="coerce",
    )

    if market["start_time_utc"].isna().any():
        raise ValueError(
            "Market dataset contains invalid UTC timestamps."
        )

    if market["start_time_utc"].duplicated().any():
        raise ValueError(
            "Market dataset contains duplicate UTC timestamps."
        )

    market = market.sort_values(
        "start_time_utc"
    ).reset_index(drop=True)

    return market


def load_consumption_data():
    if not CONSUMPTION_FILE.exists():
        raise FileNotFoundError(
            f"Consumption dataset not found:\n{CONSUMPTION_FILE}"
        )

    consumption = pd.read_csv(
        CONSUMPTION_FILE,
        sep=";",
        thousands=",",
        decimal=".",
    )

    required_columns = {
        "Start date",
        "End date",
        *CONSUMPTION_COLUMNS.keys(),
    }

    missing_columns = required_columns - set(consumption.columns)

    if missing_columns:
        raise ValueError(
            f"Consumption dataset is missing columns: {missing_columns}"
        )

    consumption["start_local_naive"] = pd.to_datetime(
        consumption["Start date"],
        format="%b %d, %Y %I:%M %p",
        errors="coerce",
    )

    consumption["end_local_naive"] = pd.to_datetime(
        consumption["End date"],
        format="%b %d, %Y %I:%M %p",
        errors="coerce",
    )

    if consumption[
        ["start_local_naive", "end_local_naive"]
    ].isna().any().any():
        raise ValueError(
            "Consumption dataset contains invalid timestamps."
        )

    consumption = consumption.rename(
        columns=CONSUMPTION_COLUMNS
    )

    numeric_columns = list(
        CONSUMPTION_COLUMNS.values()
    )

    for column in numeric_columns:
        consumption[column] = pd.to_numeric(
            consumption[column],
            errors="coerce",
        )

    if consumption[numeric_columns].isna().any().any():
        raise ValueError(
            "Consumption dataset contains missing or invalid numeric values."
        )

    return consumption


def align_consumption(market, consumption):
    print("\n" + "=" * 70)
    print("CONSUMPTION ALIGNMENT")
    print("=" * 70)

    market_start = market["start_time_utc"].min()
    market_end = market["start_time_utc"].max()

    market_start_local = market_start.tz_convert(
        "Europe/Berlin"
    ).tz_localize(None)

    market_end_local = market_end.tz_convert(
        "Europe/Berlin"
    ).tz_localize(None)

    print(f"Market first UTC interval: {market_start}")
    print(f"Market last UTC interval:  {market_end}")
    print(f"Market first local time:  {market_start_local}")
    print(f"Market last local time:   {market_end_local}")

    # Keep consumption intervals whose local start time
    # falls within the market dataset's local coverage.
    #
    # This removes the three 2023 boundary records without
    # relying on a hard-coded row count.

    consumption = consumption.loc[
        (
            consumption["start_local_naive"]
            >= market_start_local
        )
        &
        (
            consumption["start_local_naive"]
            <= market_end_local
        )
    ].copy()

    consumption = consumption.reset_index(drop=True)

    market = market.reset_index(drop=True)

    print(f"\nMarket rows: {len(market):,}")
    print(f"Consumption rows after boundary filtering: {len(consumption):,}")

    if len(market) != len(consumption):
        raise ValueError(
            "Row counts do not match after boundary filtering. "
            "Do not merge yet. Investigate missing or extra intervals."
        )

    # The datasets are expected to cover the same chronological
    # hourly interval sequence. Preserve the source row order,
    # including both repeated autumn DST observations.
    #
    # Verify each consumption local start/end against the
    # market dataset's timezone-aware local interval labels.

    market_start_local = pd.to_datetime(
        market["start_time_local"],
        utc=True,
        errors="coerce",
    ).dt.tz_convert("Europe/Berlin").dt.tz_localize(None)

    market_end_local = pd.to_datetime(
        market["end_time_local"],
        errors="coerce",
    )

    # end_time_local in the market file is naive local time.
    # The source values should correspond to the local end
    # of each interval.

    if market_start_local.isna().any():
        raise ValueError(
            "Market local start timestamps could not be parsed."
        )

    if market_end_local.isna().any():
        raise ValueError(
            "Market local end timestamps could not be parsed."
        )

    start_matches = (
        market_start_local.reset_index(drop=True)
        == consumption["start_local_naive"]
    )

    end_matches = (
        market_end_local.reset_index(drop=True)
        == consumption["end_local_naive"]
    )

    if not start_matches.all():
        mismatch_indices = start_matches[
            ~start_matches
        ].index.tolist()[:10]

        raise ValueError(
            "Local start timestamps do not align. "
            f"First mismatched row indices: {mismatch_indices}"
        )

    if not end_matches.all():
        mismatch_indices = end_matches[
            ~end_matches
        ].index.tolist()[:10]

        raise ValueError(
            "Local end timestamps do not align. "
            f"First mismatched row indices: {mismatch_indices}"
        )

    print("\nLocal interval validation:")
    print(f"Start timestamp matches: {start_matches.sum():,}")
    print(f"End timestamp matches:   {end_matches.sum():,}")

    # Merge by chronological row order only after validating
    # interval boundaries. This preserves the two autumn
    # observations as separate intervals.

    consumption_values = consumption[
        list(CONSUMPTION_COLUMNS.values())
    ].reset_index(drop=True)

    merged = pd.concat(
        [
            market.reset_index(drop=True),
            consumption_values,
        ],
        axis=1,
    )

    if len(merged) != len(market):
        raise ValueError(
            "Merged row count differs from market row count."
        )

    if merged[
        list(CONSUMPTION_COLUMNS.values())
    ].isna().any().any():
        raise ValueError(
            "Merged consumption columns contain missing values."
        )

    return merged


def main():
    print("=" * 70)
    print("GRIDSIGNAL - CONSUMPTION DATA PREPARATION")
    print("=" * 70)

    market = load_market_data()
    consumption = load_consumption_data()

    merged = align_consumption(
        market,
        consumption,
    )

    print("\n" + "=" * 70)
    print("MERGED DATASET")
    print("=" * 70)

    print(f"Rows: {len(merged):,}")
    print(f"Columns: {merged.columns.tolist()}")

    print("\nFirst 3 rows:")
    print(merged.head(3).to_string(index=False))

    print("\nLast 3 rows:")
    print(merged.tail(3).to_string(index=False))

    print("\nConsumption summary:")
    print(
        merged[
            list(CONSUMPTION_COLUMNS.values())
        ].describe().round(2).to_string()
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    merged.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n" + "=" * 70)
    print("SUCCESS")
    print("=" * 70)

    print(f"Saved merged dataset to:\n{OUTPUT_FILE}")
    print(f"Total rows: {len(merged):,}")


if __name__ == "__main__":
    main()
