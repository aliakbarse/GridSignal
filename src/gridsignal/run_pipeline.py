"""Run the whole GridSignal workflow in order.

The stages are: clean prices and generation, combine them, add
consumption, run the analyses and draw the charts. Each stage is a module
in this package with a main() function. The script imports each one in
turn, runs it and prints how long it took. An error in any stage stops the
run.

Run with: python -m gridsignal.run_pipeline
"""

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