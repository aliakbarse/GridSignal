import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

OUTPUT_FILE = config.DOCS_DIR / "price_by_residual_load_band_2024_2025.csv"

# Fixed bands in MWh per hour (about MW). Edges are meaningful thresholds,
# unlike quintiles, whose edges depend on this particular dataset.
BIN_EDGES = [float("-inf"), 0, 5_000, 10_000, 15_000, 20_000, 30_000, float("inf")]
BIN_LABELS = [
    "<= 0 GW", "0-5 GW", "5-10 GW", "10-15 GW",
    "15-20 GW", "20-30 GW", "> 30 GW",
]


def build_bands(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise prices by fixed residual-load band."""
    df = df.copy()
    df["residual_load_band"] = pd.cut(
        df["residual_load_mwh"], bins=BIN_EDGES, labels=BIN_LABELS
    )

    table = (
        df.groupby("residual_load_band", observed=True)
        .agg(
            hours=("price_eur_mwh", "size"),
            negative_hours=("is_negative_price", "sum"),
            avg_price_eur_mwh=("price_eur_mwh", "mean"),
            median_price_eur_mwh=("price_eur_mwh", "median"),
        )
        .reset_index()
    )
    table["negative_share_pct"] = table["negative_hours"] / table["hours"] * 100
    return table


def main() -> None:
    df = load_market_data(config.CONSUMPTION_COMBINED_FILE)
    table = build_bands(df)

    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_FILE, index=False)

    print(table.round(1).to_string(index=False))
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()