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
    
    def move(self, dx, dy):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x = self.x + dx*self.speed
        self.y = self.y + dy*self.speed
    
    def propose_move(self, observation):
        
        return self.policy.choose_action(self, observation)

class Snake(Agent):
    def __init__(self, x, y, policy):
        super().__init__(x, y, policy,symbol = 'S')

        # Removed the previous location parameters to agent class as it is generally useful to all agents


# Removed all q-learning functionality and logic to q_learning.py
class Prey(Agent):
    def __init__(self, x, y, policy):
        super().__init__(x, y, policy,speed = 1, symbol="P")
        self.alive = True
        self.generation = 0 # generation of the prey - also used to track how many times the prey has been captured and respawned.
        self.last_act = (int(0),int(0)) # This records the last move the prey proposed not the action enforced by the game class
    