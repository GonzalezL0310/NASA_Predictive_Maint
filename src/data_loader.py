import pandas as pd
from pathlib import Path
from typing import List
from config.settings import ALL_COLUMNS


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """
    Loads the raw CMAPSS dataset from a text file.

    Args:
        file_path (Path): Absolute or relative path to the .txt file.

    Returns:
        pd.DataFrame: DataFrame with correctly named columns.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")

    # The CMAPSS dataset uses spaces as separators and lacks a header.
    # engine='c' is faster, but 'python' is more robust with complex separators.
    # We use '\s+' regex to handle multiple spaces.
    df = pd.read_csv(
        file_path,
        sep=r'\s+',
        header=None,
        names=ALL_COLUMNS
    )

    return df