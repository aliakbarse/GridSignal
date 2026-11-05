import importlib
import time

STAGES = [
    "clean_data",
    "clean_generation",
    "combine_data",
    "prepare_consumption_data",
    "analyze_prices",
    "analyze_generation_by_price",
    "analyze_monthly_generation",
    "analyze_solar_consistency",
    "analyze_solar_controls",
    "analyze_residual_load",
    "analyze_hour_of_day",
    "analyze_negative_price_hours",
    "analyze_demand_price",
    "plot_negative_price_frequency",
    "plot_negative_price_severity",
    "plot_monthly_solar_comparison",
    "plot_hour_of_day_analysis",
]


def main() -> None:
    for name in STAGES:
        print(f"\n=== {name} ===")
        start = time.perf_counter()
        module = importlib.import_module(f"gridsignal.{name}")
        module.main()
        print(f"[ok] {name} ({time.perf_counter() - start:.1f}s)")

    print("\nPipeline finished.")


if __name__ == "__main__":
    main()