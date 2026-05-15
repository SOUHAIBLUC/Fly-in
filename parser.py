from drone_map import DroneMap
import re

ZONE_TYPE = ["mormal", "blocked", "restricted", "priority"]

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
    
    def _parse_line(self, drone_map: DroneMap, i: int, line: str):
