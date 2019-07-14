"""Module containing the Maze data class for the game Dimensional Maze.

This module contains the class Maze which holds all data relating to a level in
the Dimensional Maze game.
"""
from item import Item
from event import Event
from player import Player

import json


class Maze:
    """Maze data class for the game Dimensional Maze.

    This module contains the class Maze which holds all data relating to a level in
    the Dimensional Maze game. That includes the structure of the maze, number and
    length of dimensions, item, event objects and the player objects.
    """
    def __init__(self, dimension_count, dimension_lengths, dimensions_locked,
                 player, goal, items, events, walls):
        """Initialisation function for a Maze object.

        All arguments passed into this function are assigned to the
        corresponding parameter in this maze object.

        Keyword arguments:
        dimension_count -- Number of dimensions in this maze as an integer.
        dimension_lengths -- An ordered array of the length of each dimension.
        dimensions_locked -- An array of booleans indicating whether a dimension
            is currently locked.
        player -- An object of type Player holding the player information.
        goal -- An array of numbers representing the coordinates for the goal of
            the maze.
        items -- A list of objects of type Item holding data about each item.
        events -- A list of objects of type Event holding data about each event.
        walls -- A n-dimensional array of numbers representing information
        on where the walls of the maze are in each grid cell of the maze.
        """
        self.dimension_count = dimension_count
        self.dimension_lengths = dimension_lengths
        self.dimensions_locked = dimensions_locked
        self.player = player
        self.goal = goal
        self.items = items
        self.events = events
        self.walls = walls

    @classmethod
    def load_from_file_name(maze, json_file_name):
        """Parses a json file to create a Maze object.

        The name of a json file is passed in and if that json file contains data
        for a Maze object, that data is untangled into the relevant objects and
        passed into the Maze initialisation method to create a Maze object.
        That maze object is returned from this function.

        Keyword arguments:
        maze -- Maze object being created.
        json_file_name -- Name of the the json file containing the Maze object's
        data.
        """
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

                walls = json_object['walls']

            return maze(dimension_count, dimension_lengths, dimensions_locked,
                        player, goal, items, events, walls)


    def move_player(self, dimension, direction):
        """Moves a player within the maze if possible.

        On receiving the dimension and direction a player wishes to move this is
        contrasted with the walls of the maze. If a wall is obstructing the
        player's path, the player won't move and False well be returned,
        otherwise the player will move and True will be returned.

        The walls of a grid cell in the maze are represented by a binary number.
        A 0 in the lowest bit of that number means there is no wall in +ve
        direction of the 1st dimension, a 1 in that place means there is a wall.
        0 and 1 mean the same thing in the second lowest bit for the -ve
        direction of the 1st dimension. This pattern continues for the 3rd and
        4th lowest bits for the 2nd dimension, the 5th and 6th lowest bits for
        third dimension and so on.

        Keyword arguments:
        dimension -- The number of the dimension the player is moving through.
        direction -- The direction the player is moving along that dimension,
            1 for +ve and -1 for -ve.
        """
        #Translate player's is movment to a power of 2, 1 for +ve 1st dimension,
        #2 for -ve 1st dimension, 4 for +ve 2nd dimension and so on.
        test = 2 ** (dimension * 2 + int(direction < 0))

        #Perform a bitwise and to test if there is a wall in the player's way.
        if not (self.get_wall_number() & test):
            self.player.move(dimension, direction)
            return True

        return False

    def get_wall_number(self):
        """Gets number for walls in the grid cell the player is currently in."""
        wall_number = self.walls
        for i in reversed(self.player.position):
            wall_number = wall_number[i]

        return wall_number