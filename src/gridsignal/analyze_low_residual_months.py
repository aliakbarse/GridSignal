"""Hours with low residual load, by month: how often is the price negative,
and what do neighbouring markets pay in those hours?"""

import pandas as pd

from gridsignal import config
from gridsignal.data_loader import load_market_data

RAW_PRICE_FILE = config.RAW_DIR / "Day-ahead_prices_202312312100_202512312100_Hour.csv"
OUTPUT_FILE = config.DOCS_DIR / "low_residual_hours_by_month_2024_2025.csv"

LOW_RESIDUAL_MWH = 10_000  # below 10 GW: wind and solar cover almost everything
MONTHS = range(4, 11)  # April-October


def load_neighbour_prices() -> pd.DataFrame:
    """Neighbours' average day-ahead price, keyed by UTC start time."""
    raw = pd.read_csv(
        RAW_PRICE_FILE, sep=";", na_values=["-"], encoding="utf-8-sig", thousands=","
    )
    de_col = next(c for c in raw.columns if c.startswith("Germany/Luxembourg"))
    nb_col = next(c for c in raw.columns if c.startswith("\u2205 DE/LU neighbours"))

    # Raw timestamps are German local time; the repeated autumn hour is inferred.
    raw["start_time_utc"] = (
        pd.to_datetime(raw["Start date"], format="%b %d, %Y %I:%M %p")
        .dt.tz_localize(config.TIMEZONE, ambiguous="infer", nonexistent="raise")
        .dt.tz_convert("UTC")
    )
    return raw.rename(
        columns={de_col: "price_raw", nb_col: "neighbours_avg_eur_mwh"}
    )[["start_time_utc", "price_raw", "neighbours_avg_eur_mwh"]]


def build_table(df: pd.DataFrame, neighbours: pd.DataFrame) -> pd.DataFrame:
    """Summarise low-residual-load hours by month and year."""
    merged = df.merge(neighbours, on="start_time_utc", how="left", validate="one_to_one")

    if merged["neighbours_avg_eur_mwh"].isna().any():
        raise ValueError("Neighbour prices are missing for some hours.")
    if (merged["price_eur_mwh"] - merged["price_raw"]).abs().max() != 0:
        raise ValueError("German prices do not match the raw file: check alignment.")

    low = merged[
        (merged["residual_load_mwh"] < LOW_RESIDUAL_MWH) & merged["month"].isin(MONTHS)
    ].copy()
    low["spread"] = low["neighbours_avg_eur_mwh"] - low["price_eur_mwh"]

    table = (
        low.groupby(["month", "year"])
        .agg(
            low_residual_hours=("price_eur_mwh", "size"),
            negative_hours=("is_negative_price", "sum"),
            de_median_eur_mwh=("price_eur_mwh", "median"),
            neighbours_median_eur_mwh=("neighbours_avg_eur_mwh", "median"),
            spread_median_eur_mwh=("spread", "median"),
        )
        .reset_index()
    )
    table["negative_share_pct"] = (
        table["negative_hours"] / table["low_residual_hours"] * 100
    )
    return table.round(1)[
        [
            "month", "year", "low_residual_hours", "negative_hours",
            "negative_share_pct", "de_median_eur_mwh",
            "neighbours_median_eur_mwh", "spread_median_eur_mwh",
        ]
    ]


def main() -> None:
    df = load_market_data(config.CONSUMPTION_COMBINED_FILE)
    table = build_table(df, load_neighbour_prices())

    print("HOURS WITH RESIDUAL LOAD BELOW 10 GW, APRIL-OCTOBER")
    print(table.to_string(index=False))

    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()