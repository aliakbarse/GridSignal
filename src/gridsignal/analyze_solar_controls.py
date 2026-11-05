import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

OUTPUT_FILE = config.DOCS_DIR / "solar_comparison_controls_2024_2025.csv"


def comparison_row(year: int, label: str, data: pd.DataFrame) -> dict:
    """Mean solar output in negative vs non-negative hours for one subset."""
    grouped = data.groupby("is_negative_price")["solar_mwh"]
    means = grouped.mean()
    counts = grouped.size()

    negative = means.get(True, float("nan"))
    nonnegative = means.get(False, float("nan"))

    return {
        "year": year,
        "comparison": label,
        "negative_hours": int(counts.get(True, 0)),
        "nonnegative_hours": int(counts.get(False, 0)),
        "solar_negative_mwh": negative,
        "solar_nonnegative_mwh": nonnegative,
        "difference_mwh": negative - nonnegative,
        "ratio": negative / nonnegative,
    }


def build_comparisons(df: pd.DataFrame) -> pd.DataFrame:
    """Compare solar output by price category with progressively tighter controls."""
    rows = []

    for year, data in df.groupby("year"):
        midday = data[data["hour"].between(11, 14)]
        summer = midday[midday["month"].between(4, 9)]
        weekday = summer[summer["start_time_local"].dt.dayofweek < 5]
        weekend = summer[summer["start_time_local"].dt.dayofweek >= 5]

        subsets = [
            ("1. All hours", data),
            ("2. Midday (11:00-14:59)", midday),
            ("3. Midday, Apr-Sep", summer),
            ("4a. Midday, Apr-Sep, weekdays", weekday),
            ("4b. Midday, Apr-Sep, weekends", weekend),
        ]
        for label, subset in subsets:
            rows.append(comparison_row(int(year), label, subset))

    return pd.DataFrame(rows)


def main() -> None:
    df = load_market_data()
    results = build_comparisons(df)

    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print(results.round(2).to_string(index=False))
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()