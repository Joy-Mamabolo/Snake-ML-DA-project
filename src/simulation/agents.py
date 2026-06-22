#############################################################################################
# The intent of this file is to manage all agent related code in one place.
# Agents are decision makers only. They do not do anything else other than get the data they need to make decisions.
# This will make it easier to locate agent related code in the future should changes need to be made.
# Important to also note that the prey agent also had with it elements of q-learning logic, which will now be decoupled
# and transfered to the q_learning.py script. This will help scale q-learning logic to other agents in future should
# that become desirable.
##############################################################################################
class Agent:
    def __init__(self, x, y, policy, speed = 1, symbol = 'A'):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.speed = speed
        self.symbol = symbol
        self.actions = [(0,self.speed),(0,-self.speed),(self.speed,0),(-self.speed,0)] #Up, Down, Right, Left
        self.policy = policy
    
    def move(self, dx, dy, grid_size):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x = max(0, min(grid_size-1, self.x + dx*self.speed))
        self.y = max(0, min(grid_size-1, self.y + dy*self.speed))
    
    def propose_move(self, observation):
        
        return self.policy.choose_action(self, observation)

class Snake(Agent):
    def __init__(self, x, y, policy):
        super().__init__(x, y, policy,symbol = 'S')

        # Removed the previous location parameters to agent class as it is generally useful to all agents


# TODO: Remove all q-learning functionality and logic to q_learning.py
class Prey(Agent):
    def __init__(self, x, y, policy):
        super().__init__(x, y, policy,speed = 1, symbol="P")
        self.alive = True
        self.generation = 0 # generation of the prey - also used to track how many times the prey has been captured and respawned.
        self.last_act = (int(0),int(0)) # This records the last move the prey proposed not the action enforced by the game class
    

    def observe(self, world): # potential_act is no longer necessary as the function is only used to observe the current state and not potential next states.
        # This function defines how the prey observes the world. Characters are used to encode different things as follows:
        # Each cell contains 2 pieces of information: cell type and occupant
        # cell type can be either active safe zone ('O+'), inactive safe zone ('O-'), or empty ('.')
        # occupant will be 'P' for prey and 'S' for snake or "." for neither.
        # walls will be encoded as 'XXX' in order to maintain consistent patterns and lengths.
        # Safe zone distance pointers will also be given representing closer, further or same

        # 3x3 grid around the prey
        neighbourhood = ""

        # Modify observe so that it can provide next state as well as current state.

        # reverted back to the original implementation.
        for dx in range(-1,2):
            for dy in range(-1,2):
                nx = self.x + dx
                ny = self.y+dy

                if world.is_in_bounds(nx,ny):
                    # cell type:
                    in_sz, sz_active = world.is_in_safe_zone(nx,ny)

                    if in_sz:
                        if sz_active:
                            neighbourhood+="O+"
                        else:
                            neighbourhood+="O-"
                    else:
                        # normal cell type encoded with "NN" for normal, and doubled to maintain consistent length with other cell type
                        neighbourhood+="NN"

                    # Occupant type
                    if world.snake.x == nx and world.snake.y == ny:
                        neighbourhood+="S"
                    elif any(prey.x == nx and prey.y == ny for prey in world.prey_list):
                        neighbourhood+='P'
                    else:
                        neighbourhood+='.'
                else:
                    neighbourhood+='XXX'# Out of bounds
        
        return neighbourhood 