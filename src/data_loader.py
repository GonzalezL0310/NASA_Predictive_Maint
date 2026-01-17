import shutil
import pandas as pd
import kagglehub
from pathlib import Path
from config.settings import ALL_COLUMNS, DATA_RAW_DIR


def download_dataset_if_missing(filename: str = "train_FD001.txt") -> Path:
    """
    Checks if the raw dataset exists locally. If not, downloads it using the Kaggle API
    and moves it to the defined raw data directory.

    Args:
        filename (str): The specific file to look for (default: train_FD001.txt).

    Returns:
        Path: The absolute path to the local raw file.
    """
    target_path = DATA_RAW_DIR / filename

    # 1. Check if file already exists to avoid re-downloading
    if target_path.exists():
        print(f"[INFO] Dataset found at {target_path}. Skipping download.")
        return target_path

    print("[INFO] Dataset not found locally. Downloading from KaggleHub...")

    # 2. Download latest version (Returns path to the cache folder)
    # Note: This specific dataset is public, so no API key is usually required for kagglehub.
    try:
        cache_path = kagglehub.dataset_download("palbha/cmapss-jet-engine-simulated-data")
    except Exception as e:
        print(f"[ERROR] Failed to connect to Kaggle: {e}")
        raise

    # 3. Locate the specific file in the downloaded folder
    downloaded_file = Path(cache_path) / filename

    if not downloaded_file.exists():
        raise FileNotFoundError(f"Downloaded folder {cache_path} does not contain {filename}")

    # 4. Move the file to our project structure (data/raw)
    # We ensure the directory exists just in case
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Moving file to project directory: {DATA_RAW_DIR}...")
    shutil.move(str(downloaded_file), str(target_path))

    print("[INFO] Download and setup complete.")
    return target_path


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
    df = pd.read_csv(
        file_path,
        sep=r'\s+',
        header=None,
        names=ALL_COLUMNS
    )

    return df
