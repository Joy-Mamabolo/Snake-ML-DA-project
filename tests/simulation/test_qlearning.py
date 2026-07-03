from src.simulation.observations import Observation
from src.simulation.policy import QlearningPolicy
from src.simulation.agents import Prey
from src.simulation.environment import SafeZone

"______________________________test_build_state_functions___________________________________________________"

def test_build_state_produces_same_encoding_from_same_observation():

    ### Arrange
    q_learner = QlearningPolicy()

    # Build observation
    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    # Get agent
    agent = Prey(1,3,QlearningPolicy())

    

    # Act
    state_1 = q_learner.build_state(agent, obs)
    state_2 = q_learner.build_state(agent,obs)

    # Assert
    assert state_1 == state_2, "for the same observation, build_state produces different state encoding string"

    #print(state_1)

def test_build_state_updates_safe_zone_active_measure():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    # Get agent
    agent = Prey(1,3,QlearningPolicy())
    
    # Act
    s1 = q_learner.build_state(agent, obs) # default sz_active = True

    sz_list[0].active = False
    #obs = Observation(snake_pos, prey_list, wall_position,grid_size,sz_list,valid_moves)
    s2 = q_learner.build_state(agent,obs)
    

    # Assert
    assert s1[-1]=='T', f"{s1} does not indicate T by default. sz_active currently reads: {sz_list[0].active}"
    assert s2[-1]=='F', f"{s2} does not indicate F. sz_active currently reads: {sz_list[0].active}"

def test_build_state_updates_safe_zone_occupancy_correctly():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    # Get agent
    agent = Prey(1,3,QlearningPolicy())

    # Act
    # update occupants in sz
    s_default = q_learner.build_state(agent,obs)

    sz_list[0].current_occupants = 3
    s_LO = q_learner.build_state(agent, obs)

    sz_list[0].current_occupants = 7
    s_MO = q_learner.build_state(agent, obs)

    sz_list[0].current_occupants = 9
    s_HO = q_learner.build_state(agent, obs)

    sz_list[0].current_occupants = 11
    s_CO = q_learner.build_state(agent, obs)

    # Assert
    assert "LO" in s_default, f"{s_default} does not indicate Low occupancy by default."
    assert "LO" in s_LO, f"{s_LO} does not indicate Low occupancy."
    assert "MO" in s_MO, f"{s_MO} does not indicate Medium occupancy."
    assert "HO" in s_HO, f"{s_HO} does not indicate High occupancy."
    assert "CO" in s_CO, f"{s_CO} does not indicate Critical occupancy."

def test_build_state_updates_safe_zone_direction_correctly():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    # Get agent
    agent = Prey(1,10,QlearningPolicy())

    # Act
    s_dE = q_learner.build_state(agent,obs)

    agent.x,agent.y = (15,10) # move agent
    s_dW = q_learner.build_state(agent,obs)

    agent.x,agent.y = (10,0) # move agent
    s_dN = q_learner.build_state(agent,obs)

    agent.x,agent.y = (10,19) # move agent
    s_dS = q_learner.build_state(agent,obs)

    # Assert
    assert "dE" in s_dE, f"{s_dE} does not indicate due East"
    assert "dW" in s_dW, f"{s_dW} does not indicate due West"
    assert "dN" in s_dN, f"{s_dN} does not indicate due North "
    assert "dS" in s_dS, f"{s_dS} does not indicate due South"

def test_build_state_updates_safe_zone_distance_correctly():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    # Get agent
    agent = Prey(1,10,QlearningPolicy())

    # Act
    s_FDx = q_learner.build_state(agent,obs)

    agent.x,agent.y = (2,10)
    s_MDx = q_learner.build_state(agent,obs)

    agent.x,agent.y = (6,10)
    s_CDx = q_learner.build_state(agent,obs)

    agent.x,agent.y = (10,19)
    s_FDy = q_learner.build_state(agent,obs)

    agent.y = 18
    s_MDy = q_learner.build_state(agent,obs)

    agent.y = 16
    s_CDy = q_learner.build_state(agent,obs)

    # Assert
    assert "FD" in s_FDx, f"{s_FDx} does not indicate Far Distance"
    assert "FD" in s_FDy, f"{s_FDy} does not indicate Far Distance"

    assert "MD" in s_MDx, f"{s_MDx} does not indicate Mid Distance"
    assert "MD" in s_MDy, f"{s_MDy} does not indicate Mid Distance"

    assert "CD" in s_CDx, f"{s_CDx} does not indicate Close Distance"
    assert "CD" in s_CDy, f"{s_CDy} does not indicate Close Distance"

def test_build_state_handles_agent_in_safe_zone_as_expected():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy()) # Agent positioned in safe zone

    # Act
    s_in_SZ_active = q_learner.build_state(agent,obs)
    
    sz_list[0].active = False
    s_in_SZ_not_active = q_learner.build_state(agent, obs)

    # Assert
    assert s_in_SZ_active.count("-") == 4, f"{s_in_SZ_active} does not indicate -- for distance, direction or both while sz is active"
    assert s_in_SZ_not_active.count("-") == 4, f"{s_in_SZ_not_active} does not indicate -- for distance, direction or both while sz is inactive"

def test_build_state_handles_3x3_encoding_as_expected():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy()) # Agent positioned in safe zone

    # Act
    s_in_centre_sz = q_learner.build_state(agent, obs)

    agent.y = 13 # change agent position
    s_on_right_edge_sz = q_learner.build_state(agent,obs)

    agent.x = 12
    agent.y = 12
    snake_pos = (agent.x-1,agent.y) # change snake position - expected to fail
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)
    s_in_sz_with_snake_above = q_learner.build_state(agent,obs)

    agent.x,agent.y = 5,5   # change agent position
    s_in_empty_space = q_learner.build_state(agent,obs)


    agent.x,agent.y = 18,18
    # set up walls
    for i in range(grid_size):
        for j in range(grid_size):

            if i==0 or j ==0 or i ==grid_size-1 or j==grid_size-1:
                wall_position.add((i,j))
    s_in_map_corner = q_learner.build_state(agent,obs)

    snake_pos = (17,17)
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)
    s_in_map_corner_with_snake_on_top_left = q_learner.build_state(agent,obs)

    sz_list.append(SafeZone(1,1,2,2)) # add another safe zone
    agent.x,agent.y = 1,2
    snake_pos = (agent.x+1,agent.y+1)
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)
    s_sz_next_to_wall_with_snake_outside = q_learner.build_state(agent,obs)

    # Assert
    assert s_in_centre_sz[:9].count('O') == 9, f"{s_in_centre_sz[:9]} does not render in the centre of sz as expected"

    assert s_on_right_edge_sz[:9].count('O')==6 , f"{s_on_right_edge_sz[:9]} does not render at the right edge of safe zone as expected. safe zone cell count off"
    assert s_on_right_edge_sz[:9].count('.')==3, f"{s_on_right_edge_sz[:9]} does not render at the right edge of sz as expected. empty cell count off"
    assert s_on_right_edge_sz[8]=='.', f"{s_on_right_edge_sz[:9]} does not render at the right edge of sz as expected. empty cell placement off"

    assert s_in_sz_with_snake_above[:9].count("O")==8, f"{s_in_sz_with_snake_above[:9]} does not render snake in safe zone as expected. safe zone cell count off"
    assert s_in_sz_with_snake_above[1]=="S", f"{s_in_sz_with_snake_above[:9]} does not render snake in safe zone as expected. Snake position off"
    
    assert s_in_empty_space[:9].count(".") == 9, f"{s_in_empty_space[:9]} does not render in empty space correctly. empty cell count off"

    assert s_in_map_corner[:9].count("X") ==5, f"{s_in_map_corner[:9]} does not render in map corner as expected. wall count off"

    assert s_in_map_corner_with_snake_on_top_left[0]=="S", f"{s_in_map_corner_with_snake_on_top_left[:9]} does not render snake near map corner as expected. Snake position off"
    assert s_in_map_corner_with_snake_on_top_left[:9].count('.')==3, f"{s_in_map_corner_with_snake_on_top_left[:9]} does not render snake near map corner as expected. empty cell count off"
    assert s_in_map_corner_with_snake_on_top_left[:9].count("X") ==5, f"{s_in_map_corner_with_snake_on_top_left[:9]} does not render snake near map corner as expected. wall count off"

    assert s_sz_next_to_wall_with_snake_outside[:9].count("X")==3, f"{s_sz_next_to_wall_with_snake_outside[:9]} does not render sz next to wall with snake out side as expected. wall count off"
    assert s_sz_next_to_wall_with_snake_outside[:9].count('S')==1, f"{s_sz_next_to_wall_with_snake_outside[:9]} does not render sz next to wall with snake outside as expected. snake count off"
    assert s_sz_next_to_wall_with_snake_outside[:9].count('O')==4, f"{s_sz_next_to_wall_with_snake_outside[:9]} does not render sz next to wall with snake outside as expected. sz cell count off"
    assert s_sz_next_to_wall_with_snake_outside[:9].count('.')==1, f"{s_sz_next_to_wall_with_snake_outside[:9]} does not render sz next to wall with snake outside as expected. empty cell count off"
    assert s_sz_next_to_wall_with_snake_outside[8]=="S", f"{s_sz_next_to_wall_with_snake_outside[:9]} does not render sz next to wall with snake outside as expected. snake position off"
    assert ".OOS" in s_sz_next_to_wall_with_snake_outside[:9], f"{s_sz_next_to_wall_with_snake_outside[:9]} does not render sz next to wall with snake outside as expected. character sequence off "

def test_build_state_handles_multiple_safe_zones_as_expected():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(2,2,4,12), SafeZone(2,10,4,12),SafeZone(15,7,4,12)]

    sz_list[0].current_occupants = 1 # Expected low occupancy
    sz_list[1].current_occupants = 6 # Expected medium occupancy
    sz_list[2].current_occupants = 11 # Expected critical occupancy
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy()) # Agent positioned in safe zone

    # Act
    
    #Scenario 1: All safe zones active - near low-occupancy sz
    agent.x = 9
    agent.y = 2
    s_near_LO_sz = q_learner.build_state(agent,obs)

    # Scenario 2: All safe zones active - near medium occupancy sz
    agent.y = 10
    s_near_MO_sz = q_learner.build_state(agent,obs)

    # Scenario 3: All safe zones active - near critical occupancy sz
    agent.y = 7
    s_near_CO_sz = q_learner.build_state(agent,obs)

    # Scenario 4: Near LO sz but LO sz inactive
    agent.y = 2
    sz_list[0].active = False
    s_near_LO_inactive = q_learner.build_state(agent,obs)

    # Scenario 5: Near CO sz but CO and LO sz inactive
    agent.y = 7
    sz_list[2].active = False
    s_near_CO_inactive = q_learner.build_state(agent,obs)

    # Scenario 6: All SZ inactive but near LO sz
    sz_list[1].active = False
    agent.y = 2
    s_near_LO_all_inactive = q_learner.build_state(agent,obs)

    # Scenario 7: All SZ inactive but near MO sz
    agent.y = 10
    s_near_MO_all_inactive = q_learner.build_state(agent,obs)

    # Scenario 8: All SZ inactive but near CO sz
    agent.y = 7
    s_near_CO_all_inactive = q_learner.build_state(agent,obs)

    # Assert
    assert "LO" in s_near_LO_sz, f"{s_near_LO_sz} does not correctly capture nearest active sz details. expected LO"
    assert "MO" in s_near_MO_sz, f"{s_near_MO_sz} does not correctly capture nearest active sz details. expected MO"
    assert "CO" in s_near_CO_sz, f"{s_near_CO_sz} does not correctly capture nearest active sz details. expected CO"

    assert "CO" in s_near_LO_inactive, f"{s_near_LO_inactive} does not correctly capture nearest active sz details. expected CO"
    assert "MO" in s_near_CO_inactive, f"{s_near_CO_inactive} does not correctly capture nearest active sz details. expected MO"

    assert "LO" in s_near_LO_all_inactive, f"{s_near_LO_all_inactive} does not correctly capture nearest sz in all sz inactive scenario. expected LO"
    assert s_near_LO_all_inactive.count("-") == 4, f"{s_near_LO_all_inactive} does not correctly capture sz details correctly in all sz inactive case. expected distance and direction metrics to be unavailbale"
    assert s_near_LO_all_inactive[-1] == 'F', f"{s_near_LO_all_inactive} does not correctly capture sz details correctly in all sz inactive case. sz active flag as expected F"

    assert "MO" in s_near_MO_all_inactive, f"{s_near_MO_all_inactive} does not correctly capture nearest sz in all sz inactive scenario. expected MO"
    assert s_near_MO_all_inactive.count("-") == 4, f"{s_near_MO_all_inactive} does not correctly capture sz details correctly in all sz inactive case. expected distance and direction metrics to be unavailbale"
    assert s_near_MO_all_inactive[-1] == 'F', f"{s_near_MO_all_inactive} does not correctly capture sz details correctly in all sz inactive case. sz active flag as expected F"

    assert "CO" in s_near_CO_all_inactive, f"{s_near_CO_all_inactive} does not correctly capture nearest sz in all sz inactive scenario. expected CO"
    assert s_near_CO_all_inactive.count("-") == 4, f"{s_near_CO_all_inactive} does not correctly capture sz details correctly in all sz inactive case. expected distance and direction metrics to be unavailbale"
    assert s_near_CO_all_inactive[-1] == 'F', f"{s_near_CO_all_inactive} does not correctly capture sz details correctly in all sz inactive case. sz active flag as expected F"

"____________________________________________________________________________________________________________________"

"_______________________________________test_get_q_function__________________________________________________________"

def test_get_q_adds_a_new_state_when_queried_state_and_action_does_not_exist_in_q_table_and_returns_correct_default_value():
    
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy())

    # Act
    s = q_learner.build_state(agent, obs)
    agent.policy.q_table = {(s, (0,1)): 1.2} # add a singe state-action pair to q_table

    s_out = agent.policy.get_q(s, (1,0)) # query a state-action pair that does not exist in q_table
    
    # Assert
    assert (s, (1,0)) in agent.policy.q_table, f"state-action pair {(s, (1,0))} was not added to q_table when queried but did not exist"
    assert s_out == 0.0, f"get_q did not return the default value of 0.0 for a recently added state-action pair. Instead, {s_out} was returned"

def test_get_q_retrieves_the_correct_q_value_for_state_action_pair():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy())

    # Act
    s = q_learner.build_state(agent, obs)
    # add state-action pairs to q_table
    agent.policy.q_table = {(s, (0,1)): 1.2}
    agent.policy.q_table[(s,(1,0))] = 2.5
    agent.policy.q_table[(s,(-1,0))] = -0.5
    agent.policy.q_table[(s,(0,-1))] = 0.0 

    s1 = agent.policy.get_q(s, (1,0))
    s2 = agent.policy.get_q(s, (0,1))
    s3 = agent.policy.get_q(s, (-1,0))
    s4 = agent.policy.get_q(s, (0,-1))

    # Assert
    assert s1 == 2.5, f"get_q did not return the correct q-value for state-action pair {(s,(1,0))}. Instead, {s1} was returned"
    assert s2 == 1.2, f"get_q did not return the correct q-value for state-action pair {(s,(0,1))}. Instead, {s2} was returned"
    assert s3 == -0.5, f"get_q did not return the correct q-value for state-action pair {(s,(-1,0))}. Instead, {s3} was returned"
    assert s4 == 0.0, f"get_q did not return the correct q-value for state-action pair {(s,(0,-1))}. Instead, {s4} was returned"

"____________________________________________________________________________________________________________________"

"_______________________________________test_choose_action_function__________________________________________________________"
def test_choose_action_returns_best_action_from_q_table_when_epsilon_is_zero():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy(epsilon=0.0)) # set epsilon to 0 to force exploitation of q_table

    # Act
    s = q_learner.build_state(agent, obs)
    # add state-action pairs to q_table
    agent.policy.q_table = {(s, (0,1)): 1.2}
    agent.policy.q_table[(s,(1,0))] = 2.5
    agent.policy.q_table[(s,(-1,0))] = -0.5
    agent.policy.q_table[(s,(0,-1))] = 0.0

    action1 = agent.policy.choose_action(agent, obs)

    agent.policy.q_table[(s,(0,-1))] = 3.0 # update q-value for (0,-1) to be the highest
    action2 = agent.policy.choose_action(agent, obs)

    # Assert
    assert action1 == (1,0), f"choose_action did not return the best action from q_table when epsilon was 0. Instead, {action1} was returned"
    assert action2 == (0,-1), f"choose_action did not return the best action from q_table when epsilon was 0. Instead, {action2} was returned"

def test_choose_action_returns_an_action_when_epsilon_is_zero_and_q_values_are_negative():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy(epsilon=0.0)) # set epsilon to 0 to force exploitation of q_table

    # Act
    s = q_learner.build_state(agent, obs)
    # add state-action pairs to q_table
    agent.policy.q_table = {(s, (0,1)): -1.2}
    agent.policy.q_table[(s,(1,0))] = -2.5
    agent.policy.q_table[(s,(-1,0))] = -0.5
    agent.policy.q_table[(s,(0,-1))] = -0.9

    action = agent.policy.choose_action(agent, obs)

    # Assert
    assert  action == (-1,0), f"choose_action did not return the right action when epsilon was 0 and q-values were negative. Actions returned: {action}"

def test_choose_action_returns_random_action_from_q_table_when_epsilon_is_one():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy(epsilon=1.0)) # set epsilon to 1 to force exploration of q_table

    # Act
    s = q_learner.build_state(agent, obs)
    # add state-action pairs to q_table
    agent.policy.q_table = {(s, (0,1)): 1.2}
    agent.policy.q_table[(s,(1,0))] = 2.5
    agent.policy.q_table[(s,(-1,0))] = -0.5
    agent.policy.q_table[(s,(0,-1))] = 0.0

    actions_taken = set()
    
    for _ in range(100): # run multiple times to ensure randomness is captured
        action = agent.policy.choose_action(agent, obs)
        actions_taken.add(action)

    # Assert
    assert len(actions_taken) > 1, f"choose_action did not return random actions from q_table when epsilon was 1. Only one action was returned: {actions_taken}"
"_____________________________________________________________________________________________________________________________"
"_______________________________________test_update_q_table_function__________________________________________________________"

def test_update_q_table_updates_q_value_correctly():
    # Arrange
    q_learner = QlearningPolicy(alpha=0.5, gamma=0.9)

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy(alpha=0.5, gamma=0.9))

    # Act
    s = q_learner.build_state(agent, obs)
    # add state-action pairs to q_table
    agent.policy.q_table = {(s, (0,1)): 1.0}

    # next state 
    agent.x, agent.y = 11, 12 # move agent to a new position
    next_s = q_learner.build_state(agent, obs)
    agent.policy.q_table[(next_s,(0,1))] = -3.0
    agent.policy.q_table[(next_s,(0,-1))] = 0.0
    agent.policy.q_table[(next_s,(1,0))] = 1.0
    agent.policy.q_table[(next_s,(-1,0))] = 3.0
    
    
    # Update q-value for (0,1) with a reward of 2.0 and next state with max q-value of 3.0
    reward = 2.0
    agent.policy.update_q_table(s, (0,1), agent.actions, reward, next_s)

    updated_q_value = agent.policy.get_q(s, (0,1))

    # Assert
    expected_q_value = 1.0 + 0.5 * (reward + 0.9 * 3.0 - 1.0) # Q-learning update formula
    assert updated_q_value == expected_q_value, f"update_q_table did not update the q-value correctly. Expected {expected_q_value}, but got {updated_q_value}"

def test_update_q_table_handles_capture_reward_where_next_state_is_unknown():
    # Arrange
    q_learner = QlearningPolicy(alpha=0.5, gamma=0.9)

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]
    
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    
    # Get agent
    agent = Prey(11,11,QlearningPolicy(alpha=0.5, gamma=0.9))

    # Act
    s = q_learner.build_state(agent, obs)
    # add state-action pairs to q_table
    agent.policy.q_table = {(s, (0,1)): 1.0}

    
    # Update q-value for (0,1) with a reward of -10 and next state with max q-value of 0.0 (since it's unknown)
    reward = -10
    agent.policy.update_q_table(s, (0,1), agent.actions, reward)

    updated_q_value = agent.policy.get_q(s, (0,1))

    # Assert
    expected_q_value = 1.0 + 0.5 * (reward + 0.9 * 0.0 - 1.0) # Q-learning update formula with max Q(next_s) as 0.0
    assert updated_q_value == expected_q_value, f"update_q_table did not handle unknown next state correctly. Expected {expected_q_value}, but got {updated_q_value}"

"_____________________________________________________________________________________________________________________________"
"__________________________________________test_get_last_action_function______________________________________________________"
def test_get_last_action_returns_last_agent_proposed_action_and_not_game_enforced_action():
    # Arrange
    q_learner = QlearningPolicy()

    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]

    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    agent = Prey(11,11,q_learner)

    # Act
    # simulate the agent proposing an action
    agent.last_act = (0,1) # agent proposed to move right
    # simulate the game enforcing a different action due to collision or other rules
    agent.prev_x, agent.prev_y = agent.x, agent.y

    # assume agent got a no movement penalty enforced by the game, so the agent's position remains the same

    last_action_P = agent.policy.get_last_action(agent) # retrieve the last action proposed by the agent

    agent.symbol = 'S'
    last_action_S = agent.policy.get_last_action(agent) # retrieve the last action enforced by the game (which is not stored in this implementation)

    # Assert
    assert last_action_P == (0,1), f"get_last_action did not return the last action proposed by the agent. Expected (0,1), but got {last_action_P}"
    assert last_action_S == (0,0), f"get_last_action did not return the last action enforced by the game. Expected (0,0), but got {last_action_S}"

"_____________________________________________________________________________________________________________________________"
"__________________________________________test_learn_function____________________________________________________________"

def test_learn_function_updates_q_table_correctly_given_observations_and_reward():
    # Arrange

    q_learner = QlearningPolicy(alpha=0.5, gamma=0.9)
    
    snake_pos = (2,3) # Not used
    prey_list = [] # observation not used
    wall_position = set() # Not used
    grid_size = 20

    sz_list = [SafeZone(10, 10, 2)]

    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)
    
    agent = Prey(11,11,q_learner)
    agent.last_act = (0,1) # agent proposed to move right
    snake_pos = (12,12)

    obs_next = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    reward = 5.0

    # Act
    q_learner.learn(agent, reward, obs, obs_next)

    q_val = 0.0 + 0.5 * (reward + 0.9 * 0.0 - 0.0) # Q-learning update formula with max Q(next_s) as 0.0
    s = q_learner.build_state(agent, obs)
    updated_q_value = q_learner.get_q(s, agent.last_act)

    # Assert
    assert len(q_learner.q_table) == 5, f"learn did not update the q_table correctly. Expected 5 entries, but got {len(q_learner.q_table)} - see{q_learner.q_table}"
    assert q_val == updated_q_value, f"learn did not update the q-value correctly. Expected {q_val}, but got {updated_q_value}"
"_____________________________________________________________________________________________________________________________"
if __name__ == "__main__":

    # build_state function tests
    test_build_state_produces_same_encoding_from_same_observation()
    test_build_state_updates_safe_zone_active_measure()
    test_build_state_updates_safe_zone_occupancy_correctly()
    test_build_state_updates_safe_zone_direction_correctly()
    test_build_state_updates_safe_zone_distance_correctly()
    test_build_state_handles_agent_in_safe_zone_as_expected()
    test_build_state_handles_3x3_encoding_as_expected()
    test_build_state_handles_multiple_safe_zones_as_expected()

    # get_q function tests
    test_get_q_adds_a_new_state_when_queried_state_and_action_does_not_exist_in_q_table_and_returns_correct_default_value()
    test_get_q_retrieves_the_correct_q_value_for_state_action_pair()

    # choose_action function tests
    test_choose_action_returns_best_action_from_q_table_when_epsilon_is_zero()
    test_choose_action_returns_an_action_when_epsilon_is_zero_and_q_values_are_negative()
    test_choose_action_returns_random_action_from_q_table_when_epsilon_is_one()
    
    # update_q_table function tests
    test_update_q_table_updates_q_value_correctly()
    test_update_q_table_handles_capture_reward_where_next_state_is_unknown()

    # get_last_action function tests
    test_get_last_action_returns_last_agent_proposed_action_and_not_game_enforced_action()

    # learn function tests
    test_learn_function_updates_q_table_correctly_given_observations_and_reward()

    print("All tests passed!")
