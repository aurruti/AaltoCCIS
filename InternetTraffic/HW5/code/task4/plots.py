# File task4/plots.py
#Aitor Urruticoechea 2023
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def timefun(timestampdf):
    start_time = float(timestampdf[0])
    timestampdf = timestampdf.apply(lambda x: float(x)-start_time)
    return timestampdf

df = pd.read_csv('bytes.csv')
df['Time'] = df['Time'].str.replace(' EEST', '', regex=False)
df['Time'] = df['Time'].apply(lambda x: (datetime.strptime(x, '%a %b %d %H:%M:%S %Y')).timestamp())
df['Time'] = timefun(df['Time'])
corr_matrix = df.corr()
column_names = df.columns

# Pair plots
fig, axes = plt.subplots(nrows=len(column_names), ncols=len(column_names), figsize=(12, 12))
fig.subplots_adjust(wspace=0, hspace=0)

for i, row_var in enumerate(column_names):
    for j, col_var in enumerate(column_names):
        if i == j:
            axes[i, j].axis('off')
        if i != j:
            axes[i, j].scatter(df[col_var], df[row_var], marker='.', alpha=0.5)
            if i == len(column_names) - 1:
                axes[i, j].set_xlabel(col_var)
            else:
                axes[i, j].get_xaxis().set_ticks([])
            if j == 0:
                axes[i, j].set_ylabel(row_var)
            else:
                axes[i, j].get_yaxis().set_ticks([])
axes[3,4].set_xlabel('TX Packets')
axes[0,1].set_ylabel('Time')

plt.show()

