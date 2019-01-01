
import sys
sys.path.append('D:\PyProject')
from decgym.envs.flocking2d import flocking_math as fm

#example of parameters
{
    'p_rep':0.0,
    'd_rep':0.0,
    'p_ali':0.0,
    'd_ali':0.0,
    'p_att':0.0,
    'd_att':0.0,
    'p_obstacal':0.0,
    'v_obstacal':0.0,
    'd_obstacal':0.0
}

def norm(pointA):
    return (pointA[0]**2 + pointA[1]**2)**0.5
def vector2d_sum(vect_list):
    result =[0.0,0.0]
    for point in vect_list:
        result[0] += point[0]
        result[1] += point[1]
    return result

def velocity(obser_self = {} , parameters = {}, targetloc=[], v_flock=10.0 ,v_max=0.0):
    v_desired = [0.0,0.0]
    velocitylist =[v_desired , v_rep(obser_self,parameters) ,v_ali(obser_self,parameters) , v_att(obser_self,parameters) , v_obstacal(obser_self,parameters)]
    
    v_target =[targetloc[0]-obser_self['loc'][0], targetloc[1]-obser_self['loc'][1]]
    v_target = [v_target[0]/norm(v_target) * v_flock,v_target[1]/norm(v_target) * v_flock]
    velocitylist.append(v_target)

    v_desired = vector2d_sum(velocitylist)
    v_max_d = v_desired/ norm(v_desired) * v_max
    if norm(v_desired)<v_max:          
        return v_desired
    else:
        return v_max_d
    

def v_rep(obser_self = {} , parameters = {}):
    v_rep = [0.0,0.0]
    velocitylist = []
    velocitylist.append(v_rep)
    for partner in obser_self['nearby_loc']:
        #dist_vec=fm.numpy.array(obser_self['loc'])-fm.numpy.array(partner)
        dist_vec=[obser_self['loc'][0]-partner[0], obser_self['loc'][1]-partner[1]]
        dist = norm(dist_vec)
        if dist == 0:
            pass
        elif dist < parameters['d_rep']:
            dist_vec_u= [dist_vec[0]/dist, dist_vec[1]/dist]
            r = [parameters['p_rep'] * (parameters['d_rep'] - dist) * dist_vec_u[0] , parameters['p_rep'] * (parameters['d_rep'] - dist) * dist_vec_u[1]] 
            #v_rep += parameters['p_rep'] * (parameters['d_rep'] - dist) * (dist_vec / dist)
            velocitylist.append(r)
    v_rep = vector2d_sum(velocitylist)
    return v_rep

def v_ali(obser_self = {} , parameters = {}):
    v_ali = [0.0,0.0]
    vlist =[]
    vlist.append([0.0,0.0])
    for i in range(len(obser_self['nearby_loc'])):
        #dist_vec=fm.numpy.array(obser_self['loc'])-fm.numpy.array(obser_self['nearby_loc'][i])
        dist_vec = [obser_self['loc'][0] - obser_self['nearby_loc'][i][0] , obser_self['loc'][1] - obser_self['nearby_loc'][i][1] ]
        dist = norm(dist_vec)
        #v_rela = fm.numpy.array(obser_self['loc'])-fm.numpy.array(obser_self['nearby_velocity'][i])
        v_rela = [obser_self['velocity'][0] - obser_self['nearby_velocity'][i][0] , obser_self['velocity'][1] - obser_self['nearby_velocity'][i][1] ]
        v_rela_mag = norm(v_rela)
        if dist == 0 or v_rela_mag ==0:
            pass
        elif dist < parameters['d_ali']:
            v_rela = [v_rela[0]*parameters['p_ali']*(parameters['d_ali'] - dist ) , v_rela[1]*parameters['p_ali']*(parameters['d_ali'] - dist )  ]
            #v_ali += (parameters['d_ali']/parameters['p_ali']) * (parameters['d_ali'] - dist )  * v_rela_mag + parameters['p_ali']
            vlist.append(v_rela)
        v_ali = vector2d_sum(vlist)
    return v_ali    
    
def v_att(obser_self = {} , parameters = {}):
    v_att =[0.0,0.0]
    v_list =[]
    for partner in obser_self['nearby_loc']:
        dist_vec=[partner[0]-obser_self['loc'][0], partner[1]-obser_self['loc'][1]]
        dist = norm(dist_vec)
        
        if dist==0:
            pass
        elif dist > parameters['d_att']:
            dist_u = [dist_vec[0]/dist , dist_vec[1]/dist]
            v =[parameters['p_att'] * (dist - parameters['d_att']) * dist_u[0] , parameters['p_att'] * (dist - parameters['d_att']) * dist_u[1]]
            v_list.append(v)
        v_att = vector2d_sum(v_list) 
    return v_att
    

def v_obstacal(obser_self = {} , parameters = {}):
    v_obstacal = fm.numpy.array([0.0,0.0])
    for partner in obser_self['obs_wall']:
        dist_vec=[partner[0]-obser_self['loc'][0], partner[1]-obser_self['loc'][1]]
        dist = norm(fm.numpy.array(dist_vec))
        if dist == 0:
            pass
        elif dist < parameters['d_obstacal']:
            v_obstacal += parameters['p_obstacal'] * (parameters['p_obstacal'] - dist) * (dist_vec / dist)
    return v_obstacal
    