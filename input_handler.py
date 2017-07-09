"""TODO: Complete Docstring: input_handler.py"""

import pygame
from enum import Enum

class Input_Handler:

    """TODO: Complete Docstring: Event Class."""

    def __init__(self):

        """TODO: Complete Docstring: __init__ Function."""

        pygame.init()

    def handle_key_event(self, keys):

        if keys[pygame.K_ESCAPE]:
            return (Input_Type.EXIT, -1, -1)

        for direction in range(0, 2):
            for dimension in range(0, 9):
                if (keys[pygame.K_1 + dimension] and 
                    keys[pygame.K_UP + direction]):
                    print("MOVE_4D", dimension, -2 * direction + 1)
                    return (Input_Type.MOVE_4D, dimension, -2 * direction + 1)

        for direction in range(0, 2):
            for dimension in range(1, 9):
                if (keys[pygame.K_1 + dimension] and
                    keys[pygame.K_w - 4 * direction]):
                    print("ROTATE_4D", dimension, -2 * direction + 1)
                    return (Input_Type.ROTATE_4D, dimension, -2 * direction + 1)

        if (keys[pygame.K_UP]):
            print("UP")
            return (Input_Type.MOVE_3D, 0, 1)
        elif (keys[pygame.K_DOWN]):
            print("DOWN")
            return (Input_Type.MOVE_3D, 0, -1)
        elif keys[pygame.K_RIGHT]:
            print("RIGHT")
            return (Input_Type.MOVE_3D, 1, 1)
        elif keys[pygame.K_LEFT]:
            print("LEFT")
            return (Input_Type.MOVE_3D, 1, -1)
        elif keys[pygame.K_z]:
            print("Z")
            return (Input_Type.MOVE_3D, 2, 1)
        elif keys[pygame.K_x]:
            print("X")
            return (Input_Type.MOVE_3D, 2, -1)
        elif keys[pygame.K_d]:
            print("D")
            return (Input_Type.ROTATE_3D, [0, 1], 1)
        elif keys[pygame.K_a]:
            print("A")
            return (Input_Type.ROTATE_3D, [0, 1], -1)
        elif keys[pygame.K_w]:
            print("W")
            return (Input_Type.ROTATE_3D, [0, 2], 1)
        elif keys[pygame.K_s]:
            print("S")
            return (Input_Type.ROTATE_3D, [0, 2], -1)
        elif keys[pygame.K_q]:
            print("Q")
            return (Input_Type.ROTATE_3D, [1, 2], 1)
        elif keys[pygame.K_e]:
            print("E")
            return (Input_Type.ROTATE_3D, [1, 2], -1)
        else:
            print("Invalid")
            return (Input_Type.INVALID_MOVE, -1, -1)

class Input_Type(Enum):

    """TODO: Complete Docstring: ItemType Class."""

    INVALID_MOVE = -1
    EXIT = 0
    MOVE_3D = 1
    ROTATE_3D = 2
    MOVE_4D = 3
    ROTATE_4D = 4