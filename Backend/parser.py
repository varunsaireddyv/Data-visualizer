from datetime import datetime

### edit folowing feilds based on your ESP logging Format ###

# Key used for ESP timestamp, e.g. ts=2025-06-25T23:00:00
TIMESTAMP_KEY = "ts"

# Character that splits sensor name from its field (like 'gyro_x')
SENSOR_FIELD_SEPARATOR = "_"

# Default field name if no separator is present
DEFAULT_FIELD_NAME = "value"



# Main praser funtions

def parse_sensor_data(raw_line: str) -> list:
    """
    Parses an ESP32 serial line into a list of structured readings.
    
    Each reading is a dict: {
        'timestamp': "...",
        'sensor': "...",
        'field': "...",
        'value': float
    }
    """
    readings = []
    timestamp = datetime.now().isoformat()

    try:
        pairs = raw_line.strip().split(',')

        for pair in pairs:
            if '=' not in pair:
                continue

            key, val = pair.split('=')
            key = key.strip()
            val = val.strip()

            if key == TIMESTAMP_KEY:
                timestamp = val
                continue

            sensor, field = split_sensor_field(key)
            value = float(val)

            readings.append({
                "timestamp": timestamp,
                "sensor": sensor,
                "field": field,
                "value": value
            })

    except Exception as e:
        print(f"[Parser Error] Failed to parse: '{raw_line}' → {e}")
    
    return readings

def split_sensor_field(key: str):
    """
    Splits keys like 'gyro_x' → ('gyro', 'x')
    If no separator is found, returns (key, DEFAULT_FIELD_NAME)
    """
    parts = key.split(SENSOR_FIELD_SEPARATOR, 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return key, DEFAULT_FIELD_NAME
