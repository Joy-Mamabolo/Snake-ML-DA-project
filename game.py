# General imports
import sys
import pandas as pd

# Dependency imports


# World global variables moved to environment.py
DEBUG = False

# Agent class moved to agents.py; TODO: replace code with necessary imports

# SafeZone class moved to environment.py; TODO: replace with necessary imports

# Game class moved to environment.py; TODO: replace with necessary imports

# visualize_game function moved to visualization/visualize.py; TODO: replace with necessary imports

def main(no_steps = STEPS):
    global STEPS 

    STEPS = no_steps

if __name__ == "__main__":
    
    if DEBUG:
        main(int(sys.argv[1])) # To allow for quick changes in step counts during debugging
    
    mode = input("Enter 1 to play the game, 2 to visualize a past game: ")

    if mode == "1":
        # New simulation and visualization
        print("Starting new game simulation...")
        game = Game()
        for _ in range(STEPS):
            snake, prey_list, safe_zone = game.step()
            game.game_write_to_file()
        
        game_states = game.game_from_file('game_log.json')
        game_data = pd.read_json('game_log.json', lines = True)

        print("Game simulation completed. Starting Visualization...")

        seek = int(input(f"Enter the step number to seek to (0 - {len(game_states)-1}) or -1 to run through all: "))
        
        if seek == -1:
            visualize_game(game_states)
        else:
            interval = int(input(f"Enter the number of steps to visualize from the seek point (1 - {len(game_states) - seek}): "))
            visualize_game(game_states, seek = seek, step_interval = interval)

    else:
        # Visualization of past game from file. This is for analysis and debugging purposes, not for resuming a game.
        print("Visualizing past game from file...")
        game = Game() # dummy game instance to access the game_from_file method. This can be refactored later to avoid the need for a dummy instance.
        try:
            game_states = game.game_from_file('game_log.json')
            game_data = pd.read_json('game_log.json', lines = True) # TODO:consider moving functionality to environment.py
            seek = int(input(f"Enter the step number to seek to (0 - {len(game_states)-1}) or -1 to run through all: "))
        
            if seek == -1:
                visualize_game(game_states)
            else:
                interval = int(input(f"Enter the number of steps to visualize from the seek point (1 - {len(game_states) - seek}): "))
                visualize_game(game_states, seek = seek, step_interval = interval)

        except FileNotFoundError:
            print("File not found.")
            
            

        


    

    #print(game_data.head())
    #print(game_data.tail(10))
    #print(game_data.summary())