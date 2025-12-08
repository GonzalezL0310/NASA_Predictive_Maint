import pandas as pd
import numpy as np


def add_rul_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Remaining Useful Life (RUL) for each record.
    Logic: RUL = Max(time_cycles) of the unit - current time_cycles.
    """
    max_cycles = df.groupby('unit_nr')['time_cycles'].transform('max')
    df['RUL'] = max_cycles - df['time_cycles']
    return df


def add_health_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a categorical 'Health_Status' label based on RUL.

    Business Logic:
    - RUL > 75: Healthy (Green)
    - 25 < RUL <= 75: Warning (Yellow)
    - RUL <= 25: Critical (Red)

    Args:
        df (pd.DataFrame): DataFrame containing 'RUL' column.

    Returns:
        df (pd.DataFrame): DataFrame with 'Health_Status' column.
    """
    # Bin definitions: (-inf, 25], (25, 75], (75, +inf)
    bins = [-np.inf, 25, 75, np.inf]
    labels = ['Critical', 'Warning', 'Healthy']

    df['Health_Status'] = pd.cut(df['RUL'], bins=bins, labels=labels)

    return df