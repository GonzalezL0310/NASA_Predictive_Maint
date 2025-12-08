import pandas as pd


def add_rul_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Remaining Useful Life (RUL) for each record.
    Logic: RUL = Max(time_cycles) of the unit - current time_cycles.

    Args:
        df (pd.DataFrame): DataFrame with 'unit_nr' and 'time_cycles' columns.

    Returns:
        pd.DataFrame: DataFrame with the new 'RUL' column.
    """
    # Calculate max cycles per unit
    max_cycles = df.groupby('unit_nr')['time_cycles'].transform('max')

    # Direct pandas vectorization
    df['RUL'] = max_cycles - df['time_cycles']

    return df