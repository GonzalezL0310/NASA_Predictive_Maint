import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_sensor_trends(df: pd.DataFrame, unit_nr: int, sensors: list, save_path: Path = None):
    """
    Plots the raw sensor values, moving average, and calculated slope for a specific unit.

    Args:
        df (pd.DataFrame): The processed DataFrame.
        unit_nr (int): The unit ID to visualize.
        sensors (list): List of sensor names (e.g., ['s_2', 's_4']).
        save_path (Path, optional): If provided, saves the plot to this path.
    """
    subset = df[df['unit_nr'] == unit_nr]

    if subset.empty:
        print(f"[WARN] No data found for Unit {unit_nr}")
        return

    # Setup figure
    fig, axes = plt.subplots(len(sensors), 1, figsize=(10, 4 * len(sensors)), sharex=True)
    if len(sensors) == 1:
        axes = [axes]  # Ensure iterable if only one sensor

    for ax, sensor in zip(axes, sensors):
        # 1. Raw Data
        ax.plot(subset['time_cycles'], subset[sensor],
                label='Raw', color='lightgray', alpha=0.6)

        # 2. Moving Average (if exists)
        if f'{sensor}_ma' in subset.columns:
            ax.plot(subset['time_cycles'], subset[f'{sensor}_ma'],
                    label='Moving Avg (Trend)', color='blue', linewidth=2)

        # 3. Slope (Scaled for visualization)
        # Slope represents rate of change. We plot it on a twin axis to see correlation.
        if f'{sensor}_slope' in subset.columns:
            ax2 = ax.twinx()
            ax2.plot(subset['time_cycles'], subset[f'{sensor}_slope'],
                     label='Degradation Slope', color='red', linestyle='--', alpha=0.7)
            ax2.set_ylabel('Slope (Rate of Change)', color='red')

        ax.set_title(f"Sensor {sensor} Analysis - Unit {unit_nr}")
        ax.set_ylabel("Sensor Value")
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

    plt.xlabel("Time (Cycles)")
    plt.tight_layout()

    if save_path:
        # Create directory if it doesn't exist
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
        print(f"[INFO] Plot saved to {save_path}")
        plt.close()
    else:
        plt.show()