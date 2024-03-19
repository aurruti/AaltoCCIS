# File task3/plots.py
# Aitor Urruticoechea 2023
from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf

def timefun(timestampdf):
    start_time = float(timestampdf[0])
    timestampdf = timestampdf.apply(lambda x: float(x)-start_time)
    return timestampdf

lag = 1 

df1 = pd.read_csv('linkload-1.txt', sep=' ', names=['Timestamp', 'Bits/s'])
df1['Timestamp'] = timefun(df1['Timestamp'])
df1['Value_Lagged'] = df1['Bits/s'].shift(lag)
df2 = pd.read_csv('linkload-2.txt', sep=' ', names=['Timestamp', 'Bits/s'])
df2['Bits/s'] = df2['Timestamp']
df2['Timestamp'] = timefun(df1['Timestamp'])
df2['Value_Lagged'] = df2['Bits/s'].shift(lag)
df3 = pd.read_csv('linkload-3.txt', sep=' ', names=['Timestamp', 'Bits/s'])
df3['Timestamp'] = timefun(df3['Timestamp'])
df3['Value_Lagged'] = df3['Bits/s'].shift(lag)
df4 = pd.read_csv('linkload-4.txt', sep=' ', names=['Timestamp', 'Bits/s'])
df4['Timestamp'] = timefun(df4['Timestamp'])
df4['Value_Lagged'] = df4['Bits/s'].shift(lag)



# Time Plots
plt.figure(figsize=(12, 6))
plt.plot(df1['Timestamp'], df1['Bits/s'], label='Link 1')
plt.plot(df2['Timestamp'], df2['Bits/s'], label='Link 2')
plt.plot(df3['Timestamp'], df3['Bits/s'], label='Link 3')
plt.plot(df4['Timestamp'], df4['Bits/s'], label='Link 4')
plt.xlabel('Time (s)')
plt.ylabel('Bits/s')
plt.yscale('log')
plt.title('Time Plot')
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df4['Timestamp'], df4['Bits/s'], label='Link 4')
plt.xlabel('Time (s)')
plt.ylabel('Bits/s')
plt.yscale('log')
plt.title('Time Plot')
plt.grid(True)
plt.legend()
plt.show()

# Lag Plot
plt.figure(figsize=(6, 6))
plt.scatter(df2['Bits/s'], df2['Value_Lagged'], marker='o', color='blue', alpha=0.5)
plt.title(f'Lag Plot (Lag = {lag})')
plt.xlabel('Bits/s (t)')
plt.ylabel(f'Bits/s (t - {lag})')
plt.grid(True)
plt.show()

# Autocorrelation Plot
plt.figure(figsize=(8, 4))
plot_acf(df4['Bits/s'], lags=100) 
plt.title('Autocorrelation Plot')
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.grid(True)
plt.show()

