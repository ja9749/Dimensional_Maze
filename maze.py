import json

class Maze:

	def __init__(self, dimension_count, dimension_lengths,
                     dimensions_locked, start, goal, items, events,
                     grid_walls):
                self.dimension_count = dimension_count
                self.dimension_lengths = dimension_lengths
                self.dimensions_locked = dimensions_locked
                self.start = start
                self.goal = goal
                self.items = items
                self.events = events
                self.grid_walls = grid_walls