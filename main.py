import sys
import pandas as pd
from config.settings import DATA_RAW_DIR, DATA_PROCESSED_DIR, SENSOR_COLS, WINDOW_SIZE
from src.data_loader import load_raw_data
from src.numerical_ops import apply_moving_average, calculate_slope
from src.feature_eng import add_rul_target


def main():
    print("[INFO] Starting Predictive Maintenance ETL Pipeline...")

    # 1. Define paths
    input_file = DATA_RAW_DIR / "train_FD001.txt"
    output_file = DATA_PROCESSED_DIR / "train_FD001_processed.csv"

    # 2. Loading
    try:
        print(f"[INFO] Loading data from {input_file}...")
        df = load_raw_data(input_file)
        print(f"[INFO] Data loaded. Shape: {df.shape}")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # 3. Numerical Ops (Cleaning and Feature Engineering)
    # Selecting some key sensors for the example (or all based on settings)
    sensors_to_process = ['s_2', 's_3', 's_4', 's_7', 's_11', 's_12']
    # Filter only those that exist in SENSOR_COLS to avoid errors
    target_sensors = [s for s in sensors_to_process if s in SENSOR_COLS]

    print(f"[INFO] Applying Moving Average (Window={WINDOW_SIZE})...")
    df = apply_moving_average(df, target_sensors, WINDOW_SIZE)

    print(f"[INFO] Calculating Degradation Slope (Vectorized)...")
    df = calculate_slope(df, target_sensors, WINDOW_SIZE)

    # 4. Feature Engineering (Target)
    print("[INFO] Generating RUL (Remaining Useful Life) target...")
    df = add_rul_target(df)

    # 5. Saving
    print(f"[INFO] Saving processed dataset to {output_file}...")
    df.to_csv(output_file, index=False)

    print("[INFO] Pipeline finished successfully.")


if __name__ == "__main__":
    main()