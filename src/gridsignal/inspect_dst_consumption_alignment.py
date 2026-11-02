
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MERGED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_consumption_combined_2024_2025.csv"
)


def inspect_transition(df, date):
    print("\n" + "=" * 80)
    print(f"AUTUMN DST INSPECTION: {date}")
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
        "price_eur_mwh",
        "grid_load_mwh",
        "renewables_selected_mwh",
        "residual_load_mwh",
    ]

    transition_data = df.loc[mask, columns]

    if transition_data.empty:
        print("No records found for this date.")
        return

    print(
        transition_data
        .to_string(index=False)
    )

    print("\nRepeated local timestamps:")

    duplicates = transition_data[
        transition_data["start_time_local"].duplicated(
            keep=False
        )
        | transition_data["start_time_local"].duplicated(
            keep=False
        )
    ]

    if duplicates.empty:
        print("No repeated local timestamps found.")
    else:
        print(
            duplicates[
                [
                    "start_time_local",
                    "start_time_utc",
                    "price_eur_mwh",
                    "grid_load_mwh",
                ]
            ].to_string(index=False)
        )


def main():
    if not MERGED_FILE.exists():
        raise FileNotFoundError(
            f"Merged dataset not found:\n{MERGED_FILE}"
        )

    df = pd.read_csv(MERGED_FILE)

    required_columns = [
        "start_time_local",
        "start_time_utc",
        "price_eur_mwh",
        "grid_load_mwh",
        "renewables_selected_mwh",
        "residual_load_mwh",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df["start_time_utc"] = pd.to_datetime(
        df["start_time_utc"],
        utc=True,
        errors="raise",
    )

    print(f"Total rows: {len(df):,}")

    print(
        "Duplicate UTC timestamps:",
        df["start_time_utc"].duplicated().sum(),
    )

    for date in [
        "2024-10-27",
        "2025-10-26",
    ]:
        inspect_transition(df, date)


if __name__ == "__main__":
    main()
