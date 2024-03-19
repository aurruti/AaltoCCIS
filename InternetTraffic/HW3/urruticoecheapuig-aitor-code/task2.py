import pandas as pd
from matplotlib import pyplot as plt

filepath = 'output-all-ended.t2'

# From output-all-ended.t2 to DataFrame
data = []
current_table = None
current_protocol = None 

# Open the .t2 file for reading
with open(filepath, 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('# begin'):
            current_table = []
            if "IPv6" in line:
                current_protocol = "IPv6"
            else:
                current_protocol = "IPv4"
            continue
        if line.startswith('# end of text table'):
            if current_table:
                data.extend(current_table)
            current_table = None
            continue
        if line.startswith('#') or not line:
            continue
        parts = line.split('\t')
        row_data = {
            'src': parts[0],
            'dst': parts[1],
            'pro': int(parts[2]),
            'ok': int(parts[3]),
            'sport': int(parts[4]),
            'dport': int(parts[5]),
            'pkts': int(parts[6]),
            'bytes': int(parts[7]),
            'flows': int(parts[8]),
            'first': float(parts[9]),
            'latest': float(parts[10]),
            'IPvX': current_protocol
        }
        if current_table is not None:
            current_table.append(row_data)

wsdata = pd.DataFrame(data)

# (2.1) Relevant data extraction
print(wsdata['flows'].sum())
print('By bytes')
print(wsdata['bytes'].max())
print(wsdata['bytes'].min())
print(wsdata['bytes'].median())
print(wsdata['bytes'].mean())
print('By packets')
print(wsdata['pkts'].max())
print(wsdata['pkts'].min())
print(wsdata['pkts'].median())
print(wsdata['pkts'].mean())

# (2.2) Plot the traffic volume
wsdata['data_rate'] = wsdata['bytes'] / (wsdata['latest'] - wsdata['first'])
wsdata['Time (s)'] = wsdata['first'] - wsdata['first'].min()

plt.figure(figsize=(12, 6))
plt.scatter(wsdata['Time (s)'],wsdata['data_rate'])
plt.xlabel('Time (seconds)')
plt.yscale('log')
plt.ylabel('Data Rate (bytes per second)')
plt.title('Data Rate vs. Time (s)')
plt.grid(True)
plt.show()

# (2.3) Top5 Protocols
pro_flows = wsdata.groupby('pro')['flows'].sum().reset_index()
top_5_protocols = pro_flows.sort_values(by='flows', ascending=False).head(5)
print('Top 5 protocols')
print(top_5_protocols)
for index, row in top_5_protocols.iterrows():
    protocol = row['pro']
    protocol_data = wsdata[wsdata['pro'] == protocol]
    total_packets = protocol_data['pkts'].sum()
    total_bytes = protocol_data['bytes'].sum()
    dst = protocol_data['dst'].mode().iloc[0]
    print(protocol)
    print(total_packets)
    print(total_bytes)
    print(dst)
    print('')

# (2.4) Top10 pairs
host_pairs_flows = wsdata.groupby(['src', 'dst'])['flows'].sum().reset_index()
host_pairs_bytes = wsdata.groupby(['src', 'dst'])['bytes'].sum().reset_index()
print(host_pairs_flows.nlargest(10, 'flows'))
print(host_pairs_bytes.nlargest(10, 'bytes'))

# (2.5) plot top100 pairs
top100 = host_pairs_flows.nlargest(100, 'flows')
pos = 0
t100position = []
t100flow = []
for index in top100.index:
    pos += 1
    t100position.append(pos)
    t100flow.append(top100['flows'][index])
plt.figure(figsize=(12, 6))
plt.bar(t100position,t100flow)
plt.xlabel('Position in top100')
plt.yscale('log') #change for scale
plt.ylabel('Number of Flows')
plt.title('Number of Flows of top100 pairs of hosts')
plt.grid(True)
plt.show()

### 
