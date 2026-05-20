from drone_map import DroneMap
from zone import Zone, VALID_ZONE_TYPE
from connection import Connection
import re


class Parse:
    def parse(self, filepath: str) -> DroneMap:
        drone_map = DroneMap()
        with open(filepath) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                self._parse_line(drone_map, i, line)
        return drone_map

    def _parse_metadata(self, line: str) -> dict[str, str]:
        result: dict[str, str] = {}
        match = re.search(r"\[([^\]]*)\]", line)
        if match:
            for tag in match.group(1).split():
                if "=" in tag:
                    k, v = tag.split("=", 1)
                    result[k] = v
        return result

    def _parse_hub(self, line: str, i: int) -> Zone:
        if ":" in line:
            payload = line.split(":", 1)[1].strip()
        else:
            payload = line.strip()
        meta = self._parse_metadata(line)

        core = payload.split("[", 1)[0].strip()
        tokens = core.replace(",", " ").split()
        if len(tokens) < 3:
            raise ValueError(
                f"Line {i}: invalid hub payload, need 'name x y'"
            )

        name = tokens[0]
        try:
            x = int(tokens[1])
            y = int(tokens[2])
        except Exception:
            raise ValueError(f"Line {i}: invalid coordinates for hub '{line}'")

        zone_type = meta.get("zone", "normal")
        if zone_type not in VALID_ZONE_TYPE:
            raise ValueError(f" {zone_type} is invalid zone type ")

        color = meta.get("color") or meta.get("zone_clore") or "None"

        try:
            max_dron = int(meta.get("max_drones", meta.get("max_dron", 1)))
        except Exception:
            max_dron = 1

        is_start = False
        is_end = False

        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            zone_clore=color,
            max_dron=max_dron,
            is_start=is_start,
            is_end=is_end,
        )

    def _parse_connection(self, line: str, i: int) -> Connection:
        """Parse a connection line and return a Connection object.

        Expected forms (flexible):
        - "A - B [max_link_capacity=2]"
        - "A -> B [max_link_capacity=2]"
        """
        content = line.split("[", 1)[0].strip()
        content = content.replace("->", "-")

        parts = content.split("-", 1)
        if len(parts) != 2:
            raise ValueError(f"Line {i}: invalid connection format: '{line}'")

        a = parts[0].strip()
        b = parts[1].strip()
        if not a or not b:
            raise ValueError(
                f"Line {i}: invalid connection endpoints"
            )

        meta = self._parse_metadata(line)

        limit_meta = meta.get("max_link_capacity", None)
        if limit_meta is None:
            limit_meta = meta.get("limit_max_drone", None)
        if limit_meta is None:
            limit_meta = meta.get("capacity", 1)
        try:
            limit = int(limit_meta)
        except Exception:
            limit = 1

        return Connection(zone_a=a, zone_b=b, limit_max_drone=limit)

    def _parse_line(self, drone_map: DroneMap, i: int, line: str):
        s = line.strip()

        if s.lower().startswith("nb_drones:"):
            payload = s.split(":", 1)[1].strip()
            if not payload.isdigit():
                raise ValueError(f"Line {i}: invalid nb_drones value")
            drone_map.nb_drones = int(payload)
            return

        if s.lower().startswith("start_hub:"):
            zone = self._parse_hub(s, i)
            zone.is_start = True
            drone_map.add_zone(zone)
            drone_map.start = zone.name
            return

        if s.lower().startswith("end_hub:"):
            zone = self._parse_hub(s, i)
            zone.is_end = True
            drone_map.add_zone(zone)
            drone_map.end = zone.name
            return

        if s.lower().startswith("hub:"):
            zone = self._parse_hub(s, i)
            drone_map.add_zone(zone)
            return

        if s.lower().startswith("connection:"):
            payload = s.split(":", 1)[1].strip()
            conn_line = payload
            conn = self._parse_connection(conn_line, i)
            # Validate that both endpoints exist as zones
            if conn.zone_a not in drone_map.zones:
                raise ValueError(f"Line {i}: unknown zone '{conn.zone_a}' in connection '{line}'")
            if conn.zone_b not in drone_map.zones:
                raise ValueError(f"Line {i}: unknown zone '{conn.zone_b}' in connection '{line}'")
            drone_map.add_connection(conn)
            return

        raise ValueError(f"Line {i}: unrecognized line format: '{line}'")
