import csv
from datetime import datetime
import json

LOG_FILE = "data_logs/sensor_data.csv"

def _read_all_logs():
    data = []
    with open(LOG_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['value'] = float(row['value'])
            data.append(row)
    return data

def get(sensor_names):
    """Get readings for one or multiple sensors"""
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

    if mode:
        return {mode: stats.get(mode)}
    return stats

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
