###########################################################################################
# File holds the data contract of observations that are used by agents for consistency.
###########################################################################################

# imports
from dataclasses import dataclass

# Implementation
@dataclass
class Observation:
    snake_position: tuple # (x,y) coordinates of the snake. This can later be made into a list if there are multiple snakes.
    prey_list: list # list of prey objects
    wall_position: list # currently not in use, but may be used when geometries become more sophisticated
    grid_size: int # currently a single integer, but can be made into a tuple if the grid is no longer a square shape.
    sz_list: list # list of safe_zone objects containing all safe zone related data for all existing safe zones.
    valid_moves: list # list containing candidate moves for an agent