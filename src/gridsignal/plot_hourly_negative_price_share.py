
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "docs"
    / "hourly_negative_price_share_2024_2025.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "docs"
    / "hourly_negative_price_share_2024_2025.png"
)


def main():
    df = pd.read_csv(INPUT_FILE)

    # Validate the expected years.
    expected_years = {2024, 2025}
    actual_years = set(df["year"].unique())

    if actual_years != expected_years:
        raise ValueError(
            f"Expected years {expected_years}, "
            f"but found {actual_years}"
        )

    # Validate hourly coverage.
    if df.duplicated(["year", "hour"]).any():
        raise ValueError(
            "Duplicate year-hour combinations found."
        )

    if not df["hour"].between(0, 23).all():
        raise ValueError(
            "Hour values must be between 0 and 23."
        )

    # Plot each year separately.
    fig, ax = plt.subplots(figsize=(11, 6))

    for year in [2024, 2025]:
        yearly = (
            df[df["year"] == year]
            .sort_values("hour")
        )

        ax.plot(
            yearly["hour"],
            yearly["negative_price_share_pct"],
            marker="o",
            markersize=4,
            linewidth=2,
            label=str(year),
        )

    ax.set_title(
        "Hourly Negative-Price Rate in Germany "
        "(2024 vs. 2025)"
    )

    ax.set_xlabel("Hour of Day (UTC)")
    ax.set_ylabel("Negative-Price Observations (%)")

    ax.set_xticks(range(24))
    ax.set_xlim(0, 23)
    ax.set_ylim(bottom=0)

    ax.grid(True, alpha=0.3)
    ax.legend(title="Year")

    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fig.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Chart saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
