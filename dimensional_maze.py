"""TODO: Complete Docstring: dimensional_maze.py"""

import pygame
import numpy
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from input_handler import Input_Handler
from input_handler import Input_Type
from maze import Maze
from display import Display

def rel_vec_dim(dimension, orientation):
    vector = numpy.array([0] * len(orientation))
    vector[dimension] = 1
    vector = orientation.dot(vector).astype(int)
    dimension = numpy.nonzero(vector)[0][0]

    return (vector, dimension)


def relative_move(orientation, dimension, direction):
    (vector, dimension) = rel_vec_dim(dimension, orientation)
    direction = vector[dimension] * direction

    return (dimension, direction)


def relative_rotate(orientation, dimension, direction):
    (vector_1, dimension[0]) = rel_vec_dim(dimension[0], orientation)
    (vector_2, dimension[1]) = rel_vec_dim(dimension[1], orientation)

    dimension.sort()

    test_vectors = [numpy.array([0] * len(orientation)),
                    numpy.array([0] * len(orientation)),
                    numpy.array([0] * len(orientation)),
                    numpy.array([0] * len(orientation))]

    test_vectors[0][dimension[0]] = 1
    test_vectors[1][dimension[1]] = 1
    test_vectors[2][dimension[0]] = -1
    test_vectors[3][dimension[1]] = -1

    for v2 in range(0,4):
        v1 = (v2 + 1) % 4
        if (numpy.array_equal(vector_1, test_vectors[v1]) and 
            numpy.array_equal(vector_2, test_vectors[v2])):
            direction = -1 * direction

    return (dimension, direction)


def play_game(input_handler, maze, display):

    """TODO: Complete Docstring: play_game Function"""

    display.draw_3D(maze)

    game_exit = False
    while not game_exit:

        if maze.player.position.tolist() == maze.goal:
            print("WIN")
            game_exit = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_exit = True
                
            elif event.type == pygame.KEYDOWN:

                keys_pressed = pygame.key.get_pressed()
                output = input_handler.handle_key_event(keys_pressed)
                (input_type, dimension, direction) = output

                if input_type == pygame.K_ESCAPE:
                    game_exit = True
                elif (input_type == Input_Type.MOVE_3D or 
                      input_type == Input_Type.MOVE_4D):

                    if input_type == Input_Type.MOVE_3D:
                        (dimension, direction) = relative_move(maze.player.orientation,
                                                               dimension,
                                                               direction)

                    if maze.move_player(dimension, direction):
                        display.draw_move(dimension, direction, maze)

                elif (input_type == Input_Type.ROTATE_3D or
                      input_type == Input_Type.ROTATE_4D):

                    if input_type == Input_Type.ROTATE_4D:
                        dimension = [0, dimension]

                    (dimension, direction) = relative_rotate(maze.player.orientation,
                                                             dimension,
                                                             direction)

                    maze.player.rotate(dimension, direction)
                    display.draw_rotate(dimension, direction, maze)                        

            pygame.event.clear()

def main():

    """TODO: Complete Docstring: main Function"""
    
    pygame.init()

    input_handler = Input_Handler()
    maze = Maze.load_from_file_name('test.json')
    display = Display(maze.player.position,
                      maze.player.orientation,
                      maze.grid_walls)
    
    play_game(input_handler, maze, display)

    pygame.quit()


if __name__ == '__main__':
    main()
    quit()