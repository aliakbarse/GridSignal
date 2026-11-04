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