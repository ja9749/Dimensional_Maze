"""TODO: Complete Docstring: player.py"""

import numpy


class Player:

    """TODO: Complete Docstring: Player Class."""

    def __init__(self, position, orientation):

        """TODO: Complete Docstring: __init__ Function."""

        self.position = numpy.array(position).astype(int)
        self.orientation = numpy.array(orientation).astype(int)
        self.visible_dimensions = (0, 1, 2)
        #print(vars(self), "\n")

    def move(self, dimension, direction):

        """TODO: Complete Docstring: move Function."""

        self.position[dimension] += direction

    def rotate(self, dimension, direction):

        """TODO: Complete Docstring: rotate Function."""

        direction_matrix = numpy.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]], int)

        if dimension[0] == 1 and dimension[1] == 2:
            direction_matrix[dimension[0]][dimension[1]] = direction
            direction_matrix[dimension[1]][dimension[0]] = -direction
            direction_matrix[dimension[0]][dimension[0]] = 0
            direction_matrix[dimension[1]][dimension[1]] = 0
        else:
            direction_matrix[dimension[0]][dimension[1]] = -direction
            direction_matrix[dimension[1]][dimension[0]] = direction
            direction_matrix[dimension[0]][dimension[0]] = 0
            direction_matrix[dimension[1]][dimension[1]] = 0

        self.orientation = numpy.matmul(self.orientation, direction_matrix)