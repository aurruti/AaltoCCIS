# File task1ps3.py
# Aitor Urruticoechea 2023

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('ps3.csv', header=1, skiprows=range(1, 8), skip_blank_lines=True)


# TASK 3.1
plt.hist(df["RTT_avg_a2b"], bins=100)
plt.xlabel("RTT (avg, s)")
plt.ylabel("Frequency")
plt.title("Histogram - RTT a2b")
plt.yscale('log')
plt.show()

plt.hist(df["RTT_avg_b2a"], bins=100)
plt.xlabel("RTT (avg, s)")
plt.ylabel("Frequency")
plt.title("Histogram - RTT b2a")
plt.yscale('log')
plt.show()

def relevant_statistics(data):
    mean = data.mean()
    median = data.median()
    std = data.std()
    min = data.min()
    max = data.max()
    print("Mean: ", mean)
    print("Median: ", median)
    print("Standard deviation: ", std)
    print("Min: ", min)
    print("Max: ", max)

print('A2B')
relevant_statistics(df["RTT_avg_a2b"])
print('B2A')
relevant_statistics(df["RTT_avg_b2a"])

# TASK 3.2
df['total_data_volume'] = df['actual_data_bytes_a2b'] + df['actual_data_bytes_b2a']
plt.hist(df['total_data_volume'], bins=100)
plt.xlabel("Total Data Volume")
plt.ylabel("Frequency")
plt.title("Histogram - Total Data Volume")
plt.yscale('log')
plt.show()


