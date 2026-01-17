import sys
import pandas as pd
from config.settings import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    SENSOR_COLS,
    WINDOW_SIZE,
    SENSOR_MAP
)
from src.data_loader import load_raw_data, download_dataset_if_missing
from src.numerical_ops import apply_moving_average, calculate_slope
from src.feature_eng import add_rul_target, add_health_status
from src.metadata_gen import generate_sensor_metadata
from src.visualization import plot_sensor_trends


def main():
    print("[INFO] Starting Predictive Maintenance ETL Pipeline (BI Layer)...")

    # --- 1. METADATA GENERATION (DIMENSION TABLE) ---
    metadata_path = DATA_PROCESSED_DIR / "sensor_metadata.csv"
    generate_sensor_metadata(metadata_path)

    # --- 2. DATA INGESTION ---
    try:
        input_file = download_dataset_if_missing("train_FD001.txt")
        df = load_raw_data(input_file)
    except Exception as e:
        print(f"[ERROR] Setup failed: {e}")
        sys.exit(1)

    # --- 3. NUMERICAL PROCESSING (KERNEL) ---
    # We keep using raw IDs (s_2, s_3) here to maintain code stability
    sensors_to_process = ['s_2', 's_3', 's_4', 's_7', 's_11', 's_12', 's_15', 's_17', 's_20', 's_21']
    target_sensors = [s for s in sensors_to_process if s in SENSOR_COLS]

    print(f"[INFO] Applying Moving Average & Vectorized Slope (Window={WINDOW_SIZE})...")
    df = apply_moving_average(df, target_sensors, WINDOW_SIZE)
    df = calculate_slope(df, target_sensors, WINDOW_SIZE)

    # --- 4. FEATURE ENGINEERING ---
    print("[INFO] Calculating RUL and Health Status...")
    df = add_rul_target(df)
    df = add_health_status(df)

    # --- 5. RENAMING & PROJECTION (SERVING LAYER) ---
    print("[INFO] Renaming columns to Engineering Terms for BI...")

    # 5.1 Create a renaming dictionary
    # Map 's_x' -> 'Technical_Name'
    rename_dict = {k: v[0] for k, v in SENSOR_MAP.items()}

    # 5.2 Also map the generated columns (_ma and _slope)
    # Strategy: s_2_slope -> LPC_Outlet_Temp_Slope
    for s_id, (tech_name, _, _) in SENSOR_MAP.items():
        rename_dict[f"{s_id}_ma"] = f"{tech_name}_MA"
        rename_dict[f"{s_id}_slope"] = f"{tech_name}_Slope"

    # Apply renaming
    df_bi = df.rename(columns=rename_dict)

    # --- 6. EXPORT ---
    fact_table_path = DATA_PROCESSED_DIR / "engine_data.csv"
    print(f"[INFO] Exporting Fact Table to {fact_table_path}...")
    df_bi.to_csv(fact_table_path, index=False)
    
    print("[INFO] BI Data Preparation Complete.")
    print(f"   -> Dimension Table: {metadata_path}")
    print(f"   -> Fact Table:      {fact_table_path}")


if __name__ == "__main__":
    main()
