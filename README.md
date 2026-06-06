This project has been created as part of the 42 curriculum by so-ait-l.

# Fly-in — Drone Pathfinding & Simulation

## Description

Fly-in is a small Python project that simulates multiple drones navigating a network
of hubs (zones) and connections. The program reads a simple text map describing
zones, their types and coordinates, and connections with capacity limits, then
computes paths and simulates drones moving from a defined start hub to an end hub.

The primary goal is to model constrained movement (zone capacity, connection
limits and movement cost) and to demonstrate a pathfinding + simulation pipeline
that can be extended or visualized further.

## Instructions

- Requirements: Python 3.8+.
- The project root contains a `Makefile` to automate common tasks (install,
  run, debug, clean, lint).

Basic usage:

1. Install dependencies (will use `requirements.txt` if present, otherwise
   installs `flake8` and `mypy`):

```bash
make install
```

2. Run the simulator with a map file (example `map.txt` provided):

```bash
make run
# Or directly:
python main.py map.txt
```

3. Debug with Python's pdb:

```bash
make debug
```

4. Clean caches and generated files:

```bash
make clean
```

5. Run linters:

```bash
make lint
make lint-strict
```

Command-line expectations: `main.py` expects a path to a map file as its
first argument. Map lines define `nb_drones`, `hub`, `start_hub`, `end_hub`, and
`connection` entries. See `map.txt` for an example.

## Algorithm choices and implementation strategy

- Pathfinding algorithm: A* search is used to find shortest paths between the
  start and end hubs. The `PathFinder` implementation uses a Manhattan distance
  heuristic (|dx| + |dy|) which is admissible for orthogonal grid-like maps and
  is cheap to compute.
- Cost model: Each `Zone` provides a `movement_cost()`:
  - `normal` zones cost 1
  - `restricted` zones cost 2
  - `blocked` zones are effectively impassable (very high cost)

- Data structures:
  - `DroneMap` holds zone objects and `Connection` objects and provides neighbor
    lookup.
  - `Zone` is a dataclass containing coordinates, zone type, capacity and flags
    for start/end.
  - `Connection` objects track current usage and a `limit_max_drone` capacity.

- Simulation strategy:
  1. Compute a reference path for drones with the `PathFinder`.
  2. Instantiate `nb_drones` `Drone` objects sharing the reference path.
  3. On each turn, attempt to move each drone to its next zone if:
     - the next zone has free capacity (zone-level limit), and
     - the connection between current and next zone has available capacity.
  4. Movement increments connection usage for that turn; connections are
     reset at the start of each new turn.
  5. Zones with higher movement cost impose extra turns in transit for drones,
     modeling slower traversal.

This strategy keeps simulation logic simple and deterministic, and concentrates
constraints into zone and connection objects so the system is easy to extend.

## Visual representation features

- Terminal colorization: The simulator color-codes moves in the terminal output
  using ANSI color codes depending on zone type:
  - `normal`: light/white
  - `restricted`: red
  - `priority`: green
  - `blocked`: magenta
  - `end` zone highlighted in yellow

- Output format: Each turn prints a list of moves like `D1-B D2-C` where each
  token denotes a drone id and the destination zone. Colors make it easy to see
  when drones move through restricted or priority areas, improving readability
  for quick demos and debugging.

These choices provide a compact, human-readable visualization suitable for
terminals without depending on heavyweight GUI libraries. If you want a richer
visualization (graphical map or animated simulation), the code is organized so
the simulation core can be reused and plugged into a renderer.

## Resources

- A* search algorithm: Hart, Nilsson and Raphael — "A Formal Basis for the
  Heuristic Determination of Minimum Cost Paths" (classic paper and references)
- Heuristic design (Manhattan distance): discussion in numerous algorithm
  tutorials (e.g., Red Blob Games pathfinding guide)
- Python documentation: https://docs.python.org/3/
- 42 curriculum: check your school's internal resources and project subject

AI usage disclosure

This repository used AI assistance for the following tasks:
- Generating project automation: `Makefile` was created with the help of an
  AI assistant to standardize install/run/debug/clean/lint targets.
- Writing documentation: This `README.md` was drafted with AI help to
  summarize the project, provide example usage, and explain algorithmic choices.

AI was not used to write core algorithm logic or simulation code — the
implementation files (`parser.py`, `pathefinder.py`, `simulator.py`, etc.) were
authored or reviewed by the developer. The AI contributions listed above were
limited to auxiliary project files and documentation.

## Extending the project

- Add alternative pathfinding strategies (Dijkstra, multi-agent cooperative
  routing) by implementing new classes that reuse the `DroneMap` API.
- Add a GUI or export traces for visualization in a browser / plotting tool.
- Add unit tests and CI to run `make lint` and `make test` (if tests are added).

## Contact

If you have questions, open an issue or reach out to the repository owner.
# Fly-in
Drones are interesting.
