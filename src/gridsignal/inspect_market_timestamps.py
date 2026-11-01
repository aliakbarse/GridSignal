
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


def inspect_market_data():
    print("\n" + "=" * 70)
    print("MARKET DATASET")
    print("=" * 70)

    if not MARKET_FILE.exists():
        raise FileNotFoundError(
            f"Market dataset not found:\n{MARKET_FILE}"
        )

    df = pd.read_csv(MARKET_FILE)

    print(f"\nFile: {MARKET_FILE}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {df.columns.tolist()}")

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    print("\nLast 3 rows:")
    print(df.tail(3).to_string(index=False))

    timestamp_column = "start_time_utc"

    if timestamp_column not in df.columns:
        print(
            f"\nERROR: Expected timestamp column "
            f"'{timestamp_column}' was not found."
        )
        print("Available columns:", df.columns.tolist())
        return

    timestamps = pd.to_datetime(
        df[timestamp_column],
        utc=True,
        errors="coerce",
    )

    invalid_count = timestamps.isna().sum()

    print("\nTimestamp validation:")
    print(f"Invalid timestamps: {invalid_count}")

    valid_timestamps = timestamps.dropna()

    if valid_timestamps.empty:
        print("No valid timestamps available.")
        return

    local_timestamps = valid_timestamps.dt.tz_convert(
        "Europe/Berlin"
    )

    print("\nUTC coverage:")
    print(f"First: {valid_timestamps.min()}")
    print(f"Last:  {valid_timestamps.max()}")

    print("\nGermany local-time coverage:")
    print(f"First: {local_timestamps.min()}")
    print(f"Last: {local_timestamps.max()}")

    print("\nDuplicate UTC timestamps:")
    print(valid_timestamps.duplicated().sum())

    print("\nUTC interval differences:")
    print(
        valid_timestamps.sort_values()
        .diff()
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nLocal timestamps around spring DST transitions:")

    spring_dates = ["2024-03-31", "2025-03-30"]

    for date in spring_dates:
        mask = local_timestamps.dt.strftime("%Y-%m-%d") == date

        print(f"\n{date}")
        print(
            local_timestamps[mask]
            .to_string(index=False)
        )

    print("\nLocal timestamps around autumn DST transitions:")

    autumn_dates = ["2024-10-27", "2025-10-26"]

    for date in autumn_dates:
        mask = local_timestamps.dt.strftime("%Y-%m-%d") == date

        print(f"\n{date}")
        print(
            local_timestamps[mask]
            .to_string(index=False)
        )


def inspect_consumption_data():
    print("\n" + "=" * 70)
    print("RAW CONSUMPTION DATASET")
    print("=" * 70)

    if not CONSUMPTION_FILE.exists():
        raise FileNotFoundError(
            f"Consumption dataset not found:\n{CONSUMPTION_FILE}"
        )

    df = pd.read_csv(
        CONSUMPTION_FILE,
        sep=";",
    )

    print(f"\nFile: {CONSUMPTION_FILE}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {df.columns.tolist()}")

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    print("\nLast 3 rows:")
    print(df.tail(3).to_string(index=False))

    timestamp_column = "Start date"

    if timestamp_column not in df.columns:
        print(
            f"\nERROR: Expected timestamp column "
            f"'{timestamp_column}' was not found."
        )
        return

    timestamps = pd.to_datetime(
        df[timestamp_column],
        format="%b %d, %Y %I:%M %p",
        errors="coerce",
    )

    print("\nRaw timestamp validation:")
    print(f"Invalid timestamps: {timestamps.isna().sum()}")
    print(f"First: {timestamps.min()}")
    print(f"Last: {timestamps.max()}")

    print("\nDuplicate local timestamps:")
    duplicates = timestamps[
        timestamps.duplicated(keep=False)
    ]

    print(duplicates.to_string(index=False))

    print("\nRaw timestamp interpretation:")
    print(
        "These timestamps do not contain timezone information."
    )
    print(
        "Repeated autumn timestamps cannot be uniquely converted "
        "to UTC without additional source information."
    )


def main():
    inspect_market_data()
    inspect_consumption_data()

    print("\n" + "=" * 70)
    print("INSPECTION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
