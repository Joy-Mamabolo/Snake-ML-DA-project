#############################################################################################
# File holds code for visualising simulation using matplotlib
############################################################################################

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.simulation.environment import GRID_SIZE, STEPS

DEBUG = True

def visualize_game(game_states, grid_size = GRID_SIZE,seek = 0, step_interval = STEPS):

    # the use of seek and step interval will allow for the game to be viewed at an arbitrary point. This will be useful when game steps become excessively large.
    if seek !=0 and step_interval == STEPS:
        step_interval = STEPS-seek # this to handle the default case where step_interval is not defined but SEEK is defined, in which case we want to visualize from SEEK to the end of the game.

    grid = np.zeros((grid_size, grid_size))
    _, ax = plt.subplots()
    img = ax.imshow(grid, cmap = 'tab20', vmin=0, vmax = 4, alpha = 0.5, zorder = 1)

    capture_text = ax.text(1.05,0.95,f"Captures", transform = ax.transAxes, color = "black", fontsize = 8, verticalalignment = "top")

    snake_scatter = ax.scatter([],[], c = "red", label = "Snake", zorder = 3)
    prey_scatter = ax.scatter([], [], c = ["yellow"], label = "Prey", zorder = 2)

    # placeholder markers for legend update to reflect learning and non-learning prey
    learning_prey_marker = ax.scatter([],[], color = "green", marker = "o", label = "Prey (Learning)")
    non_learning_prey_marker = ax.scatter([],[], color = "yellow", marker = "o", label = "Prey (Non-learning)")


    ax.legend(handles = [snake_scatter, learning_prey_marker, non_learning_prey_marker],loc = "upper right", labels = ["Snake", "Prey (Learning)", "Prey (Non-learning)"], framealpha = 0.3)

    for game_state in game_states[seek:seek+step_interval]:

        grid = np.zeros((grid_size, grid_size)) # grid to be used for environment and safezones only, kept here in case the safe zone needs to be updated

        # Mark safe zone
        for sz in game_state['safe_zone_status']:
            grid[sz[0]:sz[0] + sz[2], sz[1]:sz[1] + sz[2]] = 3 if sz[3] else 1

        # Mark snake position
        # grid[game_state['snake_position'][0], game_state['snake_position'][1]] = 1 # No longer using grids because overlaps loses data
        snake_x, snake_y = game_state['snake_position']


        # Mark prey positions
        prey_position = [ (prey[0], prey[1]) for prey in game_state['prey_positions']]

        img.set_data(grid)
        
        snake_scatter.set_offsets([[snake_y, snake_x]])

        if prey_position:
            prey_scatter.set_offsets([(p[1], p[0]) for p in prey_position])

            new_colors = ["yellow" if not p[2] else "green" for p in game_state['prey_positions']]
            prey_scatter.set_facecolor(new_colors)
            
            # TODO: Update legend to reflect learning and non-learning prey 
            # plt.legend(loc = "upper right", labels = ["Snake", "Prey (Non-learning)", "Prey (Learning)"])

            # Add total capture per prey
            capture_string = "\n".join(
                f"Prey_ID {i}: {prey[-1]}times" for i, prey in enumerate(game_state['prey_positions'])
            )
        else:
            prey_scatter.set_offsets([])
            capture_string = ""
            
        capture_text.set_text("Captures:\n"+ capture_string)

        

        plt.title(f'Snake Game Visualization: Step {game_state["step"]}')

        plt.pause(0.5)
    
    plt.show()

    if DEBUG:
        # overwrite JSON file
        with open('game_log.jsonl', 'w'):
            pass