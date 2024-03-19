# File task2.py
# Aitor Urruticoechea 2023
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

headers = ['src','dst','pro','ok','sport','dport','pkts','bytes','flows','first','latest']

## FS2 Analysis

df = pd.read_csv('FS2-continue.t2',names=headers,sep='\t')
df['first'] = pd.to_datetime(df['first'], unit='s')
df['latest'] = pd.to_datetime(df['latest'], unit='s')

def plot_flows_vs_dport(df, title):
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

def plot_timebytes_period(df, start_time, end_time, title):
    df_zoom = df[(df['first'] >= start_time) & (df['first'] <= end_time)]
    plt.figure(figsize=(10, 6))
    plt.scatter(df_zoom['first'], df_zoom['bytes'])
    plt.title('Traffic Volume vs Time - ' + title)
    plt.xlabel('Time')
    plt.ylabel('Bytes')
    plt.yscale('log')
    plt.show()

plot_flows_vs_dport(df, 'All')
plot_timebytes_period(df, datetime(2017, 4, 12, 6, 00), datetime(2017, 4, 12, 9, 00), 'All')
plot_timebytes_period(df, datetime(2017, 4, 12, 12, 00), datetime(2017, 4, 12, 15, 00), 'All')

def user_analysis(df):
    aggregate = []
    for user in range(0, 255):
        user = '163.35.116.' + str(user)
        df_user = df[(df['src'] == user) | (df['dst'] == user)]
        aggregate.append(df_user['bytes'].sum())
    # Aggregate historiogram
    plt.hist(aggregate, bins=100)
    plt.xlabel('Bytes')
    plt.ylabel('Number of Users')
    plt.title('User Analysis')	
    plt.yscale('log')
    plt.show()
    return aggregate

user_analysis(df)



## FS1 Sample Analysis

df_ipv4 = pd.read_csv('FS1_sample_ipv4.txt',names=headers,sep='\t')
df_ipv6 = pd.read_csv('FS1_sample_ipv6.txt',names=headers,sep='\t')
df_ipv4['first'] = pd.to_datetime(df_ipv4['first'], unit='s')
df_ipv4['latest'] = pd.to_datetime(df_ipv4['latest'], unit='s')
df_ipv6['first'] = pd.to_datetime(df_ipv6['first'], unit='s')
df_ipv6['latest'] = pd.to_datetime(df_ipv6['latest'], unit='s')

plot_flows_vs_dport(df_ipv4, 'IPv4 - FS1 Sample')
plot_flows_vs_dport(df_ipv6, 'IPv6 - FS1 Sample')
plot_timebytes_period(df_ipv4, datetime(2017, 4, 12, 6, 00), datetime(2017, 4, 12, 9, 00), 'IPv4 - FS1 Sample')
plot_timebytes_period(df_ipv4, datetime(2017, 4, 12, 12, 00), datetime(2017, 4, 12, 15, 00), 'IPv4 - FS1 Sample')
plot_timebytes_period(df_ipv6, datetime(2017, 4, 12, 6, 00), datetime(2017, 4, 12, 9, 00), 'IPv6 - FS1 Sample')
plot_timebytes_period(df_ipv6, datetime(2017, 4, 12, 12, 00), datetime(2017, 4, 12, 15, 00), 'IPv6 - FS1 Sample')

