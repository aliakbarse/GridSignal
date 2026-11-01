
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "germany_market_combined_2024_2025.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "docs"
    / "hourly_renewables_by_price_category_2024_2025.csv"
)

MINIMUM_NEGATIVE_PRICE_HOURS = 30

REQUIRED_COLUMNS = [
    "start_time_utc",
    "price_eur_mwh",
    "solar_mwh",
    "wind_total_mwh",
]

GENERATION_COLUMNS = [
    "solar_mwh",
    "wind_total_mwh",
]


def load_data() -> pd.DataFrame:
    """Load and validate hourly renewable generation and price data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            "Run the data pipeline first."
        )

    data = pd.read_csv(INPUT_FILE)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    data = data[REQUIRED_COLUMNS].copy()

    data["start_time_utc"] = pd.to_datetime(
        data["start_time_utc"],
        utc=True,
        errors="coerce",
    )

    numeric_columns = [
        "price_eur_mwh",
        *GENERATION_COLUMNS,
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    original_rows = len(data)

    invalid_timestamp = data["start_time_utc"].isna()

    invalid_price = (
        data["price_eur_mwh"].isna()
        | ~data["price_eur_mwh"].map(
            lambda value: pd.notna(value)
        )
    )

    invalid_solar = (
        data["solar_mwh"].isna()
        | data["solar_mwh"].lt(0)
    )

    invalid_wind = (
        data["wind_total_mwh"].isna()
        | data["wind_total_mwh"].lt(0)
    )

    invalid_rows = (
        invalid_timestamp
        | invalid_price
        | invalid_solar
        | invalid_wind
    )

    invalid_row_count = int(invalid_rows.sum())

    data = data.loc[~invalid_rows].copy()

    data["start_time_local"] = (
        data["start_time_utc"]
        .dt.tz_convert("Europe/Berlin")
    )

    data["year"] = data["start_time_local"].dt.year
    data["hour"] = data["start_time_local"].dt.hour

    data = data[
        data["year"].isin([2024, 2025])
    ].copy()

    data["combined_renewables_mwh"] = (
        data["solar_mwh"]
        + data["wind_total_mwh"]
    )

    data["price_category"] = (
        data["price_eur_mwh"]
        .lt(0)
        .map(
            {
                True: "Negative price",
                False: "Nonnegative price",
            }
        )
    )

    print(f"Original records: {original_rows:,}")
    print(f"Excluded invalid records: {invalid_row_count:,}")
    print(f"Valid records retained: {len(data):,}")
    print(f"Years covered: {sorted(data['year'].unique().tolist())}")

    return data


def analyze_renewables_by_hour(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Compare solar, wind, and combined generation by hour and price."""

    summary = (
        data.groupby(
            ["year", "hour", "price_category"],
            observed=True,
        )
        .agg(
            observed_hours=("combined_renewables_mwh", "size"),
            average_solar_mwh=("solar_mwh", "mean"),
            average_wind_mwh=("wind_total_mwh", "mean"),
            average_combined_mwh=(
                "combined_renewables_mwh",
                "mean",
            ),
            median_combined_mwh=(
                "combined_renewables_mwh",
                "median",
            ),
        )
        .reset_index()
    )

    results = []

    for year in sorted(data["year"].unique()):
        for hour in range(24):
            hour_data = summary[
                (summary["year"] == year)
                & (summary["hour"] == hour)
            ]

            negative = hour_data[
                hour_data["price_category"] == "Negative price"
            ]

            nonnegative = hour_data[
                hour_data["price_category"] == "Nonnegative price"
            ]

            negative_row = (
                negative.iloc[0]
                if not negative.empty
                else None
            )

            nonnegative_row = (
                nonnegative.iloc[0]
                if not nonnegative.empty
                else None
            )

            negative_hours = (
                int(negative_row["observed_hours"])
                if negative_row is not None
                else 0
            )

            nonnegative_hours = (
                int(nonnegative_row["observed_hours"])
                if nonnegative_row is not None
                else 0
            )

            if negative_hours == 0:
                comparison_status = (
                    "No negative-price observations"
                )

            elif nonnegative_hours == 0:
                comparison_status = (
                    "No nonnegative-price observations"
                )

            elif (
                negative_hours
                < MINIMUM_NEGATIVE_PRICE_HOURS
            ):
                comparison_status = (
                    "Below minimum negative-price sample"
                )

            else:
                comparison_status = (
                    "Meets minimum negative-price sample"
                )

            meets_minimum_sample = (
                negative_hours
                >= MINIMUM_NEGATIVE_PRICE_HOURS
                and nonnegative_hours > 0
            )

            result = {
                "year": year,
                "hour": hour,
                "negative_price_hours": negative_hours,
                "nonnegative_price_hours": nonnegative_hours,
                "comparison_status": comparison_status,
                "meets_minimum_sample": meets_minimum_sample,
                "minimum_negative_price_hours_required": (
                    MINIMUM_NEGATIVE_PRICE_HOURS
                ),
            }

            metrics = [
                "average_solar_mwh",
                "average_wind_mwh",
                "average_combined_mwh",
                "median_combined_mwh",
            ]

            for metric in metrics:
                negative_value = (
                    negative_row[metric]
                    if negative_row is not None
                    else float("nan")
                )

                nonnegative_value = (
                    nonnegative_row[metric]
                    if nonnegative_row is not None
                    else float("nan")
                )

                result[
                    f"{metric}_negative_price"
                ] = negative_value

                result[
                    f"{metric}_nonnegative_price"
                ] = nonnegative_value

                result[
                    f"{metric}_difference"
                ] = (
                    negative_value - nonnegative_value
                )

            results.append(result)

    results_df = pd.DataFrame(results)

    return results_df.sort_values(
        ["year", "hour"]
    ).reset_index(drop=True)


def print_summary(results: pd.DataFrame) -> None:
    """Print hourly renewable-generation comparison results."""

    print("\nHOURLY RENEWABLE GENERATION BY PRICE CATEGORY")

    display_columns = [
        "year",
        "hour",
        "negative_price_hours",
        "nonnegative_price_hours",
        "comparison_status",
        "meets_minimum_sample",
        "average_solar_mwh_difference",
        "average_wind_mwh_difference",
        "average_combined_mwh_difference",
    ]

    display = results[display_columns].copy()

    print(
        display.to_string(
            index=False,
            na_rep="N/A",
            float_format=lambda value: f"{value:,.2f}",
        )
    )

    print("\nSAMPLE QUALIFICATION SUMMARY")

    for year in sorted(results["year"].unique()):
        year_data = results[
            results["year"] == year
        ]

        eligible = year_data[
            year_data["meets_minimum_sample"]
        ]

        below_threshold = year_data[
            year_data["comparison_status"]
            == "Below minimum negative-price sample"
        ]

        no_negative = year_data[
            year_data["comparison_status"]
            == "No negative-price observations"
        ]

        no_nonnegative = year_data[
            year_data["comparison_status"]
            == "No nonnegative-price observations"
        ]

        print(f"\n{year}")
        print(
            f"Hourly groups meeting threshold: "
            f"{len(eligible)}"
        )
        print(
            f"Hourly groups below threshold: "
            f"{len(below_threshold)}"
        )
        print(
            f"Hourly groups with no negative-price observations: "
            f"{len(no_negative)}"
        )
        print(
            f"Hourly groups with no nonnegative-price observations: "
            f"{len(no_nonnegative)}"
        )

    print("\nYEARLY SUMMARY")

    for year in sorted(results["year"].unique()):
        year_data = results[
            results["year"] == year
        ]

        eligible = year_data[
            year_data["meets_minimum_sample"]
        ]

        print(f"\n{year}")

        if eligible.empty:
            print(
                "No hourly groups meet the minimum sample "
                "requirement."
            )
            continue

        for metric in [
            "average_solar_mwh",
            "average_wind_mwh",
            "average_combined_mwh",
        ]:
            difference_column = f"{metric}_difference"

            valid = eligible[
                eligible[difference_column].notna()
            ]

            if valid.empty:
                print(
                    f"{metric}: no eligible hourly comparisons"
                )
                continue

            positive_count = int(
                valid[difference_column].gt(0).sum()
            )

            negative_count = int(
                valid[difference_column].lt(0).sum()
            )

            zero_count = int(
                valid[difference_column].eq(0).sum()
            )

            print(
                f"{metric}: positive differences = "
                f"{positive_count}, negative differences = "
                f"{negative_count}, zero differences = "
                f"{zero_count}"
            )

    print(
        "\nInterpretation: Positive differences mean average "
        "generation was higher during negative-price observations. "
        "Negative differences mean it was lower. "
        "The sample threshold is a practical screening rule; "
        "it does not establish statistical significance or causation."
    )


def main() -> None:
    data = load_data()

    results = analyze_renewables_by_hour(data)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(f"\nResults saved to: {OUTPUT_FILE}")

    print_summary(results)

    print(
        "\nCombined renewable hourly analysis "
        "completed successfully."
    )


if __name__ == "__main__":
    main()
