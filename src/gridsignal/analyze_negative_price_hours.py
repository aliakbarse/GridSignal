"""Compare negative-price hours with all other hours.

Groups the hourly data into negative and non-negative price hours and
reports, for each group, the number of hours, average and median price,
average demand, average wind and solar generation, average residual load
and the share of all hours. Stops with an error if a required column is
missing or contains missing values.

Writes docs/negative_price_comparison_2024_2025.csv.

Run with: python -m gridsignal.analyze_negative_price_hours
"""

import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

OUTPUT_FILE = config.DOCS_DIR / "negative_price_comparison_2024_2025.csv"

REQUIRED_COLUMNS = [
    "price_eur_mwh",
    "grid_load_mwh",
    "renewables_selected_mwh",
    "residual_load_mwh",
]


def load_data():
    df = load_market_data(config.CONSUMPTION_COMBINED_FILE)

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("Missing values found in required columns.")

    df["price_category"] = df["is_negative_price"].map(
        {True: "Negative price", False: "Non-negative price"}
    )

    return df


def analyze_negative_prices(df):
    results = (
        df.groupby(
            "price_category",
            observed=False,
        )
        .agg(
            hours=("price_eur_mwh", "count"),
            average_price_eur_mwh=(
                "price_eur_mwh",
                "mean",
            ),
            median_price_eur_mwh=(
                "price_eur_mwh",
                "median",
            ),
            average_demand_mwh=(
                "grid_load_mwh",
                "mean",
            ),
            average_renewables_mwh=(
                "renewables_selected_mwh",
                "mean",
            ),
            average_residual_load_mwh=(
                "residual_load_mwh",
                "mean",
            ),
        )
        .reset_index()
    )

    total_hours = len(df)

    results["share_of_all_hours_pct"] = (
        results["hours"]
        / total_hours
        * 100
    )

    print("\n" + "=" * 70)
    print("NEGATIVE VS NON-NEGATIVE PRICE HOURS")
    print("=" * 70)

    print(
        results.round(2).to_string(index=False)
    )

    return results


def main():
    print("=" * 70)
    print("GRIDSIGNAL - NEGATIVE PRICE ANALYSIS")
    print("=" * 70)

    df = load_data()

    print(f"\nTotal observations: {len(df):,}")

    results = analyze_negative_prices(df)

    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    results.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\nAnalysis complete.")

    print(
        f"Results saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()