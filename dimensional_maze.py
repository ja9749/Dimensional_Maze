"""Starting point of the game Dimensional Maze.

This module initialises all the necessary components, runs the game loop and 
handles the exit for the game.
"""
import logging
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from input_handler import handle_key_event, Input_Type
from maze import Maze
from display import Display
from dimensional_maze_library import *

#Module level logger. Outputs debug info to external file.
logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG)
logger = logging.getLogger('dimensional_maze')


def play_game(maze):
    """Run game loop until quit or win.

    Run the game loop, listening for and handling inputs while updating the
    display until the player either wins or quits the game.
    
    Keyword arguments:
    maze -- Main game object containing layout of the maze as well as player,
        enemy and item information.
    """
    #Initialise display object and draw maze.
    display = Display(
        maze.player.position, maze.player.orientation, maze.walls)
    display.draw_3D(maze)

    #Variable signalling when to quit the game
    game_exit = False

    #Main game loop. Carries on until an exit condition sets game_exit to True.
    while not game_exit:

        # If the player's position matches the position of the goal, quit game.
        if maze.player.position.tolist() == maze.goal:
            logger.debug("WIN")
            game_exit = True

        # Loop through all events in pygame. This also clears the event queue.
        for event in pygame.event.get():

            #If event is of type QUIT, signal end of game.
            if event.type == pygame.QUIT:
                game_exit = True
                break

            #The only other useful event type is KEYDOWN.
            elif event.type == pygame.KEYDOWN:
                #Get the currently pressed keys and interpret them.
                keys_pressed = pygame.key.get_pressed()
                output = handle_key_event(keys_pressed)
                (input_type, dimension, direction) = output

                #If input_type is of type Exit, signal end of game.
                if input_type == Input_Type.EXIT:
                    game_exit = True
                    break

                #Else if input_type is of type MOVE_, attempt to move player.
                elif (input_type == Input_Type.MOVE_3D or
                      input_type == Input_Type.MOVE_4D):

                    #If input_type is of type MOVE_3D, get relative dimension
                    #and direction from the players current orientation.
                    if input_type == Input_Type.MOVE_3D:
                        (dimension, direction) = relative_move(
                            maze.player.orientation, dimension, direction)

                    #If moving the player is successful, draw the move.
                    if maze.move_player(dimension, direction):
                        display.draw_move(dimension, direction, maze)

                    break

                #Else if input_type is of type ROTATE_XD, rotate player.
                elif (input_type == Input_Type.ROTATE_3D or
                      input_type == Input_Type.ROTATE_4D):

                    #If input_type is of type ROTATE_, transform dimension
                    #into an array of 0 and itself to indicate rotating the
                    #currently facing dimension (0) with the dimension chosen.
                    if input_type == Input_Type.ROTATE_4D:
                        dimension = [0, dimension]

                    #Get relative dimension and direction from the players
                    #current orientation.
                    (dimension, direction) = relative_rotate(
                        maze.player.orientation, dimension, direction)

                    #Rotate player and draw that rotation.
                    maze.player.rotate(dimension, direction)
                    display.draw_rotate(dimension, direction, maze)
                    break


def main():
    """Run Dimensional Maze Game.

    Initialise all necessary data, run game and finally exit. Initialise pygame
    module first, then the maze and subsequent game objects. Run game until
    the player wins or exits the game. Clean up data and quit.
    """
    pygame.init()

    maze = Maze.load_from_file_name('test.json')
    play_game(maze)

    pygame.quit()


if __name__ == '__main__':
    main()
    quit()