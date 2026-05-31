from __future__ import annotations
from typing import List

from drone_map import DroneMap
from pathefinder import PathFinder


class Drone:
    def __init__(self, drone_id: int, start_zone: str, path: List[str]) -> None:
        self.id: int = drone_id
        self.position: str = start_zone
        self.path: List[str] = list(path)
        self.done: bool = False
        self.turns_in_transit: int = 0

    def next_zone(self) -> str | None:
        return self.path[0] if self.path else None

class Simulator:
    def __init__(self, drone_map: DroneMap, pathfinder: PathFinder) -> None:
        self.drone_map = drone_map
        self.pathfinder = pathfinder
        self.zone_occupancy: dict[str, int] = {
            zone_name: 0 for zone_name in self.drone_map.zones
        }

    def _create_drones(self) -> List[Drone]:
        if not self.drone_map.start or not self.drone_map.end:
            raise ValueError("Map must define both start and end zones")

        full_path = self.pathfinder.find_path(self.drone_map.start, self.drone_map.end)
        if not full_path:
            raise ValueError("No path from start to end")

        if full_path[0] == self.drone_map.start:
            drone_path = full_path[1:]
        else:
            drone_path = full_path[:]

        drones: List[Drone] = []
        for drone_id in range(1, self.drone_map.nb_drones + 1):
            drones.append(Drone(drone_id, self.drone_map.start, drone_path))

        self.zone_occupancy[self.drone_map.start] = len(drones)
        return drones
    
    def _can_move(self, drone: Drone, next_zone: str) -> bool:
        zone = self.drone_map.zones[next_zone]
        if self.zone_occupancy[next_zone] >= zone.max_dron:
            return False

        connection = self.drone_map.get_connection(drone.position, next_zone)
        return connection.avilable_connection()

    def _move_drone(self, drone: Drone, next_zone: str) -> None:
        connection = self.drone_map.get_connection(drone.position, next_zone)
        connection.current_use += 1

        self.zone_occupancy[drone.position] -= 1
        self.zone_occupancy[next_zone] += 1

        drone.position = next_zone
        drone.path.pop(0)

        if self.drone_map.zones[next_zone].zone_type == "restricted":
            drone.turns_in_transit = 1

        if next_zone == self.drone_map.end:
            drone.done = True

    def _reset_connections(self) -> None:
        for connection in self.drone_map.Connections:
            connection.reset_usage()

    def run(self) -> None:
        drones = self._create_drones()
        turn = 0

        while not all(drone.done for drone in drones):
            turn += 1
            self._reset_connections()
            moves: List[str] = []

            for drone in drones:
                if drone.done:
                    continue

                if drone.turns_in_transit > 0:
                    drone.turns_in_transit -= 1
                    moves.append(f"Drone {drone.id} waits in {drone.position}")
                    continue

                next_zone = drone.next_zone()
                if next_zone is None:
                    drone.done = True
                    continue

                if self._can_move(drone, next_zone):
                    previous_zone = drone.position
                    self._move_drone(drone, next_zone)
                    moves.append(
                        f"Drone {drone.id} moved from {previous_zone} to {next_zone}"
                    )
                else:
                    moves.append(f"Drone {drone.id} waits in {drone.position}")

            print(f"Turn {turn}: {', '.join(moves)}")

        print("All drones have arrived.")