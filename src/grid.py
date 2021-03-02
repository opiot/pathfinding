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


@dataclass
class Grid:
    h: int
    w: int
    points: Dict = field(default_factory=dict)


    def neighbors(self, pt: Point) -> Point:
        for x, y in pt.neighbors():
            if (x, y) in self.points:
                yield self.points[(x, y)]

    def get(self, x, y):
        return self.points.get((x, y))

    def add(self, x, y, t):
        self.points[(x, y)] = Point(x, y, t)


if __name__ == '__main__':

    grid = Grid(1, 1)

    grid.add(0, 0, ".")

    o = grid.get(0, 0)

    for pt in grid.neighbors(o):
        print("{}".format(pt))
        print("distance {}".format(o.distance(pt)))
