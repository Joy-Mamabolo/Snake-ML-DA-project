#############################################################################################
# The intent of this file is to manage all agent related code in one place.
# Agents are decision makers only. They do not do anything else other than get the data they need to make decisions.
# This will make it easier to locate agent related code in the future should changes need to be made.
# Important to also note that the prey agent also had with it elements of q-learning logic, which will now be decoupled
# and transfered to the q_learning.py script. This will help scale q-learning logic to other agents in future should
# that become desirable.
##############################################################################################
class Agent:
    def __init__(self, x, y, speed = 1, symbol = 'A'):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.speed = speed
        self.symbol = symbol
        self.actions = [(0,self.speed),(0,-self.speed),(self.speed,0),(-self.speed,0)] #Up, Down, Right, Left
    
    def move(self, dx, dy, grid_size):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x = max(0, min(grid_size-1, self.x + dx*self.speed))
        self.y = max(0, min(grid_size-1, self.y + dy*self.speed))

class Snake(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, symbol = 'S')

        # Removed the previous location parameters to agent class as it is generally useful to all agents

    
    def choose_action(self, observation):

        # added an observation object that contains prey_list among other things

        #prey_distance = [] 

        closest_prey = None
        min_distance = float('inf')

        for prey in observation.prey_list:
            distance = (abs(self.x-prey.x) + abs(self.y - prey.y))
            # prey_distance.append((prey, distance))
            
            if distance < min_distance:
                min_distance = distance
                closest_prey = prey
        
        if closest_prey:
            if closest_prey.x == self.x:
                # snake and prey are on the same vertical line, but at different heights
                return (0, self.speed) if closest_prey.y>=self.y else (0, -self.speed) # go up if the prey is above, otherwise go down
            elif closest_prey.y == self.y:
                # snake and prey are on the same horizontal line, but at different widths
                return (self.speed, 0) if closest_prey.x>=self.x else (-self.speed,0) # go right if prey is to the right, otherwise left
            elif closest_prey.x>closest_prey.y:
                # when deciding whether to move vertically or horizontally, favour the larger distance - x
                return (self.speed, 0) if closest_prey.x>=self.x else (-self.speed, 0)
            else:
                # when deciding whether to move vertically or horizontally, favour the larger distance - y
                return (0, self.speed) if closest_prey.y>=self.y else (0, -self.speed)
        else:
            return 0, 0 # if there are no prey, stay in place - should not be the case since the game should end when all prey are captured


# TODO: Remove all q-learning functionality and logic to q_learning.py
class Prey(Agent):
    def __init__(self, x, y, learning = False):
        super().__init__(x, y, speed = 1, symbol="P")
        self.alive = True
        self.generation = 0 # generation of the prey - also used to track how many times the prey has been captured and respawned.
        self.last_act = (int(0),int(0)) # This records the last move the prey proposed not the action enforced by the game class

        self.learning = learning

        if learning:
            self.q_table = {} # State-action value table for Q-learning not implemented yet
            #self.reward = 0 # reward received in the current step, used for learning prey. Not implemented yet
            self.alpha = 0.3
            self.gamma = 0.9
            self.epsilon = 0.1
            self.old_state = ""
            
    
    def get_q(self, state, action):
        # Function takes q_table key consisting of a state string and action tuple, where the action is itself a tuple encoding
        # up, down, left, right using positive and negative binary digit combinations. if the dictionary key does not exist, it returns 0.0
        # In a scenario where the prey agent is captured, the function must return a next_q value of 0.0, as it is not known at this stage where
        # the prey will respawn

        if self.alive:
            try: 
                return self.q_table[(state, action)]
            
            except KeyError:
                # KeyError means that state and action combination do not exist in the current q-table. Update q-table and return 0.0

                self.q_table[(state, action)] = 0.0

                return 0.0
            else:
                print("Unknown Error involving q-table data extraction using key.")
                raise UnboundLocalError
        else:
            # It is assumed that this will only be used for getting next_q after prey capture
            return 0.0
    
    def update_q_table(self, state, action, reward, next_state = None):
        old_q = self.get_q(state, action) #because of how get_q is defined, if state and action combination do not exist, they are created
        
        if next_state:
            next_q = max([self.get_q(next_state, a) for a in self.actions]) # Return the largest q-value (assuming optimal play)
        else:
            next_q = 0.0

        # Bellman Eq.
        new_q = old_q + self.alpha*(reward + self.gamma*next_q-old_q)

        self.q_table[(state, action)] = new_q

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
    
    def propose_move(self, world): # Function is used to propose a move for prey agents. It no longer computes potential next states, and thus does not need the potential_act argument anymore.
        if self.learning:
            # Observe the world and update the Q-table based on the reward received from the previous action. Then select an action based on the Q-table. Not implemented yet.
            
            # Observe
            current_state = self.observe(world)

            # Determine if we consult q-table or explore using epsilon
            if random.random()<self.epsilon:
                # Be adventurous, explore - ignore q-table and make a random move
                candidate = [random.choice(self.actions)] # made it a list for consistency
            else:
                # Be principled - consult your q-table
                candidate = [(0,0)] # default value although it should not be necessary  TODO: Remove default candidate value. It is guaranteed that there will be at least one action with a q-value of at least 0.0
                threshold = 0.0

                for action in self.actions:
                    q = self.get_q(current_state, action)
                    if q > threshold:
                        # Best move thus far
                        threshold = q # raise standard for best move
                        candidate = [action] # Erase previous moves if there were any
                    elif q == threshold:
                        # One of the best moves, choose any
                        candidate.append(action)
                    else:
                        # Not good enough
                        pass

                # Make final choice randomly if more than one decision possible
            if len(candidate)>1:
                # more than one best move
                last_act= random.choice(candidate)
            else:
                # Only one answer
                last_act= candidate[0] # tuple not list
            
            
            return last_act, current_state
            
        else:
            last_act =  random.choice(self.actions)
        
        return last_act, ""