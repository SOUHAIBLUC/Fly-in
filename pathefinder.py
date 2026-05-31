from __future__ import annotations
import heapq
from typing import Any

from drone_map import DroneMap
from parser import Parse


class PathFinder:
    """Path finder using A* and alternative shortest path strategies."""

    def __init__(self, drone_map: DroneMap):
        self.drone_map = drone_map

    @classmethod
    def from_file(cls, filepath: str) -> "PathFinder":
        """Load a map from a file and create a path finder."""
        return cls(Parse().parse(filepath))

    def heuristic(self, a: str, b: str) -> int:
        """Use Manhattan distance as the heuristic between two zones."""
        zone_a = self.drone_map.zones[a]
        zone_b = self.drone_map.zones[b]
        return abs(zone_a.x - zone_b.x) + abs(zone_a.y - zone_b.y)
    def find_path(self , star_zone, end_zone):
        open_heap : list[tuple[str, int]] = []
        heapq.heappush(open_heap, (0, star_zone))

        g_score: dict[str, int] = {star_zone: 0}
        came_from: dict[str, str] = {}
        closed_set: set[str] = set()
        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current == end_zone:
                return self.reconstruct_path(came_from, current)
            if current in closed_set:
                continue
            closed_set.add(current)

            for neighbor in self.drone_map.get_neighbor(current):
                if neighbor in closed_set:
                    continue

                new_g_score = g_score[current] + self.drone_map.zones[neighbor].movement_cost()
                if new_g_score < g_score.get(neighbor, 10**9):
                    came_from[neighbor] = current
                    g_score[neighbor] = new_g_score
                    f = new_g_score + (self.heuristic(neighbor, end_zone))
                    heapq.heappush(open_heap, (f, neighbor))

        return []
    
    def reconstruct_path(self, came_from: dict[str, str], current: str) -> list[str]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
    