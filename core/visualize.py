import pandas as pd
from sklearn.ensemble import IsolationForest
import re
import matplotlib
# Use 'Agg' backend for matplotlib, which does not require Tkinter
import matplotlib.pyplot as plt

matplotlib.use('Agg')
def parse_logs(path):
    """
    Reads the log file and extracts relevant data into a DataFrame
    """
    with open(path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        # Use regex to parse timestamp, level, component, and value
        match = re.match(r"(.*?) \[(.*?)\] (\w+): (\d+)%", line)
        if match:
            timestamp, level, component, value = match.groups()
            data.append([timestamp, level, component, int(value)])

    # Return parsed data as a pandas DataFrame
    return pd.DataFrame(data, columns=["timestamp", "level", "component", "value"])

def detect_anomalies(df, target_component="CPU"):
    """
    Detects anomalies in the specified component using Isolation Forest
    """
    # Filter the DataFrame for the selected component
    component_df = df[df["component"] == target_component]
    if component_df.empty:
        return None, None

    # Initialize the Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)
    component_df = component_df.copy()
    # Predict anomalies and add them to the DataFrame
    component_df["anomaly"] = model.fit_predict(component_df[["value"]])

    # Extract rows where anomalies are detected
    anomalies = component_df[component_df["anomaly"] == -1]
    return component_df, anomalies

def visualize_anomalies(df, anomalies, target_component="CPU"):
    """
    Generates a plot highlighting anomalies in the specified component
    """
    plt.figure(figsize=(14, 7))
    plt.plot(df['timestamp'], df['value'], label='Normal', color='blue')  # Normal data
    plt.scatter(anomalies['timestamp'], anomalies['value'], color='red', label='Anomaly')  # Anomalies

    # Configure plot title and labels
    plt.title(f"Anomalies in {target_component} Component")
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    plt.legend()
    
    # Save the plot to a file instead of displaying it
    plt.savefig(f'anomalies_{target_component}.png')

def start_visualize():
    # Load logs into a DataFrame
    df = parse_logs("./logs/system_logs.log")
    
    # Detect anomalies for CPU
    cpu_df, cpu_anomalies = detect_anomalies(df, target_component="CPU")
    if cpu_anomalies is not None:
        print("ANOMALIES FOUND FOR CPU:\n", cpu_anomalies.tail())
        visualize_anomalies(df, cpu_anomalies, target_component="CPU")
    else:
        print("NO ANOMALIES FOUND FOR CPU.")

    # Detect anomalies for DISK
    disk_df, disk_anomalies = detect_anomalies(df, target_component="DISK")
    if disk_anomalies is not None:
        print("ANOMALIES FOUND FOR DISK:\n", disk_anomalies.tail())
        visualize_anomalies(df, disk_anomalies, target_component="DISK")
    else:
        print("NO ANOMALIES FOUND FOR DISK.")