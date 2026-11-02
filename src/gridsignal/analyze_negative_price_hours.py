
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_consumption_combined_2024_2025.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "docs"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "negative_price_comparison_2024_2025.csv"
)


def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "price_eur_mwh",
        "grid_load_mwh",
        "renewables_selected_mwh",
        "residual_load_mwh",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df[required_columns].isna().any().any():
        raise ValueError(
            "Missing values found in required columns."
        )

    df["price_category"] = (
        df["price_eur_mwh"]
        .lt(0)
        .map({
            True: "Negative price",
            False: "Non-negative price",
        })
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
    print("GRIDSIGNAL AI - NEGATIVE PRICE ANALYSIS")
    print("=" * 70)

    df = load_data()

    print(f"\nTotal observations: {len(df):,}")

    results = analyze_negative_prices(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

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
