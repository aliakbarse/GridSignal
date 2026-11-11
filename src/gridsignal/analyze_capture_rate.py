"""Solar capture rate: what solar earns per MWh compared with the average price.

capture rate = generation-weighted average price / simple average price
A value below 1 means solar produces when prices are lower than average.
"""

import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

OUTPUT_FILE = config.DOCS_DIR / "solar_capture_rate_2024_2025.csv"


def build_table(df: pd.DataFrame) -> pd.DataFrame:
    """Capture rate and related figures by year."""
    rows = []
    for year, group in df.groupby("year"):
        solar = group["solar_mwh"]
        price = group["price_eur_mwh"]
        weighted_price = (price * solar).sum() / solar.sum()
        solar_at_negative = solar[group["is_negative_price"]].sum()
        rows.append(
            {
                "year": year,
                "average_price_eur_mwh": price.mean(),
                "solar_weighted_price_eur_mwh": weighted_price,
                "capture_rate": weighted_price / price.mean(),
                "solar_share_at_negative_prices_pct": solar_at_negative / solar.sum() * 100,
            }
        )
    return pd.DataFrame(rows).round(3)


def main() -> None:
    df = load_market_data(config.CONSUMPTION_COMBINED_FILE)
    table = build_table(df)

    print("SOLAR CAPTURE RATE")
    print(table.to_string(index=False))

    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()