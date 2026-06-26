################################################################################################################
# File holds pure logic only. It is not meant to receive or return any objects, only the rules that govern the
# simulation. It only receives required data, and not complete objects that hold that data. e.g. instead of getting
# prey object which contains multiple things, it will get only prey_position which it may use to define one rule or
# another. This also means that it cannot have object lists passed to it, only the minimum information needed for it
# to define a rule completely.
###############################################################################################################
     
def is_in_safe_zone(sz_x, sz_y, sz_size, x, y):
        
    if (sz_x<=x<=sz_x+sz_size) and (sz_y<=y<=sz_y+sz_size):
        return True
        
    return False

def is_safe_zone_active(sz_capacity, sz_occupancy, sz_x, sz_y, sz_size, snake_x, snake_y):
    if is_in_safe_zone(sz_x, sz_y, sz_size, snake_x, snake_y):
        return False
    
    elif sz_occupancy>=sz_capacity:
        return False
    else:
        return True
    
def is_in_bounds(x, y, grid_size):
    return False if x < 0 or x >= grid_size or y < 0 or y >= grid_size else True

def boundary_collision(walls: set, agent_x:int, agent_y:int):

    """This function will eventually be used to determine if there is a collision (attempted or actual) with walls by
       agents. It will also be adapted to include the is_in_bounds functionality as this function is more general and
       scales better """

    # collision between moving and stationary entities (walls)
    return True if (agent_x,agent_y) in walls else False

def agent_collision(agent_1, agent_2):
    """Function will be primarily used to detect if a capture happened, although it is built in such a way that
       it will detect all collisions should that be desired."""
    
    if (agent_1.x==agent_2.x and agent_1.y == agent_2.y) or (agent_1.x == agent_2.prev_x and agent_1.y==agent_2.prev_y 
                                                             and
                                                             agent_1.prev_x == agent_2.x and agent_1.prev_y == agent_2.y):
        
        # First logical check happens when two agents are occupying the same square
        # Second logical check happens when two agents swap positions in a manner differentiated from following - ie.
        # it is only possible for this to happen by colliding in infinitesimal time (step)

        return True
    else:
        return False
        