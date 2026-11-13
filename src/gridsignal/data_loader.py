"""Load the combined hourly dataset for the analysis scripts.

Every analysis and plotting script reads the data through
load_market_data(). It parses the UTC timestamps, converts them to German
local time, adds year, month, hour and is_negative_price columns, keeps
the analysed years and returns the rows sorted by time.
"""

from pathlib import Path

import pandas as pd

from gridsignal import config


def load_market_data(path: Path = config.COMBINED_FILE) -> pd.DataFrame:
    """Load the combined market dataset with consistent time fields.

    All calendar fields (year, month, hour) come from UTC timestamps
    converted to German local time, so daylight-saving changes are handled
    in one place.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Run the data pipeline first."
        )

    df = pd.read_csv(path)

    df["start_time_utc"] = pd.to_datetime(
        df["start_time_utc"], utc=True, errors="raise"
    )
    local = df["start_time_utc"].dt.tz_convert(config.TIMEZONE)

    df["start_time_local"] = local
    df["year"] = local.dt.year
    df["month"] = local.dt.month
    df["hour"] = local.dt.hour
    df["is_negative_price"] = df["price_eur_mwh"] < 0

    df = df[df["year"].isin(config.YEARS)]
    return df.sort_values("start_time_utc").reset_index(drop=True)