import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

FREQUENCY_FILE = config.DOCS_DIR / "hourly_negative_price_frequency_2024_2025.csv"
SOLAR_FILE = config.DOCS_DIR / "hourly_solar_by_price_category_2024_2025.csv"

PRICE_CATEGORY_LABELS = {True: "Negative price", False: "Nonnegative price"}


def load_data() -> pd.DataFrame:
    """Load the market data and label each hour by price category."""
    data = load_market_data()
    data["price_category"] = data["is_negative_price"].map(PRICE_CATEGORY_LABELS)
    print(f"Loaded {len(data):,} hourly records.")
    print(f"Years covered: {sorted(data['year'].unique().tolist())}")
    return data


def analyze_hourly_frequency(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate negative-price frequency by local hour and year."""
    summary = data.groupby(["year", "hour"], as_index=False).agg(
        observed_hours=("is_negative_price", "size"),
        negative_price_hours=("is_negative_price", "sum"),
    )
    summary["negative_price_rate_pct"] = (
        summary["negative_price_hours"] / summary["observed_hours"] * 100
    )
    return summary.sort_values(["year", "hour"]).reset_index(drop=True)


def analyze_solar_by_hour(data: pd.DataFrame) -> pd.DataFrame:
    """Compare solar generation by price category, hour, and year."""
    summary = data.groupby(
        ["year", "hour", "price_category"], as_index=False, observed=True
    ).agg(
        observed_hours=("solar_mwh", "size"),
        average_solar_mwh=("solar_mwh", "mean"),
        median_solar_mwh=("solar_mwh", "median"),
        solar_std_mwh=("solar_mwh", "std"),
    )
    return summary.sort_values(["year", "hour", "price_category"]).reset_index(
        drop=True
    )


def print_hourly_frequency(summary: pd.DataFrame) -> None:
    """Print the peak negative-price hour for each year."""
    print("\nHighest negative-price rates by year:")
    for year in sorted(summary["year"].unique()):
        year_data = summary[summary["year"] == year]
        top = year_data.loc[year_data["negative_price_rate_pct"].idxmax()]
        print(
            f"{year}: {int(top['hour']):02d}:00 - "
            f"{top['negative_price_rate_pct']:.2f}% "
            f"({int(top['negative_price_hours'])} negative-price hours "
            f"out of {int(top['observed_hours'])} observed)"
        )


def main() -> None:
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_data()
    hourly_frequency = analyze_hourly_frequency(data)
    solar_by_hour = analyze_solar_by_hour(data)

    hourly_frequency.to_csv(FREQUENCY_FILE, index=False)
    solar_by_hour.to_csv(SOLAR_FILE, index=False)
    print(f"\nSaved: {FREQUENCY_FILE}")
    print(f"Saved: {SOLAR_FILE}")

    print_hourly_frequency(hourly_frequency)


if __name__ == "__main__":
    main()