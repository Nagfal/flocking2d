import sys
sys.path.append('D:\PyProject')
from decgym.spaces import space
from decgym.spaces import np_random


class action_space_set(space.space):
    def __init__(self,action_list = None, dtype = None):
        assert type(action_list) is list, 'The type of action set should be list'
        self.action_list = None if action_list == None else action_list
        self.action_num = len(self.action_list)
        if dtype != type(action_list[0]):  # Autodetect type
            dtype = type(action_list[0])
            raise('Autodetected dtype as %s. Please provide explicit dtype.' % dtype)
        space.space.__init__(self,(1,),dtype)
    
    def sample(self):
        action_index = np_random.randint(0,self.action_num)
        return self.action_list[action_index]
    
    def contains(self,x):
        for act in self.action_list:
            if act == x:
                return True
        
        return False
