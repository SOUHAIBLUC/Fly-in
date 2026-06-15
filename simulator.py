from __future__ import annotations
from typing import List
from drone_map import DroneMap
from pathefinder import PathFinder


class Drone:
    def __init__(
        self,
        drone_id: int,
        start_zone: str,
        path: List[str]
    ) -> None:
        self.id: int = drone_id
        self.position: str = start_zone
        self.path: List[str] = list(path)
        self.done: bool = False
        self.turns_in_transit: int = 0
        self.pending_zone: str | None = None

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

        full_path = self.pathfinder.find_path(
            self.drone_map.start,
            self.drone_map.end
        )

        if not full_path:
            raise ValueError("No path from start to end")

        drone_path = (
            full_path[1:]
            if full_path[0] == self.drone_map.start
            else full_path[:]
        )

        drones: List[Drone] = []

        for drone_id in range(1, self.drone_map.nb_drones + 1):
            drones.append(
                Drone(drone_id, self.drone_map.start, drone_path)
            )

        self.zone_occupancy[self.drone_map.start] = len(drones)
        return drones

    def _can_move(self, drone: Drone, next_zone: str) -> bool:
        if (
            next_zone == self.drone_map.start
            or next_zone == self.drone_map.end
        ):
            connection = self.drone_map.get_connection(
                drone.position,
                next_zone
            )
            return connection.avilable_connection()

        zone = self.drone_map.zones[next_zone]

        if self.zone_occupancy[next_zone] >= zone.max_dron:
            return False

        connection = self.drone_map.get_connection(
            drone.position,
            next_zone
        )

        return connection.avilable_connection()

    def _move_drone(self, drone: Drone, next_zone: str) -> None:
        connection = self.drone_map.get_connection(
            drone.position,
            next_zone
        )

        connection.current_use += 1

        self.zone_occupancy[drone.position] -= 1
        self.zone_occupancy[next_zone] += 1

        drone.position = next_zone
        drone.path.pop(0)

        if next_zone == self.drone_map.end:
            drone.done = True

    def _reset_connections(self) -> None:
        for connection in self.drone_map.Connections:
            connection.reset_usage()

    def _colorize(self, move: str, zone_name: str) -> str:
        zone = self.drone_map.zones.get(zone_name)

        if zone is None:
            return move

        colors = {
            "normal": "\x1b[37m",
            "restricted": "\x1b[31m",
            "priority": "\x1b[32m",
            "blocked": "\x1b[35m",
        }

        color = colors.get(zone.zone_type, "\x1b[37m")

        if zone_name == self.drone_map.end:
            color = "\x1b[33m"

        reset = "\x1b[0m"

        return f"{color}{move}{reset}"

    def run(self) -> None:
        drones = self._create_drones()
        turn = 0

        while not all(drone.done for drone in drones):
            turn += 1
            self._reset_connections()
            moves: List[str] = []

            for drone in drones:

                # 1. Skip completed drones
                if drone.done:
                    continue

                # 2. Finish a restricted move
                if (
                    drone.turns_in_transit > 0
                    and drone.pending_zone is not None
                ):
                    destination = drone.pending_zone

                    self._move_drone(drone, destination)

                    moves.append(
                        self._colorize(
                            f"D{drone.id}-{destination}",
                            destination
                        )
                    )

                    drone.pending_zone = None
                    drone.turns_in_transit -= 1

                    continue

                # 3. Determine next zone
                next_zone = drone.next_zone()

                if next_zone is None:
                    drone.done = True
                    continue

                if not self._can_move(drone, next_zone):
                    continue

                zone = self.drone_map.zones[next_zone]

                # 4. Start a restricted move
                if zone.zone_type == "restricted":
                    drone.pending_zone = next_zone
                    drone.turns_in_transit = 1

                    moves.append(
                        self._colorize(
                            f"D{drone.id}({drone.position}->{next_zone})",
                            next_zone
                        )
                    )

                    continue

                # 5. Normal move
                self._move_drone(drone, next_zone)

                moves.append(
                    self._colorize(
                        f"D{drone.id}-{next_zone}",
                        next_zone
                    )
                )

            print(" ".join(moves))

        print("All drones have arrived.")
