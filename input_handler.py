"""TODO: Complete Docstring: input_handler.py"""

import pygame


class Input_Handler:

    """TODO: Complete Docstring: Event Class."""

    def __init__(self):

        """TODO: Complete Docstring: __init__ Function."""

        pygame.init()
        #print(vars(self), "\n")

    def handle_key_event(self, key, maze):
        if key == pygame.K_UP:
            print("UP")
            return (0, 0, 1)
        elif key == pygame.K_DOWN:
            print("DOWN")
            return (0, 0, -1)
        elif key == pygame.K_RIGHT:
            print("RIGHT")
            return (0, 1, 1)
        elif key == pygame.K_LEFT:
            print("LEFT")
            return (0, 1, -1)
        elif key == pygame.K_z:
            print("Z")
            return (0, 2, 1)
        elif key == pygame.K_x:
            print("X")
            return (0, 2, -1)
        elif key == pygame.K_d:
            print("D")
            return (1, (0, 1), 1)
        elif key == pygame.K_a:
            print("A")
            return (1, (0, 1), -1)
        elif key == pygame.K_w:
            print("W")
            return (1, (0, 2), 1)
        elif key == pygame.K_s:
            print("S")
            return (1, (0, 2), -1)
        elif key == pygame.K_e:
            print("E")
            return (1, (1, 2), 1)
        elif key == pygame.K_q:
            print("Q")
            return (1, (1, 2), -1)
        else:
            return (-1, 0, 0)