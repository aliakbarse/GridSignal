
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
    / "demand_price_analysis_2024_2025.csv"
)


def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "start_time_utc",
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

    df["start_time_utc"] = pd.to_datetime(
        df["start_time_utc"],
        utc=True,
        errors="coerce",
    )

    if df["start_time_utc"].isna().any():
        raise ValueError(
            "Invalid timestamps found."
        )

    if df[required_columns].isna().any().any():
        raise ValueError(
            "Missing values found in required columns."
        )

    return df


def calculate_correlations(df):
    variables = [
        "price_eur_mwh",
        "grid_load_mwh",
        "renewables_selected_mwh",
        "residual_load_mwh",
    ]

    correlation = df[variables].corr()

    print("\n" + "=" * 70)
    print("CORRELATION MATRIX")
    print("=" * 70)

    print(correlation.round(3).to_string())

    return correlation


def analyze_demand_levels(df):
    print("\n" + "=" * 70)
    print("PRICE BY ELECTRICITY DEMAND LEVEL")
    print("=" * 70)

    df = df.copy()

    df["demand_category"] = pd.qcut(
        df["grid_load_mwh"],
        q=5,
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Very High",
        ],
    )

    results = (
        df.groupby(
            "demand_category",
            observed=False,
        )
        .agg(
            hours=("price_eur_mwh", "count"),
            average_demand_mwh=("grid_load_mwh", "mean"),
            average_price_eur_mwh=("price_eur_mwh", "mean"),
            median_price_eur_mwh=("price_eur_mwh", "median"),
            negative_price_hours=(
                "is_negative_price",
                "sum",
            ),
        )
        .reset_index()
    )

    print(results.round(2).to_string(index=False))

    return results


def analyze_residual_load_levels(df):
    print("\n" + "=" * 70)
    print("PRICE BY RESIDUAL LOAD LEVEL")
    print("=" * 70)

    df = df.copy()

    df["residual_load_category"] = pd.qcut(
        df["residual_load_mwh"],
        q=5,
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Very High",
        ],
    )

    results = (
        df.groupby(
            "residual_load_category",
            observed=False,
        )
        .agg(
            hours=("price_eur_mwh", "count"),
            average_residual_load_mwh=(
                "residual_load_mwh",
                "mean",
            ),
            average_price_eur_mwh=(
                "price_eur_mwh",
                "mean",
            ),
            median_price_eur_mwh=(
                "price_eur_mwh",
                "median",
            ),
            negative_price_hours=(
                "is_negative_price",
                "sum",
            ),
        )
        .reset_index()
    )

    print(results.round(2).to_string(index=False))

    return results


def main():
    print("=" * 70)
    print("GRIDSIGNAL AI - DEMAND AND PRICE ANALYSIS")
    print("=" * 70)

    df = load_data()

    print(f"\nDataset rows: {len(df):,}")

    print(
        f"First timestamp: "
        f"{df['start_time_utc'].min()}"
    )

    print(
        f"Last timestamp: "
        f"{df['start_time_utc'].max()}"
    )

    correlation = calculate_correlations(df)

    demand_results = analyze_demand_levels(df)

    residual_results = analyze_residual_load_levels(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    demand_results.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    print(
        f"Demand analysis saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
