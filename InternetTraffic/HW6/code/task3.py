# File task3.py
# Aitor Urruticoechea 2023
import pandas as pd
import matplotlib.pyplot as plt
from random import sample

file_path = 'sampling-data/flowdata.txt'
column_names = [
    "Source IP (Anonymized)",
    "Destination IP (Anonymized)",
    "Protocol",
    "Is the port number valid",
    "Source port",
    "Destination port",
    "Number of packets",
    "Number of bytes",
    "Number of flows",
    "First packet arrival time",
    "Last packet arrival time"
]
df = pd.read_csv(file_path, delimiter='\t', header=None, names=column_names)

# 1000 random plot
random_sample = df.sample(n=1000, random_state=42).astype(str)
plt.figure(figsize=(24, 6))
pd.plotting.parallel_coordinates(random_sample, 'Number of packets')
plt.title('Parallel Coordinates Plot')
plt.xlabel('Attributes')
plt.ylabel('Attribute Values')
plt.show()

# Scatter plots
random_sample = df.sample(n=1000, random_state=42)
plt.figure(figsize=(10, 6))
plt.scatter(df['Number of bytes'], df['Number of packets'], alpha=0.5, marker='x', color='b')
plt.title('Scatter Plot of Bytes vs Packets (whole dataset)')
plt.xlabel('Number of bytes')
plt.ylabel('Number of packets')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.show()
total_bytes = df['Number of bytes'].sum()
total_packets = df['Number of packets'].sum()
average_packet_size = total_bytes / total_packets
print(average_packet_size)

plt.figure(figsize=(10, 6))
plt.scatter(random_sample['Number of bytes'], random_sample['Number of packets'], alpha=0.5, marker='x', color='b')
plt.title('Scatter Plot of Bytes vs Packets (random 1000 points)')
plt.xlabel('Number of bytes')
plt.ylabel('Number of packets')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.show()
total_bytes = random_sample['Number of bytes'].sum()
total_packets = random_sample['Number of packets'].sum()
average_packet_size = total_bytes / total_packets
print(average_packet_size)


# Throughput
valid_connections = df[df['Last packet arrival time'] != df['First packet arrival time']]
total_time = (valid_connections['Last packet arrival time'] - valid_connections['First packet arrival time']).sum()
total_bytes = valid_connections['Number of bytes'].sum()
average_throughput = total_bytes / total_time
print(average_throughput)

valid_connections = random_sample[random_sample['Last packet arrival time'] != random_sample['First packet arrival time']]
total_time = (valid_connections['Last packet arrival time'] - valid_connections['First packet arrival time']).sum()
total_bytes = valid_connections['Number of bytes'].sum()
average_throughput = total_bytes / total_time
print(average_throughput)