###################################################################################################################
# File will contain all decision making policies for all agents.
# These currently include greedy policy for snake based; random policy for some prey and q-learning for the rest.
###################################################################################################################

# Imports
import random # will later import from an rng.py file that will handle seeding
from src.simulation.rules import is_in_safe_zone
from src.simulation.observations import Observation


class GreedyPolicy:

    def propose_action(self, agent, observation):
        closest_prey = None
        min_distance = float('inf')

        for prey in observation.prey_list:
            distance = (abs(agent.x-prey.x) + abs(agent.y - prey.y))
            # prey_distance.append((prey, distance))
            
            if distance < min_distance:
                min_distance = distance
                closest_prey = prey
        
        if closest_prey:
            if closest_prey.x == agent.x:
                # snake and prey are on the same vertical line, but at different heights
                return (0, agent.speed) if closest_prey.y>=agent.y else (0, -agent.speed) # go up if the prey is above, otherwise go down
            elif closest_prey.y == agent.y:
                # snake and prey are on the same horizontal line, but at different widths
                return (agent.speed, 0) if closest_prey.x>=agent.x else (-agent.speed,0) # go right if prey is to the right, otherwise left
            elif closest_prey.x>closest_prey.y:
                # when deciding whether to move vertically or horizontally, favour the larger distance - x
                return (agent.speed, 0) if closest_prey.x>=agent.x else (-agent.speed, 0)
            else:
                # when deciding whether to move vertically or horizontally, favour the larger distance - y
                return (0, agent.speed) if closest_prey.y>=agent.y else (0, -agent.speed)
        else:
            return 0, 0 # if there are no prey, stay in place - should not be the case since the game should end when all prey are captured
        
    
    def alternate_move(self, agent, observation):
        
        # Function is called when the Greedy Algorithm recommends a move that is currently not valid.
        # This scenario is likely to happen when the snake attempts to go into a safe zone while it is active.
        # In more complex world geometries, this can also happen if prey sits behind a wall and snake attempts to go
        # towards the prey.
        # The implementation is simplified in order to avoid duplicating world rules into the policy.py file.
        # The snake will move parallel to the obstacle in the direction of the largest open world.
        # This means if the snake is in the bottom half of the map, it will move towards the top for example.
        # This assumes simple obstacles where prohibition in one direction means the lateral direction is not prohibited.
        # Code will need to be updated when environment obstacles become more complex than this.

        if (0,1) not in observation.valid_moves or (0, -1) not in observation.valid_moves:
            # Right or left move prohibited - which means vertical motion is parallel

            return (agent.speed,0) if agent.y<=observation.grid_size//2 else (-agent.speed,0)
        else:
            # Up or down move prohibited - which means horizontal motion is parallel

            return (0,agent.speed) if agent.x<=observation.grid_size//2 else (-agent.speed,0)

    def choose_action(self, agent, observation):

        action = self.propose_action(agent, observation)

        if action not in observation.valid_moves:

            return self.alternate_move(agent, observation)
        
        return action



class RandomPolicy:
    
    def choose_action(self, agent, observation):

        return random.choice(agent.actions)


class QlearningPolicy:
    
    def __init__(self, q_table=None, epsilon = 0.1, alpha = 0.3, gamma = 0.9):
        self.q_table = q_table if q_table is not None else {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
    
    def get_q(self, state, action):
        # Function takes q_table key consisting of a state string and action tuple, where the action is itself a tuple encoding
        # up, down, left, right using positive and negative binary digit combinations. if the dictionary key does not exist, it returns 0.0
        # In a scenario where the prey agent is captured, the function must return a next_q value of 0.0, as it is not known at this stage where
        # the prey will respawn

        try: 
            return self.q_table[(state, action)]
            
        except KeyError:
            # KeyError means that state and action combination do not exist in the current q-table. Update q-table and return 0.0

            self.q_table[(state, action)] = 0.0

            return 0.0
        else:
            print("Unknown Error involving q-table data extraction using key.")
            raise UnboundLocalError

    def update_q_table(self, state, action, actions, reward, next_state = None):
        old_q = self.get_q(state, action) #because of how get_q is defined, if state and action combination do not exist, they are created
        
        if next_state:
            next_q = max([self.get_q(next_state, a) for a in actions]) # Return the largest q-value (assuming optimal play)
        else:
            next_q = 0.0

        # Bellman Eq.
        new_q = old_q + self.alpha*(reward + self.gamma*next_q-old_q)

        self.q_table[(state, action)] = new_q
    
    def learn(self, agent, reward, observation, next_observation):

        state = self.build_state(agent, observation)
        next_state = self.build_state(agent, next_observation)

        # Get last action
        action = self.get_last_action(agent)
        actions = agent.actions

        # Update q-table
        self.update_q_table(state, action,actions,reward,next_state)
        

        
    def choose_action(self, agent, observation):

        state = self.build_state(agent,observation)
        # Observe the world and update the Q-table based on the reward received from the previous action. Then select an action based on the Q-table.

        # Determine if we consult q-table or explore using epsilon
        if random.random()<self.epsilon:
            # Be adventurous, explore - ignore q-table and make a random move
            candidate = [random.choice(agent.actions)] # made it a list for consistency
        else:
            # Be principled - consult your q-table
            candidate = []
            threshold = 0.0

            for action in agent.actions:
                q = self.get_q(state, action)
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
            act = random.choice(candidate)
        else:
            # Only one answer
            act = candidate[0] # candidate is a list containing a tuple
            
            
        return act

    def build_state(self, agent, observation:Observation):
        """
        The state is a string that encodes what is currently visible to an agent that is available for decision making.
        This function replaces the observe function in previous implementations which was moved to the prey class.
        The state is used as a key in the q-table to store and retrieve q-values for each action.
        Care was taken to ensure that the length of the state is consistent in all possible scenarios.

        The following information is encoded in the state string:
        1. The agent's (prey) current position (x,y)
        2. The position of the snake if it is in its immediate vicinity (3x3 grid around the agent)
        3. Any wall tiles in the agent's immediate vicinity.
        4. The position of any safe zone tiles in the agent's immediate vicinity.
        5. A flag indicating whether the nearest safe zone is active or not.
        6. Distance to the nearest safe zone in bucket ranges (e.g. 0-2, 3-5, 6+ indicated as close, medium, far). The exact ranges may be changed based on the size of the grid in future.
        7. A direction pointer to the nearest safe zone (i.e. N, E, S, W) based on the longest distance and relative position of the agent to the safe zone. 
           e.g. if safe zone is 2 units right and 4 units down relative to the agent, the direction pointer will be S. If 4 and 2 are swapped around, the resulting direction pointer will be E. 
           If the distances are equal, whichever direction is determined first will be used. 
        8. A measure of the occupancy of the safe zone in ranges (e.g. 0%-30%, 30%-60%, 60%-90%, >90% indicated as low, medium, high, critical). The exact ranges may be changed in future. 
        The following is the structure of the state string:
        > '{3x3 grid details showing what is in the immediate vicinity}|{SZ_distance}|{SZ_direction}|{SZ_occupancy}|{SZ_active}'
        > The 3x3 grid details will include:
            - walls represented by 'X'
            - snake represented by 'S'
            - safe zone represented by 'O'
            - empty tiles represented by '.'
        > The safe zone distance and direction measures will default to '-' when agent presently in active safezone
        > SZ_active will have T for true and F for false.
        """
        # Helper functions
        def sz_occupancy(sz_cap, sz_pop):
            
            occ = sz_pop/sz_cap

            # Single letters are used to represent the different ranges to keep state lengths consistent regardless of situation

            if occ <=0.3:
                return "LO" # For low occupancy
            elif occ<=0.6:
                return "MO" # For medium occupancy
            elif occ<=0.9:
                return "HO" # For high occupancy
            else:
                return "CO" # For critical occupancy

        def dnd_to_SZ(x,y,sz_x,sz_y):
            """
            Helper function only required in this method that returns the distance and direction to the nearest
            safe zone. It is based on the current implementation of the safe zone where an anchor point (x,y) is
            given, and everything is calculated relative to that anchor point. At the time of coding this, the
            anchor point represents the bottom left corner of the safe zone. This will need to be changed should
            safe zone definitions change.
            """

            dist_x = sz_x - x
            dist_y = sz_y - y

            if abs(dist_y)>=abs(dist_x):
                # vertical dominates: N or S

                if dist_y>0:
                    direction = "dN" # due North 
                else:
                    direction = "dS" # due South
            else:

                if dist_x>0:
                    direction = "dE" # due East
                else:
                    direction = "dW" # due West

            dist = abs(dist_x)+abs(dist_y)

            # ranges developed on assumption that grid size is 20. TODO: make ranges more robust for different map sizes
            if dist<=6:
                range = "CD" # close distance
            elif dist<=8:
                range = "MD" # Medium distance
            else:
                range = "FD" # Far distance

            return (dist, range, direction)
        

        state = ""

        # build 3x3 grid list of coordinates centered around the prey
        vicinity = []

        for i in range(-1,2):
            for j in range(-1,2):
                vicinity.append((agent.x+i, agent.y+j))
        
        # Populate state string
        for i in vicinity:
            if i == observation.snake_position:
                state+='S'
            elif i in observation.wall_position:
                state+='X'
            else:
                for sz in observation.sz_list:
                    # borrow is in safe zone from rules.py instead of recoding it.
                    if is_in_safe_zone(sz.x, sz.y,sz.size,i[0],i[1]):
                        state+='O'
                        break # once the cell is populated, there is no need to continue checking in other safe zones
                else:
                    # Executed only if the exact vicinity tile is not a safe zone tile.
                    state+='.'
        state+="|" # End of the 3x3 grid section

        # Determine distance and direction to nearest safe zone
        # place holders
        min_distance = float('inf')
        min_rng = "--" 
        min_dire = '--'
        sz_o = ""
        sz_active = ""

        min_inactive_distance = float('inf')
        sz_inactive_o = ""
        

        for sz in observation.sz_list:
            if sz.active and is_in_safe_zone(sz.x,sz.y,sz.size,agent.x,agent.y):
                state+='--' # For distance
                state+='|' # Next section
                state+='--' # For direction
                state+='|' # Next section
                state+=sz_occupancy(sz.capacity,sz.current_occupants) # SZ occupancy measure
                state+='|' # Next section
                state+='T' # Safe zone active: 'T' for True otherwise 'F'

                break # No need to continue with the loop
            elif sz.active:
                # safe zone active but not in safe zone
                d,rng,dire=dnd_to_SZ(agent.x, agent.y,sz.x,sz.y)

                if d<min_distance:
                    min_rng = rng
                    min_dire = dire
                    sz_o = sz_occupancy(sz.capacity, sz.current_occupants)
                    sz_active = 'T' if sz.active else 'F'
                    min_distance = d
            else:
                # safe zone is inactive
                # agent is either in the safe zone or not in the safe zone. Responses should be the same for both
                
                d,_,_ = dnd_to_SZ(agent.x,agent.y,sz.x,sz.y)

                if d<min_inactive_distance:
                    min_inactive_distance = d
                    sz_inactive_o = sz_occupancy(sz.capacity, sz.current_occupants)

                
                
        else:
            
            if min_distance == float('inf'):
                # Case where no other active safe zone
                # this will only be the case if the safe zone minimum distance has never updated. It only updates for active safe zones.

                """ if no other safe zones are active:
                    direction should be: --
                    distance should be: --
                    occupancy should be that of the nearest safe zone even though inactive
                    safe zone active flag should also be that of the nearest safe zone.
                """

                state+='--'             # For distance
                state+='|'              # Next section
                state+='--'             # For direction
                state+='|'              # Next section
                state+=sz_inactive_o    # SZ occupancy measure
                state+='|'              # Next section
                state+='F'              # Safe zone active: 'T' for True otherwise 'F'

            else:
                # Executes only if agent was not in an active SZ - meaning distance and other measures have not been added to state, but an active safe zone exists.
                state+=min_rng  # distance
                state+="|"      # next section
                state+=min_dire # direction
                state+="|"      # next section
                state+=sz_o     # safe zone occupancy measure
                state+="|"      # next section
                state+=sz_active

        return state

    def get_last_action(self, agent):

        """ Function uses current agent position and previous agent position to determine last action.
            Function set up in such a way that it can be used for snakes, however, the current implementation
            would only return the enforced action and not the snake's proposed action, meanwhile the agent's last_act
            gives the proposed action whether or not it was actually implemented. It is this action that must be rewarded
            and not the enforced action.
            TODO: Stress test for what happens around captures and respawns
        """
        if agent.symbol == "P":
            return agent.last_act
        else:
            return (agent.x - agent.prev_x, agent.y - agent.prev_y)
        
            

