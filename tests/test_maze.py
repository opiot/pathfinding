# import pytest

from pathfinding.grid import Grid


def test_create_grid():
    grid = Grid(2, 3)
    assert grid.h == 2
    assert grid.w == 3
