import matplotlib.pyplot as plt
import polars as pl


df = pl.read_parquet(r"C:\Users\prane\PycharmProjects\PythonProject\data\08102025Endurance1_FirstHalf.parquet")


df = (
    df
    .filter(pl.col("VDM_GPS_Latitude") != 0)
    .filter(pl.col("VDM_GPS_Longitude") != 0)
    .with_row_index("Time_Index")
)

fig = plt.figure()

ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


ax1.plot(df["Time_Index"], df["VDM_GPS_SPEED"], label = "speed")
ax1.plot(df["Time_Index"], df["ETC_STATUS_RTDS"], label = "RTDS")
ax1.set_ylabel("Speed (mph)")
ax1.legend()


ax2.plot(df["VDM_GPS_Longitude"], df["VDM_GPS_Latitude"])



ax3.plot(df["Time_Index"], df["ETC_STATUS_RTDS"])


ax4.plot(df["Time_Index"], df["ACC_POWER_PACK_VOLTAGE"])

plt.show()
