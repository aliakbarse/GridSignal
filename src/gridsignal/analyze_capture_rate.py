"""Solar capture rate: what solar earns per MWh compared with the average price.

capture rate = generation-weighted average price / simple average price
A value below 1 means solar produces when prices are lower than average.
"""

import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

YEARLY_FILE = config.DOCS_DIR / "solar_capture_rate_2024_2025.csv"
MONTHLY_FILE = config.DOCS_DIR / "solar_capture_rate_by_month_2024_2025.csv"


def summarise(group: pd.DataFrame) -> dict:
    """Capture-rate figures for one group of hours."""
    solar = group["solar_mwh"]
    price = group["price_eur_mwh"]
    weighted_price = (price * solar).sum() / solar.sum()
    at_negative = group["is_negative_price"]
    return {
        "average_price_eur_mwh": price.mean(),
        "solar_weighted_price_eur_mwh": weighted_price,
        "capture_rate": weighted_price / price.mean(),
        "solar_share_at_negative_prices_pct": solar[at_negative].sum() / solar.sum() * 100,
        # Market value of solar output sold in negative-price hours (a cost, so negative).
        "value_at_negative_prices_eur_million": (price[at_negative] * solar[at_negative]).sum() / 1e6,
    }


def build_yearly_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = [{"year": year, **summarise(group)} for year, group in df.groupby("year")]
    return pd.DataFrame(rows).round(3)


def build_monthly_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"year": year, "month": month, **summarise(group)}
        for (year, month), group in df.groupby(["year", "month"])
    ]
    return pd.DataFrame(rows).round(3)


def main() -> None:
    df = load_market_data(config.CONSUMPTION_COMBINED_FILE)
    yearly = build_yearly_table(df)
    monthly = build_monthly_table(df)

    print("SOLAR CAPTURE RATE BY YEAR")
    print(yearly.to_string(index=False))
    print("\nSOLAR CAPTURE RATE BY MONTH")
    print(monthly.to_string(index=False))

    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    yearly.to_csv(YEARLY_FILE, index=False)
    monthly.to_csv(MONTHLY_FILE, index=False)
    print(f"\nSaved: {YEARLY_FILE}\nSaved: {MONTHLY_FILE}")


if __name__ == "__main__":
    main()