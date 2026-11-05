import matplotlib.pyplot as plt
import pandas as pd

from gridsignal import config

FREQUENCY_FILE = config.DOCS_DIR / "hourly_negative_price_frequency_2024_2025.csv"
SOLAR_FILE = config.DOCS_DIR / "hourly_solar_by_price_category_2024_2025.csv"
OUTPUT_FILE = config.DOCS_DIR / "hour_of_day_analysis_2024_2025.png"

MIDDAY_HOURS = range(10, 17)  # 10:00-16:59 German local time
MIN_HOURS = 30  # fewer negative-price hours than this = flagged as a small sample
ALL_HOURS = range(24)

COLORS = {
    "2024": "#4776A8",
    "2025": "#D97736",
    "Negative price": "#C65353",
    "Nonnegative price": "#4776A8",
}
LABELS = {
    "Negative price": "Negative-price hours",
    "Nonnegative price": "Other hours",
}

# Peak labels sit in empty space beside each curve, not on top of it.
PEAK_LABEL_OFFSETS = {2024: (105, 6), 2025: (-60, 8)}
PEAK_LABEL_ALIGN = {2024: "left", 2025: "right"}

REQUIRED_FREQUENCY = {
    "year", "hour", "observed_hours",
    "negative_price_hours", "negative_price_rate_pct",
}
REQUIRED_SOLAR = {
    "year", "hour", "price_category", "observed_hours", "average_solar_mwh",
}


def load_data():
    """Load and validate the outputs of analyze_hour_of_day.py."""
    for path in (FREQUENCY_FILE, SOLAR_FILE):
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found: {path}\n"
                "Run analyze_hour_of_day.py first."
            )

    frequency = pd.read_csv(FREQUENCY_FILE)
    solar = pd.read_csv(SOLAR_FILE)

    for name, table, required in (
        ("Frequency", frequency, REQUIRED_FREQUENCY),
        ("Solar", solar, REQUIRED_SOLAR),
    ):
        missing = required - set(table.columns)
        if missing:
            raise ValueError(f"{name} file is missing columns: {sorted(missing)}")

    return frequency, solar


def midday_share(frequency):
    """Share of all negative-price hours that fall in the midday window."""
    total = frequency["negative_price_hours"].sum()
    midday = frequency.loc[
        frequency["hour"].isin(MIDDAY_HOURS), "negative_price_hours"
    ].sum()
    return midday / total * 100


def style_axis(ax):
    """Apply consistent styling to a chart axis."""
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{hour:02d}:00" for hour in range(0, 24, 2)])
    ax.grid(axis="y", alpha=0.25, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_frequency(ax, frequency):
    """Plot the share of hours with a negative price, by hour of day."""
    years = sorted(frequency["year"].unique())

    for year in years:
        year_data = frequency[frequency["year"] == year].sort_values("hour")
        ax.plot(
            year_data["hour"],
            year_data["negative_price_rate_pct"],
            color=COLORS[str(year)],
            linewidth=2.4,
            marker="o",
            markersize=4,
            label=str(year),
        )

    # Mark the highest observed rate in each year (computed from the data).
    for year in years:
        year_data = frequency[frequency["year"] == year]
        peak = year_data.loc[year_data["negative_price_rate_pct"].idxmax()]
        ax.annotate(
            f"{int(year)} peak\n"
            f"{int(peak['hour']):02d}:00 - {peak['negative_price_rate_pct']:.0f}%",
            xy=(peak["hour"], peak["negative_price_rate_pct"]),
            xytext=PEAK_LABEL_OFFSETS.get(int(year), (0, 12)),
            textcoords="offset points",
            color=COLORS[str(year)],
            fontsize=9,
            ha=PEAK_LABEL_ALIGN.get(int(year), "center"),
            va="center",
            arrowprops={
                "arrowstyle": "-",
                "color": COLORS[str(year)],
                "alpha": 0.7,
                "linewidth": 0.8,
            },
        )

    ax.set_title(
        "A. How often is the price negative, hour by hour?",
        loc="left",
        fontweight="bold",
        pad=12,
    )
    ax.set_ylabel("Share of hours with a negative price (%)")
    ax.set_ylim(0, frequency["negative_price_rate_pct"].max() * 1.2)
    ax.legend(frameon=False, ncol=2, loc="upper left")
    style_axis(ax)


def plot_solar_year(ax, solar, year, letter):
    """Compare solar output in negative-price and other hours for one year."""
    year_data = solar[solar["year"] == year]

    for category in ("Nonnegative price", "Negative price"):
        # Reindex to all 24 hours so an hour with no observations becomes a
        # gap in the line instead of a straight line drawn across it.
        category_data = (
            year_data[year_data["price_category"] == category]
            .set_index("hour")
            .reindex(ALL_HOURS)
        )
        ax.plot(
            category_data.index,
            category_data["average_solar_mwh"] / 1000,  # MWh per hour -> GW
            color=COLORS[category],
            linewidth=2.3,
            marker="o",
            markersize=3.5,
            label=LABELS[category],
        )

    # Overnight negative-price averages rest on very few hours; flag them
    # instead of hiding the uncertainty.
    negative = year_data[year_data["price_category"] == "Negative price"]
    sparse = negative[negative["observed_hours"] < MIN_HOURS]
    if not sparse.empty:
        ax.scatter(
            sparse["hour"],
            sparse["average_solar_mwh"] / 1000,
            s=48,
            facecolors="none",
            edgecolors=COLORS["Negative price"],
            linewidths=1.3,
            zorder=5,
            label=f"Fewer than {MIN_HOURS} negative-price hours",
        )

    ax.set_title(
        f"{letter}. Average solar output by hour - {year}",
        loc="left",
        fontweight="bold",
        pad=12,
    )
    ax.set_ylabel("Average solar output (GW)")
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    style_axis(ax)


def main():
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    frequency, solar = load_data()
    share = midday_share(frequency)

    fig = plt.figure(figsize=(15, 11), layout="constrained")
    grid = fig.add_gridspec(nrows=2, ncols=2, height_ratios=[1, 1.15])

    ax_frequency = fig.add_subplot(grid[0, :])
    ax_solar_2024 = fig.add_subplot(grid[1, 0])
    ax_solar_2025 = fig.add_subplot(grid[1, 1])

    plot_frequency(ax_frequency, frequency)
    plot_solar_year(ax_solar_2024, solar, 2024, "B")
    plot_solar_year(ax_solar_2025, solar, 2025, "C")

    fig.suptitle(
        f"{share:.0f}% of negative-price hours fell between 10:00 and 17:00",
        fontsize=17,
        fontweight="bold",
    )

    fig.text(
        0.5,
        -0.045,
        "Source: SMARD, Germany/Luxembourg day-ahead prices, German local time. "
        "From 1 Oct 2025, hourly values average four 15-minute prices.\n"
        "Negative = below 0 EUR/MWh. Solar averages are descriptive, not causal, "
        "and seasons are not controlled in panels B and C.",
        ha="center",
        fontsize=9,
    )

    fig.savefig(OUTPUT_FILE, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Visualization saved: {OUTPUT_FILE}")
    print(f"Midday share of negative-price hours: {share:.1f}%")


if __name__ == "__main__":
    main()