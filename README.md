# NASA CMAPSS Predictive Maintenance ETL

## Overview
This project implements a high-performance ETL pipeline for Predictive Maintenance using the NASA CMAPSS Turbofan Jet Engine dataset. It focuses on **Clean Code principles**, **Vectorized Numerical Operations** (using NumPy logic instead of loops), and **Static Typing**.

## Key Features
- **Vectorized Slope Calculation:** Implements a sliding window Linear Regression using `numpy.lib.stride_tricks` for maximum performance (O(1) vs iterative approaches).
- **Modular Architecture:** Separation of concerns between Data Loading, Numerical Operations, and Feature Engineering.
- **Robust Error Handling:** Explicit typing and docstrings for maintainability.

## Project Structure
```text
NASA_Predictive_Maint/
├── config/             # Configuration and constants
├── data/               # Raw and processed data (excluded from git)
├── src/                # Source code modules
│   ├── data_loader.py  # Data ingestion logic
│   ├── numerical_ops.py# Vectorized math operations
│   └── feature_eng.py  # RUL calculation
├── main.py             # Pipeline orchestrator
└── requirements.txt    # Dependencies
```

## Setup & Usage
Install Dependencies: Bash
```
pip install -r requirements.txt
```

Data Placement 
```text
Download the train_FD001.txt file from the NASA CMAPSS 
repository and place it in data/raw/.
```

Run Pipeline:
Bash

    python main.py

Requirements

    Python 3.9+

    pandas

    numpy