"""TODO: Complete Docstring: player.py"""

import numpy as np
import math
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

TITLE = 'Dimensional Maze'
DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 1000


class Display:

    """TODO: Complete Docstring: Display Class."""

    def __init__(self, position, orientation):

        """TODO: Complete Docstring: __init__ Function."""

        self.position = np.array(position).astype(float)
        self.orientation = np.array(orientation).astype(float)
        self.visible_dimensions = (0, 1, 2)

        pygame.init()
        pygame.display.set_caption(TITLE)
        display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.game_display = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        pygame.display.toggle_fullscreen()
        gluPerspective(60.0, (display[0]/display[1]), 1, 50.0)
        glTranslatef(0.0, 0.0, -1.0)
        glRotatef(20, 0, 0, 0)

        #print(vars(self), "\n")

    def move(self, dimension, direction):

        """TODO: Complete Docstring: move Function."""

        self.position[dimension] += direction

    def rotate(self, dimension, direction):

        """TODO: Complete Docstring: rotate Function."""

        direction_matrix = np.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]], float)
        direction_matrix[dimension[0]][dimension[1]] = math.sin(direction)
        direction_matrix[dimension[1]][dimension[0]] = -math.sin(direction)
        direction_matrix[dimension[0]][dimension[0]] = math.cos(direction)
        direction_matrix[dimension[1]][dimension[1]] = math.cos(direction)
        self.orientation = np.matmul(self.orientation, direction_matrix)

    def draw(self, maze):

        """TODO: Complete Docstring: draw Function"""

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        rotation_matrix = np.copy(self.orientation)
        rotation_matrix[0][0] = self.orientation[1][1]
        rotation_matrix[0][1] = self.orientation[2][1]
        rotation_matrix[0][2] = self.orientation[0][1]
        rotation_matrix[1][0] = self.orientation[1][2]
        rotation_matrix[1][1] = self.orientation[2][2]
        rotation_matrix[1][2] = self.orientation[0][2]
        rotation_matrix[2][0] = self.orientation[1][0]
        rotation_matrix[2][1] = self.orientation[2][0]
        rotation_matrix[2][2] = self.orientation[0][0]

        vertices = ((0.9999, -0.9999, -0.9999), (0.9999, 0.9999, -0.9999),
                    (-0.9999, 0.9999, -0.9999), (-0.9999, -0.9999, -0.9999),
                    (0.9999, -0.9999, 0.9999), (0.9999, 0.9999, 0.9999),
                    (-0.9999, -0.9999, 0.9999), (-0.9999, 0.9999, 0.9999))

        line_vertices = ((0.999, -0.999, -0.999), (0.999, 0.999, -0.999),
                     (-0.999, 0.999, -0.999), (-0.999, -0.999, -0.999),
                    (0.999, -0.999, 0.999), (0.999, 0.999, 0.999),
                    (-0.999, -0.999, 0.999), (-0.999, 0.999, 0.999))

        edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
                 (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))

        surfaces = ((0, 1, 2, 3), (6, 7, 5, 4), (4, 5, 1, 0),
                    (3, 2, 7, 6), (1, 5, 7, 2), (4, 0, 3, 6))

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glLineWidth(5.0);

        for k in range(0, maze.dimension_lengths[2]):
            for j in range(0, maze.dimension_lengths[1]):
                for i in range(0, maze.dimension_lengths[0]):

                    translated_vertices = np.array([[0, 0, 0]] * 8, float)
                    rotated_vertices = np.array([[0, 0, 0]] * 8, float)

                    t_x = 2 * (j - self.position[1])
                    t_y = 2 * (k - self.position[2])
                    t_z = -2 * (i - self.position[0])

                    for vertex in range(0, len(vertices)):

                        translated_vertices[vertex] = (
                            vertices[vertex][0] + t_x,
                            vertices[vertex][1] + t_y,
                            vertices[vertex][2] + t_z)
                        rotated_vertices[vertex] = rotation_matrix.dot(
                            translated_vertices[vertex])

                    glBegin(GL_QUADS)

                    red = i / maze.dimension_lengths[0]
                    green =  j / maze.dimension_lengths[1]
                    blue = k / maze.dimension_lengths[2]
                    glColor3fv((red, green, blue))

                    for index in range(0, len(surfaces)):
                        if maze.grid_walls[k][j][i] & int(math.pow(2, index)):
                            for vertex in surfaces[index]:
                                if (i == maze.goal[0] and
                                    j == maze.goal[1] and
                                    k == maze.goal[2]):
                                    glColor3fv((1, 1, 1))

                                glVertex3fv(rotated_vertices[vertex])

                    glEnd()

                    glBegin(GL_LINES)

                    for vertex in range(0, len(vertices)):
                        translated_vertices[vertex] = (
                            line_vertices[vertex][0] + t_x,
                            line_vertices[vertex][1] + t_y,
                            line_vertices[vertex][2] + t_z)
                        rotated_vertices[vertex] = rotation_matrix.dot(
                            translated_vertices[vertex])

                    for edge in edges:
                        for vertex in edge:
                            glColor3fv((0, 0, 0))
                            glVertex3fv(rotated_vertices[vertex])

                    glEnd()

        pygame.display.flip()