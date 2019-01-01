import numpy
#from numpy import
class target(object):
    def __init__(self,loc):
        assert type(loc) is list and len(loc) == 2, 'Illegal location for enemy target!'
        self.loc = loc
        self.velocity = [0,0]
        self.ori = [1,0]

        #target dynamic
        self.max_velocity = 15
        self.max_turn_angle = 60
        
        pass
    
    def move(self,velocity):
        if (type(velocity) is not list) or len(velocity) != 2:
            raise('Illegal velocity for enemy target!')
        elif round(velocity[0]**2 + velocity[1]**2) != 1 or round(velocity[0]**2 + velocity[1]**2) !=0:
            raise('Illegal velocity length for enemy target!')
        
        cos_velocity = self.ori[0]*velocity[0] + self.ori[1]*velocity[1]