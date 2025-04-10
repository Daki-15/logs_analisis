import pandas as pd

# Corrective actions based on detected anomalies
def take_action(anomalies):
    """
    Performs corrective actions based on detected anomalies and logs them to a file
    """
    with open("./logs/actions.log", "a", encoding="utf-8") as file:
        for _, row in anomalies.iterrows():
            # Extract component, value, and timestamp for each anomaly
            component = row['component']
            value = row['value']
            timestamp = row['timestamp']

            # Based on the component and value, decide the appropriate action
            if component == "CPU":
                if value > 95:
                    action = f"{timestamp} ACTION: CPU {value}% → Restart critical service\n"
                elif value > 90:
                    action = f"{timestamp} ACTION: CPU {value}% → Pause non-critical processes\n"
                else:
                    action = f"{timestamp} INFO: CPU under heavy load ({value}%)\n"
            elif component == "MEMORY":
                if value > 90:
                    action = f"{timestamp} ACTION: MEMORY {value}% → Restart application (possible memory leak)\n"
                elif value > 80:
                    action = f"{timestamp} ACTION: MEMORY {value}% → Clear cache\n"
                else:
                    action = f"{timestamp} INFO: MEMORY OK ({value}%)\n"

            elif component == "DISK":
                if value > 95:
                    action = f"{timestamp} ACTION: DISK {value}% → Take system snapshot and alert\n"
                elif value > 90:
                    action = f"{timestamp} ACTION: DISK {value}% → Delete temp files / rotate logs\n"
                else:
                    action = f"{timestamp} INFO: DISK OK ({value}%)\n"
            else:
                # Handle unknown components
                action = f"{timestamp} INFO: Unknown component → {component}\n"
            # Print the action to the console
            print("[ACTION]", action.strip())

            # Write the action to the log file
            file.write(action)

def start_correctve_action():
    # Load detected anomalies from the CSV file
    anomalies = pd.read_csv("logs/anomalies.csv")

    if not anomalies.empty:
        # Perform corrective actions if anomalies exist
        take_action(anomalies)
    else:
        # Indicate that no anomalies are available for action
        print("No anomalies detected for corrective action.")