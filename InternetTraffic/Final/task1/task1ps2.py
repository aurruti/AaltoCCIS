# File task1ps2.py
# Aitor Urruticoechea 2023
import re
import pandas as pd
import numpy as np
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import scipy.stats as stats

# Function to extract data from the Tuple Table section
def extract_data(file_content, table_type):
    start_pattern = f"# begin {table_type} ID: 0[0] ("
    end_pattern = "# end of text table"
    start_index = file_content.find(start_pattern)
    end_index = file_content.find(end_pattern, start_index)
    table_data = file_content[start_index + len(start_pattern):end_index].strip().split('\n')[1:]
    # Extracting column names
    columns = table_data[0].split()
    # Extracting data rows
    data_rows = [re.split(r'\t+', row) for row in table_data[2:]]
    
    return columns, data_rows

# Function to plot flows against dport using pandas
def plot_flows_vs_dport(columns, data_rows, title):
    # Create a DataFrame
    df = pd.DataFrame(data_rows, columns=columns)
    df['dport'] = pd.to_numeric(df['dport'])
    df['flows'] = pd.to_numeric(df['flows'])
    # Group by dport and sum flows, get only top and bottom 15
    grouped = df.groupby('dport')['flows'].sum().sort_values()
    top15 = grouped.tail(15)
    bottom15 = grouped.head(15)
    # Plotting
    bottom15.plot(kind='bar')
    plt.xlabel('Port')
    plt.ylabel('Number of Flows')
    plt.yscale('log')
    plt.title('Flows vs Port - Bottom 15 - ' + title)
    plt.show()
    top15.plot(kind='bar')
    plt.xlabel('Port')
    plt.ylabel('Number of Flows')
    plt.yscale('log')
    plt.title('Flows vs Port - Top 15 - ' + title)
    plt.show()
    return df

with open('ps2.t2', 'r') as file:
    file_content = file.read()

ipv4_columns, ipv4_data_rows = extract_data(file_content, 'Tuple Table (expired)')
ipv6_columns, ipv6_data_rows = extract_data(file_content, 'IPv6 Tuple Table (expired)')

df_ipv4 = plot_flows_vs_dport(ipv4_columns, ipv4_data_rows, 'IPv4')
df_ipv6 = plot_flows_vs_dport(ipv6_columns, ipv6_data_rows, 'IPv6')

# Convert relevant data
df_ipv4['first'] = pd.to_datetime(df_ipv4['first'], unit='s')  
df_ipv4['latest'] = pd.to_datetime(df_ipv4['latest'], unit='s')
df_ipv4['bytes'] = pd.to_numeric(df_ipv4['bytes']) 
df_ipv6['first'] = pd.to_datetime(df_ipv6['first'], unit='s')  
df_ipv6['latest'] = pd.to_datetime(df_ipv6['latest'], unit='s')  
df_ipv6['bytes'] = pd.to_numeric(df_ipv6['bytes']) 

# Function to plot traffic volume against time
def plot_timebytes_period(df_ipv4, df_ipv6, start_time, end_time, title):
    df_ipv4_filtered = df_ipv4[(df_ipv4['first'] >= start_time) & (df_ipv4['first'] <= end_time)]
    df_ipv6_filtered = df_ipv6[(df_ipv6['first'] >= start_time) & (df_ipv6['first'] <= end_time)]
    plt.figure(figsize=(10, 6))
    plt.scatter(df_ipv4_filtered['first'], df_ipv4_filtered['bytes'], label='IPv4')
    plt.scatter(df_ipv6_filtered['first'], df_ipv6_filtered['bytes'], label='IPv6')
    plt.title('Traffic Volume vs Time - ' + title)
    plt.xlabel('Time')
    plt.ylabel('Bytes')
    plt.yscale('log')
    plt.show()
start_time = pd.to_datetime('2023-11-19 16:00:00')
end_time = pd.to_datetime('2023-11-19 17:00:00')
#plot_timebytes_period(df_ipv4, df_ipv6, start_time, end_time, 'Period 1')
start_time = pd.to_datetime('2023-11-19 18:00:00')
end_time = pd.to_datetime('2023-11-19 19:00:00')
#plot_timebytes_period(df_ipv4, df_ipv6, start_time, end_time, 'Period 2')

# Destinations and countries
top10dest_ipv4 = df_ipv4.groupby('dst')['flows'].sum().sort_values().tail(10)
top10dest_ipv6 = df_ipv6.groupby('dst')['flows'].sum().sort_values().tail(10)
#print(top10dest_ipv4)
#print(top10dest_ipv6)

def zipf_plot(df_ipv4, df_ipv6):
    df_ipv4['pair'] = df_ipv4['#src'] + ' -\n ' + df_ipv4['dst']
    df_ipv6['pair'] = df_ipv6['#src'] + ' -\n ' + df_ipv6['dst']
    
    pair_freq_ipv4 = df_ipv4['pair'].value_counts().values
    pair_freq_ipv6 = df_ipv6['pair'].value_counts().values
    
    rank_ipv4 = np.arange(1, len(pair_freq_ipv4)+1)
    rank_ipv6 = np.arange(1, len(pair_freq_ipv6)+1)
    
    plt.figure(figsize=(10, 5))
    plt.loglog(rank_ipv4, pair_freq_ipv4, marker="o", label='IPv4')
    plt.loglog(rank_ipv6, pair_freq_ipv6, marker="o", label='IPv6')
    plt.title('Zipf plot for Pair Frequencies')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

# zipf_plot(df_ipv4, df_ipv6)

def flow_length_dist(df_ipv4, df_ipv6):
    df_ipv4['flow_length'] = (df_ipv4['latest'] - df_ipv4['first']).dt.total_seconds()
    df_ipv6['flow_length'] = (df_ipv6['latest'] - df_ipv6['first']).dt.total_seconds()
    
    plt.figure(figsize=(10, 5))
    plt.hist(df_ipv4['flow_length'], bins=100, label='IPv4')
    plt.hist(df_ipv6['flow_length'], bins=100, label='IPv6')
    plt.title('Flow Length Distribution')
    plt.xlabel('Flow Length (s)')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.legend()
    plt.show()
    return df_ipv4, df_ipv6

def ecdf(data):
    x = np.sort(data)
    y = np.arange(1, len(x)+1) / len(x)
    return x, y

def relevant_statistics(data):
    try:
        mean = np.mean(data)
        print('Mean: ' + str(mean))
    except:
        pass
    median = np.median(data)
    print('Median: ' + str(median))
    std = np.std(data)
    print('Standard Deviation: ' + str(std))
    min = np.min(data)
    print('Min: ' + str(min))
    max = np.max(data)
    print('Max: ' + str(max))

df_ipv4, df_ipv6 = flow_length_dist(df_ipv4, df_ipv6)
x4, y4 = ecdf(df_ipv4['pkts'])
x6, y6 = ecdf(df_ipv6['pkts'])
# Plot ECDFs
plt.figure(figsize=(10, 5))
plt.plot(x4, y4, marker='.', linestyle='none', label='IPv4')
plt.title('ECDF for IPv4')
plt.xlabel('Packets')
plt.ylabel('ECDF')
plt.xscale('log')
plt.yscale('log')
plt.show()
plt.plot(x6, y6, marker='.', linestyle='none', label='IPv6')
plt.title('ECDF for IPv6')
plt.xlabel('Packets')
plt.ylabel('ECDF')
plt.xscale('log')
plt.yscale('log')
plt.show()

# Relevant statistics
print('IPv4')
relevant_statistics(df_ipv4['bytes'])
relevant_statistics(df_ipv4['flow_length'])
print('IPv6')
relevant_statistics(df_ipv6['bytes'])
relevant_statistics(df_ipv6['flow_length'])

# Fit best distribution for flow length
def best_fit(data):
    # Distributions to fit
    dist_names = ['expon', 'gamma', 'lognorm', 'norm']
    dist_results = []
    params = {}
    for dist_name in dist_names:
        dist = getattr(stats, dist_name)
        param = dist.fit(data)
        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        D, p = stats.kstest(data, dist_name, args=param)
        dist_results.append((dist_name, p))
    # Select the best fitted distribution
    best_dist, best_p = (max(dist_results, key=lambda item: item[1]))
    # Store the name of the best fit and its p value
    return best_dist, best_p, params[best_dist]

def plot_bestfit(data, best_dist, params, title):
    # Plotting the best fit
    plt.figure(figsize=(10, 5))
    plt.hist(data, bins=100, density=True, label='Data')
    # Generating the x values
    x = np.linspace(np.min(data), np.max(data), 100)
    # Generating the PDF
    pdf = getattr(stats, best_dist).pdf(x, *params)
    plt.plot(x, pdf, label='Best Fit')
    plt.title(title)
    plt.xlabel('Flow Length (s)')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.legend()
    plt.show()

print('Best Fits')
best_fit_ipv4 = best_fit(df_ipv4['flow_length'])
print(best_fit_ipv4)
plot_bestfit(df_ipv4['flow_length'], best_fit_ipv4[0], best_fit_ipv4[2], 'Best Fit for IPv4')
best_fit_ipv6 = best_fit(df_ipv6['flow_length'])
print(best_fit_ipv6)
plot_bestfit(df_ipv6['flow_length'], best_fit_ipv6[0], best_fit_ipv6[2], 'Best Fit for IPv6')


