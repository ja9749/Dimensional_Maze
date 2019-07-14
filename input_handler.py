"""Input Handler for the game Dimensional Maze.

This module handles takes in all user input for and translates it into actions
in the Dimensional Maze game.
"""
import logging
import pygame
from enum import Enum

#Module level logger. Outputs debug info to external file.
logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG)
logger = logging.getLogger('input_handler')


def handle_key_event(keys):
    """Take in an array of currently pressed down keys and return a game
    action.

    An array of currently pressed down keys is turned into a game action. That
    action is a tuple containing an Input_Type enum value describing the type
    of action, the dimensions involved in the action and the direction the
    action is going.
    
    Keyword arguments:
    keys -- An array representing the keys which are currently pressed down.
        This array is navigatable using the pygame module.
    """
    #If Escape key has been pressed, return the EXIT Input_Type.
    if keys[pygame.K_ESCAPE]:
        logger.debug("Escape")
        return (Input_Type.EXIT, -1, 0)

    #This loop handles commands for movement in any numbered dimension up to
    #nine. If any of the keys 1-9 is pressed at the same time as the Up or Down
    #key, then a this returns the MOVE_4D Input_Type as well as the numbered
    #dimension (from the numbered key pressed minus one) and direction (Up = 1,
    #Down = -1). The numbering of the dimensions is absolute based on the
    #maze's perspective.
    for direction in range(0, 2):
        for dimension in range(0, 9):
            if (keys[pygame.K_1 + dimension] and 
                keys[pygame.K_UP + direction]):
                log = ' '.join(
                    ["MOVE_4D", str(dimension), str(-2 * direction + 1)])
                logger.debug(log)
                return (Input_Type.MOVE_4D, dimension, -2 * direction + 1)

    #This loop handles commands for rotation between the first dimension and
    #any other numbered dimension up to nine. If any of the keys 2-9 is pressed
    #at the same time as the W or S key, then a this returns the ROTATE_4D
    #Input_Type as well as the numbered dimensions involved in the rotation (0
    #and the numbered key pressed minus one) and direction (W = 1, S = -1). The
    #numbering of the dimensions is absolute based on the maze's perspective.
    #The numbering of the dimensions is relative based on the player's
    #orientation, meaning the first dimension is always facing forward.
    for direction in range(0, 2):
        for dimension in range(1, 9):
            if (keys[pygame.K_1 + dimension] and
                keys[pygame.K_w - 4 * direction]):
                log = ' '.join(
                    ["ROTATE_4D", str(dimension), str(-2 * direction + 1)])
                logger.debug(log)
                return (Input_Type.ROTATE_4D, dimension, -2 * direction + 1)

    #This if-else statement handles all commands for movement and rotation
    #within the first three dimensions based on the player's orientation. The
    #keys Up, Down, Right, Left, Z and X move the player forwards, backwards,
    #right, left, up and down in 3D space respectively, while the keys D, A, W,
    #S, Q and E turn the player right, left, up, down, anti-clockwise and
    #clock-wise in 3D space respectively. The  MOVE_3D or ROTATE_3D Input_Type
    #is returned along with the dimension/s involved and the direction.
    if (keys[pygame.K_UP]):
        logger.debug("UP")
        return (Input_Type.MOVE_3D, 0, 1)
    elif (keys[pygame.K_DOWN]):
        logger.debug("DOWN")
        return (Input_Type.MOVE_3D, 0, -1)
    elif keys[pygame.K_RIGHT]:
        logger.debug("RIGHT")
        return (Input_Type.MOVE_3D, 1, 1)
    elif keys[pygame.K_LEFT]:
        logger.debug("LEFT")
        return (Input_Type.MOVE_3D, 1, -1)
    elif keys[pygame.K_z]:
        logger.debug("Z")
        return (Input_Type.MOVE_3D, 2, 1)
    elif keys[pygame.K_x]:
        logger.debug("X")
        return (Input_Type.MOVE_3D, 2, -1)
    elif keys[pygame.K_d]:
        logger.debug("D")
        return (Input_Type.ROTATE_3D, [0, 1], 1)
    elif keys[pygame.K_a]:
        logger.debug("A")
        return (Input_Type.ROTATE_3D, [0, 1], -1)
    elif keys[pygame.K_w]:
        logger.debug("W")
        return (Input_Type.ROTATE_3D, [0, 2], 1)
    elif keys[pygame.K_s]:
        logger.debug("S")
        return (Input_Type.ROTATE_3D, [0, 2], -1)
    elif keys[pygame.K_q]:
        logger.debug("Q")
        return (Input_Type.ROTATE_3D, [1, 2], 1)
    elif keys[pygame.K_e]:
        logger.debug("E")
        return (Input_Type.ROTATE_3D, [1, 2], -1)
    else:
        #If no combination of keys was recognised then it is an invalid
        #command and the INVALID_MOVE Input_Type is returned.
        logger.debug(' '.join(["Invalid", ' '.join(str(key) for key in keys)]))
        return (Input_Type.INVALID_MOVE, -1, -1)

class Input_Type(Enum):
    """An enumerated class for the types of input received from the player

    INVALID_MOVE    For use when an input is not recognised.
    EXIT            For use when an 'exit or quit game' command is recognised.
    MOVE_3D         For use when a command to move within the first three
                    dimensions is recognised.
    ROTATE_3D       For use when a command to rotate within the first three
                    dimensions is recognised.
    MOVE_4D         For use when a command to move through any dimension is
                    recognised.
    ROTATE_4D       For use when a command to rotate through any dimension is
                    recognised.
    """
    INVALID_MOVE = -1
    EXIT = 0
    MOVE_3D = 1
    ROTATE_3D = 2
    MOVE_4D = 3
    ROTATE_4D = 4