import sys
from queue import Queue


class Grid:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.squares = {}
        self.traps = {}
        self.balls = {}
        self.switches = {}
        self.bender = None
        self.fry = None


    def load(self, grid):
        self.squares = {}
        for y, row in enumerate(grid):
            for x, square in enumerate(row):
                location = (x, y)
                if square == ".":
                    self.squares[location] = square
                    continue
                if square == "+":
                    self.balls[location] = square


    def load_switches(self, lines):
        for line in lines:
            s_x, s_y, t_x, t_y, state = line
            self.traps[(t_x, t_y)] = {'state' : state, 'switch': (s_x, s_y)}
            self.switches[(s_x, s_y)] = (t_x, t_y)



    def square(self, location):
        if location == self.bender:
            return "B"        
        if location == self.fry:
            return "F"
        if location in self.traps:
            if self.traps[location]["state"] == 0:
                return "U"
            else:
                return "T"
        if location in self.switches:
            return "S"            
        if location in self.balls:
            return self.balls[location]

        if location in self.squares:
            return self.squares[location]


        return "#"

    def neighbors(self, location):
        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            square = (location[0] + x, location[1] + y)
            if square in self.squares:
                yield square

    @staticmethod
    def direction(pt1, pt2):
        if pt2[0] - pt1[0] == 1:
            return "D"
        if pt2[0] - pt1[0] == -1:
            return "U"        
        if pt2[1] - pt1[1] == 1:
            return "R"
        if pt2[1] - pt1[1] == -1:
            return "L"    


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

    def switch(self, loc):
        trap = self.switches[loc]
        if self.traps[trap]["state"] == 0:
            self.traps[trap]["state"] = 1
        else:
            self.traps[trap]["state"] = 0


    def explore(self, path):
        activated = []
        switch = None
        for pt in path:
            if pt in self.switches:
                activated += [pt]
                self.switch(pt)
            if pt in self.traps and self.traps[pt]["state"] == 1:                
                switch =  self.traps[pt]["switch"]
                break

        for a in activated:
            self.switch(a)
        
        if switch:
            return switch

        return path[-1]


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



    def checkpoint(self, start, target):
            segment = self.bfs(start, target)
            current = self.explore(segment)
            if current == target:
                return target
            
            return self.checkpoint(start, current), self.checkpoint(current, target)


    def move(self,start, target):
        pass
        

    def __str__(self) -> str:
        rows = []

        for y in range(0, self.h):
            row = ""
            for x in range(0, self.w):
                row += self.square((x, y))
            rows += [row]

        return "\n".join(rows)[:]


if __name__ == "__main__":
    square = """##########
#........#
#.######.#
#........#
########.#
#..#.###.#
#.##...#.#
#..###.#.#
#........#
##########"""
    w = 10
    h = 10
    start = (3, 3)
    target = (8, 3)
    switches = [[2, 3, 7, 3, 1]]
    grid = Grid(w, h)
    grid.bender = start
    grid.fry = target
    grid.load(square.splitlines())
    grid.load_switches(switches)

    print(grid.checkpoint(start, target))

    # print(grid)

