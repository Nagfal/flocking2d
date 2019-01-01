import sys
sys.path.append('D:\PyProject')
import decgym
from decgym import DecEnv
from numpy import random as np_random
class terrohunting(DecEnv):
    
    def __init__(self):
        #env basic configrition
        self.x_range = 3000
        self.y_range = 5000
        self.stronghold_alpha = [1000,1000]
        self.stronghold_beta = [2000,4000]
        self.aa_alpha = [1000,4000]
        self.aa_beta = [2000,1000]
        self.patrol_vehicle_alphe = [1000,1000]
        self.patrol_vehicle_beta = [2000,4000]
        self.target_refreash_range = (300,500)
        self.target_num = 5
        self.targets = []

        self.chaser_num_UAV = 6
        self.chaser_num_UGV = 10
        #team red init loc

        #time step counter
        self.time_counter = 0

        #total reward for team red and blue
        self.reward_red = 0
        self.reward_blue = 0
        #total for each individual in both team
        self.reward_red_indi = [0]*6
        self.reward_blue_indi = [0]*10
        pass
    
    def step(self,actions_red, actions_blue):
        
        pass

    def reset(self):
        #total reward for team red and blue
        self.reward_red = 0
        self.reward_blue = 0
        #total for each individual in both team
        self.reward_red_indi = [0]*6
        self.reward_blue_indi = [0]*10
        #time step counter
        
        self.time_counter = 0

        #team red back to init loc

        #refresh all enemy state (including target and patrol vehicle)
        pass


    def render(self,mode):
        pass
    
    def target_refresh(self):
        target_refresh_dict = np_random.uniform(self.target_refreash_range[0],self.target_refreash_range[1],[6,])
        #
        # for i in range 
        pass
        

    