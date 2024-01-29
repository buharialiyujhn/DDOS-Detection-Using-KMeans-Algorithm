import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# Function to read and preprocess data from a file
def read_and_prepare_data(file_path):
    # Specify the columns to be used
    columns = ['Destination Address', 'Source Address', 'Destination Port',
               'Protocol', 'Start Timestamp', 'Number of Packets',
               'SYN Flag', 'Packet Direction']
    # Read the file with specified columns, and convert timestamp to datetime object
    df = pd.read_csv(file_path, sep=" ", header=None, names=columns,
                     usecols=[0, 1, 2, 4, 5, 9, 10, 15])
    df['Start Timestamp'] = pd.to_datetime(df['Start Timestamp'], unit='s')
    return df.set_index('Start Timestamp')

# Function to process data using sliding window
def process_window(current_window, min_count, n_clusters, random_state, n_init, start_time, window_size):
    # Filter packets with SYN flag set
    syn_packets = current_window[current_window['SYN Flag'] == 1]
    if syn_packets.empty:
        return None, [], []

    # Group packets by destination address and port, then count occurrences
    grouped = syn_packets.groupby(['Destination Address', 'Destination Port']).size().reset_index(name='Count')

    # Apply KMeans clustering to the grouped data
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=n_init)
    labels = kmeans.fit_predict(grouped[['Count']])
    grouped['Cluster'] = labels

    # Consider all data points and labels for silhouette score calculation
    all_data_points = grouped[['Count']]
    all_labels = labels.tolist()

    # Identify the cluster with the highest mean packet count as anomalous
    anomaly_cluster = grouped.groupby('Cluster')['Count'].mean().idxmax()
    anomalies = grouped[(grouped['Cluster'] == anomaly_cluster) & (grouped['Count'] >= min_count)]

    # Annotate anomalies with their respective time windows
    if not anomalies.empty:
        anomalies = anomalies.assign(Start_Window=start_time, End_Window=start_time + pd.Timedelta(window_size))

    return anomalies, all_data_points, all_labels

# Function to calculate silhouette score
def calculate_silhouette_score(all_data, labels):
    # Ensure there are enough clusters to compute the score
    if len(set(labels)) > 1:
        return silhouette_score(all_data, labels)
    else:
        print("Not enough clusters to compute Silhouette Score.")
        return None

# Main function to detect SYN flooding attacks and evaluate clustering
def detect_and_evaluate_syn_flooding(file_path, window_size='300S', min_count=500, n_clusters=2, random_state=None, n_init=10):
    df = read_and_prepare_data(file_path)
    anomalies = pd.DataFrame(columns=['Destination Address', 'Destination Port', 'Count', 'Start Window', 'End Window'])
    all_data = pd.DataFrame()
    labels = []

    # Iterate over time windows in the dataset
    start_time = df.index.min()
    end_time = df.index.max()

    while start_time + pd.Timedelta(window_size) <= end_time:
        current_window = df[(df.index >= start_time) & (df.index < start_time + pd.Timedelta(window_size))]
        current_anomalies, window_data, window_labels = process_window(current_window, min_count, n_clusters, random_state, n_init, start_time, window_size)

        # Aggregate anomalies and data points for silhouette score calculation
        if current_anomalies is not None and not current_anomalies.empty:
            anomalies = pd.concat([anomalies, current_anomalies], ignore_index=True)

        # Append all data points and labels, not just anomalies
        all_data = pd.concat([all_data, window_data], ignore_index=True)
        labels.extend(window_labels)

        start_time += pd.Timedelta(window_size)

    # Calculate the average silhouette score
    silhouette_avg = None
    if len(all_data) == len(labels):
        silhouette_avg = calculate_silhouette_score(all_data, labels)
    else:
        print("Mismatch in length of all_data and labels, cannot calculate Silhouette Score.")

    # Print detected anomalies
    for index, row in anomalies.iterrows():
        print(f"SYN Flooding Attack Anomaly Details:")
        print(f"Start Time: {row['Start_Window']}")
        print(f"End Time: {row['End_Window']}")
        print(f"Destination IP: {row['Destination Address']}")
        print(f"Destination Port: {row['Destination Port']}")
        print(f"Packet Count: {row['Count']}")
        print(f"Cluster: {row['Cluster']}")
        print()

    return anomalies, silhouette_avg


file_path = 'trace2.txt'
anomalies, silhouette_score = detect_and_evaluate_syn_flooding(file_path)
print(f"silhouette score: {silhouette_score}")
