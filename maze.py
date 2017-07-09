"""TODO: Complete Docstring: item.py"""

from item import Item
from event import Event
from player import Player

import json


class Maze:

    def __init__(self, dimension_count, dimension_lengths,
                     dimensions_locked, player, goal, items, events,
                     grid_walls):

        """TODO: Complete Docstring: __init__ Function."""

        self.dimension_count = dimension_count
        self.dimension_lengths = dimension_lengths
        self.dimensions_locked = dimensions_locked
        self.player = player
        self.goal = goal
        self.items = items
        self.events = events
        self.grid_walls = grid_walls

    @classmethod
    def load_from_file_name(maze, json_file_name):
        with open(json_file_name) as json_file:
            json_object = json.load(json_file)
            if '__type__' in json_object and json_object['__type__'] == 'Maze':

                dimension_count = json_object['dimension_count']
                dimension_lengths = json_object['dimension_lengths']
                dimensions_locked = json_object['dimensions_locked']

                player = Player(json_object['player']['position'],
                                json_object['player']['orientation'])

                goal = json_object['goal']

                items = []
                for item in json_object['items']:
                    items.append(Item(item['item_type'],
                                      item['shape_file'],
                                      item['position']))

                events = []
                for event in json_object['events']:
                    events.append(Event(event['audio_file'],
                                        event['position']))

                grid_walls = json_object['grid_walls']

            return maze(dimension_count, dimension_lengths, dimensions_locked,
                        player, goal, items, events, grid_walls)


    def move_player(self, dimension, direction):

        test = 0
        if direction > 0:
            test = 2 ** (dimension * 2)
        else:
            test = 2 ** (dimension * 2 + 1)

        if not (self.get_grid_walls_number() & test):
            self.player.move(dimension, direction)
            return True

        return False

    def get_grid_walls_number(self):
        grid_number = self.grid_walls
        for i in reversed(self.player.position):
            grid_number = grid_number[i]

        return grid_number