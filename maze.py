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
        if dimension == 0 and direction > 0:
            test = 1
        elif dimension == 0 and direction < 0:
            test = 2
        elif dimension == 1 and direction > 0:
            test = 4
        elif dimension == 1 and direction < 0:
            test = 8
        elif dimension == 2 and direction > 0:
            test = 16
        elif dimension == 2 and direction < 0:
            test = 32
        
        pos_x = self.player.position[0]
        pos_y = self.player.position[1]
        pos_z = self.player.position[2]

        if not ((self.grid_walls[pos_z][pos_y][pos_x] & test)):
            self.player.move(dimension, direction)
            return True

        return False