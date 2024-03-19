# File task2/plots.py
# Aitor Urruticoechea 2023

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF

data = np.loadtxt('flows.txt')

# 2.1.1 Scatterplot
plt.scatter(range(len(data)), data)
plt.xlabel("Number of Observations")
plt.ylabel("Flows")
plt.title("Scatterplot - Linear Scale")
plt.show()
plt.scatter(range(len(data)), data)
plt.xlabel("Number of Observations")
plt.yscale('log')
plt.xscale('log')
plt.ylabel("Flows")
plt.title("Scatterplot - Log Scale")
plt.show()


# 2.1.2 Histogram
plt.hist(data, bins=100)
plt.xlabel("Data Value")
plt.ylabel("Frequency")
plt.title("Histogram - Linear Scale")
plt.show()
plt.hist(data, bins=100)
plt.xlabel("Data Value")
plt.ylabel("Frequency")
plt.yscale('log')
plt.title("Histogram - Log Scale")
plt.show()


# 2.1.3 Boxplot
plt.boxplot(data)
plt.ylabel("Flows")
plt.title("Boxplot - Linear Scale")
plt.show()
plt.boxplot(data)
plt.ylabel("Flows")
plt.title("Boxplot - Log Scale")
plt.yscale('log')
plt.show()


# 2.1.4 Empirical CDF
ecdf = ECDF(data)
x = np.sort(data)
y = ecdf(x)
plt.step(x, y)
plt.xlabel('Flows')
plt.ylabel('CDF Value')
plt.title('Empirical CDF - Linear Scale')
plt.show()
plt.step(x, y)
plt.xlabel('Flows')
plt.ylabel('CDF Value')
plt.xscale('log')
plt.title('Empirical CDF - Log Scale')
plt.show()

# 2.2 Relevant data
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
iqr = q3 - q1
print(np.median(data))
print(np.min(data))
print(iqr)



