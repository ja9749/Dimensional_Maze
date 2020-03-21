"""TODO: Complete Docstring: player.py"""

import numpy as np
import math
import pygame
import time
import itertools
import scipy.special

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

TITLE = 'Dimensional Maze'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 500
MOVE_FRAMES = 10
ROTATE_FRAMES = 20
ROTATE_ANGLE = math.pi * 0.5 / ROTATE_FRAMES
TOLERANCE = 1e-5


class HyperCube:
    def __init__(self, dim_num):
        print("\ndim_num", dim_num)

        line_vertices = list(itertools.product([0.999, -0.999], repeat=dim_num))
        temp_vertices = list(itertools.product([0.9999, -0.9999], repeat=dim_num))

        wall_vertices = []
        wall_line_vertices = []
        for i in range(0, 2 * dim_num):
            wall_vertices.append([])
            wall_line_vertices.append([])
            for vertex in temp_vertices:
                if ((i & 1) and (vertex[i >> 1] < 0)) \
                or (not (i & 1) and (vertex[i >> 1] > 0)):
                    wall_vertices[i].append(vertex)
                    wall_line_vertices[i].append(vertex)

        wall_edges = []
        wall_surfaces_vertices = []
        wall_surface_edges = []
        wall_cube_vertices = []
        wall_cube_edges = []
        vertices = wall_vertices[0]

        edges = []
        line_edges = []
        surfaces_vertices = []
        surface_edges = []
        line_surfaces_vertices = []
        line_surface_edges = []
        cube_vertices = []
        cube_edges = []

        edge_combo = [(i, j) for i in range(0, len(vertices))
                             for j in range(i + 1, len(vertices))]

        for (i, j) in edge_combo:
            if np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1:
                edges.append((i, j))

        line_edge_combo = [(i, j) for i in range(0, len(line_vertices))
                             for j in range(i + 1, len(line_vertices))]

        for (i, j) in line_edge_combo:
            if np.sum(np.array(line_vertices[i]) != np.array(line_vertices[j])) == 1:
                line_edges.append((i, j))

        surface_combo = [(i, j, k, l) for i in range(0, len(vertices))
                                      for j in range(i + 1, len(vertices))
                                      for k in range(j + 1, len(vertices))
                                      for l in range(k + 1, len(vertices))]

        for (i, j, k, l) in surface_combo:
            if np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[k])) == 1:
                surfaces_vertices.append((i, j, l, k))
                surface_edges.append((edges.index((i, j)),
                                    edges.index((i, k)),
                                    edges.index((j, l)),
                                    edges.index((k, l))))

        line_surface_combo = [(i, j, k, l) for i in range(0, len(line_vertices))
                                      for j in range(i + 1, len(line_vertices))
                                      for k in range(j + 1, len(line_vertices))
                                      for l in range(k + 1, len(line_vertices))]

        for (i, j, k, l) in line_surface_combo:
            if np.sum(np.array(line_vertices[i]) != np.array(line_vertices[j])) == 1 \
            and np.sum(np.array(line_vertices[i]) != np.array(line_vertices[k])) == 1 \
            and np.sum(np.array(line_vertices[l]) != np.array(line_vertices[j])) == 1 \
            and np.sum(np.array(line_vertices[l]) != np.array(line_vertices[k])) == 1:
                line_surfaces_vertices.append((i, j, l, k))
                line_surface_edges.append((line_edges.index((i, j)),
                                    line_edges.index((i, k)),
                                    line_edges.index((j, l)),
                                    line_edges.index((k, l))))

        cube_combo = [(i, j, k, l, m, n, o, p) for i in range(0, len(vertices))
                                               for j in range(i + 1, len(vertices))
                                               for k in range(j + 1, len(vertices))
                                               for l in range(k + 1, len(vertices))
                                               for m in range(l + 1, len(vertices))
                                               for n in range(m + 1, len(vertices))
                                               for o in range(n + 1, len(vertices))
                                               for p in range(o + 1, len(vertices))]

        count = 0
        for (i, j, k, l, m, n, o, p) in cube_combo:
            if np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[m]) != np.array(vertices[n])) == 1 \
            and np.sum(np.array(vertices[m]) != np.array(vertices[o])) == 1 \
            and np.sum(np.array(vertices[p]) != np.array(vertices[n])) == 1 \
            and np.sum(np.array(vertices[p]) != np.array(vertices[o])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[p])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[p])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[p])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[p])) == 1:
                count += 1
                cube_vertices.append((i, j, k, l, m, n, o, p))
                cube_edges.append((
                    edges.index((i, j)),
                    edges.index((i, k)),
                    edges.index((i, m)),
                    edges.index((j, l)),
                    edges.index((j, n)),
                    edges.index((k, l)),
                    edges.index((k, o)),
                    edges.index((l, p)),
                    edges.index((m, n)),
                    edges.index((m, o)),
                    edges.index((n, p)),
                    edges.index((o, p)),
                ))

        self.vertices = wall_vertices
        self.line_vertices = line_vertices
        self.edges = edges
        self.line_edges = line_edges
        self.surfaces_vertices = surfaces_vertices
        self.surface_edges = surface_edges
        self.line_surfaces_vertices = line_surfaces_vertices
        self.line_surface_edges = line_surface_edges
        self.cube_vertices = cube_edges
        self.cube_edges = cube_edges


class Display:
    """Display class for the game Dimensional Maze.

    This module contains the class Display which draws and displays the
    current game state.
    """
    def __init__(self, position, orientation, walls, maze):
        """Initialisation function for a Display object.

        All arguments passed into this function are assigned to the
        corresponding parameter in this player object.

        Keyword arguments:
        position -- The player's starting coordinates in the Maze.
        orientation -- The player's starting orientation in the Maze.
        walls -- The walls of the maze.
        """
        self.position = np.array(position).astype(float)
        
        #Orientation of maze is inverse of player's orientation.
        self.orientation = np.linalg.inv(np.array(orientation).astype(float))

        #Calculate subset of maze cells visible to player
        self.calculate_visible_dimensions()
        self.walls = self.create_wall_info(walls, int(self.position.size - 1), maze.dimension_lengths, maze.goal)
        self.sub_walls = self.create_sub_walls(self.walls,
                                               int(self.position.size - 1))
        self.n_cubes = []
        
        for i in range(3, len(position)+1):
            self.n_cubes.append(HyperCube(i))

        #Initialise pygame display
        #TODO: Understand this section and make it editable for player.
        pygame.init()
        pygame.display.set_caption(TITLE)
        display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        # pygame.display.toggle_fullscreen()
        gluPerspective(60.0, (display[0]/display[1]), 1, 50.0)
        glTranslatef(0.0, 0.0, -1.0)
        glRotatef(20, 0, 0, 0)

    def draw_move(self, dimension, direction):
        """Draw the animation of a the player moving through the maze.

        The maze is drawn a number of times with incremental changes in
        player position along the given dimention and direction.

        Keyword arguments:
        dimension -- The dimension being moved through.
        direction -- The direction being moved through.
        maze -- Main game object containing layout of the maze as well
            as player, enemy and item information.
        """
        for _ in range(0, MOVE_FRAMES):
            self.position[dimension] += direction / MOVE_FRAMES
            self.sub_walls = self.create_sub_walls(self.walls,
                                                   self.position.size - 1)
            self.draw()

    def draw_rotate(self, dimensions, direction):
        """Draw the animation of a the player rotating in the maze.

        The maze is drawn a number of times with incremental changes in
        player orientation around the given dimensions and direction.

        Keyword arguments:
        dimensions -- The dimensions being rotated around.
        direction -- The direction the player is rotating.
        maze -- Main game object containing layout of the maze as well
            as player, enemy and item information.
        """
        angle = direction * ROTATE_ANGLE
        rotation_matrix = np.identity(len(self.position))
        rotation_matrix[dimensions[0]][dimensions[1]] = math.sin(angle)
        rotation_matrix[dimensions[1]][dimensions[0]] = -math.sin(angle)
        rotation_matrix[dimensions[0]][dimensions[0]] = math.cos(angle)
        rotation_matrix[dimensions[1]][dimensions[1]] = math.cos(angle)

        self.orientation = np.matmul(self.orientation, rotation_matrix)
        self.calculate_visible_dimensions()
        self.sub_walls = self.create_sub_walls(self.walls,
                                               self.position.size - 1)

        for _ in range(1, ROTATE_FRAMES):
            self.draw()
            self.orientation = np.matmul(self.orientation, rotation_matrix)

        self.calculate_visible_dimensions()
        self.sub_walls = self.create_sub_walls(self.walls,
                                               self.position.size - 1)
        self.draw()

    def create_wall_info(self, walls, level, dimension_lengths, goal, position = []):
        """Create a multi-dimensional array which is a subset of the 
        walls passed in representing what is visible to the player.

        This function recursively iterates through the multi-dimensional
        array 'walls' picking out the grid cubes that are visible
        according to self.visible dimensions to be added to a return
        multi-dimensional array sub_walls.

        Keyword arguments:
        walls -- The walls of the maze.
        level -- The recursion level representing the dimension of
            walls being interated through.
        """
        sub_walls = []

        if level > 0:
            for i in range(0, len(walls)):
                sub_walls.append(self.create_wall_info(walls[i],
                                                       level - 1,
                                                       dimension_lengths,
                                                       goal,
                                                       [i] + position)) 
        else:
            for i in range(0, len(walls)):
                if goal == [i] + position:
                    wall_info = (walls[i], [i] + position, (1, 1, 1))
                else:
                    wall_info = (walls[i], [i] + position, self.calculate_colours([i] + position, range(0,len(dimension_lengths)), dimension_lengths))

                sub_walls.append(wall_info)

        return sub_walls


    def create_sub_walls(self, walls, level):
        """Create a multi-dimensional array which is a subset of the 
        walls passed in representing what is visible to the player.

        This function recursively iterates through the multi-dimensional
        array 'walls' picking out the grid cubes that are visible
        according to self.visible dimensions to be added to a return
        multi-dimensional array sub_walls.

        Keyword arguments:
        walls -- The walls of the maze.
        level -- The recursion level representing the dimension of
            walls being interated through.
        """
        sub_walls = []

        if level in self.visible_dimensions:
            if level > 0:
                for i in range(0, len(walls)):
                    sub_walls = sub_walls + self.create_sub_walls(walls[i],
                                                           level - 1)
            else:
                for i in range(0, len(walls)):
                    sub_walls = sub_walls + [walls[i]]
        else:
            wall_index = int(round(self.position[level]))
            if level > 0:
                sub_walls = sub_walls + self.create_sub_walls(walls[wall_index], level - 1)
            else:
                sub_walls = sub_walls + [walls[wall_index]]

        return sub_walls

    def calculate_visible_dimensions(self):
        """Calculate the dimensions visible to the player using
        orientation.
        """
        self.visible_dimensions = []

        for j in range(0, len(self.orientation)):
            for i in range(0, 3):
                if abs(self.orientation[i][j]) > TOLERANCE:
                    self.visible_dimensions.append(j)
                    break


    def calculate_colours(self, cube_pos, sub_dimensions, dimension_lengths):
        """TODO: Complete Docstring: calculate_colours Function"""
        count = 0
        red = 0
        blue = 0
        green = 0

        red_total = 1
        blue_total = 1
        green_total = 1

        position = [round(num) for num in self.position]

        for i in range(0, len(position)):
            if i % 3 == 0:
                if i in sub_dimensions:
                    red = red + cube_pos[count] * red_total
                    count = count + 1
                else:
                    red = red + position[i] * red_total
                red_total *= dimension_lengths[i]
            elif i % 3 == 1:
                if i in sub_dimensions:
                    green = green + cube_pos[count] * green_total
                    count = count + 1
                else:
                    green = green + position[i] * green_total
                green_total *= dimension_lengths[i]
            elif i % 3 == 2:
                if i in sub_dimensions:
                    blue = blue + cube_pos[count] * blue_total
                    count = count + 1
                else:
                    blue = blue + position[i] * blue_total
                blue_total *= dimension_lengths[i]

        return [red / red_total, green / green_total, blue / blue_total]


    def draw(self):
        """Transform, Colour and Render the maze and all its elements
        according to the game state.

        Keyword arguments:
        """

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glLineWidth(5.0)

        dim_num = len(self.visible_dimensions)

        sub_orientation = np.zeros((dim_num, dim_num))

        rows = []

        for i in self.visible_dimensions:
            for j in range(0, len(self.orientation)):
                if abs(self.orientation[j][i]) >= TOLERANCE:
                    if j not in rows:
                        rows.append(j)

        rows.sort()

        for i in range(0, len(rows)):
            for j in range(0, len(rows)):
                sub_orientation[i][j] = self.orientation[rows[i]][self.visible_dimensions[j]]

        n_cube = self.n_cubes[dim_num-3]
        line_vertices = n_cube.line_vertices
        edges = n_cube.edges
        line_edges = n_cube.line_edges
        surfaces_vertices = n_cube.surfaces_vertices
        surfaces_edges = n_cube.surface_edges
        line_surfaces_vertices = n_cube.line_surfaces_vertices
        line_surfaces_edges = n_cube.line_surface_edges
        cubes_vertices = n_cube.cube_vertices
        cubes_edges = n_cube.cube_edges

        glBegin(GL_QUADS)

        for cube in self.sub_walls:
            coords = [cube[1][vis_dim] for vis_dim in self.visible_dimensions]
            (red, green, blue) = cube[2]

            for index in range(0, 2 * dim_num):
                dim = self.visible_dimensions[int(index / 2)]
                even = index & 1

                if cube[0] & int(math.pow(2, (dim * 2 + even))):
                    vertices = n_cube.vertices[index]
                    translated_vertices = np.array([[0] * dim_num] * pow(2, dim_num), float)
                    rotated_vertices = np.array([[0] * dim_num] * pow(2, dim_num), float)

                    t_coords = [2 * (coord - self.position[dim]) for (coord, dim) in zip(coords, self.visible_dimensions)]

                    for i in range(0, len(vertices)):
                        translated_vertices[i] = [v + t for (v, t) in zip(vertices[i], t_coords)]

                        rotated_vertices[i] = np.matmul(sub_orientation, translated_vertices[i])
                        if dim_num == 3:
                            rotated_vertices[i] = [rotated_vertices[i][1],rotated_vertices[i][2],-rotated_vertices[i][0]]


                    glColor3fv((red, green, blue))

                    if dim_num == 3:
                        for surfaces in surfaces_vertices:
                            for vertex in surfaces:
                                glVertex3fv(rotated_vertices[vertex])
                    else:
                        [intersecting_vertices, edge_numbers] = self.calculate_intersections(rotated_vertices, edges)

                        if len(intersecting_vertices) > 0:
                            for vertex in range(0, len(intersecting_vertices)):
                                intersecting_vertices[vertex] = [intersecting_vertices[vertex][1],intersecting_vertices[vertex][2],-intersecting_vertices[vertex][0]]

                            vertex_numbers = []
                            for vertex in cubes_vertices[0]:
                                if vertex in edge_numbers:
                                    vertex_numbers.append(edge_numbers.index(vertex))
                            vertex_numbers = self.sort_vertex_numbers(vertex_numbers, intersecting_vertices)

                            for vertex in vertex_numbers:
                                glVertex3fv(intersecting_vertices[vertex])

        glEnd()

        glBegin(GL_LINES)
        glColor3fv((0, 0, 0))
        for cube in self.sub_walls:
            coords = [cube[1][vis_dim] for vis_dim in self.visible_dimensions]

            translated_vertices = np.array([[0] * dim_num] * pow(2, dim_num), float)
            rotated_vertices = np.array([[0] * dim_num] * pow(2, dim_num), float)

            t_coords = [2 * (coord - self.position[dim]) for (coord, dim) in zip(coords, self.visible_dimensions)]

            for i in range(0, len(line_vertices)):
                translated_vertices[i] = [v + t for (v, t) in zip(line_vertices[i], t_coords)]

                rotated_vertices[i] = np.matmul(sub_orientation, translated_vertices[i])
                if dim_num == 3:
                    rotated_vertices[i] = [rotated_vertices[i][1],rotated_vertices[i][2],-rotated_vertices[i][0]]

            if dim_num == 3:
                for edge in line_edges:
                    for vertex in edge:
                        glVertex3fv(rotated_vertices[vertex])
            else:
                [intersecting_vertices, edge_numbers] = self.calculate_intersections(rotated_vertices, line_edges)

                if len(intersecting_vertices) > 0:
                    for vertex in range(0, len(intersecting_vertices)):
                        intersecting_vertices[vertex] = [intersecting_vertices[vertex][1],intersecting_vertices[vertex][2],-intersecting_vertices[vertex][0]]

                    for surface in line_surfaces_edges:
                        vertex_numbers = []
                        for vertex in surface:
                            if vertex in edge_numbers:
                                vertex_numbers.append(edge_numbers.index(vertex))

                        if len(vertex_numbers) == 2:
                            for vertex in vertex_numbers:
                                glVertex3fv(intersecting_vertices[vertex])

        glEnd()

        pygame.display.flip()

    def calculate_intersections(self, vertices, edges):
        intersecting_vertices = []
        edge_numbers = []
        count = 0

        for edge in edges:
            v_1 = vertices[edge[0]]
            v_2 = vertices[edge[1]]
            if sum([coord for coord in v_1[3:]]) == 0:
                intersecting_vertices.append([v_1[0], v_1[1], v_1[2]])
                edge_numbers.append(count)
            elif sum([coord for coord in v_1[3:]]) == 0:
                intersecting_vertices.append([v_2[0], v_2[1], v_2[2]])
                edge_numbers.append(count)
            else:
                can_hit = [(c_1 < 0 and c_2 > 0) or (c_1 > 0 and c_2 < 0)
                        for (c_1, c_2) in zip(v_1[3:], v_2[3:])]
                if all(can_hit):
                    ratio = abs(float(v_1[3] / (v_1[3] - v_2[3])))
                    crosses = [abs(c_1 - (c_1 - c_2) * ratio) <= 1e-6
                            for (c_1, c_2) in zip(v_1[4:], v_2[4:])]
                    if all(crosses):
                        x = v_1[0] - (v_1[0] - v_2[0]) * ratio
                        y = v_1[1] - (v_1[1] - v_2[1]) * ratio
                        z = v_1[2] - (v_1[2] - v_2[2]) * ratio
                        intersecting_vertices.append([x, y, z])
                        edge_numbers.append(count)
            count = count + 1
        return [np.array(intersecting_vertices), edge_numbers]

    def sort_vertex_numbers(self, vertex_numbers, intersecting_vertices):
        if len(vertex_numbers) != 4:
            return []

        new_vertex_numbers = [vertex_numbers[0]]

        dist = [[[0]] * len(vertex_numbers)] * len(vertex_numbers)

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
