from src.simulation.environment import Game
from src.simulation.rules import boundary_collision

import random

def test_build_world_function_creates_square_default_walls():
    # Arrange
    game = Game(grid_size=5)

    # Act
    game.build_world(special_walls=[]) # No special walls, just the default outer walls

    correct_wall = (0, 0)

    not_walls_count = 0
    for i in range(1, game.grid_size-1):
        for j in range(1, game.grid_size-1):
            if boundary_collision(game.walls, i, j):
                not_walls_count += 1
    
    # Assert 
    assert boundary_collision(game.walls, *correct_wall), f"Wall at {correct_wall} was not created."
    assert not_walls_count == 0, f"Inner walls were created when they should not have been. Count of inner walls: {not_walls_count}"


















if __name__ == "__main__":
    test_build_world_function_creates_square_default_walls()
    print("All tests passed!")