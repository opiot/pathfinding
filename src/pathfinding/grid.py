import sys
from dataclasses import dataclass
from typing import Dict
from dataclasses import field
from random import choice


@dataclass
class Point:
    x: int
    y: int
    topography: str = "?"

    def is_crossing(self):
        return self.topography == "."

    def is_blocked(self):
        return self.topography in ["#", "?"]

    def neighbors(self):
        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            yield (self.x + x, self.y + y)

    def around(self):
        for x in range(-1,2):
            for y in range(-1,2):
                if (x, y) == (0, 0):
                    continue
                yield (self.x + x, self.y + y)

    def direction(self, pt) -> str:
        if pt.x - self.x == 1:
            return "DOWN"
        if pt.x - self.x == -1:
            return "UP"        
        if pt.y - self.y == 1:
            return "RIGHT"
        if pt.y - self.y == -1:
            return "LEFT"                   

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

    def __eq__(self, node) -> bool:
        return self.point == node.point

    def __hash__(self):
        return hash((self.point.x, self.point.y))        


@dataclass
class Grid:
    h: int
    w: int
    alarm: int = 65536
    scan: bool = True
    back: bool = False
    _gate = None
    _room = None
    points: Dict = field(default_factory=dict)

    def neighbors(self, pt: Point, walk=False) -> Point:
        for x, y in pt.neighbors():
            if (x, y) not in self.points:
                continue
            if walk and self.get(x, y).is_blocked():
                continue

            yield self.get(x, y)


    def unknown(self, pt: Point) -> Point:
        for x, y in pt.neighbors():
            if (x, y) not in self.points:
                continue
            if self.get(x, y).topography == "?":
                return True        

        return False


    def incognita(self) -> Point:
        for pt in self.points.values():
            if pt.topography != ".":
                continue
            
            if self.unknown(pt):
                yield pt


    def explore(self, pt: Point) -> Point:
        pts = {}
        for i in self.incognita():
            path = self.astar(pt, i)
            if len(path) > 0:
                pts[len(path)] = pts.get(len(path),[]) + [i]

        if not pts:
            return []

        destinations = pts[min(pts.keys())]
        return(choice(destinations))


    def move(self, pt: Point) -> str:
        
        if self.room() and self.room() == pt:
            self.back = True
        
        if self.room() and self.gate() and self.scan:
            distance = len(self.astar(self.room(), self.gate())) - 1
            print("distance: {} alarm: {}".format(distance, self.alarm), file=sys.stderr, flush=True)
            if distance < 0:
                pass
            elif distance <= self.alarm:
                self.scan = False

        print("scan: {}, back: {}".format(self.scan, self.back), file=sys.stderr, flush=True)        
        if not self.scan and not self.back:
            goal = self.room()
        
        elif self.back:
            goal = self.gate()   
           
        else:
            goal = self.explore(pt)

        print("goal: {}".format(goal), file=sys.stderr, flush=True) 


        
        for node in self.astar(pt, goal):
            if pt == node.point:
                continue
            return pt.direction(node.point)


    def get(self, x, y):
        return self.points.get((x, y))

    def add(self, x, y, t):
        self.points[(x, y)] = Point(x, y, t)

    def load(self, maze):
        for x, row in enumerate(maze.splitlines()):
            for y, topo in enumerate(row):
                if topo == "T":
                    self._gate = (x, y)
                    self.add(x, y, ".")
                    continue

                if topo == "C":
                    self._room = (x, y)
                    if not self.scan:
                        self.add(x, y, ".")
                        continue
                self.add(x, y, topo)

    def load(self, maze):
        for x, row in enumerate(maze):
            for y, topo in enumerate(row):
                if topo == "T":
                    self._gate = (x, y)
                    self.add(x, y, ".")
                    continue

                if topo == "C":
                    self._room = (x, y)
                    if not self.scan:
                        self.add(x, y, ".")
                        continue
                self.add(x, y, topo)


    def room(self):
        return self.points.get(self._room)


    def gate(self):
        return self.points.get(self._gate)

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
            for neighbor in self.neighbors(current.point, walk=True):
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

    def __str__(self) -> str:
        grid = ""
        row = 0
        for (x, _), pt in self.points.items():
            if row != x:
                grid += "\n"
                row = x
            grid += pt.topography
        return grid


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

    print(grid)

    pt = Point(0, 0, ".")
    print([a for a in pt.around()])
