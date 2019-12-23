"""Library of useful functions for the game Dimensional Maze.

This module contains a library of useful functions used to run the
Dimensional Maze game.
"""
import numpy


def rel_vec_dim(dimension, orientation):
    """Rotates a unit vector pointing in the direction of a given
    dimension and rotates it by a given orientation matrix.

    Keyword arguments:
    dimension -- The dimension the unit vector is pointing in.
    orientation -- The orientation matrix used to rotate the vector.
    """
    vector = numpy.array([0] * len(orientation))
    vector[dimension] = 1
    vector = orientation.dot(vector).astype(int)
    dimension = numpy.nonzero(vector)[0][0]

    return (vector, dimension)


def relative_move(orientation, dimension, direction):
    """Calculate the actual dimension the player is moving through and
    in what direction based on the player's orientation.

    Keyword arguments:
    orientation -- The orientation of the player in matrix form.
    dimension -- The dimension being moved through assuming the
        orientation is the identity matrix.
    direction -- The direction being moved through assuming the
        orientation is the identity matrix.
    """
    (vector, dimension) = rel_vec_dim(dimension, orientation)
    direction = vector[dimension] * direction

    return (dimension, direction)


def relative_rotate(orientation, dimension, direction):
    """Calculate the actual dimensions the player is rotating through
    and in what direction based on the player's orientation.

    Keyword arguments:
    orientation -- The orientation of the player in matrix form.
    dimension -- The two dimensions being rotated assuming the
        orientation is the identity matrix.
    direction -- The direction being rotated assuming the orientation is
        the identity matrix.
    """
    (vector_1, dimension[0]) = rel_vec_dim(dimension[0], orientation)
    (vector_2, dimension[1]) = rel_vec_dim(dimension[1], orientation)

    if (dimension[0] > dimension[1] and
            vector_1[dimension[0]] == vector_2[dimension[1]]):
        direction *= -1

    elif (dimension[0] < dimension[1] and 
             vector_1[dimension[0]] != vector_2[dimension[1]]):
        direction *= -1

    dimension.sort()

    return (dimension, direction)