import sys
import pandas as pd
from config.settings import DATA_RAW_DIR, DATA_PROCESSED_DIR, SENSOR_COLS, WINDOW_SIZE
from src.data_loader import load_raw_data, download_dataset_if_missing
from src.numerical_ops import apply_moving_average, calculate_slope
from src.feature_eng import add_rul_target
from src.visualization import plot_sensor_trends
from config.settings import BASE_DIR

def main():
    print("[INFO] Starting Predictive Maintenance ETL Pipeline...")

    # 1. Data Ingestion (Auto-Download logic)
    # We ask the data loader to ensure the file is there.
    try:
        input_file = download_dataset_if_missing("train_FD001.txt")
        output_file = DATA_PROCESSED_DIR / "train_FD001_processed.csv"
    except Exception as e:
        print(f"[ERROR] Failed to download or locate dataset: {e}")
        sys.exit(1)

    # 2. Loading
    try:
        print(f"[INFO] Loading data from {input_file}...")
        df = load_raw_data(input_file)
        print(f"[INFO] Data loaded. Shape: {df.shape}")
    except FileNotFoundError as e:
        # This catch is double-check, though step 1 should handle it.
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

    # 6. Visualization Reporting
    print("[INFO] Generating visual reports...")

    # Define report directory
    reports_dir = BASE_DIR / "reports" / "figures"

    # We choose Unit 1 as a sample for the portfolio
    sample_unit = 1
    sample_sensors = ['s_2', 's_4', 's_7', 's_11']  # Sensores con alta correlación a fallas

    plot_path = reports_dir / f"unit_{sample_unit}_analysis.png"

    # Verificamos que las columnas existan antes de graficar
    # (El código de plot maneja internamente si falta alguna, pero es buena práctica)
    plot_sensor_trends(df, unit_nr=sample_unit, sensors=sample_sensors, save_path=plot_path)

    print("[INFO] Pipeline finished successfully.")

if __name__ == "__main__":
    main()