#example of ob
[
    {
        'loc':[50.0,60.1],
        'velocity':[10,5],
        'nearby_velocity':[[1.5,2.1],[3.0,3.2]],
        'nearby_loc':[[55.1,59.2],[48.5,61.5]],
        'obs_wall':[[50,50],[51,51],[52,52]]
    }
]

#example of reward
{
    'team':10,
    'indi':[10,10,10,-1,-3]
}

#example of info 
{
    'collision':2,
    'target_loc':[500,521]
}

import sys
sys.path.append('D:\PyProject')
import decgym
import math
from decgym import DecEnv
from numpy import random as np_random

import flocking_math as fm

import time
#from numpy import linalg

config ={
    'UAV_num':20,
    'UAV_locs':[],
    'end_time': 400,
    'comm_dist': 40,
    'map_size':[300,300],
    'collisionless_reward':0,
    'reach_reward':10,
    'collision_reward_factor':-10,
    'start_loc':[200,200],
    'target_dist':30
}

class flocking2d_env(DecEnv):
    def __init__(self):
        self.UAV_num = config['UAV_num']
        self.UAV_locs =config['UAV_locs'].copy()
        self.timestep = 0 
        self.end_time = config['end_time']
        self.total_reward = 0
        self.comm_dist = config['comm_dist']
        
        self.map_size = config['map_size']
        self.reach_num = 0
        self.collision_num = 0
        self.collisionless_reward = config['collisionless_reward']
        self.reach_reward = config['reach_reward']
        self.collision_reward_factor = config['collision_reward_factor']
        self.target_loc = config['start_loc']
        self.target_dist = config['target_dist']
        

        self.loc_history = []

        self.episode = 0
        self.path = ''
        self.uav_change_time = []
        for i in range(0,10):
            self.uav_change_time.append(np_random.randint(0,200))

        self.wall_step = 50
        wall_a = []
        for i in range(0,self.map_size[1],50):
            wall_a.append([0,i])
        wall_b = []
        for i in range(0,self.map_size[0],50):
            wall_b.append([i,0])
        wall_c = []
        for i in range(0,self.map_size[1],50):
            wall_c.append([self.map_size[0],i])
        wall_d = []
        for i in range(0,self.map_size[0],50):
            wall_d.append([i,self.map_size[1]])
        self.action =[]
        self.wall = wall_a + wall_b + wall_c + wall_d
        pass

    def norm(self,pointA):
        return (pointA[0]**2 + pointA[1]**2)**0.5

    def step(self,action_red,action_blue=None):
        """ within this env, we got only one team, team red, which need to be implemented as a flock.

        Accepts a list of velocities of omnidirectional UAVs in team red and returns a truple(observation, reward, done, info).

        Args:
        action_red: a list of velocities of omnidirectional UAVs in team red. The length  of each vector in action_red should be the magnitude of its velocity.
        action_blue: Should be none in this env

        returns:+
        observation(list): list of observations should be obtained by UAVs in team red respectivly.
                     With in this env, the observation includes the locations of itself, the locations & velocities of nearby UAVs.
        reward(dict): amount of reward returned after previous action. With in this env, only reward[0][] is meaningful.
                if this timestep is collisionless then the reward is 0, else if there are collisions then the reward is -1 times the number of collisions, else 10 for reaching
                target location (centroid get in the a circle with target location as its center and r=5 as its radiu)
        done(boolean): whether the episode has ended, in which case further step() calls will return undefined results.
              with in this env, the episode is ended if it reaches a predefined timestep.
        info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning) """
        """ init_start = time.clock()
        elapsed = (time.clock() - init_start)
        print("Init Time used:",elapsed) """
        self.action = action_red.copy()
        if len(action_red) < len(self.UAV_locs):
            raise('there are UAVs still not been specified velocity')
        elif len(action_red) > len(self.UAV_locs):
            raise('commanding more UAVs then u got')
        #self.collision_num = 0
        # move, collisions detect and collisions adapt
        for id in range(0,len(action_red)):
            self.UAV_locs[id][0]=self.UAV_locs[id][0] + action_red[id][0]
            self.UAV_locs[id][1]=self.UAV_locs[id][1] + action_red[id][1]
        

        #coll_dect_start = time.clock()
        collisions = self.collisions_detect() 
        #elapsed = (time.clock() - coll_dect_start)
        #print("coll_dect Time used:",elapsed)

        
        self.collisions_adapt(collisions,action_red)
        

        #add uavs with a random number
        if self.timestep in self.uav_change_time:
            var = np_random.randint(-2,3)
            #update self.uav_num
            #self.UAV_num += var
            #update self.uav_loc
            if var >= 0:
                for i in range(0,var):
                    uav_x = np_random.uniform(0,self.map_size[0]-15)
                    uav_y = np_random.uniform(0,self.map_size[1]-15)
                    self.UAV_num+=1
                    self.UAV_locs.append([uav_x,uav_y])
                    self.loc_history.append([(uav_x,uav_y)])
                    action_red.append([0,0])
                    self.action.append([0,0])
                pass
            else:
                for i in range(0,-1*var):
                    remove_uav_index = np_random.randint(0,len(self.UAV_locs))
                    self.UAV_num-=1
                    self.UAV_locs.pop(remove_uav_index)
                    self.loc_history.pop(remove_uav_index)
                    action_red.pop(remove_uav_index)
                    self.action.pop(remove_uav_index)
                pass

        #store trajectory 
        for id in range(0,len(self.loc_history)):
            self.loc_history[id].append((self.UAV_locs[id][0],self.UAV_locs[id][1]))
            if len(self.loc_history[id])>60:
                self.loc_history[id].pop(0)

        

        #package the observations
        observations = []
        for uav in range(0,len(self.UAV_locs)):
            loc = self.UAV_locs[uav]
            nearby_velocity,nearby_loc = self.find_nearby(uav,action_red)
            #selfvelocity =[0.0,0.0]
            #if uav < len(self.action):
            selfvelocity = self.action[uav]
            indi_obv = {
                'loc':loc,
                'velocity':selfvelocity,
                'nearby_velocity' : nearby_velocity,
                'nearby_loc' : nearby_loc,
                'obs_wall':self.wall
            }
            observations.append(indi_obv.copy())
            pass
        self.timestep += 1

        #package the reward
        reward={
            'team':0.0,
            'indi':[self.collisionless_reward] * len(self.UAV_locs)
        }

        if len(collisions) == 0:
            reward['team'] = self.collisionless_reward           
        else:
            reward['team'] = self.collision_reward_factor * len(collisions)
            for coll in collisions:
                if coll[0] < len(reward['indi']):
                    reward['indi'][coll[0]] -= -1 * self.collision_reward_factor
                if coll[1] < len(reward['indi']):
                    reward['indi'][coll[1]] -= -1 * self.collision_reward_factor
            for r in reward['indi']:
                if r < self.collisionless_reward:
                    r -= self.collisionless_reward 
        
        centorid = self.centroid_loc()
        cen_tar = [ centorid[0]-self.target_loc[0] , centorid[1] - self.target_loc[1] ]
        cen_tar_dist = cen_tar[0]**2 + cen_tar[1]**2
        if cen_tar_dist <= (self.target_dist**2):
            # get 10 points of reward
            reward['team'] += self.reach_reward
            self.reach_num += 1
            for r in reward['indi']:
                r += self.reach_reward
            # renew target_loc
            self.target_loc = self.renew_target_loc()
        else:
            #get 0 point of reward
            pass
        self.total_reward += reward['team']
        self.collision_num += len(collisions)
        info ={
            'collision':len(collisions),
            'target_loc':self.target_loc,
            'reach_num':self.reach_num
        }
             
        return observations , reward , (False if self.timestep<self.end_time else True) , info   

    def reset(self):
        #renew config
        #if self.timestep == 200:
            #self.episode = 0
        #else:
            #self.episode += 1
        self.UAV_num = config['UAV_num']
        self.UAV_locs =config['UAV_locs'].copy()
        self.timestep = 0 
        self.end_time = config['end_time']
        self.total_reward = 0
        self.comm_dist = config['comm_dist']
        
        self.map_size = config['map_size']
        self.action =[]
        self.collision_num = 0
        self.collisionless_reward = config['collisionless_reward']
        self.reach_reward = config['reach_reward']
        self.collision_reward_factor = config['collision_reward_factor']
        self.target_loc = config['start_loc']
        self.target_dist = config['target_dist']
        self.loc_history = []
        
        
        self.reach_num = 0
        self.uav_change_time = []
        for i in range(0,10):
            self.uav_change_time.append(np_random.randint(0,200))
        #init uav locations
        for i in range(0,self.UAV_num):
            uav_x = np_random.uniform(50,self.map_size[0]-50)
            uav_y = np_random.uniform(50,self.map_size[1]-50)
            self.UAV_locs.append([uav_x,uav_y])
            self.loc_history.append([(uav_x,uav_y)])


        #build a new test folder location for render
        path = 'flocking_2d_resaults/episode_'+ str(self.episode)
        
        #package return values
        #ob
        observations = []
        for uav in self.UAV_locs:
            loc = uav
            nearby_velocity,nearby_loc = self.find_nearby(self.UAV_locs.index(uav),[[0,0]]*len(self.UAV_locs))
            indi_obv = {
                'loc':loc,
                'velocity':[0.0,0.0],
                'nearby_velocity' : nearby_velocity,
                'nearby_loc' : nearby_loc,
                'obs_wall':self.wall
            }
            observations.append(indi_obv.copy())
        #reward
        reward={
            'team':0.0,
            'indi':[0] * len(self.UAV_locs)
        }
        #done
        done = False
        #info
        info ={
            'collision':0,
            'target_loc':self.target_loc,
            'reach_num':self.reach_num
        }
        return observations, reward, done, info


    def render(self, mode = 'image', timestep=(0,0),filepath=''):
        """ Render the environment.

        If mode is:
        -- image : render the current environment to a iamge and return nothing
        -- vedio : render a vedio start at timestep[0] end at timestep[1]

        Args:
            mode (str): the mode to render with
            timestep(tuple): the start timestep and end timestep of vedio """
        if mode == 'image':
            import image_render
            image_render.render(self.episode, self.timestep, self.collision_num,self.target_loc,self.target_dist,self.total_reward,True,self.loc_history,self.path,self.map_size,filepath)
        else:
            import vedio_render
            vedio_render.render()    
        pass
    def centroid_loc(self):
        centroid = [0,0]
        for warm in self.UAV_locs:
            centroid[0] += warm[0]
            centroid[1] += warm[1]

        centroid[0] = centroid[0] / len(self.UAV_locs)
        centroid[1] = centroid[1] / len(self.UAV_locs)
        return centroid             

    def renew_target_loc(self, parameter_list = None):
        for i in range(0,100):
            new_target_x = np_random.uniform(50, self.map_size[0] - 50)
            new_target_y = np_random.uniform(50, self.map_size[1] - 50)
            dist = (new_target_x - self.target_loc[0])**2 + (new_target_y - self.target_loc[1])**2
            if dist >= 100:
                return [new_target_x,new_target_y]
        raise ('Cannot renew target_loc')

    def collisions_detect(self):
        """ detect UAV who involves into a collision
        accepts nothing and returns collision UAV id truples in a list

        accept:
        self

        return: 
        collisions(list): collision UAV id truples """
        collisions = []
        uav_num = len(self.UAV_locs)
        for uav_a in range(0,uav_num):
            for uav_b in range(uav_a,uav_num):
                if uav_a != uav_b:
                    dist = (self.UAV_locs[uav_a][0]-self.UAV_locs[uav_b][0])**2 + (self.UAV_locs[uav_a][1]-self.UAV_locs[uav_b][1])**2
                    if dist < 1**2:
                        collisions.append((uav_a,uav_b))

        return collisions
        
    def collisions_adapt(self,collisions,action):
        """ adapt locations of UAVs who involves into a collision, by relocate them with a random distance.
        accpets nothing and retruns nothing

        accpet:
        collisions

        return:
        None """
        for coll in collisions:
            
        
            rep_vector = [self.UAV_locs[coll[0]][0] - self.UAV_locs[coll[1]][0], self.UAV_locs[coll[0]][1] - self.UAV_locs[coll[1]][1]]
            dist = rep_vector[0]**2 + rep_vector[1]**2
            if dist != 0:
                adapt_theta = np_random.uniform(-0.25*math.pi,0.25*math.pi)
                rep_vector = [rep_vector[0]*math.cos(adapt_theta) - rep_vector[1]*math.sin(adapt_theta) , 
                                rep_vector[0]*math.sin(adapt_theta) + rep_vector[1]*math.cos(adapt_theta)]
                adapt_dist = np_random.uniform(0.4,0.8)
                adapt = [(rep_vector[0]/dist) * adapt_dist , (rep_vector[1]/dist) * adapt_dist]
                self.UAV_locs[coll[0]] = [self.UAV_locs[coll[0]][0] + adapt[0] , self.UAV_locs[coll[0]][1] + adapt[1]]
                self.UAV_locs[coll[1]] = [self.UAV_locs[coll[1]][0] - adapt[0] , self.UAV_locs[coll[1]][1] - adapt[1]]
            else:
                velocity_sum = [action[coll[0]][0]+action[coll[1]][0] ,  action[coll[0]][1]+action[coll[1]][1]]
                dist = velocity_sum[0]**2 + velocity_sum[1]**2
                adapt_theta_a = np_random.uniform(-0.5*math.pi , -0.25*math.pi)
                adapt_theta_b = np_random.uniform(0.25*math.pi , 0.5*math.pi)
                adapt_dist = np_random.uniform(0.4,0.8)
                adapt_vector_a = velocity_sum/dist * adapt_dist
                adapt_vector_b = velocity_sum/dist * adapt_dist
                adapt_vector_a = [adapt_vector_a[0]*math.cos(adapt_theta_a) - adapt_vector_a[1]*math.sin(adapt_theta_a),
                                    adapt_vector_a[0]*math.sin(adapt_theta_a) + adapt_vector_a[1]*math.cos(adapt_theta_a) ]
                adapt_vector_b = [adapt_vector_b[0]*math.cos(adapt_theta_b) - adapt_vector_b[1]*math.sin(adapt_theta_b),
                                    adapt_vector_b[0]*math.sin(adapt_theta_b) + adapt_vector_b[1]*math.cos(adapt_theta_b) ]
                self.UAV_locs[coll[0]] = [self.UAV_locs[coll[0]][0] + adapt_vector_a[0] , self.UAV_locs[coll[0]][1] + adapt_vector_a[1]]
                self.UAV_locs[coll[1]] = [self.UAV_locs[coll[1]][0] + adapt_vector_b[0] , self.UAV_locs[coll[1]][1] + adapt_vector_b[1]]
            

    def find_nearby(self,id,action):
        nv = []
        nl = []
        uav_num = self.UAV_num
        #for uav_a in range(0,uav_num):
        uav_a = id
        for uav_b in range(0,len(self.UAV_locs)):
            if uav_a != uav_b:
                dist = (self.UAV_locs[uav_a][0]-self.UAV_locs[uav_b][0])**2 + (self.UAV_locs[uav_a][1]-self.UAV_locs[uav_b][1])**2
                if dist < self.comm_dist**2:
                    nv.append(action[uav_b])
                    nl.append(self.UAV_locs[uav_b])
        return nv,nl

            