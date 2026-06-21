###########################################################################################
# File holds the data contract of observations that are used by agents for consistency.
###########################################################################################

# imports
from dataclasses import dataclass

# Implementation
@dataclass
class Observation:
    prey_list: list # list of prey objects
    wall_position: list # currently not in use, but may be used when geometries become more sophisticated
    grid_size: tuple
    sz_position: list # list of locating anchors of all safe zones