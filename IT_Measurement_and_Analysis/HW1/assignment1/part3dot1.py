# File part3dot1.py
# Aitor Urruticoechea 2023
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Importing data from file into pandas dataframe
ping_path = "/work/courses/unix/T/ELEC/E7130/general/basic_data/ping_data.csv"
ping_data = pd.read_csv(ping_path)

# Plotting Average RTT
timestamp = pd.to_datetime(ping_data['Timestamp'],unit='s')
avg_rtt = pd.DataFrame(ping_data,columns=["Avg RTT (ms)"])
#Timestamp format is simplified to make the axis readeable
timestamp = timestamp.transform(lambda x: x.strftime('%d %H:%M'))
fig, ax = plt.subplots()
ax.plot(timestamp,avg_rtt)
loc = plticker.MultipleLocator(base=29)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Timestamp")
plt.ylabel("Average RTT (ms)")
plt.show()

# Hourly data
hrtt = []
hmax = []
hloss = []
hour = 0
hlist = []
for hour in range(int(max(ping_data.count())/6)):
    ping0 = 6*hour
    pingmax = 6*hour+6
    sum_rtt = 0
    max_rtt = 0
    for ping in range(ping0,pingmax):
        if ping_data["Avg RTT (ms)"][ping] != float('inf'):
            sum_rtt += ping_data["Avg RTT (ms)"][ping]
            if max_rtt < ping_data["Avg RTT (ms)"][ping]:
                max_rtt = ping_data["Avg RTT (ms)"][ping]
    hrtt.append(sum_rtt/6)
    hmax.append(max_rtt)
    success = sum(ping_data["Successful packets"][ping0:pingmax])
    sent = sum(ping_data["Transmitted packets"][ping0:pingmax])
    hloss.append(100*(sent-success)/sent)
    hlist.append(timestamp[ping])

hourly_data = pd.DataFrame({'Hour':hlist,'Avg RTT (ms)':hrtt, 'Max RTT (ms)':hmax, 'Packet Loss (%)':hloss})    
                
# Plotting hourly averages
fig, ax = plt.subplots()
ax.plot(hourly_data['Hour'],hourly_data['Avg RTT (ms)'], label='Hourly Average')
ax.plot(hourly_data['Hour'],hourly_data['Max RTT (ms)'], label='Hourly Maximum')
loc = plticker.MultipleLocator(base=4)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Hour")
plt.ylabel("RTT (ms)")
plt.legend()
plt.show()

fig, ax = plt.subplots()
ax.plot(hourly_data['Hour'],hourly_data['Packet Loss (%)'])
loc = plticker.MultipleLocator(base=4)
ax.xaxis.set_major_locator(loc)
plt.xlabel("Hour")
plt.ylabel("Packet Loss (%)")
plt.show()