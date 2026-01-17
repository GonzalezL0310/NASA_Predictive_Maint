import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def plot_sensor_trends(df: pd.DataFrame, unit_nr: int, sensors: list, save_path: Path = None):
    subset = df[df['unit_nr'] == unit_nr]

    if subset.empty:
        print(f"[WARN] No data found for Unit {unit_nr}")
        return

    fig, axes = plt.subplots(len(sensors), 1, figsize=(10, 4 * len(sensors)), sharex=True)
    if len(sensors) == 1:
        axes = [axes]

    for ax, sensor in zip(axes, sensors):
        # 1. Raw Data (Nombre técnico directo)
        ax.plot(subset['time_cycles'], subset[sensor],
                label='Raw', color='green', alpha=0.6)

        # 2. Moving Average (Debe ser _MA en mayúsculas)
        if f'{sensor}_MA' in subset.columns:
            ax.plot(subset['time_cycles'], subset[f'{sensor}_MA'],
                    label='Moving Avg (Trend)', color='blue', linewidth=2)

        # 3. Slope (Debe ser _Slope en mayúsculas)
        if f'{sensor}_Slope' in subset.columns:
            ax2 = ax.twinx()
            ax2.plot(subset['time_cycles'], subset[f'{sensor}_Slope'],
                     label='Degradation Slope', color='red', linestyle='--', alpha=0.7)
            ax2.set_ylabel('Slope (Rate of Change)', color='red')

        ax.set_title(f"Sensor {sensor} Analysis - Unit {unit_nr}")
        ax.set_ylabel("Sensor Value")
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

    plt.xlabel("Time (Cycles)")
    plt.tight_layout()

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
        print(f"[INFO] Plot saved to {save_path}")
        plt.close()
    else:
        plt.show()
