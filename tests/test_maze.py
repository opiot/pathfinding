# import pytest

from pathfinding.grid import Grid

square = """######
#....#
#....#
#....#
#....#
######"""


def test_size_grid():
    grid = Grid(6, 6)
    assert grid.h == 6
    assert grid.w == 6


def test_load_grid():
    grid = Grid(6, 6)
    grid.load(square)
    # start = grid.get(1, 1)
    # end = grid.get(5, 5)
    assert square == "{}".format(grid)


def test_point_grid():
    grid = Grid(6, 6)
    grid.load(square)
    start = grid.get(1, 1)
    assert start.topography == "."
    assert list(start.neighbors()) == [(1, 2), (2, 1), (1, 0), (0, 1)]
    assert list(grid.neighbors(start)) == [
        grid.get(1, 2),
        grid.get(2, 1),
        grid.get(1, 0),
        grid.get(0, 1),
    ]
    assert list(grid.neighbors(start, walk=True)) == [
        grid.get(1, 2),
        grid.get(2, 1),
    ]
