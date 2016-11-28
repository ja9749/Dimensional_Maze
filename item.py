"""TODO: Complete Docstring: item.py"""


from enum import Enum


class Item:

    """TODO: Complete Docstring: Item Class."""

    def __init__(self, item_type, shape_file, position):

        """TODO: Complete Docstring: __init__ Function."""

        self.item_type = ItemType[item_type]
        self.shape_file = shape_file
        self.position = position
        #print(vars(self), "\n")


class ItemType(Enum):

    """TODO: Complete Docstring: ItemType Class."""

    dimension_unlocker = 'dimension_unlocker'
    orientation_resetter = 'orientation_resetter'
    coordinates_displayer = 'coordinates_displayer'
    path_rememberer = 'path_rememberer'
    maze_navigator = 'maze_navigator'
    dimension_swapper = 'dimension_swapper'