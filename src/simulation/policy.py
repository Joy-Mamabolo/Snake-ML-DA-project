###################################################################################################################
# File will contain all decision making policies for all agents.
# These currently include greedy policy for snake based; random policy for some prey and q-learning for the rest.
###################################################################################################################

# Imports
import random # will later import from an rng.py file that will handle seeding


class GreedyPolicy:

    def choose_action(self, observation, agent):
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
    
    def choose_action(self, state, agent):

        # Observe the world and update the Q-table based on the reward received from the previous action. Then select an action based on the Q-table. Not implemented yet.

        # Determine if we consult q-table or explore using epsilon
        if random.random()<self.epsilon:
            # Be adventurous, explore - ignore q-table and make a random move
            candidate = [random.choice(agent.actions)] # made it a list for consistency
        else:
            # Be principled - consult your q-table
            candidate = [(0,0)] # default value although it should not be necessary  TODO: Remove default candidate value. It is guaranteed that there will be at least one action with a q-value of at least 0.0
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
            last_act= random.choice(candidate)
        else:
            # Only one answer
            last_act= candidate[0] # tuple not list
            
            
        return last_act, state
            

