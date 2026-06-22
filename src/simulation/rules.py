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