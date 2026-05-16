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
        """Parse a zone/hub line and return a Zone object.

        Expected forms (flexible):
        - "Name X Y [type=... color=... max_drones=... start=true]"
        """
        content = line.split("[", 1)[0].strip()
        m = re.match(r"^(\w+)\s+(-?\d+)\s*,?\s*(-?\d+)", content)
        if not m:
            raise ValueError(f"Line {i}: invalid hub format: '{line}'")

        name, xs, ys = m.group(1), m.group(2), m.group(3)
        meta = self._parse_metadata(line)

        zone_type = meta.get("type") or meta.get("zone_type") or "normal"
        if zone_type not in VALID_ZONE_TYPE:
            zone_type = "normal"

        color = meta.get("color") or meta.get("zone_clore") or "None"

        try:
            max_dron = int(meta.get("max_drones", meta.get("max_dron", 1)))
        except Exception:
            max_dron = 1

        _start_val = str(meta.get("start", "")).lower()
        is_start = _start_val in ("1", "true", "yes", "on")
        _end_val = str(meta.get("end", "")).lower()
        is_end = _end_val in ("1", "true", "yes", "on")

        zone = Zone(
            name=name,
            x=int(xs),
            y=int(ys),
            zone_type=zone_type,
            zone_clore=color,
            max_dron=max_dron,
            is_start=is_start,
            is_end=is_end,
        )

        return zone

    def _parse_connection(self, line: str, i: int) -> Connection:
        """Parse a connection line and return a Connection object.

        Expected forms (flexible):
        - "A - B [max_link_capacity=2]"
        - "A -> B [max_link_capacity=2]"
        """
        content = line.split("[", 1)[0].strip()

        m = re.match(r"^(\w+)\s*[-]>\s*(\w+)", content)
        if not m:
            m = re.match(r"^(\w+)\s*-\s*(\w+)", content)
        if not m:
            raise ValueError(f"Line {i}: invalid connection format: '{line}'")

        a, b = m.group(1), m.group(2)
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
        if line.isdigit():
            drone_map.nb_drones = int(line)
            return

        content = line.split("[", 1)[0].strip()
        if re.match(r"^\w+\s+-?\d+\s*,?\s*-?\d+", content):
            zone = self._parse_hub(line, i)
            drone_map.add_zone(zone)
            if zone.is_start:
                drone_map.start = zone.name
            if zone.is_end:
                drone_map.end = zone.name
            return

        _conn_match = re.match(r"^\w+\s*[-]>\s*\w+", content)
        _conn_match2 = re.match(r"^\w+\s*-\s*\w+", content)
        if _conn_match or _conn_match2:
            conn = self._parse_connection(line, i)
            drone_map.add_connection(conn)
            return

        raise ValueError(f"Line {i}: unrecognized line format: '{line}'")
