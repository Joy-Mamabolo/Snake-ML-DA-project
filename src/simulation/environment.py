##################################################################################################################
# This file is the world object file. It holds the state of all objects and controls the simulation loop.
##################################################################################################################

# General imports
import json
import random
from collections import defaultdict

# Dependency imports
from src.simulation.observations import Observation
from src.simulation.agents import Snake, Prey
from src.simulation.policy import GreedyPolicy, RandomPolicy, QlearningPolicy
from src.simulation.rules import is_in_safe_zone, is_in_bounds, is_safe_zone_active, boundary_collision, agent_collision


# Global variables - TODO: Place these in a configuration file.

GRID_SIZE = 20
NUM_PREY = 6
NUM_LEARNING_PREY = 3
STEPS = 1000
DEBUG = False
SZ_SIZE = 6
SZ_CAP = 3

# Rewards
CAPTURE = -10
SURVIVOR = 1
SAFE_SURVIVOR = 2
BOUNDARY = -5

# Could potentially be moved else where later
class Custom_Error(Exception):
    """ Base Class for custom errors 
    """
    pass

class World_Building_Error(Custom_Error):
    """ The intent of this class is to capture world building errors and interrupt the simulation.
        These can include: 
            > gaps in the outer boundary which could allow some to cause index errors by moving into 
            spaces beyond the allocated array space.
            > respawn zone overlaps with any existing walls (special or boundary)
    """
    def __init__(self, x, y):

        self.message = f"Respawn zone tile and wall tile overlap at {x,y}"
        super().__init__(self.message)
    
    def get_message(self):
        return self.message



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

        # world
        self.grid_size = grid_size
        self.walls = set() # Will hold a set of tuples of all walls. Made these sets, since overlaps are redundant. This will make membership checks quicker.
        self.spawn_zones = []
        self.build_world() # world_builder function that populates self.walls
        self.safe_zone = [SafeZone(5, 5)] # x,y of safe zone represents bottom left corner
        
        
        # agents
        self.snake = Snake(grid_size//2, grid_size//2, GreedyPolicy())
        self.prey_list = self.build_prey_list(num_prey, NUM_LEARNING_PREY)

        # rewards description for ease of access and modification.
        self.rewards = {"boundary_collision": BOUNDARY,
                        "unauthorized_sz_entry": BOUNDARY,
                        "capture": CAPTURE,
                        "survival": SURVIVOR,
                        "survival_in_sz": SAFE_SURVIVOR}

        # utility
        self.step_count = 0 # keep track of the number of steps taken in the game
    
    def build_world(self, special_walls = [], spawn_zones = []):
        """
        Function populates the walls attribute of the world returning a list of tuples representing each tile that
        exists in the world.
        Current implementation is used for only outer boundaries, but function was built to scale if additional 
        obstacles are added to the world.
        
        Add designated spawn zones for prey. These zones are for ease of deciding respawn points for prey.
        This will be especially useful when the map geometry becomes more complex
        If spawn_zones are not specified, the default will be assumed to be the 4 corner areas of the square map.
        spawn_zones are specified as a list of tuples(x,y) each representing a possible respawning coordinate.
        This will make complex respawning area geometry possible
        """

        # Add outer boundary walls - Currently only supports square maps
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if x == 0 or x == self.grid_size-1 or y == 0 or y == self.grid_size-1:
                    self.walls.add((x,y))
        
        # Add special walls if defined where special walls are defined as a list of tuples
        for x,y in special_walls:
            self.walls.add((x,y))

        # Add spawn zones
        try:
            if spawn_zones:

                for x,y in spawn_zones:

                    if boundary_collision(self.walls, x,y):
                        raise World_Building_Error(x,y)
                    else:
                        self.spawn_zones.append((x,y))

            else:
                
                for x,y in [(0,0),(0,self.grid_size-1), (self.grid_size-1, 0), (self.grid_size-1, self.grid_size-1)]:

                    for i in range(1,3):

                        if x:
                            i = -i

                        for j in range(1,3):
                            
                            if y:
                                j = -j

                            if boundary_collision(self.walls, x+i,y+j):
                                raise World_Building_Error(x+i,y+j)
                            else:
                                self.spawn_zones.append((x+i,y+j))

        except World_Building_Error as e:
                print(e)
                exit(1) # exit the program if there is a world building error. This is to prevent the simulation from running in an invalid state.
                

    def build_prey_list(self, total_prey, num_learning):
        
        prey_list = [Prey(random.randint(0,self.grid_size-1), random.randint(0,self.grid_size-1),RandomPolicy()) for _ in range(total_prey-num_learning)]

        for _ in range(num_learning):

            prey_list.append(Prey(random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1), QlearningPolicy()))
        
        return prey_list
    
    def agent_spawn(self, prey_list):

        for agent in prey_list:

            # Function handles prey respawning after captures.
            # It assigns the value directly and does not return anything.

            if agent.alive == False: 
                # if the agent is prey (for future scaling)
                agent.alive = True
                agent.last_act = (0,0) # Default value after spawning (representing a diagonal move which is not permitted)
                agent.generation+=1 # Counter for number of captures

                # More sophisticated implementation is possible, like furthest from current position, but this is sufficient for now.
                agent.x,agent.y = random.choice([(i,j) for i,j in self.spawn_zones])


    # is_in_safezone function moved to rules.py. Replaced with necessary imports.

    # is_in_bounds function moved to rules.py. Replaced with necessary imports.
    
    def get_valid_moves(self, agent)->list:

        if agent == self.snake:
            
            actions = []

            for act in agent.actions:
                
                # For all possible actions

                # Check attempted safe zone entry
                for sz in self.safe_zone:

                    if sz.active and is_in_safe_zone(sz.x, sz.y, sz.size, agent.x+act[0], agent.y+act[1]):
                        # attempted to enter an active safe zone - prevent invalid move
                        break
                else:
                    # check wall interaction only if cleared safe zone checks

                    if not boundary_collision(self.walls, agent.x+act[0], agent.y+act[1]):
                        # Only append action after boundary_collision checked.
                        actions.append(act)

            return actions

        else:
            # All prey actions attract a reward and are therefore not restricted by the environment
            return agent.actions

    def build_observation(self, agent=None):
        """Build observations for all agents in the game."""
        
        if agent is None:
            # Build observation for prey agents which is by default all available actions since prey actions carry rewards and are therefore not restricted by the environment
            candidate_moves = [] # Valid moves are not required for prey agents since all actions attract a reward and are therefore not restricted by the environment
        else:
            candidate_moves = self.get_valid_moves(agent)

        return Observation(
            snake_position = (self.snake.x, self.snake.y),
            prey_list = self.prey_list,
            wall_position = self.walls, # Currently implemented for boundary walls to make scaling to more complex geometries easier.
            grid_size = self.grid_size,
            sz_list = self.safe_zone,
            valid_moves = candidate_moves
        )
    
    def get_actions(self, snake_obs, prey_obs):
        """Get proposed actions for all agents based on the current observation."""

        actions = {}

        actions[self.snake] = self.snake.propose_move(snake_obs)
        
        for prey in self.prey_list:
            actions[prey] = prey.propose_move(prey_obs)

            """ This is to keep record of prey's proposed move which will be used to assign the reward in scenarios where
                the game class enforces a different move due to an illegal proposed move
            """
            prey.last_act = actions[prey] 
        
        return actions

    def enforce_actions(self, actions):
        """
        Enforce the proposed actions for all agents. This function checks if proposed actions are valid and executes them. It imposes alternative actions if proposed actions are invalid. 
        Function does not return anything, but updates the state of the game in place."""
        
        events = defaultdict(list) # to be used for reward allocations

        for agent, action in actions.items():

            if boundary_collision(self.walls, agent.x+action[0], agent.y+action[1]):
                events[agent].append("boundary_collision")
                agent.move(0,0)
            
            if agent == self.snake:
                
                # implement the safe_zone check   
                for sz in self.safe_zone:
                    if is_in_safe_zone(sz.x, sz.y, sz.size, agent.x+action[0],agent.y+action[1]):
                        events[agent].append("unauthorized_sz_entry")
                        agent.move(0,0)
                        break
                else:
                    agent.move(action[0],action[1])
            else:
                agent.move(action[0],action[1])

        return events         
            
    def detect_events(self, events:dict):
        """
        events is a dictionary that has illegal move events populated if there were any
        The intent of this function is to add remaining events which also attract rewards for learning agents.
        These include survival, survival in safe zone, and captures.
        It should be noted that the values of events are lists which should be appended to in the event that
        more than one event is possible for an agent - for instance illegal move + capture"""

        # check for captures
        for prey in self.prey_list:

            if agent_collision(self.snake,prey):

                # Mark prey as captured
                prey.alive = False
                prey.generation+=1 # increment generation counter for number of captures

                # Update events
                if prey in events:
                    events[prey].append("capture")
                else:
                    events[prey] = ["capture"]

            else:
                # Check for survival and survival in safe zone
                
                for sz in self.safe_zone:

                    if sz.active and is_in_safe_zone(sz.x, sz.y, sz.size, prey.x, prey.y):
                        # event only applicable if sz is active
                        if prey in events:
                            events[prey].append("survival_in_sz")
                        else:
                            events[prey] = ["survival_in_sz"]
                        break
                else:
                    # Executes if break in for loop not triggered
                    if prey in events:
                        events[prey].append("survival")
                    else:
                        events[prey] = ["survival"]

        return events
    
    def assign_rewards(self, all_events:dict):
        """
        Function takes the reward dictionary and assigns rewards to all the agents that have rewards due
        The reward values are defined in the game constructor for ease of access and modification.
        The result will be used for learning for the agents that have the capability
        Note that rewards are computed for all agents, whether they have learning functionality or not.
        This is so that should their policies change in the future, the reward assignment system will not need to be changed much. """
        
        rewards = defaultdict(int) # some agents may be due for more than one reward, for instance for boundary_collision + capture in the same turn

        for agent, events in all_events.items():

            for event in events:
                rewards[agent]+=self.rewards[event]
        
        return rewards
    
    def update_learning(self, rewards, observations: tuple, next_observations: tuple):

        """
        Function updates the learning agents with the rewards they are due.
        The function assumes no knowledge of learning and non-learning agents and accommodates both.
        The observation and next_observation tuples are in the order of snake first then prey in both cases.
        It is worth noting, however, that in the current implementation, only the prey has learning functionality.
        """

        for agent, val in rewards.items():

            if hasattr(agent.policy, "learn"):

                if agent == self.snake:
                    agent.policy.learn(agent, val, observations[0], next_observations[0])
                else:
                    agent.policy.learn(agent, val, observations[1], next_observations[1])
        
    def sz_admissions(self):

        for sz in self.safe_zone: # there is only one safe zone for now but this allows for more than one should we wish

            sz.current_occupants = 0 # must reset in every step so that it keeps the current count and not total count

            # Set safe zone to off as soon as snake is inside, even if snake spawned there. Alternatively prohibit snake from spawning in sz

            for prey in self.prey_list:
                if is_in_safe_zone(sz.x, sz.y, sz.size, prey.x, prey.y):
                    sz.current_occupants +=1

            sz.active = is_safe_zone_active(sz.capacity, sz.current_occupants, sz.x, sz.y, sz.size, self.snake.x, self.snake.y)


    
    def step(self):

        self.step_count+=1

        # Respawn any captured prey
        self.agent_spawn(self.prey_list)

        # Safe Zone admissions
        self.sz_admissions()

        # build observation for all agents based on current state of the game. This is done before any agent moves so that all agents make decisions based on a single source of truth.
        snake_obs = self.build_observation(self.snake)
        prey_obs = self.build_observation() # does not need to add agent argument, default is fine

        # agents propose moves
        proposed_actions = self.get_actions(snake_obs, prey_obs)

        # enforce moves based on rules and generate events of invalid moves
        events = self.enforce_actions(proposed_actions) # invalid move events

        # detect other events
        all_events = self.detect_events(events)

        # calculate rewards
        rewards = self.assign_rewards(all_events)

        # Use rewards to update Q table
        next_snake_obs = self.build_observation(self.snake)
        next_prey_obs = self.build_observation()

        self.update_learning(rewards, (snake_obs, prey_obs), (next_snake_obs, next_prey_obs))
        
        return all_events, prey_obs