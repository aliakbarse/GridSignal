
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Actual_consumption_202312312100_202512312100_Hour.csv"
)

EXPECTED_COLUMNS = [
    "Start date",
    "End date",
    "grid load [MWh] Calculated resolutions",
    "Grid load incl. hydro pumped storage [MWh] Calculated resolutions",
    "Hydro pumped storage [MWh] Calculated resolutions",
    "Residual load [MWh] Calculated resolutions",
]


def main():
    print("=" * 70)
    print("GRIDSIGNAL AI - CONSUMPTION TIMESTAMP INVESTIGATION")
    print("=" * 70)

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Consumption CSV not found:\n{RAW_FILE}"
        )

    df = pd.read_csv(
        RAW_FILE,
        sep=";",
        thousands=",",
        decimal=".",
    )

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Expected columns missing: {missing_columns}"
        )

    df["Start date"] = pd.to_datetime(
        df["Start date"],
        format="%b %d, %Y %I:%M %p",
        errors="coerce",
    )

    df["End date"] = pd.to_datetime(
        df["End date"],
        format="%b %d, %Y %I:%M %p",
        errors="coerce",
    )

    print(f"\nInput file: {RAW_FILE}")
    print(f"Total records: {len(df):,}")

    print("\n1. DUPLICATE START TIMESTAMPS")
    print("-" * 70)

    duplicate_mask = df["Start date"].duplicated(
        keep=False
    )

    duplicates = df.loc[
        duplicate_mask,
        ["Start date", "End date"],
    ].sort_values("Start date")

    if duplicates.empty:
        print("No duplicate start timestamps.")
    else:
        print(duplicates.to_string(index=False))

    print("\n2. DUPLICATE END TIMESTAMPS")
    print("-" * 70)

    duplicate_end_mask = df["End date"].duplicated(
        keep=False
    )

    duplicate_ends = df.loc[
        duplicate_end_mask,
        ["Start date", "End date"],
    ].sort_values("End date")

    if duplicate_ends.empty:
        print("No duplicate end timestamps.")
    else:
        print(duplicate_ends.to_string(index=False))

    print("\n3. TIMESTAMP GAPS")
    print("-" * 70)

    valid_starts = (
        df["Start date"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    differences = valid_starts.diff()

    gap_mask = differences > pd.Timedelta(hours=1)

    gaps = pd.DataFrame(
        {
            "Previous start": valid_starts.shift(1),
            "Current start": valid_starts,
            "Difference": differences,
        }
    )

    gaps = gaps.loc[gap_mask].copy()

    if gaps.empty:
        print("No gaps longer than one hour.")
    else:
        print(gaps.to_string(index=False))

    print("\n4. RECORDS AROUND DUPLICATES AND GAPS")
    print("-" * 70)

    relevant_timestamps = set(
        duplicates["Start date"].dropna()
    )

    if not gaps.empty:
        relevant_timestamps.update(
            gaps["Previous start"].dropna()
        )
        relevant_timestamps.update(
            gaps["Current start"].dropna()
        )

    if relevant_timestamps:
        relevant_rows = df[
            df["Start date"].isin(relevant_timestamps)
            | df["Start date"].isin(
                [
                    timestamp - pd.Timedelta(hours=1)
                    for timestamp in relevant_timestamps
                ]
            )
            | df["Start date"].isin(
                [
                    timestamp + pd.Timedelta(hours=1)
                    for timestamp in relevant_timestamps
                ]
            )
        ].sort_values("Start date")

        print(
            relevant_rows[
                ["Start date", "End date"]
            ].to_string(index=False)
        )
    else:
        print("No relevant timestamps found.")

    print("\n5. YEAR COVERAGE")
    print("-" * 70)

    print(
        df["Start date"]
        .dt.year
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\n" + "=" * 70)
    print("TIMESTAMP INVESTIGATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
