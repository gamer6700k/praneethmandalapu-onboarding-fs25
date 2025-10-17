import matplotlib.pyplot as plt
import polars as pl
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd

FILE_PATH = r"C:\Users\prane\PycharmProjects\PythonProject\data\08102025Endurance1_FirstHalf.parquet"

HEATMAP_COL = "SME_TORQUE_FB"
VOLTAGE_COL = "BMS_VOLTAGE"
BATT_CURRENT_COL = "BMS_CURRENT_DC"
MOTOR_CURRENT_COL = "INV_CURRENT_RMS"

df_clean = (
    df
    .filter(pl.col("VDM_GPS_Latitude") != 0)
    .filter(pl.col("VDM_GPS_Longitude") != 0)
    .with_row_index("Time_Index")
)

df_pd = df_clean.to_pandas()

latitude = df_pd["VDM_GPS_Latitude"].to_numpy()
longitude = df_pd["VDM_GPS_Longitude"].to_numpy()
time_index = df_pd["Time_Index"].to_numpy()

heatmap_kpi = df_pd[HEATMAP_COL].to_numpy()
voltage = df_pd[VOLTAGE_COL].to_numpy()
batt_current = df_pd[BATT_CURRENT_COL].to_numpy()
motor_current = df_pd[MOTOR_CURRENT_COL].to_numpy()

fig, (ax_kpi_map, ax_sag_plot, ax_loss_plot) = plt.subplots(
    1, 3,
    figsize=(24, 8),
    sharex=False,
    sharey=False,
    gridspec_kw={'width_ratios': [1, 1, 1]}
)
fig.suptitle(f"FSAE EV Endurance Analysis: Performance, Voltage Sag, and Current Comparison | File: {FILE_PATH}",
             fontsize=18)
def plot_track_map(ax, data, title, cmap, label):
    points = np.array([longitude, latitude]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    data_min = data.min()
    data_max = data.max()
    if data_min == data_max:
        data_max += 1.0

    norm = plt.Normalize(data_min, data_max)
    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=4.0, alpha=0.9)
    lc.set_array(data)
    ax.add_collection(lc)

    ax.set_xlim(longitude.min() - 0.0001, longitude.max() + 0.0001)
    ax.set_ylim(latitude.min() - 0.0001, latitude.max() + 0.0001)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("GPS Longitude")
    ax.set_ylabel("GPS Latitude")
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)

    cbar = fig.colorbar(lc, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label(label, fontsize=12)
    ax.plot(longitude[0], latitude[0], 'o', color='green', markersize=8, label='Start')

plot_track_map(
    ax_kpi_map,
    heatmap_kpi,
    f"Track Map: KPI ({HEATMAP_COL})",
    'inferno',
    f"{HEATMAP_COL} Value"
)

ax_sag_plot.scatter(
    batt_current,
    voltage,
    s=5,
    alpha=0.5,
    c=time_index,
    cmap='viridis'
)
ax_sag_plot.set_title("Voltage Sag Analysis (Battery V vs. Current)", fontsize=14)
ax_sag_plot.set_xlabel(f"Battery Current ({BATT_CURRENT_COL}) (A)")
ax_sag_plot.set_ylabel(f"Battery Voltage ({VOLTAGE_COL}) (V)")
ax_sag_plot.grid(True, linestyle=':', alpha=0.7)

sag_cbar = fig.colorbar(ax_sag_plot.collections[0], ax=ax_sag_plot, orientation='vertical', pad=0.02)
sag_cbar.set_label("Time Index", fontsize=12)

color_batt = 'tab:blue'
color_motor = 'tab:orange'

ax_loss_plot.plot(time_index, batt_current, color=color_batt, label=f"Battery Current ({BATT_CURRENT_COL}) (DC)",
                  linewidth=2.0)
ax_loss_plot.set_ylabel("Battery Current (A)", color=color_batt, fontsize=14)
ax_loss_plot.tick_params(axis='y', labelcolor=color_batt)
ax_loss_plot.set_xlabel("Time Index (Sample #)", fontsize=12)
ax_loss_plot.set_title("Current Comparison (DC vs. AC RMS)", fontsize=14)

ax_loss_twin = ax_loss_plot.twinx()
ax_loss_twin.plot(time_index, motor_current, color=color_motor, label=f"Motor Current ({MOTOR_CURRENT_COL}) (AC RMS)",
                  linestyle='--', linewidth=2.0)
ax_loss_twin.set_ylabel("Motor Current (A)", color=color_motor, fontsize=14)
ax_loss_twin.tick_params(axis='y', labelcolor=color_motor)

lines, labels = ax_loss_plot.get_legend_handles_labels()
lines2, labels2 = ax_loss_twin.get_legend_handles_labels()
ax_loss_plot.legend(lines + lines2, labels + labels2, loc='upper left')

ax_loss_plot.grid(True, linestyle=':', alpha=0.7)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
