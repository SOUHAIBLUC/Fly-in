from zone import Zone
from connection import Connection


class DroneMap:
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.zones: dict[str, Zone] = {}
        self.Connections: list[Connection] = []
        self.start: str = ""
        self.end: str = ""

    def add_zone(self, zone: Zone) -> None:
        if zone.name in self.zones:
            raise ValueError(f"Zone '{zone.name}' is already defined")
        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        self.Connections.append(conn)

    def get_neighbor(self, zone_name: str) -> list[str]:
        neighbors: list[str] = []
        seen: set[str] = set()
        for conn in self.Connections:
            if conn.zone_a == zone_name:
                neighbor = conn.zone_b
            elif conn.zone_b == zone_name:
                neighbor = conn.zone_a
            else:
                continue

            zone = self.zones.get(neighbor)
            if zone is None:
                continue
            if zone.zone_type != "blocked" and neighbor not in seen:
                neighbors.append(neighbor)
                seen.add(neighbor)

        return neighbors

    def get_connection(self, a: str, b: str) -> Connection:
        for conn in self.Connections:
            if conn.connection_zone(a, b):
                return conn
        raise ValueError(f"No connection between {a} and {b}")
