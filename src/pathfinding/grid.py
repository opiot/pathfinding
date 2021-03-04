from dataclasses import dataclass
from typing import Dict
from dataclasses import field


@dataclass
class Point:
    x: int
    y: int
    topography: str = "?"

    def is_crossing(self):
        return self.topography == "."

    def neighbors(self):
        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            yield (self.x + x, self.y + y)

    def distance(self, pt) -> int:
        return abs(self.x - pt.x) + abs(self.y - pt.y)

    def __eq__(self, pt) -> bool:
        return (self.x, self.y) == (pt.x, pt.y)


class Node:
    def __init__(self, point):
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other):
        return 0 if self.point.topography == "." else 1


@dataclass
class Grid:
    h: int
    w: int
    points: Dict = field(default_factory=dict)

    def neighbors(self, pt: Point) -> Point:
        for x, y in pt.neighbors():
            if (x, y) not in self.points:
                continue

            yield self.points[(x, y)]

    def get(self, x, y):
        return self.points.get((x, y))

    def add(self, x, y, t):
        self.points[(x, y)] = Point(x, y, t)

    def load(self, maze):
        for x, row in enumerate(maze.splitlines()):
            for y, topo in enumerate(row):
                self.add(x, y, topo)

    def move(self, from_point, to_point):
        return []

    def astar(self, start, goal):
        # The open and closed sets
        openset = set()
        closedset = set()
        current = Node(start)
        # Add the starting point to the open set
        openset.add(current)
        # While the open set is not empty
        while openset:
            # Find the item in the open set with the lowest G + H score
            current = min(openset, key=lambda o: o.G + o.H)
            # If it is the item we want, retrace the path and return it
            if current.point == goal:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]
            # Remove the item from the open set
            openset.remove(current)
            # Add it to the closed set
            closedset.add(current)
            # Loop through the node's children/siblings
            for neighbor in self.neighbors(current.point):
                # If it is already in the closed set, skip it
                node = Node(neighbor)
                if node in closedset:
                    continue
                # Otherwise if it is already in the open set
                if node in openset:
                    # Check if we beat the G score
                    new_g = current.G + current.move_cost(node)
                    if node.G > new_g:
                        # If so, update the node to have a new parent
                        node.G = new_g
                        node.parent = current
                else:
                    # If it isn't in the open set,
                    # calculate the G and H score for the node
                    node.G = current.G + current.move_cost(node)
                    node.H = node.point.distance(goal)
                    # Set the parent to our current item
                    node.parent = current
                    # Add it to the set
                    openset.add(node)
        # Throw an exception if there is no path
        return []


if __name__ == "__main__":
    maze = """##########
#...#....#
###.##.#.#
#.#..###.#
#.##.#...#
#..#.###.#
#.##...#.#
#..###.#.#
#........#
##########"""

    h = len(maze.splitlines())
    w = len(maze.splitlines()[0])

    grid = Grid(h, w)

    grid.load(maze)

    start = grid.get(1, 1)
    end = grid.get(1, 2)
    # o = grid.get(1, 1)

    # for pt in grid.neighbors(o):
    #     print("{}".format(pt))
    #     print("distance {}".format(o.distance(pt)))

    path = grid.astar(start, end)
    for node in path:
        print(node.point)
