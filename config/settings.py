import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

# CMAPSS Dataset Configuration
# We define columns manually because the original txt file has no header.
INDEX_COLS = ['unit_nr', 'time_cycles']
SETTING_COLS = ['setting_1', 'setting_2', 'setting_3']
SENSOR_COLS = [f's_{i}' for i in range(1, 22)]

ALL_COLUMNS = INDEX_COLS + SETTING_COLS + SENSOR_COLS

# Processing Parameters
WINDOW_SIZE = 5  # Window size for moving averages and slope calculation