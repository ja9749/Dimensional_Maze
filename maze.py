"""TODO: Complete Docstring: item.py"""


class Maze:

    """TODO: Complete Docstring: Maze Class."""

    def __init__(self, dimension_count, dimension_lengths,
                     dimensions_locked, start, goal, items, events,
                     grid_walls):

        """TODO: Complete Docstring: __init__ Function."""

        self.dimension_count = dimension_count
        self.dimension_lengths = dimension_lengths
        self.dimensions_locked = dimensions_locked
        self.player = start
        self.goal = goal
        self.items = items
        self.events = events
        self.grid_walls = grid_walls
        print(vars(self), "\n")

    def move(self, dimension, direction):

        """TODO: Complete Docstring: move Function."""

        self.player[dimension] += direction
        print(self.player)