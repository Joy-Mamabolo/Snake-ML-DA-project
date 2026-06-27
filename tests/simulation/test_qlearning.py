from src.simulation.observations import Observation
from src.simulation.policy import QlearningPolicy
from src.simulation.agents import Prey
from src.simulation.environment import SafeZone

def test_build_state_produces_same_encoding_from_same_observation():

    ### Arrange
    q_learner = QlearningPolicy()

    # Build SafeZone
    

    # Build observation
    snake_pos = (2,3)
    prey_list = [] # observation not used
    wall_position = set()
    grid_size = 20

    sz_list = [SafeZone(10,10,4,12)]
    sz_list[0].current_occupants = 6 # set an arbitrary number of occupants in the safezone
    
    valid_moves = [] # observation not used
    obs = Observation(snake_pos,prey_list,wall_position,grid_size,sz_list,valid_moves)

    # Get agent
    agent = Prey(1,3,QlearningPolicy())

    

    # Act
    state_1 = q_learner.build_state(agent, obs)
    state_2 = q_learner.build_state(agent,obs)

    # Assert
    assert state_1 == state_2, "for the same observation, build_state produces different state encoding string"

    print(state_1)


if __name__ == "__main__":

    test_build_state_produces_same_encoding_from_same_observation()

    print("All tests passed!")
