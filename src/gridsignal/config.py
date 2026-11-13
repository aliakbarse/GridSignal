"""Shared paths and settings for the GridSignal pipeline.

Defines the project folders (data/raw, data/processed and docs), the
file names of the combined datasets, the local timezone (Europe/Berlin),
the years analysed and the MIN_NEGATIVE_HOURS threshold. Scripts import
these values so that each setting is defined in one place.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

COMBINED_FILE = PROCESSED_DIR / "germany_market_combined_2024_2025.csv"
CONSUMPTION_COMBINED_FILE = (
    PROCESSED_DIR / "germany_market_consumption_combined_2024_2025.csv"
)

TIMEZONE = "Europe/Berlin"
YEARS = (2024, 2025)
MIN_NEGATIVE_HOURS = 30