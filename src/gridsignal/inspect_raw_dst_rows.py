"""Diagnostic: compare raw and merged consumption rows on clock-change days.

On the autumn clock-change days (27 October 2024 and 26 October 2025) one
local hour happens twice. This script prints the raw consumption rows and
the merged dataset rows for those two dates side by side, so you can check
that both repeated hours were kept and matched to the right values.

Not part of the normal pipeline. Run the pipeline first, because it reads
the merged dataset.

Run with: python -m gridsignal.inspect_raw_dst_rows
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Actual_consumption_202312312100_202512312100_Hour.csv"
)

MERGED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_consumption_combined_2024_2025.csv"
)


def load_raw_consumption():
    df = pd.read_csv(
        RAW_FILE,
        sep=";",
    )

    df["Start date"] = pd.to_datetime(
        df["Start date"],
        format="%b %d, %Y %I:%M %p",
        errors="raise",
    )

    df["End date"] = pd.to_datetime(
        df["End date"],
        format="%b %d, %Y %I:%M %p",
        errors="raise",
    )

    df["raw_row_number"] = range(len(df))

    return df


def inspect_raw_transition(df, date):
    print("\n" + "=" * 80)
    print(f"RAW CONSUMPTION: {date}")
    print("=" * 80)

    mask = df["Start date"].dt.strftime("%Y-%m-%d") == date

    columns = [
        "raw_row_number",
        "Start date",
        "End date",
        "grid load [MWh] Calculated resolutions",
        "Residual load [MWh] Calculated resolutions",
    ]

    result = df.loc[mask, columns]

    print(
        result.to_string(index=False)
    )


def inspect_merged_transition(df, date):
    print("\n" + "=" * 80)
    print(f"MERGED DATASET: {date}")
    print("=" * 80)

    local_dates = (
        df["start_time_local"]
        .astype(str)
        .str[:10]
    )

    mask = local_dates == date

    columns = [
        "start_time_local",
        "start_time_utc",
        "grid_load_mwh",
        "residual_load_mwh",
    ]

    result = df.loc[mask, columns]

    print(
        result.to_string(index=False)
    )


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw consumption file not found:\n{RAW_FILE}"
        )

    if not MERGED_FILE.exists():
        raise FileNotFoundError(
            f"Merged dataset not found:\n{MERGED_FILE}"
        )

    raw = load_raw_consumption()

    merged = pd.read_csv(
        MERGED_FILE,
    )

    print(f"Raw consumption rows: {len(raw):,}")
    print(f"Merged dataset rows: {len(merged):,}")

    for date in [
        "2024-10-27",
        "2025-10-26",
    ]:
        inspect_raw_transition(
            raw,
            date,
        )

        inspect_merged_transition(
            merged,
            date,
        )


if __name__ == "__main__":
    main()
