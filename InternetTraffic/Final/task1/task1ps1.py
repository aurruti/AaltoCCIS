# File task1ps1.py
# Aitor Urruticoechea 2023
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
dfudp = pd.read_csv('ps1-udp.csv')
dftcp = pd.read_csv('ps1-tcp.csv')

# Group by 'Port' and sum 'Packets'
groupudp = dfudp.groupby('Port')['Packets'].sum().sort_values()
grouptcp = dftcp.groupby('Port')['Packets'].sum().sort_values()

top15udp = groupudp.tail(15)
bottom15udp = groupudp.head(15)
top15tcp = grouptcp.tail(15)
bottom15tcp = grouptcp.head(15)

# Plots
plt.figure(figsize=(10,6))
top15udp.plot(kind='bar')
plt.title('UDP Packet Distribution by Port Numbers, Top 15 ports')
plt.xlabel('Port Number')
plt.yscale('log')
plt.ylabel('Number of Packets')
plt.show()
plt.figure(figsize=(10,6))
bottom15udp.plot(kind='bar')
plt.title('UDP Packet Distribution by Port Numbers, Bottom 15 ports')
plt.xlabel('Port Number')
plt.ylabel('Number of Packets')
plt.show()

plt.figure(figsize=(10,6))
top15tcp.plot(kind='bar')
plt.title('TCP Packet Distribution by Port Numbers, Top 15 ports')
plt.xlabel('Port Number')
plt.yscale('log')
plt.ylabel('Number of Packets')
plt.show()
plt.figure(figsize=(10,6))
bottom15tcp.plot(kind='bar')
plt.title('TCP Packet Distribution by Port Numbers, Bottom 15 ports')
plt.xlabel('Port Number')
plt.ylabel('Number of Packets')
plt.show()

# Plot histogram
plt.hist(dfudp['Bytes'], bins=100) # bins=range(min(dfudp['Bytes']), max(dfudp['Bytes']) + 1, 1))
plt.title('Packet Length Distribution - UDP')
plt.xlabel('Packet Length (bytes)')
plt.ylabel('Frequency')
plt.yscale('log')
plt.show()

plt.hist(dftcp['Bytes'], bins=100) # bins=range(min(dfudp['Bytes']), max(dfudp['Bytes']) + 1, 1))
plt.title('Packet Length Distribution - TCP')
plt.xlabel('Packet Length (bytes)')
plt.ylabel('Frequency')
plt.yscale('log')
plt.show()

# ECDF
def ecdf(data):
    n = len(data)
    x = np.sort(data)
    y = np.arange(1, n+1) / n
    return x, y

# Calculate ECDF for UDP packets
x_udp, y_udp = ecdf(dfudp['Packets'])

# Calculate ECDF for TCP bytes
x_tcp, y_tcp = ecdf(dftcp['Packets'])

# Plot ECDF for UDP packets
plt.figure(figsize=(10,6))
plt.plot(x_udp, y_udp, marker='.', linestyle='none')
plt.title('ECDF of UDP Packet Distribution')
plt.xlabel('Number of Packets')
plt.ylabel('ECDF')
plt.yscale('log')
plt.xscale('log')
plt.show()

# Plot ECDF for TCP packets
plt.figure(figsize=(10,6))
plt.plot(x_tcp, y_tcp, marker='.', linestyle='none')
plt.title('ECDF of TCP Packet Distribution')
plt.xlabel('Number of Packets')
plt.ylabel('ECDF')
plt.yscale('log')
plt.xscale('log')
plt.show()