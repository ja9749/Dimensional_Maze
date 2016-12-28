"""TODO: Complete Docstring: input_handler.py"""

import pygame


class Input_Handler:

    """TODO: Complete Docstring: Event Class."""

    def __init__(self):

        """TODO: Complete Docstring: __init__ Function."""

        pygame.init()
        #print(vars(self), "\n")

    def handle_key_event(self, keys, maze):
        if (keys[pygame.K_1] and keys[pygame.K_UP]):
            print("UP")
            return (2, 0, 1)
        elif (keys[pygame.K_1] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 0, -1)
        elif (keys[pygame.K_2] and keys[pygame.K_UP]):
            print("UP")
            return (2, 1, 1)
        elif (keys[pygame.K_2] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 1, -1)
        elif (keys[pygame.K_3] and keys[pygame.K_UP]):
            print("UP")
            return (2, 2, 1)
        elif (keys[pygame.K_3] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 2, -1)
        elif (keys[pygame.K_4] and keys[pygame.K_UP]):
            print("UP")
            return (2, 3, 1)
        elif (keys[pygame.K_4] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 3, -1)
        elif (keys[pygame.K_5] and keys[pygame.K_UP]):
            print("UP")
            return (2, 4, 1)
        elif (keys[pygame.K_5] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 4, -1)
        elif (keys[pygame.K_6] and keys[pygame.K_UP]):
            print("UP")
            return (2, 5, 1)
        elif (keys[pygame.K_6] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 5, -1)
        elif (keys[pygame.K_7] and keys[pygame.K_UP]):
            print("UP")
            return (2, 6, 1)
        elif (keys[pygame.K_7] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 6, -1)
        elif (keys[pygame.K_8] and keys[pygame.K_UP]):
            print("UP")
            return (2, 7, 1)
        elif (keys[pygame.K_8] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 7, -1)
        elif (keys[pygame.K_9] and keys[pygame.K_UP]):
            print("UP")
            return (2, 8, 1)
        elif (keys[pygame.K_9] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 8, -1)
        elif (keys[pygame.K_0] and keys[pygame.K_UP]):
            print("UP")
            return (2, 9, 1)
        elif (keys[pygame.K_0] and keys[pygame.K_DOWN]):
            print("DOWN")
            return (2, 9, -1)
        elif (keys[pygame.K_1] and keys[pygame.K_w]):
            print("UP")
            return (3, 0, 1)
        elif (keys[pygame.K_1] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 0, -1)
        elif (keys[pygame.K_2] and keys[pygame.K_w]):
            print("UP")
            return (3, 1, 1)
        elif (keys[pygame.K_2] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 1, -1)
        elif (keys[pygame.K_3] and keys[pygame.K_w]):
            print("UP")
            return (3, 2, 1)
        elif (keys[pygame.K_3] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 2, -1)
        elif (keys[pygame.K_4] and keys[pygame.K_w]):
            print("UP")
            return (3, 3, 1)
        elif (keys[pygame.K_4] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 3, -1)
        elif (keys[pygame.K_5] and keys[pygame.K_w]):
            print("UP")
            return (3, 4, 1)
        elif (keys[pygame.K_5] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 4, -1)
        elif (keys[pygame.K_6] and keys[pygame.K_w]):
            print("UP")
            return (3, 5, 1)
        elif (keys[pygame.K_6] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 5, -1)
        elif (keys[pygame.K_7] and keys[pygame.K_w]):
            print("UP")
            return (3, 6, 1)
        elif (keys[pygame.K_7] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 6, -1)
        elif (keys[pygame.K_8] and keys[pygame.K_w]):
            print("UP")
            return (3, 7, 1)
        elif (keys[pygame.K_8] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 7, -1)
        elif (keys[pygame.K_9] and keys[pygame.K_w]):
            print("UP")
            return (3, 8, 1)
        elif (keys[pygame.K_9] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 8, -1)
        elif (keys[pygame.K_0] and keys[pygame.K_w]):
            print("UP")
            return (3, 9, 1)
        elif (keys[pygame.K_0] and keys[pygame.K_s]):
            print("DOWN")
            return (3, 9, -1)
        elif (keys[pygame.K_UP]):
            print("UP")
            return (0, 0, 1)
        elif (keys[pygame.K_DOWN]):
            print("DOWN")
            return (0, 0, -1)
        elif keys[pygame.K_RIGHT]:
            print("RIGHT")
            return (0, 1, 1)
        elif keys[pygame.K_LEFT]:
            print("LEFT")
            return (0, 1, -1)
        elif keys[pygame.K_z]:
            print("Z")
            return (0, 2, 1)
        elif keys[pygame.K_x]:
            print("X")
            return (0, 2, -1)
        elif keys[pygame.K_d]:
            print("D")
            return (1, (0, 1), 1)
        elif keys[pygame.K_a]:
            print("A")
            return (1, (0, 1), -1)
        elif keys[pygame.K_w]:
            print("W")
            return (1, (0, 2), 1)
        elif keys[pygame.K_s]:
            print("S")
            return (1, (0, 2), -1)
        elif keys[pygame.K_e]:
            print("E")
            return (1, (1, 2), 1)
        elif keys[pygame.K_q]:
            print("Q")
            return (1, (1, 2), -1)
        else:
            return (-1, 0, 0)