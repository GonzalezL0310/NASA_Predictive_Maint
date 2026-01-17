# NASA CMAPSS Predictive Maintenance ETL

This project implements a high-performance ETL pipeline designed for engine degradation analysis, utilizing the NASA CMAPSS Turbofan Jet Engine dataset (FD001). The architecture is grounded in the damage propagation models described by Saxena et al. (2008), focusing on vectorized feature engineering to prepare data for Business Intelligence (BI) and prognostic modeling.

## Tech Stack
- **Language:** Python 3.9+.
- **Numerical Processing:** NumPy (Vectorized Linear Regression via Stride Tricks), Pandas.
- **Data Ingestion:** KaggleHub API.
- **Visualization:** Matplotlib.

## Key Features
- **Vectorized Numerical Core:** Implements O(1) complexity slope calculations using `numpy.lib.stride_tricks`, avoiding slow iterative loops for degradation trend analysis.
- **Automated Data Lifecycle:** Self-healing ingestion that detects, downloads, and structures raw telemetery data automatically.
- **Engineering-Ready Output:** Transforms generic sensor IDs into physically validated engineering terms (e.g., Pressure, Temperature, Speed) and generates dedicated Fact and Dimension tables.
- **Predictive Labeling:** Calculates Remaining Useful Life (RUL) and categorical Health Status (Healthy, Warning, Critical) based on cycle thresholds.

## Setup & Execution

### 1. Environment Preparation
Ensure your Linux-based system has Python 3 installed. Clone the repository and prepare the script permissions.

```bash
# Clone the repository
git clone <your-repository-url>
cd NASA_Predictive_Maint

# Grant execution permissions to the setup script
chmod +x setup.sh
```

### 2. Automated Installation
The provided setup script automates the installation of system dependencies, creates a Python virtual environment, and installs all required libraries.

```bash
./setup.sh
```

### 3.Running the Pipeline
The orchestrator handles the full ETL process, from metadata generation to the final export of processed fact tables.

```Bash
# Activate the environment
source venv/bin/activate

# Execute the ETL orchestrator
python main.py
```

## Data Architecture

Upon execution, the pipeline generates the following assets in data/processed/:

- sensor_metadata.csv: Dimension table mapping sensor IDs to technical names, units, and engine components.
- engine_data.csv: Fact table containing smoothed signals (Moving Averages), degradation rates (Slopes), RUL, and Health Status.

### References
- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation. International Conference on Prognostics and Health Management.
