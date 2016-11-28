"""TODO: Complete Docstring: dimensional_maze.py"""

import json
import pygame
import numpy as np
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from maze import Maze
from item import Item
from event import Event
from player import Player
from display import Display
from input_handler import Input_Handler


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
            
            player = Player(json_object['player']['position'],
                            json_object['player']['orientation'])

            maze = Maze(json_object['dimension_count'],
                        json_object['dimension_lengths'],
                        json_object['dimensions_locked'],
                        player,
                        json_object['goal'],
                        items,
                        events,
                        json_object['grid_walls'])
    return maze

def play_game(display, maze):

    """TODO: Complete Docstring: play_game Function"""

    game_exit = False
    redraw = True

    input_handler = Input_Handler()

    display.draw(maze)

    while not game_exit:

        if maze.player.position.tolist() == maze.goal:
            game_exit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
                else:
                    move = input_handler.handle_key_event(event.key, maze)
                    (movement_type, dimension, direction) = move
                    if movement_type == 0:
                        direction_vector = np.array(
                            [0] * maze.dimension_count)
                        direction_vector[dimension] = float(direction)
                        rotated_vector = maze.player.orientation.dot(
                            direction_vector).astype(int)
                        dimension = np.where(rotated_vector != 0)[0][0]
                        direction = rotated_vector[dimension]
                        if maze.move_player(dimension, direction):
                            for i in range(0, 10):
                                display.move(
                                    dimension, direction * 0.1)
                                display.draw(maze)
                    elif movement_type == 1:
                        maze.player.rotate(dimension, direction)

                        for i in range(0, 10):
                            display.rotate(
                                dimension, direction * 0.05 * math.pi)
                            display.draw(maze)
                    redraw = True
            pygame.event.clear() 
            break

def main():

    """TODO: Complete Docstring: main Function"""
    
    pygame.init()
    maze = load_maze('small.json')
    display = Display(maze.player.position, maze.player.orientation)
    play_game(display, maze)
    pygame.quit()
    return


if __name__ == '__main__':
    main()
    quit()