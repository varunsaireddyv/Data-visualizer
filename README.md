# Modular Sensor Terminal and Visualizer (Python + ESP32)

## Introduction

This project is a modular Python-based terminal and visualizer tool for analyzing sensor logs (CSV format) collected from an ESP32-based sensor hub. It features a full terminal command set for sensor querying, advanced statistics, data export, and live graphing. Designed for both offline analysis and future serial integration with the ESP32 microcontroller.

## Primary Design Goals

- Terminal-first interface with fast command parsing and dynamic execution  
- Graph-ready architecture with line and bar overlay support  
- Modular architecture with clean separation between logic and interface  
- CLI-based for testing, later extendable into GUI or serial-linked tools  

## Features

- Command-line interface with real-time parsing  
- Works with sensor logs in CSV format  
- Supports multi-sensor querying, time filtering, and JSON/CSV export  
- Matplotlib-based graphing (line/bar, multiple overlays supported)  
- File management and memory diagnostics commands  
- Serial communication backend prepared for ESP32 integration  

## Sample CSV Format

```csv
timestamp,sensor,value,field
2025-07-06T12:00:00,temp,26.3,room
2025-07-06T12:00:05,temp,26.8,room
2025-07-06T12:00:10,humid,45.2,room
```

## Command Reference

| Command                             | Description                                              |
|-------------------------------------|----------------------------------------------------------|
| `get <sensor>`                      | Get data for one or more sensors                         |
| `stats <sensor>`                    | Get min, max, and average values                         |
| `stats <sensor> <mode>`             | Get a specific stat (min/max/avg)                        |
| `range <sensor> <start> <end>`      | Filter data by timestamp range (ISO format)             |
| `fields <sensor>`                   | Show all fields for a given sensor                      |
| `all_sensors`                       | List all available sensors                              |
| `export <sensor> <file>`            | Export data to a JSON file                              |
| `graph <type> <sensor(s)> <x> <y>`  | Plot line/bar graph for sensor(s) vs timestamp/value     |
| `mem`                               | Print file stats, row count, and memory usage           |
| `debug`                             | Toggle debug mode                                       |
| `help`                              | Show command list                                       |
| `exit`                              | Quit the program                                        |

## Graph Command Format

```bash
graph line temp,humid timestamp value
graph bar sound timestamp value
```

- `<type>`: `line` or `bar`  
- `<sensor(s)>`: comma-separated list of sensor names  
- `<x>`: field for x-axis (usually `timestamp`)  
- `<y>`: field for y-axis (usually `value`)  

Line plot colors default to red, blue, green for the first three sensors. Additional sensors use matplotlib’s default cycle.

## Dependencies

- Python 3.9+  
- `matplotlib` for plotting (`pip install matplotlib`)  
- `pyserial` for ESP32 integration (`pip install pyserial`)  

## License

This project is licensed under the MIT License.  
You may modify, distribute, or integrate this system in your own applications.

## Contact

For questions or collaborations:  
**Varun Sai**  
**Email:** varunbillas@gmail.com
