"""Chart the share of negative-price hours by residual-load band.

Reads the band table written by analyze_residual_load.py and draws one bar
per band, labelled with the share and the number of negative-price hours.
The key-finding line is calculated from the data: the share of all
negative-price hours that happened with residual load below 10 GW.

Writes docs/negative_price_share_by_residual_load_2024_2025.png.

Run with: python -m gridsignal.plot_residual_load_bands
"""

import matplotlib.pyplot as plt
import pandas as pd

from gridsignal import config

INPUT_FILE = config.DOCS_DIR / "price_by_residual_load_band_2024_2025.csv"
OUTPUT_FILE = config.DOCS_DIR / "negative_price_share_by_residual_load_2024_2025.png"

LOW_BANDS = ["<= 0 GW", "0-5 GW", "5-10 GW"]


def main() -> None:
    bands = pd.read_csv(INPUT_FILE)

    low = bands[bands["residual_load_band"].isin(LOW_BANDS)]
    low_share = low["negative_hours"].sum() / bands["negative_hours"].sum() * 100

    fig, ax = plt.subplots(figsize=(11, 6.5))
    bars = ax.bar(
        range(len(bands)),
        bands["negative_share_pct"],
        color="#4776A8",
        width=0.65,
    )

    for bar, share, negative, hours in zip(
        bars,
        bands["negative_share_pct"],
        bands["negative_hours"],
        bands["hours"],
    ):
        ax.annotate(
            f"{share:.0f}%\n{negative:,} of {hours:,} hours",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xticks(range(len(bands)))
    ax.set_xticklabels(bands["residual_load_band"])

    ax.set_xlabel("Demand left for other power plants after wind and solar (GW), known as residual load")

    ax.set_ylabel("Share of hours in each band with a negative price (%)")
    ax.set_ylim(0, 115)
    ax.set_yticks(range(0, 101, 20))

    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title(
        "Negative Prices Happen When Wind and Solar Meet Nearly All Demand",
        loc="left",
        fontsize=17,
        fontweight="bold",
        pad=18,
    )
    ax.text(
        0,
        1.02,
        "Share of hours with a negative electricity price, by how much demand wind and solar leave uncovered, Germany 2024-2025",
        transform=ax.transAxes,
        fontsize=10,
        color="dimgray",
    )

    fig.text(
        0.01,
        0.055,
        f"KEY FINDING  |  {low_share:.0f}% of all negative-price hours happened when "
        "wind and solar left less than 10 GW of demand uncovered.",
        fontsize=9,
        fontweight="bold",
    )
    fig.text(
        0.01,
        0.015,
        "Source: SMARD, Germany/Luxembourg, German local time.",
        fontsize=8,
        color="dimgray",
    )

    fig.tight_layout(rect=[0, 0.10, 1, 0.95])
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()