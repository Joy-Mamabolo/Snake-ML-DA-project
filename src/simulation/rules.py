################################################################################################################
# File holds pure logic only. It is not meant to receive or return any objects, only the rules that govern the
# simulation. It only receives required data, and not complete objects that hold that data. e.g. instead of getting
# prey object which contains multiple things, it will get only prey_position which it may use to define one rule or
# another. This also means that it cannot have object lists passed to it, only the minimum information needed for it
# to define a rule completely.
###############################################################################################################