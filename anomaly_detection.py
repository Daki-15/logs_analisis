import pandas as pd
from sklearn.ensemble import IsolationForest
import re

def parse_logs(path):
    """
    Parses the log file and extracts relevant data into a DataFrame
    """
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        # Use regex to extract timestamp, log level, component, and value
        match = re.match(r"(.*?) \[(.*?)\] (\w+): (\d+)%", line)
        if match:
            timestamp, level, component, value = match.groups()
            data.append([timestamp.strip(), level.strip(), component.strip(), int(value)])

    # Return the parsed data as a pandas DataFrame
    return pd.DataFrame(data, columns=["timestamp", "level", "component", "value"])

def detect_anomalies_all_components(df):
    """
    Detects anomalies in the values of all system components using Isolation Forest
    """
    anomaly_dfs = []  # List to store DataFrames with detected anomalies

    for component in df["component"].unique():
        # Filter the DataFrame for the current component
        comp_df = df[df["component"] == component].copy()

        # Skip if the DataFrame for this component is empty
        if comp_df.empty:
            continue

        # Initialize the Isolation Forest model to detect anomalies
        model = IsolationForest(contamination=0.03, random_state=42)
        comp_df["anomaly"] = model.fit_predict(comp_df[["value"]])  # Predict anomalies

        # Select rows where anomalies are detected
        anomalies = comp_df[comp_df["anomaly"] == -1]
        anomaly_dfs.append(anomalies)

    # Concatenate all detected anomalies into a single DataFrame or return an empty one
    if anomaly_dfs:
        return pd.concat(anomaly_dfs)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # Parse the log file into a DataFrame
    df = parse_logs("./logs/system_logs.log")

    if df.empty:
        # Check if the log file is empty or not properly parsed
        print("The log file is empty or not properly parsed.")
    else:
        # Detect anomalies in the log data
        anomalies = detect_anomalies_all_components(df)

        if not anomalies.empty:
            # If anomalies are found, print them and save them to a CSV file
            print("ANOMALIES DETECTED:\n", anomalies)
            anomalies.to_csv("logs/anomalies.csv", index=False)
        else:
            # Indicate that no anomalies were detected
            print("NO ANOMALIES DETECTED.")