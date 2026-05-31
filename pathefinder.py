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

    def _reconstruct_path(self, came_from: dict[str, str], current: str) -> list[str]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))

    def _search(self, start: str, end: str, use_heuristic: bool) -> list[str]:
        if start not in self.drone_map.zones:
            raise ValueError(f"Start zone '{start}' not found")
        if end not in self.drone_map.zones:
            raise ValueError(f"End zone '{end}' not found")

        open_heap: list[tuple[int, str]] = []
        heapq.heappush(open_heap, (0, start))

        g_score: dict[str, int] = {start: 0}
        f_score: dict[str, int] = {start: self.heuristic(start, end) if use_heuristic else 0}
        came_from: dict[str, str] = {}
        closed_set: set[str] = set()

        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current == end:
                return self._reconstruct_path(came_from, current)

            if current in closed_set:
                continue
            closed_set.add(current)

            for neighbor in self.drone_map.get_neighbor(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + self.drone_map.zones[neighbor].movement_cost()
                if tentative_g_score < g_score.get(neighbor, 10**9):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + (self.heuristic(neighbor, end) if use_heuristic else 0)
                    heapq.heappush(open_heap, (f_score[neighbor], neighbor))

        return []

    def a_star(self, start: str | None = None, end: str | None = None) -> list[str]:
        """Find a shortest path using A*."""
        start_zone = start or self.drone_map.start
        end_zone = end or self.drone_map.end
        return self._search(start_zone, end_zone, use_heuristic=True)


if __name__ == "__main__":
    finder = PathFinder.from_file("map.txt")
    print("A* path:", finder.find_path("astar"))
    print("Dijkstra path:", finder.find_path("dijkstra"))
