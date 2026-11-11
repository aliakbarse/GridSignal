"""Load the combined hourly market data into the PostgreSQL table market_hours.

Connection settings come from the standard PostgreSQL environment variables
(PGHOST, PGUSER, PGPASSWORD, PGDATABASE), so no password is stored in the code.
The load replaces the table contents, so running it twice gives the same result.
"""

import os

import psycopg

from gridsignal import config
from gridsignal.data_loader import load_market_data

COLUMNS = [
    "start_time_utc",
    "price_eur_mwh",
    "wind_offshore_mwh",
    "wind_onshore_mwh",
    "solar_mwh",
    "grid_load_mwh",
    "residual_load_mwh",
]


def connect() -> psycopg.Connection:
    return psycopg.connect(
        dbname=os.environ.get("PGDATABASE", "gridsignal"),
        user=os.environ.get("PGUSER", "postgres"),
        host=os.environ.get("PGHOST", "localhost"),
    )


def main() -> None:
    df = load_market_data(config.CONSUMPTION_COMBINED_FILE)
    records = [
        (row.start_time_utc.to_pydatetime(), *(float(getattr(row, c)) for c in COLUMNS[1:]))
        for row in df[COLUMNS].itertuples(index=False)
    ]

    # One transaction: either the whole load succeeds or nothing changes.
    with connect() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE market_hours")
        # COPY sends all rows in one stream; much faster than one INSERT per row.
        with cur.copy(f"COPY market_hours ({', '.join(COLUMNS)}) FROM STDIN") as copy:
            for record in records:
                copy.write_row(record)

        cur.execute(
            "SELECT count(*), count(*) FILTER (WHERE is_negative_price), "
            "min(start_time_utc), max(start_time_utc) FROM market_hours"
        )
        rows, negative, first, last = cur.fetchone()

    print(f"Loaded {rows} rows ({first} to {last}); negative-price hours: {negative}")


if __name__ == "__main__":
    main()