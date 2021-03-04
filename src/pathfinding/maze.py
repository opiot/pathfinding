from typing import Tuple
from typing import List
from typing import Iterator
from typing import Optional
from typing import Dict
from typing import TypeVar
import heapq


H = 10
W = 30

Location = Tuple[int, int]
T = TypeVar("T")


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[Location] = []
        self.unknown: List[Location] = []
        self.weights: Dict[Location, int] = {}

    def in_bounds(self, id: Location) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: Location) -> bool:
        return id not in self.walls + self.unknown

    def neighbors(self, id: Location) -> Iterator[Location]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node: Location, to_node: Location) -> int:
        return self.weights.get(to_node, 1)


def heuristic(a: Location, b: Location) -> int:
    # Manathan Disctance
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[int, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: int):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def a_star_search(grid: Grid, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(
    came_from: Dict[Location, Location], start: Location, goal: Location
) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        try:
            path.append(current)
            current = came_from[current]
        except KeyError:
            return []

    return path


def main():

    maze = """??????????????
?###########??
?#..........??
?###########??
??????????????
"""
    h = len(maze.splitlines())
    w = len(maze.splitlines()[0])

    # start = (3, 3)

    grid = Grid(h, w)
    for x, row in enumerate(maze.splitlines()):
        for y, c in enumerate(row):
            if c == "#":
                grid.walls += [(x, y)]
            if c == "?":
                grid.unknown += [(x, y)]


if __name__ == "__main__":
    main()
