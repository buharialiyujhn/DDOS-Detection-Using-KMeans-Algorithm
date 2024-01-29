# DDoS Detection Using K-Means Algorithms

This repository is part of my Master's thesis submitted to the Institut supérieur d’électronique de Paris (ISEP) under the supervision of Prof. Yousrah Chouchoub. It focuses on the implementation of the K-Means algorithm for detecting DDoS attacks, specifically SYN flood attacks, using network traffic data.

## Project Overview

The project aims to develop an effective method for detecting DDoS attacks using the K-Means clustering algorithm. The approach involves analyzing network traffic data to identify abnormal patterns indicative of SYN flood attacks.

## Environment Setup

### Hardware Specifications

- **Processor:** Intel Xeon CPU with 8 cores.
- **Memory:** 16GB DDR4 RAM.
- **Storage:** 500GB SSD.

### Software Specifications

- **Operating Systems:** Linux, Windows 8 and above.
- **Programming Language:** Python 3.8.
- **Development Environments:** Jupyter Notebook and PyCharm.
- **Key Libraries:** pandas, scikit-learn, Matplotlib.

## Installation and Setup

Instructions on setting up the project environment and running the code.

### Prerequisites

- Python 3.x
- Libraries: numpy, scikit-learn, pandas, Matplotlib.

### Installation

1. Clone the repository: `git clone https://github.com/buharialiyujhn/DDOS-Detection-Using-KMeans-Algorithm`
2. Navigate to the project directory: `cd DDOS-Detection-Using-KMeans-Algorithm`
3. Install required packages: `pip install -r requirements.txt`

## Data Collection and Preparation

### Dataset Description

- **Source:** TCP dump data from Orange Labs.
- **Content:** Over 4 million rows of network traffic records with 16 columns.
- **Features:** Includes destination address, source address, ports, protocol number, timestamp, number of packets, and TCP flag.
- **Preprocessing:** Conversion of UNIX epoch time to datetime, IP address formatting.

## Implementation Details

### Feature Selection

- **Criteria:** Relevance to attack pattern, data quality, computational efficiency.
- **Selected Features:** TCP Flag, Source and Destination IP Addresses, Protocol, Timestamp, Number of Packets.

### K-Means Algorithm Implementation

- **Number of Clusters (n_clusters):** 2 (normal and potential attack traffic).
- **Initialization Method (init):** 'k-means++'.
- **Number of Initializations (n_init):** Multiple for optimal output.
- **Random State:** Fixed for reproducibility.

### Anomaly Detection

- **Threshold Determination:** Statistical analysis and cluster characteristics.
- **Real-time Monitoring:** Using sliding window technique.
- **Validation:** Against known SYN flood instances.

### Windows Sliding Technique

- **Window Size Determination:** 5 minutes.
- **Data Segmentation:** Based on destination IP and port numbers.
- **Anomaly Detection:** Flagging segments exceeding the threshold.

## Results and Analysis

### KMeans Result

The KMeans algorithm successfully identified several windows of DDoS attacks in the network traffic data. Detailed analysis of each attack window revealed key insights into the start and end times, targeted IP addresses, and the volume of packets received.

### Analysis of Attack Instances

#### DDoS Attack Analysis for IP Address 10.0.0.1

- **First Window:** 
  - Start Time: 2007-11-09 09:29:44
  - End Time: 2007-11-09 09:34:44
  - Packet Count: 50256
  - Observations: Marked beginning of SYN flood attack.
- **Second Window:** 
  - Start Time: 2007-11-09 09:34:44
  - End Time: 2007-11-09 09:39:44
  - Packet Count: 77290
  - Observations: Intensification of the attack.

[...]

#### DDoS Attack Analysis for IP Address 10.0.0.4

- **First Window:** 
  - Start Time: 2007-11-09 10:44:44
  - End Time: 2007-11-09 10:49:44
  - Packet Count: 1279
  - Observations: Noticeable increase in traffic volume.

[...]

### Observations

The identified windows for each IP address show a consistent pattern of SYN flood attacks. Notably, the destination port 5397 was consistently targeted, indicating a focused attempt to exploit a specific service or application.

### Silhouette Score Validation

The silhouette score of 0.9822 underscores the effectiveness of the model in distinguishing between normal traffic and potential attack vectors. This high score indicates distinct and well-separated clusters.

### Cluster Analysis

Cluster 1.0, encapsulating all detected anomalies, displayed characteristics consistent with SYN flood attacks:

- **Temporal Patterns:** Indicative of coordinated DDoS efforts.
- **Spatial Patterns:** Targeted attacks on a specific service or application.

### Discussion of Results

- **Packet Count Significance:** Emerged as a critical indicator of SYN flood attacks.
- **Consistency Across Windows:** Validated the overlapping window technique.
- **Cluster Homogeneity:** Demonstrates the K-Means algorithm's ability to accurately group attack instances.

### Limitations and Future Work

- **False Positives/Negatives:** Acknowledging the potential for inaccuracies, further refinement is needed.
- **Real-Time Validation:** Continuous improvement through real-time validation is essential.
- **Scalability and Performance:** Future work could explore distributed computing to handle larger datasets.

## Conclusion

The project has successfully demonstrated the potential of using K-Means clustering for detecting DDoS attacks in network traffic data. The analysis provided valuable insights into the nature and patterns of these attacks, emphasizing the importance of packet count and temporal patterns in detecting SYN flood behavior.

## Acknowledgements

Special thanks to Prof. Yousrah Chouchoub for her invaluable guidance and supervision throughout this research project.

## Contact

- Buhari Aliyu
- Email: buharialiyujhn@gmail.com
- LinkedIn: https://www.linkedin.com/in/buhari-aliyu-2b968159/

---

© Buhari Aliyu, 2024. All Rights Reserved.
