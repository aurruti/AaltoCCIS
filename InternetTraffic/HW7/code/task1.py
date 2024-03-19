# File task1.py
# Aitor Urruticoechea 2023
import matplotlib.pyplot as plt
import statistics
import random
from scipy.stats import probplot

file_path = 'sampling/sampling.txt'
with open(file_path, 'r') as file:
    data = [float(line.strip()) for line in file]

# Plot histogram
def histmean(data):
    plt.hist(data, bins=10, color='blue', edgecolor='black')
    plt.title('Histogram of Data')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()

    plt.hist(data, bins=10, color='blue', edgecolor='black')
    plt.title('Histogram of Data')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.show()

    mean_value = statistics.mean(data)
    print(f"Mean: {mean_value}")
    std_value = statistics.stdev(data)
    print(f"STD: {std_value}")
    return mean_value, std_value

# histmean(data)

random_data = random.sample(data, 5000)
# histmean(random_data)

n = input('n: ')
nmean = []
for i in range(10000):
    random_data = random.sample(data, int(n))
    nmean.append(statistics.mean(random_data))
histmean(nmean)
probplot(random_data, dist='norm', plot=plt)
plt.title('Q-Q Plot')
plt.show()
serrorm = statistics.mean(nmean) - statistics.mean(data)
print('Sample Error Mean: ' + str(serrorm))
svariance = statistics.variance(nmean)
print('Variance: ' + str(svariance))