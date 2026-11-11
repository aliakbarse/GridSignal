import importlib
import time

STAGES = [
    "clean_data",
    "clean_generation",
    "combine_data",
    "prepare_consumption_data",
    "analyze_solar_controls",
    "analyze_residual_load",
    "analyze_low_residual_months",
    "analyze_capture_rate",
    "analyze_hour_of_day",
    "analyze_negative_price_hours",
    "plot_negative_price_frequency",
    "plot_negative_price_severity",
    "plot_residual_load_bands",
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