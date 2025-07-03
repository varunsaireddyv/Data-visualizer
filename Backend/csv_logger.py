import csv
import os

### Edit given feilds based on yuor convinence ###

# Default log file path
DEFAULT_LOG_FILE = "data_logs/sensor_log.csv"

# CSV column names (in correct order)
CSV_HEADER = ["timestamp", "sensor", "field", "value"]



# Main logger funtions

def log_readings_to_csv(readings: list, filename=DEFAULT_LOG_FILE):
    """
    Appends a list of parsed sensor readings to a CSV file.

    Each item in readings must be a dict with:
    - 'timestamp'
    - 'sensor'
    - 'field'
    - 'value'
    """
    if not readings:
        return  # nothing to log

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)

        # Write header if file is empty
        if f.tell() == 0:
            writer.writeheader()

        for row in readings:
            try:
                writer.writerow({
                    "timestamp": row["timestamp"],
                    "sensor": row["sensor"],
                    "field": row["field"],
                    "value": row["value"]
                })
            except KeyError as e:
                print(f"[Logger Error] Missing field in row: {row} → {e}")


def read_last_n_lines(n=20, filename=DEFAULT_LOG_FILE):
    """
    Reads the last `n` lines from the log file.
    Returns list of CSV strings.
    """
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as f:
        lines = f.readlines()
        return lines[-n:] if len(lines) > n else lines
