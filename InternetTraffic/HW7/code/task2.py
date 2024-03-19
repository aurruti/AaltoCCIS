# File task2.py
# Aitor Urruticoechea 2023
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, median

# Read data from the text file
data = pd.read_csv('sampling/flows.txt', delimiter='\s+')
data.columns = ['Flow_Length_Packets', 'Flow_Length_Bytes']


# Compute mean and median
mean_packets = mean(data['Flow_Length_Packets'])
median_packets = median(data['Flow_Length_Packets'])

mean_bytes = mean(data['Flow_Length_Bytes'])
median_bytes = median(data['Flow_Length_Bytes'])

# Print mean and median values
print(f"Mean Flow Length (Packets): {mean_packets}")
print(f"Median Flow Length (Packets): {median_packets}")

print(f"Mean Flow Length (Bytes): {mean_bytes}")
print(f"Median Flow Length (Bytes): {median_bytes}")

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

# Plot for Flow Length in Packets
axes[0].hist(data['Flow_Length_Packets'], bins=30, color='blue', alpha=0.7)
axes[0].axvline(mean_packets, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_packets}')
axes[0].axvline(median_packets, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_packets}')
axes[0].set_title('Flow Length in Packets')
axes[0].legend()
axes[0].set_yscale('log')

# Plot for Flow Length in Bytes
axes[1].hist(data['Flow_Length_Bytes'], bins=30, color='orange', alpha=0.7)
axes[1].axvline(mean_bytes, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_bytes}')
axes[1].axvline(median_bytes, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_bytes}')
axes[1].set_title('Flow Length in Bytes')
axes[1].legend()
axes[1].set_yscale('log')

plt.tight_layout()
plt.show()

# Running mean
def running_mean(data, n):
    run = data.head(n)
    try:
        return mean(run)
    except:
        return 0

packetmean = []
bytemean = []
ncount = []
for flow in range(len(data)):
    print(str(flow) + '/' + str(len(data)),end="\r")
    ncount.append(flow)
    packetmean.append(running_mean(data['Flow_Length_Packets'], flow))
    bytemean.append(running_mean(data['Flow_Length_Bytes'], flow))

plt.plot(ncount, bytemean)
plt.xlabel('N')
plt.ylabel('N-Mean')
plt.title('meann for bytes')
plt.grid()
plt.show()
plt.plot(ncount, packetmean)
plt.xlabel('N')
plt.ylabel('N-Mean')
plt.title('meann for packets')
plt.grid()
plt.show()