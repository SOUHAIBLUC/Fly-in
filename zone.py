from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

VALID_ZONE_TYPE = {"normal", "blocked", "restricted", "priority"}


@dataclass
class zone:
    "single zone (node) in the drone network."

    name: str
    x: int
    y: int
    zone_type: str = "normal"
    zone_clore: Optional[str] = "None"
    max_dron: int = 1
    is_end: bool = False
    is_start: bool = False

    def movement_cost(self) -> int:
        if self.name == "restricted":
            return 2
        if self.name == "blocked":
            return 9999
        return 1

    def __print__(self) -> str:
        return f"zone({self.name}, {self.zone_type})"
