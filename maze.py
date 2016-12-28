"""TODO: Complete Docstring: item.py"""


class Maze:

    """TODO: Complete Docstring: Maze Class."""

    def __init__(self, dimension_count, dimension_lengths,
                     dimensions_locked, player, goal, items, events,
                     grid_walls):

        """TODO: Complete Docstring: __init__ Function."""

        self.dimension_count = dimension_count
        self.dimension_lengths = dimension_lengths
        self.dimensions_locked = dimensions_locked
        self.player = player
        self.goal = goal
        self.items = items
        self.events = events
        self.grid_walls = grid_walls
        #print(vars(self), "\n")

    def move_player(self, dimension, direction):

        test = 0
        if direction > 0:
            test = 2 ** (dimension * 2)
        else:
            test = 2 ** (dimension * 2 + 1)

        if not (self.get_grid_walls_number() & test):
            self.player.move(dimension, direction)
            return True

        return False

    def get_grid_walls_number(self):
        grid_number = self.grid_walls
        for i in reversed(self.player.position):
            grid_number = grid_number[i]

        return grid_number