import pandas as pd
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def apply_moving_average(df: pd.DataFrame, columns: list, window: int) -> pd.DataFrame:
    """
    Applies moving average smoothing to the specified columns.

    Args:
        df (pd.DataFrame): Original DataFrame.
        columns (list): List of column names to smooth.
        window (int): Size of the moving window.

    Returns:
        pd.DataFrame: DataFrame with smoothed columns (suffix _ma).
    """
    # GroupBy 'unit_nr' is vital to avoid mixing data from different engines
    # when calculating the mean at the boundaries.
    df_ma = df.copy()
    for col in columns:
        df_ma[f'{col}_ma'] = df.groupby('unit_nr')[col].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
    return df_ma


def _vectorized_slope_1d(series: np.ndarray, window: int) -> np.ndarray:
    """
    Calculates linear regression slope (least squares) vectorially.

    Math: m = (N*sum(xy) - sum(x)*sum(y)) / (N*sum(x^2) - (sum(x))^2)
    Where x is constant [0, 1, ..., window-1].
    """
    # Create a sliding window view (N_samples, window).
    # This does not copy memory; it's a view, making it highly efficient.
    shape = series.shape[:-1] + (series.shape[-1] - window + 1, window)
    strides = series.strides + (series.strides[-1],)
    windows = np.lib.stride_tricks.as_strided(series, shape=shape, strides=strides)

    # X-axis is always relative time within the window: [0, 1, 2, ..., w-1]
    x = np.arange(window)

    # Pre-calculation of X constants
    sum_x = np.sum(x)
    sum_x2 = np.sum(x ** 2)
    N = window
    denom = N * sum_x2 - sum_x ** 2

    if denom == 0:
        return np.zeros(windows.shape[0])  # Avoid division by zero if window=1

    # Calculations on Y (sensor data)
    # sum(y) for each window -> axis 1
    sum_y = np.sum(windows, axis=1)
    # sum(xy) -> dot product of each window with x
    sum_xy = np.dot(windows, x)

    # Slope formula
    slope = (N * sum_xy - sum_x * sum_y) / denom

    # Pad the first (window-1) values with NaN to align with original index
    pad = np.full(window - 1, np.nan)
    return np.concatenate([pad, slope])


def calculate_slope(df: pd.DataFrame, columns: list, window: int) -> pd.DataFrame:
    """
    Applies vectorized slope calculation grouping by unit.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        columns (list): Columns on which to calculate the trend.
        window (int): Size of the window.

    Returns:
        pd.DataFrame: Original DataFrame plus slope columns (suffix _slope).
    """
    df_res = df.copy()

    # Iterate by column, but the internal calculation is vectorized by unit block
    for col in columns:
        # Apply custom numpy function to each group
        df_res[f'{col}_slope'] = df_res.groupby('unit_nr')[col].transform(
            lambda x: _vectorized_slope_1d(x.values, window)
        )

    return df_res