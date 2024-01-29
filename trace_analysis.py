import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# We assume that the 'file_path' variable contains the path to your trace file
file_path = 'trace2.txt'  # Adjusted for the file uploaded to the session

# Read data file
columns = ['Destination Address', 'Source Address', 'Destination Port', 'Protocol', 'Start Timestamp',
           'Number of Packets', 'SYN Flag', 'Packet Direction']
df = pd.read_csv(file_path, sep=" ", header=None, names=columns, usecols=[0, 1, 2, 4, 5, 9, 10, 15])

# Convert 'Start Timestamp' to datetime and set as index
df['Start Timestamp'] = pd.to_datetime(df['Start Timestamp'], unit='s')
df.set_index('Start Timestamp', inplace=True)

# Filter for SYN packets
syn_packets = df[df['SYN Flag'] == 1]

# Resample for 1-minute intervals and calculate count
syn_count_1min = syn_packets.resample('1T').size()

# Resample for 5-minute intervals and calculate count
syn_count_5min = syn_packets.resample('5T').size()

# Normalize the index to start from 0 to 120 minutes
normalized_index_1min = (syn_count_1min.index - df.index.min()).total_seconds() / 60
normalized_index_5min = (syn_count_5min.index - df.index.min()).total_seconds() / 60

# Find the maximum count in each interval
max_syn_1min = syn_count_1min.groupby(normalized_index_1min).max()
max_syn_5min = syn_count_5min.groupby(normalized_index_5min).max()

# Plot the graph
plt.figure(figsize=(15, 7))

# Plot the data with the normalized index
plt.plot(max_syn_1min.index, max_syn_1min, label='Max SYN in 1min', linestyle='-', linewidth=1)
plt.plot(max_syn_5min.index, max_syn_5min, label='Max SYN in 5min', linestyle='--', linewidth=1)

# Formatting the Y-axis to not use a log scale
plt.yscale('linear')
plt.gca().yaxis.set_major_formatter(mticker.ScalarFormatter())

# Use the actual numbers instead of scientific notation
plt.gca().ticklabel_format(style='plain', axis='y')

# Set the limit for the X-axis
plt.xlim(0, 120)

# Labeling the axes and title
plt.xlabel('Time (minutes)')
plt.ylabel('Max SYN Count')
plt.title('Max SYN Count per Interval')

# Adding grid lines and the legend
plt.grid(True, which="both", linestyle='--')
plt.legend()

# Show the plot
plt.show()
