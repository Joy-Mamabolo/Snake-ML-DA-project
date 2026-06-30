from src.simulation.observations import Observation
from src.simulation.policy import QlearningPolicy
from src.simulation.agents import Prey
from src.simulation.environment import SafeZone

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
    pass




if __name__ == "__main__":

    test_build_state_produces_same_encoding_from_same_observation()
    test_build_state_updates_safe_zone_active_measure()
    test_build_state_updates_safe_zone_occupancy_correctly()
    test_build_state_updates_safe_zone_direction_correctly()
    test_build_state_updates_safe_zone_distance_correctly()
    test_build_state_handles_agent_in_safe_zone_as_expected()
    test_build_state_handles_3x3_encoding_as_expected()
    test_build_state_handles_multiple_safe_zones_as_expected()

    print("All tests passed!")
