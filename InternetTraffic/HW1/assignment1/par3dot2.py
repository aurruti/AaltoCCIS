# File part3dot2.py
# Aitor Urruticoechea 2023
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

# Importing data from file into pandas dataframe
iperf_path = "/work/courses/unix/T/ELEC/E7130/general/basic_data/iperf_data.csv"
iperf_data = pd.read_csv(iperf_path)
iperf_data["Timestamp"] = pd.to_datetime(iperf_data['Timestamp'],unit='s')


#Data cleaning and sorting
rows_to_drop = []
rows_normal = []
rows_reverse = []
for row in range(max(iperf_data.count())):
    if iperf_data["Server"][row] == "-1":
        rows_to_drop.append(row)
    if iperf_data["Mode"][row] == 1:
        rows_reverse.append(row)
    if iperf_data["Mode"][row] == 0:
        rows_normal.append(row)
iperf_data = iperf_data.drop(rows_to_drop)
iperf_normal = iperf_data.drop(rows_reverse)
iperf_reverse = iperf_data.drop(rows_normal)

# Bitrate and tcp retransmissions
fig, ax = plt.subplots()
ax.plot(iperf_normal["Timestamp"].transform(lambda x: x.strftime('%m-%d %H:%M:%S')),iperf_normal["Sent bitrate (bps)"], label="Sent")
ax.plot(iperf_normal["Timestamp"].transform(lambda x: x.strftime('%m-%d %H:%M:%S')),iperf_normal["Receive bitrate (bps)"], label="Receive")
loc = plticker.MultipleLocator(base=5)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Timestamp")
plt.ylabel("Bitrate (bps)")
plt.legend()
plt.show()

fig, ax = plt.subplots()
ax.plot(iperf_normal["Timestamp"].transform(lambda x: x.strftime('%m-%d %H:%M:%S')),iperf_normal["Retransmissions"])
loc = plticker.MultipleLocator(base=5)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Timestamp")
plt.ylabel("Retransmissions")
plt.show()

fig, ax = plt.subplots()
ax.plot(iperf_reverse["Timestamp"].transform(lambda x: x.strftime('%m-%d %H:%M:%S')),iperf_reverse["Sent bitrate (bps)"], label="Sent")
ax.plot(iperf_reverse["Timestamp"].transform(lambda x: x.strftime('%m-%d %H:%M:%S')),iperf_reverse["Receive bitrate (bps)"], label="Receive")
loc = plticker.MultipleLocator(base=5)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Timestamp")
plt.ylabel("Bitrate (bps)")
plt.legend()
plt.show()

fig, ax = plt.subplots()
ax.plot(iperf_reverse["Timestamp"].transform(lambda x: x.strftime('%m-%d %H:%M:%S')),iperf_reverse["Retransmissions"])
loc = plticker.MultipleLocator(base=5)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Timestamp")
plt.ylabel("Retransmissions")
plt.show()

# Scatter Plot
fig, ax = plt.subplots()
plt.scatter(iperf_normal["Retransmissions"], iperf_normal["Sent bitrate (bps)"])
a,b = np.polyfit(iperf_normal["Retransmissions"],iperf_normal["Sent bitrate (bps)"],1)
ax.plot(iperf_normal["Retransmissions"], a*iperf_normal["Retransmissions"]+b)
plt.xlabel("Retransmissions")
plt.ylabel("Sent bitrate (bps)")
plt.show()


rows_w_zero = []
for row in range(max(iperf_reverse.index)+1):
    try:
        if iperf_reverse["Retransmissions"][row] == 0:
            rows_w_zero.append(row)
    except:
        pass
iperf_reverse_nozero = iperf_reverse.drop(rows_w_zero)

fig, ax = plt.subplots()
plt.scatter(iperf_reverse_nozero["Retransmissions"], iperf_reverse_nozero["Sent bitrate (bps)"])
a,b = np.polyfit(iperf_reverse_nozero["Retransmissions"], iperf_reverse_nozero["Sent bitrate (bps)"],1)
ax.plot(iperf_reverse_nozero["Retransmissions"], a*iperf_reverse_nozero["Retransmissions"]+b)
plt.xlabel("Retransmissions")
plt.ylabel("Sent bitrate (bps)")
plt.show()