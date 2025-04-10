import os
import threading
import time
from core.anomaly_detection import parse_logs, detect_anomalies_all_components
from core.visualize import visualize_anomalies
from core.corrective_action import start_correctve_action
from core.generate_logs import start_log_generation

LOG_PATH = "./logs/system_logs.log"

def run_log_generator():
    # Pokreće se u posebnoj niti kako bi generisao logove paralelno
    start_log_generation()

def main():
    print("[INFO] Log generator started... Waiting for logs to accumulate...")
    
    # Pokreni generisanje logova u pozadini
    t = threading.Thread(target=run_log_generator, daemon=True)
    t.start()

    time.sleep(60)  # Sačekaj da se napravi dovoljno logova

    # Parsiraj logove
    df = parse_logs(LOG_PATH)

    if df.empty:
        print("[ERROR] Log file is empty or not properly parsed.")
        return

    # Detekcija anomalija
    anomalies = detect_anomalies_all_components(df)

    if anomalies.empty:
        print("[INFO] No anomalies detected.")
    else:
        print("[INFO] Anomalies detected:\n", anomalies.tail())
        anomalies.to_csv("./logs/anomalies.csv", index=False)

        # Vizualizuj anomalije po komponentama
        for component in anomalies["component"].unique():
            comp_df = df[df["component"] == component]
            comp_anomalies = anomalies[anomalies["component"] == component]
            visualize_anomalies(comp_df, comp_anomalies, target_component=component)

        # Preduzmi akcije
        start_correctve_action(anomalies)

if __name__ == "__main__":
    main()
