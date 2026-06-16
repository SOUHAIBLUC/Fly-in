import os
import sys

from parser import Parse
from pathefinder import PathFinder
from simulator import Simulator


def main() -> None:
    capacity_info = False
    if len(sys.argv) < 2:
        print("Usage: python main.py <map_file>")
        return
    if len(sys.argv) == 3:
        filepath = sys.argv[2]
        if sys.argv[1] == "--capacity-info":
            capacity_info = True

    elif len(sys.argv) == 2:
        filepath = sys.argv[1]
        if not os.path.isfile(filepath):
            print(f"File not found: {filepath}")
            return
    try:
        drone_map = Parse().parse(filepath)
        pathfinder = PathFinder(drone_map)
        simulator = Simulator(drone_map, pathfinder, capacity_info)
        simulator.run()
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
