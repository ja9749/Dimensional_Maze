"""TODO: Complete Docstring: dimensional_maze.py"""

import json
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from maze import Maze
from item import Item
from event import Event

TITLE = 'Dimensional Maze'
DISPLAY_WIDTH = 800#1800
DISPLAY_HEIGHT = 600#1000


def initialise():

    """TODO: Complete Docstring: initialise Function"""

    pygame.init()
    pygame.display.set_caption(TITLE)
    display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    game_display = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45.0, (display[0]/display[1]), 1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(20, 0, 0, 0)
    return game_display


def clean_up():

    """TODO: Complete Docstring: clean_up Function"""

    pygame.quit()
    return


def load_maze(json_file_name):

    """TODO: Complete Docstring: load_maze Function"""

    maze = []
    with open(json_file_name) as json_file:
        json_object = json.load(json_file)
        if '__type__' in json_object and json_object['__type__'] == 'Maze':
            items = []
            for item in json_object['items']:
                items.append(Item(item['item_type'],
                                  item['shape_file'],
                                  item['position']))

            events = []
            for event in json_object['events']:
                events.append(Event(event['audio_file'], event['position']))
            
            maze = Maze(json_object['dimension_count'],
                        json_object['dimension_lengths'],
                        json_object['dimensions_locked'],
                        json_object['start'],
                        json_object['goal'],
                        items,
                        events,
                        json_object['grid_walls'])
    return maze


def draw(game_display, maze):

    """TODO: Complete Docstring: draw Function"""

    vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))

    edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
             (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    return


def handle_key_event(key):

    """TODO: Complete Docstring: handle_key_event Function"""

    if key == pygame.K_UP:
        glTranslatef(0.0, 0.0, 1.0)
        return [0, 1]
    elif key == pygame.K_DOWN:
        glTranslatef(0.0, 0.0, -1.0)
        return [0, -1]
    elif key == pygame.K_RIGHT:
        glTranslatef(-1.0, 0.0, 0.0)
        return [1, 1]
    elif key == pygame.K_LEFT:
        glTranslatef(1.0, 0.0, 0.0)
        return [1, -1]


def play_game(game_display, maze):

    """TODO: Complete Docstring: play_game Function"""

    game_exit = False
    redraw = True

    while not game_exit:

        if maze.player == maze.goal:
            print("You Win!")
            game_exit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_exit = True
                else:
                    [dimension, direction] = handle_key_event(event.key)
                    maze.move(dimension, direction)
                    redraw = True

        if redraw:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            draw(game_display, maze)
            pygame.display.flip()
            redraw = False


def main():

    """TODO: Complete Docstring: main Function"""

    game_display = initialise()
    maze = load_maze('test.json')
    play_game(game_display, maze)
    clean_up()
    return


if __name__ == '__main__':
    main()
    quit()