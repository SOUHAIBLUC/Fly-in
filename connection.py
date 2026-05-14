from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Connection:
    zone_a: str
    zone_b: str
    limit_max_drone: int = 1
    current_use: int = 0

    def reset_usage(self) -> None:
        self.current_use = 0

    def avilable_connection(self) -> bool:
        return self.current_use < self.limit_max_drone

    def other_end(self, zone_name: str) -> str:
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        else:
            raise ValueError(f"{zone_name} dose not exist in the conection")

    def connection_zone(self, a: str, b: str) -> bool:
        return (self.zone_a == a and self.zone_b == b) or \
            (self.zone_a == b and self.zone_b == a)
