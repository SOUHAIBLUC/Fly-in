import os
import sys

from parser import Parse
from pathefinder import PathFinder
from simulator import Simulator


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <map_file>")
        return

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return

    drone_map = Parse().parse(filepath)
    pathfinder = PathFinder(drone_map)
    simulator = Simulator(drone_map, pathfinder)
    simulator.run()


if __name__ == "__main__":
    main()
