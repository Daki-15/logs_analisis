# 🧠 Log Analysis & Anomaly Detection System

A Python-based system that simulates log generation for system components (CPU, MEMORY, DISK), detects anomalies using machine learning, and automatically recommends corrective actions.

## 📁 Project Structure

```
logs_analisis/
│
├── core/
│   ├── anomaly_detection.py       # Detect anomalies in log data
│   ├── corrective_action.py       # Respond to detected anomalies
│   ├── generate_logs.py           # Simulate real-time system logs
│   └── visualize.py               # Visualize anomalies in plots
│
├── logs/                          # Generated logs and output files
│   ├── system_logs.log
│   ├── anomalies.csv
│   └── actions.log
│
├── main.py                        # Main entry point of the app
├── requirements.txt               # Python dependencies
└── README.md                      # You're reading it
```

## ⚙️ Features

- ✅ **Log Generator**: Simulates logs for CPU, MEMORY, and DISK every second.
- 🤖 **Anomaly Detection**: Uses Isolation Forest to detect anomalies.
- 📊 **Visualization**: Creates plots showing normal vs anomalous values.
- 🛠 **Corrective Actions**: Suggests responses based on detected issues.
- ⏱ **Auto Stop**: Automatically stops log generation after a configurable time.

## 🚀 How to Run

1. **Clone the repo**:

   ```bash
   git clone https://github.com/your-username/logs_analisis.git
   cd logs_analisis
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project**:

   ```bash
   python main.py
   ```

## 📈 Output Files

- `logs/system_logs.log`: All generated system logs
- `logs/anomalies.csv`: Detected anomalies
- `logs/actions.log`: Logged corrective actions
- `anomalies_CPU.png`, `anomalies_DISK.png`, etc.: Anomaly visualizations


## 🧠 Example Log Format

```
2025-04-10 12:30:01 [INFO] CPU: 87%
2025-04-10 12:30:02 [INFO] MEMORY: 92%
```

---

## 🛠 Corrective Actions Sample

```text
2025-04-10 12:30:02 ACTION: MEMORY 92% → Restart application (possible memory leak)
2025-04-10 12:30:03 ACTION: CPU 97% → Restart critical service
```


## ✅ To Do / Ideas

- [ ] Add email/Slack alerts for critical anomalies
- [ ] Dockerize the app for deployment
- [ ] Integrate with real system logs (syslog/Windows Event Viewer)
- [ ] Web dashboard with live plots

## 👨‍💻 Author

Made with ❤️ by Daki-15
