# General imports
import sys
import pandas as pd
import json;

# Dependency imports
from src.simulation.environment import Game, STEPS
from src.simulation.observations import Observation
from src.visualization.visualize import visualize_game


# World global variables moved to environment.py
DEBUG = False

# Agent class moved to agents.py; TODO: replace code with necessary imports

# SafeZone class moved to environment.py; TODO: replace with necessary imports

# Game class moved to environment.py; TODO: replace with necessary imports

# visualize_game function moved to visualization/visualize.py; TODO: replace with necessary imports

def game_write_to_file(observation: Observation, step_count: int):
    # Save the current game to a file for later analysis.


    data = {
        #'game': 0, # I want to implement a game counter for the visualization portion
        'step': step_count,
        'snake_position': (observation.snake_position[0], observation.snake_position[1]),
        'prey_positions': [(prey.x, prey.y, True if hasattr(prey.policy, 'learn') else False, prey.alive, prey.generation) for prey in observation.prey_list],
        'safe_zone_status': [(sz.x, sz.y, sz.size, sz.active, sz.current_occupants) for sz in observation.sz_list]
        }

    with open('game_log.jsonl', 'a') as f:
        f.write(json.dumps(data) + '\n')
    
def game_from_file(filename):
    # Load a game from a file. This is for analysis and visualization of past games, not for resuming a game. It returns a list of game states.
    with open(filename, 'r') as f:
        game_states = [json.loads(line) for line in f]
        
    return game_states

if __name__ == "__main__":
    
    game = Game()

    for _ in range(STEPS):
        events, observation = game.step()
        game_write_to_file(observation, game.step_count)
    
    try:
        game_states = game_from_file('game_log.json')
        seek = int(input(f"Enter the step number to seek to (0 - {len(game_states)-1}) or -1 to run through all: "))
        
        if seek == -1:
            visualize_game(game_states)
        else:
            interval = int(input(f"Enter the number of steps to visualize from the seek point (1 - {len(game_states) - seek}): "))
            visualize_game(game_states, seek = seek, step_interval = interval)

    except FileNotFoundError:
        print("File not found.")
    