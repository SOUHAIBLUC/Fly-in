from zone import Zone
from connection import Connection


class DroneMap:
    def __init__(self):
        self.nb_drones: int = 0
        self.zones: dict[str, Zone] = {}
        self.Connections: list[Connection] = []
        self.start: str = ""
        self.end: str = ""

    def add_zone(self, Zone):
        self.zones[Zone.name] = Zone

    def add_connection(self, conn: Connection):
        self.Connections.append(conn)

    def get_neighbor(self, zone_name: str) -> list[str]:
        neighbors: list[str] = []
        for conn in self.Connections:
            if conn.connection_zone(zone_name, conn.zone_b) or \
                conn.connection_zone(
                zone_name, conn.zone_a
            ):
                neighbor = conn.other_end(zone_name)
            if self.zones[neighbor].zone_type != "blocked":
                neighbors.append(neighbor)
        return neighbors

    def get_connection(self, a: str, b: str) -> Connection:
        for conn in self.Connections:
            if conn.connection_zone(a, b):
                return conn
        raise ValueError(f"No connection between {a} and {b}")
