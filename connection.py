from __future__ import annotations
from dataclasses import dataclass


@dataclass
class connection:
    zone_a: str = "Zone_a"
    zone_b: str = "Zone_b"
    limit_max_drone: int
    current_use: int = 0

    def avilable_connection(self) -> bool:
        return self.current_use < self.limit_max_drone

    def other_end(self, zone_name: str) -> str:
        if zone_name == self.zone_a:
            return self.zone_b
        return self.zone_a

    def connection(self, a: str, b: str) -> bool:
        return (self.zone_a == a and self.zone_b == b) or \
            (self.zone_a == b and self.zone_b == a)
