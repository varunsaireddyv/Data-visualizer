import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from cmnds import *

def main():
    print(" Sensor Terminal (type 'help' for commands)")
    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd:
                continue

            parts = cmd.split()
            command = parts[0].lower()
            args = parts[1:]

            match command:
                case "get":
                    for r in get(",".join(args)):
                        print(r)

                case "stats":
                    if len(args) == 1:
                        print(calculate_stats(args[0]))
                    elif len(args) == 2:
                        print(calculate_stats(args[0], args[1]))
                    else:
                        print("Usage: stats <sensor> [min/max/avg]")

                case "range":
                    if len(args) != 3:
                        print("Usage: range <sensor> <start> <end>")
                    else:
                        for r in get_range(args[0], args[1], args[2]):
                            print(r)

                case "export":
                    export_to_json(args[0], args[1])
                    print(f"Exported to {args[1]}")

                case "fields":
                    print("Fields:", get_fields(args[0]))

                case "sensors":
                    print("Sensors:", all_sensors())

                case "latest":
                    sensor = args[0] if args else None
                    print(get_latest(sensor))

                case "delta":
                    print("Delta:", get_delta(args[0]))

                case "trend":
                    for point in get_trend(args[0]):
                        print(point)

                case "field":
                    for r in get_by_field(args[0], args[1]):
                        print(r)

                case "graph":
                    if len(args) != 4:
                        print("Usage: graph <line/bar> <sensor[,]> <x> <y>")
                    else:
                        graph(args[0], args[1], args[2], args[3])

                case "load":
                    print("Loaded." if load_file(args[0]) else "File not found.")

                case "save":
                    print("Saved." if save_subset(args[0], args[1]) else "Failed.")

                case "append":
                    print("Appended." if append_csv(args[0]) else "Failed.")

                case "rm":
                    print("Deleted." if rm_file(args[0]) else "File not found.")

                case "mem":
                    print("Memory stats:", memstats())

                case "ping":
                    print("pong")

                case "version":
                    print(version())

                case "debug":
                    set_debug(args[0])
                    print(f"Debug mode: {args[0]}")

                case "help":
                    help_menu()

                case "exit":
                    print(" Exiting.")
                    break

                case _:
                    print(" Unknown command. Type 'help' to see available commands.")

        except (IndexError, ValueError) as e:
            print(f" Error: {e}")
            print("Tip: Type 'help' to view valid usage.")
        except KeyboardInterrupt:
            print("\n Ctrl+C received. Exiting.")
            break

if __name__ == "__main__":
    main()