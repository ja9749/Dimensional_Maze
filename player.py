"""Module containing the Player data class for the game Dimensional Maze.

This module contains the class Player which holds all data relating to a player
in a Maze object in the Dimensional Maze Game.
"""
import numpy


class Player:
    """Player data class for the game Dimensional Maze.

    This module contains the class Player which holds all data relating to a 
    player within a Maze object in the Dimensional Maze Game. That includes the
    player's position and orientation.
    """
    def __init__(self, position = [0, 0, 0],
                 orientation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        """Initialisation function for a Player object.

        All arguments passed into this function are assigned to the
        corresponding parameter in this player object.

        Keyword arguments:
        position -- The player's starting coordinates in the Maze.
        orientation -- The player's starting orientation within the Maze.
        """
        self.position = numpy.array(position).astype(int)
        self.orientation = numpy.array(orientation).astype(int)

        self.visible_dimensions = (0, 1, 2)

    def move(self, dimension, direction):
        """Moves the the player's position.

        On receiving the dimension and direction a player wishes move the 
        player's position vector is updated to reflect this.

        Keyword arguments:
        dimension -- The number of the dimension the player is moving in.
        direction -- The direction the player is moving in, 1 for +ve and -1
            for -ve.
        """
        self.position[dimension] += direction

    def rotate(self, dimension, direction):
        """Rotates the the player's orientation.

        On receiving the two dimensions and direction a player wishes rotate
        the player's orientation matrix is transformed to reflect a 90 degrees
        clockwise or anti-clockwise rotation (depending on direction) about the
        plane defined by the two dimensions given.

        Keyword arguments:
        dimension -- The numbers of the two dimensions defining the plane the
            player is rotating around.
        direction -- The direction the player is rotation along that plane,
            1 for clockwise and -1 for anti-clockwise.
        """
        #Make a rotation matrix representing the rotation being performed and
        #multiply that with the player's orientation matrix.
        direction_matrix = numpy.identity(len(self.position))

        direction_matrix[dimension[0]][dimension[1]] = -direction
        direction_matrix[dimension[1]][dimension[0]] = direction
        direction_matrix[dimension[0]][dimension[0]] = 0
        direction_matrix[dimension[1]][dimension[1]] = 0

        self.orientation = numpy.matmul(direction_matrix, self.orientation)