# File task5/plots.py
# Aitor Urruticoechea 2023
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('querytime.csv', parse_dates=['time'])

# Time plot
plt.figure(figsize=(12, 6))
plt.plot(df['time'], df['Query time(msec)'], marker='.', linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Query time (msec)')
plt.title('Time Plot')
plt.grid(True)
plt.show()