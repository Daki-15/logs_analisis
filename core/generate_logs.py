import random
import time
from datetime import datetime

def generate_log():
    """
    Simulates system operation and creates log entries
    """
    # Define log levels and components that will be monitored
    levels = ["INFO", "WARNING", "ERROR"]
    components = ["CPU", "MEMORY", "DISK", "APP"]

    while True:
        # Generate a timestamp for the current log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Randomly choose a log level and component
        level = random.choices(levels, weights=[0.7, 0.2, 0.1])[0]  # INFO is most likely
        component = random.choice(components)

        # Generate a random value to simulate system parameter (e.g., CPU usage)
        value = random.randint(30, 100)

        # Apply specific rules for CPU and DISK to adjust the log level
        if component == "CPU" and value > 85:
            level = "ERROR"  # High CPU usage results in an ERROR
        if component == "DISK" and value > 90:
            level = "WARNING"  # High DISK usage results in a WARNING

        # Format the log entry as a string
        log_line = f"{timestamp} [{level}] {component}: {value}%"
        print(log_line)  # Output the log entry to the console

        # Append the log entry to a log file
        with open("./logs/system_logs.log", "a") as file:
            file.write(log_line + "\n")

        # Wait for 1 second before generating the next log entry
        time.sleep(1)

def start_log_generation():
    generate_log()
