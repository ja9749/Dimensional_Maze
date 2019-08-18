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

    def __init__(self, position, orientation, walls):

        """TODO: Complete Docstring: __init__ Function."""

        self.position = np.array(position).astype(float)
        self.orientation = np.array(orientation).astype(float)

        self.calculate_visible_dimensions()
        self.walls = walls
        self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))

        pygame.init()
        pygame.display.set_caption(TITLE)
        display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.game_display = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        pygame.display.toggle_fullscreen()
        gluPerspective(60.0, (display[0]/display[1]), 1, 50.0)
        glTranslatef(0.0, 0.0, -1.0)
        glRotatef(20, 0, 0, 0)

    def draw_move(self, dimension, direction, maze):
        if dimension not in self.visible_dimensions:
            self.visible_dimensions.append(dimension)
            self.visible_dimensions.sort()
            self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))

        for i in range(0, 10):
            self.move(dimension, direction * 0.1)
            if len(self.visible_dimensions) == 3:
                self.draw_3D(maze)
            else:
                self.draw_4D(maze)

        self.calculate_visible_dimensions()
        self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))

    def move(self, dimension, direction):

        """TODO: Complete Docstring: move Function."""

        self.position[dimension] += direction

    def draw_rotate(self, dimension, direction, maze):
        if dimension[0] not in self.visible_dimensions:
            self.visible_dimensions.append(dimension[0])
            self.visible_dimensions.sort()
            self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))
        if dimension[1] not in self.visible_dimensions:
            self.visible_dimensions.append(dimension[1])
            self.visible_dimensions.sort()
            self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))

        if len(self.visible_dimensions) == 3:
            for i in range(0, 10):
                self.rotate(dimension, direction * 0.05 * math.pi)
                self.draw_3D(maze)
        else:
            for i in range(0, 40):
                self.rotate(dimension, direction * 0.0125 * math.pi)
                self.draw_4D(maze)

        self.calculate_visible_dimensions()
        self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))

    def rotate(self, dimension, direction):

        """TODO: Complete Docstring: rotate Function."""

        direction_matrix = np.identity(len(self.position))

        direction_matrix[dimension[0]][dimension[1]] = math.sin(direction)
        direction_matrix[dimension[1]][dimension[0]] = -math.sin(direction)
        direction_matrix[dimension[0]][dimension[0]] = math.cos(direction)
        direction_matrix[dimension[1]][dimension[1]] = math.cos(direction)
        
        self.orientation = np.matmul(self.orientation, direction_matrix)

    def create_sub_walls(self, walls, dimension_level):
        sub_walls = []

        if dimension_level in self.visible_dimensions:
            for i in range(0, len(walls)):
                if dimension_level > 0:
                    sub_walls.append(self.create_sub_walls(walls[i], dimension_level - 1))
                else:
                    sub_walls.append(walls[i])
        else:
            if dimension_level > 0:
                sub_walls = self.create_sub_walls(walls[int(round(self.position[dimension_level]))], dimension_level - 1)
            else:
                sub_walls = walls[int(round(self.position[dimension_level]))]

        return sub_walls

    def calculate_visible_dimensions(self):
        self.visible_dimensions = []

        vis_dim = np.zeros(len(self.position))
        vis_dim[0] = 1
        vis_dim = np.matmul(vis_dim, self.orientation)

        for i in range(0, len(vis_dim)):
            if (vis_dim[i] >= 0.00001 or vis_dim[i] <= -0.00001) and i not in self.visible_dimensions:
                self.visible_dimensions.append(i)

        vis_dim = np.zeros(len(self.position))
        vis_dim[1] = 1
        vis_dim = np.matmul(vis_dim, self.orientation)

        for i in range(0, len(vis_dim)):
            if (vis_dim[i] >= 0.00001 or vis_dim[i] <= -0.00001) and i not in self.visible_dimensions:
                self.visible_dimensions.append(i)

        vis_dim = np.zeros(len(self.position))
        vis_dim[2] = 1
        vis_dim = np.matmul(vis_dim, self.orientation)

        for i in range(0, len(vis_dim)):
            if (vis_dim[i] >= 0.00001 or vis_dim[i] <= -0.00001) and i not in self.visible_dimensions:
                self.visible_dimensions.append(i)

        self.visible_dimensions.sort()

    def goal_check(self, goal, position, cube_pos, sub_dimensions):
        count = 0
        for i in range(0, len(goal)):
            if i in sub_dimensions:
                if cube_pos[count] != goal[i]:
                    return False
                count = count + 1
            else:
                if position[i] != goal[i]:
                    return False
        return True

    def calculate_colour():
        return []

    def calculate_colours(self, position, cube_pos, sub_dimensions, dimension_lengths):
        count = 0
        red = 0
        blue = 0
        green = 0
        for i in range(0, len(position)):
            if i in sub_dimensions:
                if i % 3 == 0:
                    red = red + cube_pos[count] / dimension_lengths[count]
                elif i % 3 == 1:
                    green = green + cube_pos[count] / dimension_lengths[count]
                elif i % 3 == 2:
                    blue = blue + cube_pos[count] / dimension_lengths[count]
                count = count + 1

        return [red, green, blue]

    def draw_3D(self, maze):

        """TODO: Complete Docstring: draw Function"""

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        sub_dimensions = self.visible_dimensions

        sub_orientation = np.identity(3)
        sub_orientation[0][0] = self.orientation[0][sub_dimensions[0]]
        sub_orientation[0][1] = self.orientation[0][sub_dimensions[1]]
        sub_orientation[0][2] = self.orientation[0][sub_dimensions[2]]
        sub_orientation[1][0] = self.orientation[1][sub_dimensions[0]]
        sub_orientation[1][1] = self.orientation[1][sub_dimensions[1]]
        sub_orientation[1][2] = self.orientation[1][sub_dimensions[2]]
        sub_orientation[2][0] = self.orientation[2][sub_dimensions[0]]
        sub_orientation[2][1] = self.orientation[2][sub_dimensions[1]]
        sub_orientation[2][2] = self.orientation[2][sub_dimensions[2]]

        vertices = ((0.9999, 0.9999, 0.9999), (0.9999, 0.9999, -0.9999),
                    (0.9999, -0.9999, 0.9999), (0.9999, -0.9999, -0.9999),
                    (-0.9999, 0.9999, 0.9999), (-0.9999, 0.9999, -0.9999),
                    (-0.9999, -0.9999, 0.9999), (-0.9999, -0.9999, -0.9999))

        line_vertices = ((0.999, 0.999, 0.999), (0.999, 0.999, -0.999),
                    (0.999, -0.999, 0.999), (0.999, -0.999, -0.999),
                    (-0.999, 0.999, 0.999), (-0.999, 0.999, -0.999),
                    (-0.999, -0.999, 0.999), (-0.999, -0.999, -0.999))

        edges = ((0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
                 (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7))

        surfaces = ((0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4),
                    (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5))

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glLineWidth(5.0);

        for k in range(0, len(self.sub_walls)):
            for j in range(0, len(self.sub_walls[0])):
                for i in range(0, len(self.sub_walls[0][0])):

                    translated_vertices = np.array([[0, 0, 0]] * 8, float)
                    rotated_vertices = np.array([[0, 0, 0]] * 8, float)

                    t_x = 2 * (i - self.position[sub_dimensions[0]])
                    t_y = 2 * (j - self.position[sub_dimensions[1]])
                    t_z = 2 * (k - self.position[sub_dimensions[2]])

                    #t_x = 2 * (i - self.position[0])
                    #t_y = 2 * (j - self.position[1])
                    #t_z = 2 * (k - self.position[2])

                    for vertex in range(0, len(vertices)):

                        translated_vertices[vertex] = (
                            vertices[vertex][0] + t_x,
                            vertices[vertex][1] + t_y,
                            vertices[vertex][2] + t_z)

                        rotated_vertices[vertex] = np.matmul(sub_orientation, translated_vertices[vertex])
                        rotated_vertices[vertex] = [rotated_vertices[vertex][1],rotated_vertices[vertex][2],-rotated_vertices[vertex][0]]

                        #rotated_vertices[vertex] = rotation_matrix.dot(
                        #    translated_vertices[vertex])

                    glBegin(GL_QUADS)


                    [red, green, blue] = self.calculate_colours(maze.player.position, [i, j, k], sub_dimensions, maze.dimension_lengths)
                    glColor3fv((red, green, blue))

                    if self.goal_check(maze.goal, maze.player.position, [i, j, k], sub_dimensions):
                        glColor3fv((1, 1, 1))

                    for index in range(0, len(surfaces)):
                        dim = self.visible_dimensions[int(index / 2)]
                        even = index % 2
                        if self.sub_walls[k][j][i] & int(math.pow(2, (dim * 2 + even))):
                            
                            for vertex in surfaces[index]:
                                glVertex3fv(rotated_vertices[vertex])

                    glEnd()

                    glBegin(GL_LINES)

                    for vertex in range(0, len(vertices)):
                        translated_vertices[vertex] = (
                            line_vertices[vertex][0] + t_x,
                            line_vertices[vertex][1] + t_y,
                            line_vertices[vertex][2] + t_z)

                        rotated_vertices[vertex] = np.matmul(sub_orientation, translated_vertices[vertex])

                        rotated_vertices[vertex] = [rotated_vertices[vertex][1],rotated_vertices[vertex][2],-rotated_vertices[vertex][0]]

                        #rotated_vertices[vertex] = rotation_matrix.dot(
                        #    translated_vertices[vertex])

                    for edge in edges:
                        for vertex in edge:
                            glColor3fv((0, 0, 0))
                            glVertex3fv(rotated_vertices[vertex])

                    glEnd()

        pygame.display.flip()

    def calculate_intersections(self, vertices, edges):
        intersecting_vertices = []
        edge_numbers = []
        count = 0

        for edge in edges:
            vertex_1 = vertices[edge[0]]
            vertex_2 = vertices[edge[1]]
            if vertex_1[3] == 0:
                intersecting_vertices.append([vertex_1[0], vertex_1[1], vertex_1[2]])
                edge_numbers.append(count)
            elif vertex_2[3] == 0:
                intersecting_vertices.append([vertex_2[0], vertex_2[1], vertex_2[2]])
                edge_numbers.append(count)
            elif (vertex_1[3] < 0 and vertex_2[3] > 0) or (vertex_1[3] > 0 and vertex_2[3] < 0):
                ratio = abs(float(vertex_1[3] / (vertex_1[3] - vertex_2[3])))
                x = vertex_1[0] - (vertex_1[0] - vertex_2[0]) * ratio
                y = vertex_1[1] - (vertex_1[1] - vertex_2[1]) * ratio
                z = vertex_1[2] - (vertex_1[2] - vertex_2[2]) * ratio
                intersecting_vertices.append([x, y, z])
                edge_numbers.append(count)
            count = count + 1
        return [np.array(intersecting_vertices), edge_numbers]

    def sort_vertex_numbers(self, vertex_numbers, intersecting_vertices):
        if len(vertex_numbers) != 4:
            return []

        new_vertex_numbers = [vertex_numbers[0]]

        dist_0_1 = abs(intersecting_vertices[vertex_numbers[0]][0] - intersecting_vertices[vertex_numbers[1]][0]) + \
                   abs(intersecting_vertices[vertex_numbers[0]][1] - intersecting_vertices[vertex_numbers[1]][1]) + \
                   abs(intersecting_vertices[vertex_numbers[0]][2] - intersecting_vertices[vertex_numbers[1]][2])

        dist_0_2 = abs(intersecting_vertices[vertex_numbers[0]][0] - intersecting_vertices[vertex_numbers[2]][0]) + \
                   abs(intersecting_vertices[vertex_numbers[0]][1] - intersecting_vertices[vertex_numbers[2]][1]) + \
                   abs(intersecting_vertices[vertex_numbers[0]][2] - intersecting_vertices[vertex_numbers[2]][2])

        dist_0_3 = abs(intersecting_vertices[vertex_numbers[0]][0] - intersecting_vertices[vertex_numbers[3]][0]) + \
                   abs(intersecting_vertices[vertex_numbers[0]][1] - intersecting_vertices[vertex_numbers[3]][1]) + \
                   abs(intersecting_vertices[vertex_numbers[0]][2] - intersecting_vertices[vertex_numbers[3]][2])

        dist_1_2 = abs(intersecting_vertices[vertex_numbers[1]][0] - intersecting_vertices[vertex_numbers[2]][0]) + \
                   abs(intersecting_vertices[vertex_numbers[1]][1] - intersecting_vertices[vertex_numbers[2]][1]) + \
                   abs(intersecting_vertices[vertex_numbers[1]][2] - intersecting_vertices[vertex_numbers[2]][2])

        dist_1_3 = abs(intersecting_vertices[vertex_numbers[1]][0] - intersecting_vertices[vertex_numbers[3]][0]) + \
                   abs(intersecting_vertices[vertex_numbers[1]][1] - intersecting_vertices[vertex_numbers[3]][1]) + \
                   abs(intersecting_vertices[vertex_numbers[1]][2] - intersecting_vertices[vertex_numbers[3]][2])

        dist_2_3 = abs(intersecting_vertices[vertex_numbers[2]][0] - intersecting_vertices[vertex_numbers[3]][0]) + \
                   abs(intersecting_vertices[vertex_numbers[2]][1] - intersecting_vertices[vertex_numbers[3]][1]) + \
                   abs(intersecting_vertices[vertex_numbers[2]][2] - intersecting_vertices[vertex_numbers[3]][2])

        if dist_0_1 <= dist_0_2 and dist_0_1 <= dist_0_3:
            new_vertex_numbers.append(vertex_numbers[1])
            if dist_1_2 <= dist_1_3:
                new_vertex_numbers.append(vertex_numbers[2])
                new_vertex_numbers.append(vertex_numbers[3])
            else:
                new_vertex_numbers.append(vertex_numbers[3])
                new_vertex_numbers.append(vertex_numbers[2])

        elif dist_0_2 <= dist_0_3:
            new_vertex_numbers.append(vertex_numbers[2])
            if dist_1_2 <= dist_2_3:
                new_vertex_numbers.append(vertex_numbers[1])
                new_vertex_numbers.append(vertex_numbers[3])
            else:
                new_vertex_numbers.append(vertex_numbers[3])
                new_vertex_numbers.append(vertex_numbers[1])

        else:
            new_vertex_numbers.append(vertex_numbers[3])
            if dist_1_3 <= dist_2_3:
                new_vertex_numbers.append(vertex_numbers[1])
                new_vertex_numbers.append(vertex_numbers[2])
            else:
                new_vertex_numbers.append(vertex_numbers[2])
                new_vertex_numbers.append(vertex_numbers[1])

        return new_vertex_numbers

    def draw_4D(self, maze):
        """TODO: Complete Docstring: draw Function"""

        self.sub_walls = self.create_sub_walls(self.walls, int(self.position.size - 1))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        sub_dimensions = self.visible_dimensions

        sub_orientation = np.identity(4)
        sub_orientation[0][0] = self.orientation[sub_dimensions[0]][sub_dimensions[0]]
        sub_orientation[0][1] = self.orientation[sub_dimensions[0]][sub_dimensions[1]]
        sub_orientation[0][2] = self.orientation[sub_dimensions[0]][sub_dimensions[2]]
        sub_orientation[0][3] = self.orientation[sub_dimensions[0]][sub_dimensions[3]]
        sub_orientation[1][0] = self.orientation[sub_dimensions[1]][sub_dimensions[0]]
        sub_orientation[1][1] = self.orientation[sub_dimensions[1]][sub_dimensions[1]]
        sub_orientation[1][2] = self.orientation[sub_dimensions[1]][sub_dimensions[2]]
        sub_orientation[1][3] = self.orientation[sub_dimensions[1]][sub_dimensions[3]]
        sub_orientation[2][0] = self.orientation[sub_dimensions[2]][sub_dimensions[0]]
        sub_orientation[2][1] = self.orientation[sub_dimensions[2]][sub_dimensions[1]]
        sub_orientation[2][2] = self.orientation[sub_dimensions[2]][sub_dimensions[2]]
        sub_orientation[2][3] = self.orientation[sub_dimensions[2]][sub_dimensions[3]]
        sub_orientation[3][0] = self.orientation[sub_dimensions[3]][sub_dimensions[0]]
        sub_orientation[3][1] = self.orientation[sub_dimensions[3]][sub_dimensions[1]]
        sub_orientation[3][2] = self.orientation[sub_dimensions[3]][sub_dimensions[2]]
        sub_orientation[3][3] = self.orientation[sub_dimensions[3]][sub_dimensions[3]]

        vertices = ((0.9999, 0.9999, 0.9999, 0.9999), (0.9999, 0.9999, -0.9999, 0.9999),
                    (0.9999, -0.9999, 0.9999, 0.9999), (0.9999, -0.9999, -0.9999, 0.9999),
                    (-0.9999, 0.9999, 0.9999, 0.9999), (-0.9999, 0.9999, -0.9999, 0.9999),
                    (-0.9999, -0.9999, 0.9999, 0.9999), (-0.9999, -0.9999, -0.9999, 0.9999),
                    (0.9999, 0.9999, 0.9999, -0.9999), (0.9999, 0.9999, -0.9999, -0.9999),
                    (0.9999, -0.9999, 0.9999, -0.9999), (0.9999, -0.9999, -0.9999, -0.9999),
                    (-0.9999, 0.9999, 0.9999, -0.9999), (-0.9999, 0.9999, -0.9999, -0.9999),
                    (-0.9999, -0.9999, 0.9999, -0.9999), (-0.9999, -0.9999, -0.9999, -0.9999))

        line_vertices = ((0.999, 0.999, 0.999, 0.999), (0.999, 0.999, -0.999, 0.999),
                    (0.999, -0.999, 0.999, 0.999), (0.999, -0.999, -0.999, 0.999),
                    (-0.999, 0.999, 0.999, 0.999), (-0.999, 0.999, -0.999, 0.999),
                    (-0.999, -0.999, 0.999, 0.999), (-0.999, -0.999, -0.999, 0.999),
                    (0.999, 0.999, 0.999, -0.999), (0.999, 0.999, -0.999, -0.999),
                    (0.999, -0.999, 0.999, -0.999), (0.999, -0.999, -0.999, -0.999),
                    (-0.999, 0.999, 0.999, -0.999), (-0.999, 0.999, -0.999, -0.999),
                    (-0.999, -0.999, 0.999, -0.999), (-0.999, -0.999, -0.999, -0.999))

        edges = ((0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
                 (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
                 (8, 9), (8, 10), (8, 12), (9, 11), (9, 13), (10, 11),
                 (10, 14), (11, 15), (12, 13), (12, 14), (13, 15), (14, 15),
                 (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15))

        surfaces = ((0, 1, 3, 5), (0, 2, 4, 8), (1, 2, 6, 9),
                    (5, 6, 7, 11), (8, 9, 10, 11), (3, 4, 7, 10),
                    (12, 13, 15, 17), (12, 14, 16, 20), (13, 14, 18, 21),
                    (17, 18, 19, 23), (20, 21, 22, 23), (15, 16, 19, 22),
                    (0, 12, 24, 25), (1, 13, 24, 26), (2, 14, 24, 28),
                    (3, 15, 25, 27), (4, 16, 25, 29), (5, 17, 26, 27),
                    (6, 18, 26, 30), (7, 19, 27, 31), (8, 20, 28, 29),
                    (9, 21, 28, 30), (10, 22, 29, 31), (11, 23, 30, 31))

        cubes = ((0, 3, 5, 1, 12, 15, 17, 13, 24, 25, 26, 27),
                 (8, 10, 11, 9, 20, 22, 23, 21, 28, 29, 30, 31),
                 (0, 4, 8, 2, 12, 16, 20, 14, 24, 25, 29, 28),
                 (6, 11, 7, 5, 18, 23, 19, 17, 26, 27, 31, 30),
                 (1, 6, 9, 2, 13, 18, 21, 14, 24, 26, 28, 30),
                 (3, 7, 10, 4, 15, 19, 22, 16, 25, 27, 29, 31),
                 (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                 (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23))

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glLineWidth(5.0);

        for l in range(0, len(self.sub_walls)):
            for k in range(0, len(self.sub_walls[0])):
                for j in range(0, len(self.sub_walls[0][0])):
                    for i in range(0, len(self.sub_walls[0][0][0])):

                        translated_vertices = np.array([[0, 0, 0, 0]] * 16, float)
                        rotated_vertices = np.array([[0, 0, 0, 0]] * 16, float)

                        t_x = 2 * (i - self.position[sub_dimensions[0]])
                        t_y = 2 * (j - self.position[sub_dimensions[1]])
                        t_z = 2 * (k - self.position[sub_dimensions[2]])
                        t_w = 2 * (l - self.position[sub_dimensions[3]])

                        #t_x = 2 * (i - self.position[0])
                        #t_y = 2 * (j - self.position[1])
                        #t_z = 2 * (k - self.position[2])

                        for vertex in range(0, len(vertices)):

                            translated_vertices[vertex] = (
                                vertices[vertex][0] + t_x,
                                vertices[vertex][1] + t_y,
                                vertices[vertex][2] + t_z,
                                vertices[vertex][3] + t_w)

                            rotated_vertices[vertex] = np.matmul(sub_orientation, translated_vertices[vertex])
                            #rotated_vertices[vertex] = [rotated_vertices[vertex][1],rotated_vertices[vertex][2],-rotated_vertices[vertex][0]]

                            #rotated_vertices[vertex] = rotation_matrix.dot(
                            #    translated_vertices[vertex])

                        [intersecting_vertices, edge_numbers] = self.calculate_intersections(rotated_vertices, edges)

                        if len(intersecting_vertices) > 0:

                            for vertex in range(0, len(intersecting_vertices)):
                                intersecting_vertices[vertex] = [intersecting_vertices[vertex][1],intersecting_vertices[vertex][2],-intersecting_vertices[vertex][0]]

                            glBegin(GL_QUADS)

                            [red, green, blue] = self.calculate_colours(maze.player.position, [i, j, k, l], sub_dimensions, maze.dimension_lengths)
                            """red = i / maze.dimension_lengths[0]
                            green =  j / maze.dimension_lengths[1]
                            blue = k / maze.dimension_lengths[2]"""
                            glColor3fv((red, green, blue))

                            if self.goal_check(maze.goal, maze.player.position, [i, j, k, l], sub_dimensions):
                                glColor3fv((1, 1, 1))

                            for index in range(0, len(cubes)):
                                dim = self.visible_dimensions[int(index / 2)]
                                even = index % 2
                                if self.sub_walls[l][k][j][i] & int(math.pow(2, (dim * 2 + even))):
                                    vertex_numbers = []
                                    for vertex in cubes[index]:
                                        if vertex in edge_numbers:
                                            vertex_numbers.append(edge_numbers.index(vertex))
                                    
                                    vertex_numbers = self.sort_vertex_numbers(vertex_numbers, intersecting_vertices)

                                    for vertex in vertex_numbers:
                                        glVertex3fv(intersecting_vertices[vertex])

                            glEnd()

                        glBegin(GL_LINES)
                        
                        glColor3fv((0, 0, 0))

                        for vertex in range(0, len(line_vertices)):
                            translated_vertices[vertex] = (
                                line_vertices[vertex][0] + t_x,
                                line_vertices[vertex][1] + t_y,
                                line_vertices[vertex][2] + t_z,
                                line_vertices[vertex][3] + t_w)

                            rotated_vertices[vertex] = np.matmul(sub_orientation, translated_vertices[vertex])

                        [intersecting_vertices, edge_numbers] = self.calculate_intersections(rotated_vertices, edges)

                            #rotated_vertices[vertex] = [rotated_vertices[vertex][1],rotated_vertices[vertex][2],-rotated_vertices[vertex][0]]

                            #rotated_vertices[vertex] = rotation_matrix.dot(
                            #    translated_vertices[vertex])

                        if len(intersecting_vertices) > 0:

                            for vertex in range(0, len(intersecting_vertices)):
                                intersecting_vertices[vertex] = [intersecting_vertices[vertex][1],intersecting_vertices[vertex][2],-intersecting_vertices[vertex][0]]

                            for index in range(0, len(surfaces)):
                                vertex_numbers = []
                                for vertex in surfaces[index]:
                                    if vertex in edge_numbers:
                                        vertex_numbers.append(edge_numbers.index(vertex))                                        

                                if len(vertex_numbers) == 2:
                                    for vertex in vertex_numbers:
                                        glVertex3fv(intersecting_vertices[vertex])

                        glEnd()

        pygame.display.flip()