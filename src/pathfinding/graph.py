import sys
from queue import Queue
from random import choice

class Grid:
    def __init__(self, h, w, alarm=None):
        self.h = h
        self.w = w
        self.alarm = alarm
        self.squares = {}
        self.unknowns = {}
        self.scan = True
        self.back = False
        self._gate = None
        self._room = None

    def load(self, grid):
        for x, row in enumerate(grid):
            for y, square in enumerate(row):
                location = (x, y)
                if square == ".":
                    self.squares[location] = square
                    continue

                if square == "T":
                    self._gate = (x, y)
                    self.squares[location] = square
                    continue

                if square == "C":
                    self._room = (x, y)
                    self.squares[location] = square
                    continue

                if square == "?":
                    self.unknowns[location] = square
                    continue

    def room(self):
        return self._room

    def gate(self):
        return self._gate

    def square(self, location):
        if location in self.squares:
            return self.squares[location]

        if location in self.unknowns:
            return self.unknowns[location]

        return "#"

    def neighbors(self, location):
        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            square = (location[0] + x, location[1] + y)
            if self.scan and square == self._room:
                continue
            if square in self.squares:
                yield square

    def unknown(self, location):
        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            square = (location[0] + x, location[1] + y)
            if square in self.unknowns:
                return True
        return False

    def incognita(self):
        for location, _ in self.squares.items():
            
            if self.unknown(location):
                yield location

    @staticmethod
    def direction(pt1, pt2):
        if pt2[0] - pt1[0] == 1:
            return "DOWN"
        if pt2[0] - pt1[0] == -1:
            return "UP"        
        if pt2[1] - pt1[1] == 1:
            return "RIGHT"
        if pt2[1] - pt1[1] == -1:
            return "LEFT"    


    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current = goal
        path = []
        while current != start:
            try:
                path.append(current)
                current = came_from[current]
            except KeyError:
                return []

        return path

    def _bfs(self, start, goal):
        frontier = Queue()
        frontier.put(start)
        came_from = dict()
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

        return came_from


    def bfs(self,start, goal):
        came_from = self._bfs(start, goal)
        path = self.reconstruct_path(came_from, start, goal)
        return path[::-1]

    def explore(self, location):
        pts = {}
        for goal in self.incognita():
            path = self.bfs(location, goal)
            if len(path) > 0:
                pts[len(path)] = pts.get(len(path),[]) + [goal]

        if not pts:
            return []

        destinations = pts[min(pts.keys())]
        return(choice(destinations))        


    def move(self, location):
        
        if self.room() and self.room() == location:
            self.back = True
        
        if self.room() and self.gate() and self.scan:
            distance = len(self.bfs(self.room(), self.gate())) - 1
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
            goal = self.explore(location)

        print("goal: {}".format(goal), file=sys.stderr, flush=True) 


        
        for node in self.bfs(location, goal):
            return self.direction(location, node)

    def __str__(self) -> str:
        rows = []

        for x in range(0, self.h):
            row = ""
            for y in range(0, self.w):
                row += self.square((x, y))
            rows += [row]

        return "\n".join(rows)[:]


if __name__ == "__main__":
    square = """?#############################
#............................#
#.#######################.#..#
#.....T.................#.#..#
#.....#.................#.#..#
#.#######################.#..#
#.....##......##......#....###
#...####..##..##..##..#..#...#
#.........##......##.....#...#
###########################.##
#......#......#..............#
#...C..#.....................#
#...#..####################..#
#............................#
##############################"""
    grid = Grid(15, 30, 70)
    grid.load(square.splitlines())
    print(grid.room(), grid.gate())

    # len(grid.astar(grid.room(), grid.gate())) == 71

    kirk = (12, 1)

    for loc in grid.neighbors(kirk):
        print(loc, grid.square(loc))

    came_from = grid._bfs(grid.room(), grid.gate())
    path = grid.reconstruct_path(came_from, grid.room(), grid.gate())
    print(len(path), path)
    # move = grid.move(kirk)
    # assert move == "LEFT"

    print("{}".format(grid))