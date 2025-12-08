import pandas as pd
from pathlib import Path
from config.settings import SENSOR_MAP


def generate_sensor_metadata(output_path: Path) -> None:
    """
    Generates a Dimension Table (CSV) for sensor metadata based on SENSOR_MAP.

    Structure:
    - Sensor_ID: Original ID (e.g., s_2)
    - Technical_Name: Physics-based name (e.g., LPC_Outlet_Temp)
    - Unit: Unit of measurement (e.g., R, psia)
    - Component: Engine subsystem (e.g., LPC, Fan)

    Args:
        output_path (Path): Destination path for the CSV file.
    """
    print("[INFO] Generating Sensor Metadata Dimension Table...")

    # Transform dictionary to list of dicts for DataFrame creation
    data = []
    for sensor_id, attributes in SENSOR_MAP.items():
        tech_name, unit, component = attributes
        data.append({
            "Sensor_ID": sensor_id,
            "Technical_Name": tech_name,
            "Unit": unit,
            "Component": component
        })

    df_meta = pd.DataFrame(data)

    # Save to CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_meta.to_csv(output_path, index=False)
    print(f"[INFO] Metadata saved to {output_path}")