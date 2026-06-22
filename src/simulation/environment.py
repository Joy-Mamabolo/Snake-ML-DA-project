##################################################################################################################
# This file is the world object file. It holds the state of all objects and controls the simulation loop.
##################################################################################################################

# General imports
import json
import random

# Dependency imports
from observations import Observation
from agents import Snake, Prey
from policy import GreedyPolicy, RandomPolicy, QlearningPolicy
from rules import is_in_safe_zone, is_in_bounds, is_safe_zone_active


# Global variables - TODO: Place these in a configuration file.

GRID_SIZE = 20
NUM_PREY = 6
NUM_LEARNING_PREY = 3
STEPS = 100000
DEBUG = False
SZ_SIZE = 6
SZ_CAP = 3

# Rewards
CAPTURE = -10
SURVIVOR = 1
SAFE_SURVIVOR = 2
BOUNDARY = -5

# Implementation
class SafeZone:
    def __init__(self, x, y, size = SZ_SIZE, capacity = SZ_CAP):
        # x,y represents bottom left corner of safe zone
        self.x = x
        self.y = y

        self.size = size # safe zone is a square of length size

        self.capacity = capacity
        self.current_occupants = 0 # number of prey currently in the safe zone

        self.active = True # whether the safe zone is currently preventing snake entry. If the safe zone is beyond capacity, it becomes inactive and allows the snake to enter and capture prey inside. The safe zone becomes active again once the number of occupants falls below capacity and snake is no longer inside the safe zone
    
        # Deleted the list of occupants in favour of just keeping track of the number. Also don't need to track admission or release.

class Game:
    def __init__(self, grid_size = GRID_SIZE, num_prey = NUM_PREY):
        self.grid_size = grid_size
        self.snake = Snake(grid_size//2, grid_size//2, GreedyPolicy())
        
        self.prey_list = self.build_prey_list(num_prey, NUM_LEARNING_PREY)

        self.safe_zone = [SafeZone(5, 5)] # x,y of safe zone represents bottom left corner
        self.step_count = 0 # keep track of the number of steps taken in the game
    

    def build_prey_list(self, total_prey, num_learning):
        
        prey_list = [Prey(random.randint(0,self.grid_size-1), random.randint(0,self.grid_size-1),RandomPolicy()) for _ in range(total_prey-num_learning)]

        for _ in range(num_learning):

            prey_list.append(Prey(random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1), QlearningPolicy()))
        
        return prey_list

    # is_in_safezone function moved to rules.py. Replaced with necessary imports.

    # is_in_bounds function moved to rules.py. Replaced with necessary imports.

    def step(self):
        # snake moves
        self.step_count+=1
        sdx,sdy = self.snake.propose_move(observation) # chase function determines the proposed move of the snake and game checks if the move is valid before executing it.

        proposed_snake_x = self.snake.x + sdx
        proposed_snake_y = self.snake.y + sdy

        #print(f"proposed_snake-x: {self.snake.x, sdx}\tproposed_snake_y: {self.snake.y, sdy}")

        if is_in_bounds(proposed_snake_x, proposed_snake_y, self.grid_size):
            for sz in self.safe_zone:
                if (sz.active and sz.x <= proposed_snake_x < sz.x + sz.size and sz.y <= proposed_snake_y < sz.y + sz.size):
                    #print("Safe Zone Entry prevention")
                    self.snake.prev_x, self.snake.prev_y = self.snake.x, self.snake.y
                    # self.snake.move(0, 0) # if proposed move is into an active safe zone, stay in place. Would like to consider other options later.
                    # Alternative implementation of what happens after invalid move

                    if self.snake.x ==sz.x or self.snake.x==sz.x+sz.size: 
                        # stuck on left or right wall of safe zone, move either up or down
                        if self.snake.y >= sz.y+sz.size//2:
                            # more than half way up - go up (assuming wall is sketched from bottom left corner)
                            self.snake.move(0,self.snake.speed, self.grid_size)
                        else:
                            # less than half way up - go down
                            self.snake.move(0, -self.snake.speed, self.grid_size)
                    else:
                        # stuck on top or bottom wall of safe zone, move either left or right
                        if self.snake.x >= sz.x+sz.size//2:
                            # more than half way right, go right
                            self.snake.move(self.snake.speed,0, self.grid_size)
                        else:
                            # less than half way right, go left
                            self.snake.move(-self.snake.speed, 0, self.grid_size)
                else:
                    self.snake.prev_x, self.snake.prev_y = self.snake.x, self.snake.y
                    self.snake.move(sdx, sdy, self.grid_size) # proposed move is valid, execute it
        else:
            self.snake.prev_x, self.snake.prev_y = self.snake.x, self.snake.y
            #self.snake.move(0, 0) # if proposed move is out of bounds, stay in place. Would like to consider other options such as bouncing back or wrapping around later.

            # Alternative motion instead of snake not moving - though I don't think this is a likely occurence
            if self.snake.x ==0 or self.snake.x==self.grid_size-1: 
                # stuck on left or right wall of safe zone, move either up or down

                if self.snake.y >= self.grid_size//2:
                    # more than half way up - go up (assuming wall is sketched from bottom left corner)
                    self.snake.move(0,self.snake.speed, self.grid_size)
                else:
                    # less than half way up - go down
                    self.snake.move(0, -self.snake.speed, self.grid_size)
            else:
                # stuck on top or bottom wall of safe zone, move either left or right

                if self.snake.x >= self.grid_size//2:
                    # more than half way right, go right
                    self.snake.move(self.snake.speed,0, self.grid_size)
                else:
                    # less than half way right, go left
                    self.snake.move(-self.snake.speed, 0, self.grid_size)

        #prey moves/acts
        for prey in self.prey_list:
            
            if not prey.alive:
                # Captured Prey Respawns
                prey.x = 0 if self.snake.x>self.grid_size-1-self.snake.x else self.grid_size-1  # furthest distance away from the snake within bounds at that step.
                prey.y = 0 if self.snake.y>self.grid_size-1-self.snake.y else self.grid_size-1
                prey.generation+=1
                prey.alive = True
                prey.last_act = (0,0) # reset last act. It has already been used to update q table in the previous generation.
            

            elif (prey.x == self.snake.x and prey.y == self.snake.y) or (prey.x == self.snake.prev_x and prey.y == self.snake.prev_y):
                # Prey captured

                if prey.learning:
                    # update q-table with capture reward for only learning prey
                    prey.update_q_table(prey.old_state,prey.last_act,CAPTURE) # omit next_state since it will evaluate next_q to 0.0 by default as the next state after capture cannot be confirmed.
                
                prey.alive = False # repositioned to after update_q_table

                # self.prey_list.remove(prey) # remove captured prey from the game. Perhaps prey should not be removed from list, but respawned some safe distance away from snake and log the capture instead
            else:
                # Prey moves

                if prey.learning:
                    #Reward survival first:
                    if prey.last_act != (0,0):
                        # Not initial spawn or respawn, meaning prey survived
                        # update q-table showing survival before new observation in propose_move updates the current_state
                        #act, next_state = prey.propose_move(self, True) # A new move is not actually meant to be proposed yet. In order to define next_state, we only need to evaluate the state now after the prey has moved which is not the same as the prey.old_state.
                        next_state = prey.observe(self) # This is the next state after surviving the last action, but before proposing the next action. It is used to update the q-table with the survival reward for the last action. The proposed move is not actually executed until after the q-table update.

                        prey.update_q_table(prey.old_state,prey.last_act,SAFE_SURVIVOR if "+" in prey.old_state else SURVIVOR,next_state)

                        # update last act
                        # prey.last_act = act moved out of here to preserve the reward update functionality only and not mix it with action proposal.

                    else:
                        # new spawn or respawn about to move for the first time.
                        pass # no reward

                    prey.last_act,prey.old_state = prey.propose_move(self) # Now applies to all learning prey whether it is the first move after spawn/respawn or not.

                else:
                    prey.last_act,_ = prey.propose_move(self)
                
                dx,dy = prey.last_act

                if is_in_bounds(prey.x + dx, prey.y + dy, self.grid_size):
                    # Cannot assign reward here because it is possible that this move results in capture
                    prey.move(dx, dy, grid_size = self.grid_size)

                    # update old_state to actual current state and not potential as was the case for next state
                    # prey.old_state = prey.observe(self) # This is not supposed to be updated here as it overwrites the old_state that is meant to be used for the reward update after the move is executed. When it is going to be updated will be confirmed.
                else:
                    prey.move(0, 0, grid_size = self.grid_size) # if proposed move is out of bounds, stay in place
                    prey.last_act = (0,0) # reset last act since the proposed move was not executed. This also prevents the prey from being rewarded for a move that was not actually executed.
                    
                    if prey.learning:
                        prey.update_q_table(prey.old_state, prey.last_act,BOUNDARY, prey.old_state) # next state is the same as old state since prey does not move.
        
        # check safe zone admissions
        for sz in self.safe_zone: # there is only one safe zone for now but this allows for more than one should we wish

            sz.current_occupants = 0 # must reset in every step so that it keeps the current count and not total count

            # Set safe zone to off as soon as snake is inside, even if snake spawned there. Alternatively prohibit snake from spawning in sz

            for prey in self.prey_list:
                if is_in_safe_zone(sz.x, sz.y, sz.size, prey.x, prey.y):
                    sz.current_occupants +=1

            sz.active = is_safe_zone_active(sz.capacity, sz.current_occupants, sz.x, sz.y, sz.size, self.snake.x, self.snake.y)

        return self.snake, self.prey_list, self.safe_zone

    def game_write_to_file(self):
        # Save the current game to a file for later analysis.
        data = {
            #'game': 0, # I want to implement a game counter for the visualization portion
            'step': self.step_count,
            'snake_position': (self.snake.x, self.snake.y),
            'prey_positions': [(prey.x, prey.y, prey.learning, prey.alive, prey.generation) for prey in self.prey_list],
            'safe_zone_status': [(sz.x, sz.y, sz.size, sz.active, sz.current_occupants) for sz in self.safe_zone]
        }

        with open('game_log.json', 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def game_from_file(self, filename):
        # Load a game from a file. This is for analysis and visualization of past games, not for resuming a game. It returns a list of game states.
        with open(filename, 'r') as f:
            game_states = [json.loads(line) for line in f]
        
        return game_states