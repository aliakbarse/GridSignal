
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_consumption_combined_2024_2025.csv"
)


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    df["start_time_utc"] = pd.to_datetime(
        df["start_time_utc"],
        utc=True,
        errors="raise",
    )

    df = df.sort_values(
        "start_time_utc"
    ).reset_index(drop=True)

    differences = (
        df["start_time_utc"]
        .diff()
        .dropna()
    )

    print("=" * 70)
    print("MERGED DATASET TIMESTAMP VALIDATION")
    print("=" * 70)

    print(f"Rows: {len(df):,}")
    print(
        "Duplicate UTC timestamps:",
        df["start_time_utc"].duplicated().sum(),
    )

    print("\nUTC interval differences:")
    print(
        differences.value_counts()
        .sort_index()
        .to_string()
    )

    print("\nUnexpected UTC intervals:")
    unexpected = df.loc[
        differences.index[differences != pd.Timedelta(hours=1)],
        [
            "start_time_utc",
            "start_time_local",
        ],
    ]

    if unexpected.empty:
        print("None")
    else:
        print(
            unexpected.to_string(index=False)
        )

    print("\nSpring DST transitions:")

    local = df["start_time_utc"].dt.tz_convert(
        "Europe/Berlin"
    )

    for date in [
        "2024-03-31",
        "2025-03-30",
    ]:
        mask = local.dt.strftime("%Y-%m-%d") == date

        print(f"\n{date}")

        print(
            df.loc[
                mask,
                [
                    "start_time_utc",
                    "start_time_local",
                ],
        ].to_string(index=False)
        )


if __name__ == "__main__":
    main()
