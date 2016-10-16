import json
import pygame

import maze

def initialise():
    pygame.init()
    return

def load_maze(json_file_name):
    with open(json_file_name) as json_file:
        json_object = json.load(json_file)
        if '__type__' in json_object and json_object['__type__'] == 'Maze':
            maze_level = maze.Maze(json_object["dimension_count"],
                             json_object["dimension_lengths"],
                             json_object["dimensions_locked"],
                             json_object["start"],
                             json_object["goal"],
                             json_object["items"],
                             json_object["events"],
                             json_object["grid_walls"])

def main():
    initialise()
    load_maze("test.json")
    return

if __name__ == "__main__":
    main()
    quit()