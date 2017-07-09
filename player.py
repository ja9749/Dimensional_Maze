"""TODO: Complete Docstring: player.py"""

import numpy


class Player:

    """TODO: Complete Docstring: Player Class."""

    def __init__(self, position = [0, 0, 0], orientation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):

        """TODO: Complete Docstring: __init__ Function."""

        self.position = numpy.array(position).astype(int)
        self.orientation = numpy.array(orientation).astype(int)

        self.visible_dimensions = (0, 1, 2)

    def move(self, dimension, direction):

        """TODO: Complete Docstring: move Function."""

        self.position[dimension] += direction


    def rotate(self, dimension, direction):

        """TODO: Complete Docstring: rotate Function."""

        direction_matrix = numpy.identity(len(self.position))

        direction_matrix[dimension[0]][dimension[1]] = -direction
        direction_matrix[dimension[1]][dimension[0]] = direction
        direction_matrix[dimension[0]][dimension[0]] = 0
        direction_matrix[dimension[1]][dimension[1]] = 0

        self.orientation = numpy.matmul(direction_matrix, self.orientation)