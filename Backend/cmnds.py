import csv
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

LOG_FILE = "/home/varun/Downloads/sensor_data.csv"
DEBUG = False

def _read_all_logs():
    data = []
    try:
        with open(LOG_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['value'] = float(row['value'])
                data.append(row)
    except FileNotFoundError:
        if DEBUG:
            print("Log file not found.")
    return data

def get(sensor_names):
    if isinstance(sensor_names, str):
        sensor_names = [s.strip() for s in sensor_names.split(",")]
    data = _read_all_logs()
    return [row for row in data if row['sensor'] in sensor_names]

def calculate_stats(sensor_name, mode=None):
    readings = get(sensor_name)
    if not readings:
        return None
    values = [r['value'] for r in readings]
    stats = {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values)
    }
    return {mode: stats[mode]} if mode else stats

def get_range(sensor_name, start_time, end_time):
    readings = get(sensor_name)
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    return [
        r for r in readings
        if start <= datetime.fromisoformat(r['timestamp']) <= end
    ]

def export_to_json(sensor_name, filename):
    data = get(sensor_name)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_fields(sensor_name):
    readings = get(sensor_name)
    return sorted(set(r['field'] for r in readings))

def all_sensors():
    data = _read_all_logs()
    return sorted(set(row['sensor'] for row in data))

def get_latest(sensor_name=None):
    data = _read_all_logs()
    filtered = [row for row in data if (sensor_name is None or row["sensor"] == sensor_name)]
    return filtered[-1] if filtered else None

def get_delta(sensor_name):
    readings = get(sensor_name)
    if len(readings) < 2:
        return None
    return readings[-1]['value'] - readings[-2]['value']

def get_trend(sensor_name):
    return [(r["timestamp"], r["value"]) for r in get(sensor_name)]

def get_by_field(sensor_name, field_value):
    return [r for r in get(sensor_name) if r['field'] == field_value]

def load_file(filepath):
    global LOG_FILE
    if os.path.exists(filepath):
        LOG_FILE = filepath
        return True
    return False

def save_subset(sensor_name, filename):
    readings = get(sensor_name)
    if not readings:
        return False
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=readings[0].keys())
        writer.writeheader()
        writer.writerows(readings)
    return True

def append_csv(newfile):
    if not os.path.exists(newfile):
        return False
    base = _read_all_logs()
    with open(newfile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['value'] = float(row['value'])
            base.append(row)
    with open(LOG_FILE, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=base[0].keys())
        writer.writeheader()
        writer.writerows(base)
    return True

def rm_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def memstats():
    try:
        with open(LOG_FILE, 'rb') as f:
            size = len(f.read())
        return {
            "file": LOG_FILE,
            "rows": len(_read_all_logs()),
            "size_kb": size // 1024
        }
    except Exception:
        return None

def graph(plot_type, sensor_names, x_field, y_field):
    data = _read_all_logs()
    sensor_list = [s.strip() for s in sensor_names.split(",")]
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    for idx, sensor in enumerate(sensor_list):
        series = [(row[x_field], row[y_field]) for row in data if row['sensor'] == sensor]
        if not series:
            continue
        x_vals, y_vals = zip(*series)
        if plot_type == "line":
            plt.plot(x_vals, y_vals, label=sensor, color=colors[idx % len(colors)])
        elif plot_type == "bar":
            plt.bar(x_vals, y_vals, label=sensor, color=colors[idx % len(colors)])
    plt.legend()
    plt.xlabel(x_field)
    plt.ylabel(y_field)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def ping():
    return "pong"

def version():
    return "SensorCLI v1.2 | Graph & FileTools Build"

def set_debug(state):
    global DEBUG
    DEBUG = (state == "on")
def help_menu():
    print("""
    Available Commands:

    get <sensor[,sensor2,...]>             → Get readings
    stats <sensor> [min/max/avg]           → Show stats
    range <sensor> <start> <end>           → Data in time range
    export <sensor> <filename>             → Export JSON
    fields <sensor>                        → List fields
    sensors                                → List all sensors
    latest [sensor]                        → Latest reading
    delta <sensor>                         → Latest - previous
    trend <sensor>                         → Show value trend
    field <sensor> <tag>                   → Filter by field
    graph <type> <sensors> <x> <y>         → Plot data (type = line/bar)
    load <file>                            → Load another log
    save <sensor> <filename>               → Save subset to CSV
    append <file>                          → Append CSV to current
    rm <file>                              → Delete file
    mem                                    → Show memory stats
    ping                                   → Sanity check
    version                                → Show CLI version
    debug <on/off>                         → Toggle debug mode
    help                                   → Show this menu
    exit                                   → Quit
    """)
