import sys
import math
from random import choice

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
T = TypeVar('T')


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[Location] = []
        self.weights: Dict[Location, int] = {}
    
    def in_bounds(self, id: Location) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: Location) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: Location) -> Iterator[Location]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node: Location, to_node: Location) -> int:
        return self.weights.get(to_node, 1)

def heuristic(a: Location, b: Location) -> int:
    #Manathan Disctance
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

def a_star_search(grid: Maze, start: Location, goal: Location):
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


def dijkstra_search(graph: Maze, start: Location, goal: Location):
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
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far


def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        try:
            path.append(current)
            current = came_from[current]
        except KeyError:
            return []

    return path


class Kirk:
    def __init__(self, r, c, alarm):
        self.max_x = r
        self.max_y = c

        self.x = -1
        self.y = -1
        self.power = 1200
        self.alarm = alarm
        self.grid = []
        self.path = []
        self.gate = None
        self.maze = None
        self.room = None
        self.to_room = True
        self.explore = ""
    
    def position(self, x, y):
        if not self.gate:
            self.gate = (x, y)
        self.x = x
        self.y = y


    def analyze_map(self, rows):
        self.maze = Maze(self.max_x, self.max_y)
        self.grid = rows
        walls = []
        for x, row in enumerate(self.grid):
            # print("{}: {}".format(i, row), file=sys.stderr, flush=True)
            for y, c in enumerate(row):
                if c == "?" or c == "#":
                    walls += [(x,y)]
                    continue
                if c == "C":
                    self.room = (x, y)
        self.maze.walls = walls
                    





    def up(self):
        m = "UP"
        x = self.x - 1
        y = self.y
        scan_x = max(0, x - 2)
        min_y = max(0, y - 2)
        max_y = min(self.max_y, y + 3)
        w = -1
        if x < 0:
            return -1, m
        
        if self.grid[x][y] in ["#", "C"]:
            return -1, m

        area = self.grid[scan_x][min_y:max_y]
        w = len([s for s in area if s == "?"])
        return w, m

    def down(self):
        m = "DOWN"
        x = self.x + 1
        y = self.y
        scan_x = min(self.max_x - 1, x + 2)
        min_y = max(0, y - 2)
        max_y = min(self.max_y, y + 3)
        w = -1
        if x == self.max_x:
            return -1, m
        
        if self.grid[x][y] in ["#", "C"]:
            return -1, m        
        area = self.grid[scan_x][min_y:max_y]
        w = len([s for s in area if s == "?"])
        return w , m


    def left(self):
        m = "LEFT"
        x = self.x
        y = self.y - 1
        scan_y = max(0, y - 2)
        min_x = max(0, x - 2)
        max_x = min(self.max_x, x + 3)
        w = -1

        if y < 0:
            return -1, m
        
        if self.grid[x][y] in ["#", "C"]:
            return -1, m

        area = [c[scan_y] for c in self.grid[min_x:max_x]]
        w = len([s for s in area if s == "?"])
        return w, m

    def right(self):
        m = "RIGHT"
        x = self.x
        y = self.y + 1
        scan_y = min(self.max_y-1, y + 2)
        min_x = max(0, x - 2)
        max_x = min(self.max_x, x + 3)

        if y == self.max_y:
            return -1, m
        
        if self.grid[x][y] in ["#", "C"]:
            return -1, m
            
        area = [c[scan_y] for c in self.grid[min_x:max_x]]
        w = len([s for s in area if s == "?"])
        return w, m

    def find_path(self, start, end):
        # came_from, cost_so_far = a_star_search(self.maze, start, end)
        came_from, cost_so_far = dijkstra_search(self.maze, start, end)
        
        path = reconstruct_path(came_from, start, end)
        return path

    def move(self):
        moves = {}


        if self.grid[self.x][self.y] == "C":
            for rows in self.grid:
                print("{}".format(rows), file=sys.stderr, flush=True)
            
            self.to_room = False
            self.path = self.find_path((self.x, self.y), self.gate)
            print("GATE {}: path {}".format(self.gate, self.path), file=sys.stderr, flush=True)
        if self.to_room and self.room and not self.path:
            path = self.find_path(self.room, self.gate)
            print("ROOM {}: path {} alarm {}".format(self.room, len(path), self.alarm), file=sys.stderr, flush=True)
            if len(path) <= self.alarm:
                self.path = self.find_path((self.x, self.y), self.room)
                print("ROOM {}: path {}".format(self.room, self.path), file=sys.stderr, flush=True)


        if not self.path:
            for w, m in [self.up(), self.down(), self.left(), self.right()]:
                if not w in moves:
                    moves[w] = [m]
                    continue
                moves[w] += [m]
            self.power -= 1
            directions = moves[max(moves.keys())]
            if max(moves.keys()) == 0 and len(directions) > 1:
                if self.explore == "DOWN":
                    directions.remove("UP")
                if self.explore == "UP":
                    directions.remove("DOWN")
                if self.explore == "RIGHT":
                    directions.remove("LEFT")
                if self.explore == "LEFT":
                    directions.remove("RIGHT")

            direction = choice(directions)
            self.explore = direction
            return direction
        else:
            loc = self.path.pop()
            print("{} -> {}".format((self.x, self.y), loc), file=sys.stderr, flush=True)
            if loc[0] - self.x == 1:
                return "DOWN"
            if loc[0] - self.x == -1:
                return "UP"
            if loc[1] - self.y == 1:
                return "RIGHT"
            if loc[1] - self.y == -1:
                return "LEFT"     


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
kirk = Kirk(r, c, a)
# game loop
while True:
    # kr: row where Kirk is located.
    # kc: column where Kirk is located.
    kr, kc = [int(i) for i in input().split()]
    kirk.position(kr, kc)
    grid = []
    for i in range(r):
        row = input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        grid += [row]

    kirk.analyze_map(grid)

    move = kirk.move()


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Kirk's next move (UP DOWN LEFT or RIGHT).
    print("{}".format(move))
