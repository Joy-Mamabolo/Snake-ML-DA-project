from src.simulation.rules import is_in_safe_zone

def test_is_in_safe_zone_excludes_cell_beyond_boundary():

    # Arrange

    sz_x = 5
    sz_y = 5
    sz_size = 2
    

    # Act
    pos = (5,5)
    is_in = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (5,6)
    is_in2 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (6,5)
    is_in3 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (6,6)
    is_in4 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (6,7)
    is_out = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (7,6)
    is_out2 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (7,7)
    is_out3 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (4,5)
    is_out4 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (5,4)
    is_out5 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    pos = (4,4)
    is_out6 = is_in_safe_zone(sz_x, sz_y,sz_size,pos[0],pos[1])

    # Assert
    assert is_in == True
    assert is_in2 == True
    assert is_in3==True
    assert is_in4 == True
    assert is_out == False
    assert is_out2==False
    assert is_out3==False
    assert is_out4==False
    assert is_out5==False
    assert is_out6==False


if __name__ == "__main__":

    test_is_in_safe_zone_excludes_cell_beyond_boundary()
    print("All tests pass!")