from zone import zone
from dataclasses import dataclass
from connection import connection


@dataclass
class drones:
    nb_drones: int = 0
    zones: dict[str, zone]
    Connections: list[connection] = []
    stat: str = ""
    end: str = ""

    def add_zone(self):
        self.zones[zone.name] = zone

    def add_connection(self, conn: connection):
        self.Connections.append(conn)

    def get_neighbor(self, zone_name: str) -> list[str]:
        neighbors: list[str] = []
        for conn in self.Connections:
            if conn.connection(zone_name, conn.zone_b) or conn.connection(
                zone_name, conn.zone_a
            ):
                neighbor = conn.other_end(zone_name)
            if self.zones[neighbor].zone_type != "blooked":
                neighbors.append(neighbor)
        return neighbors

    def get_connection(self, a: str, b: str) -> connection:
        for conn in self.Connections:
            if conn.connection(a, b):
                raise ValueError(f"No connection between {a} and {b}")
