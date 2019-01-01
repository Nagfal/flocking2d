from numpy import random
import numpy
from numpy import linalg
import time
a = [[(0,0)]] * 6
#a=random.uniform(300,500,[6,])
#a = a * -1
b=[]
for i in range(0,10):
    v =i
    b.append(v)
print(b)

parameters_range = {
    'p_rep':(0.0,100.0),
    'd_rep':(0.0,100.0),
    'p_ali':(0.0,100.0),
    'd_ali':(0.0,100.0),
    'p_att':(0.0,100.0),
    'd_att':(0.0,100.0),
    'p_obstacal':(0.0,100.0),
    'v_obstacal':(0.0,100.0),
    'd_obstacal':(0.0,100.0)
}

print (len(parameters_range))

parameters ={
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
for i in parameters_range:
    parameters[i] = random.uniform(parameters_range[i][0],parameters_range[i][1])
    print(i)

wall_a = [[1,1]]*20
wall_a[:20][0]=0
print(wall_a)


coll_adapt_start =time.clock()
for i in range(0,500):
    dist = (5.1234**2+6.4321**2)**0.5
elapsed = (time.clock() - coll_adapt_start)
print("coll_adapt Time used:",elapsed)
import math
ab=[]
coll_adapt_start =time.clock()

for i in range(0,500):
    ab.append(i)
    #dist = linalg.norm(dist_vec)
elapsed = (time.clock() - coll_adapt_start)
print("coll_adapt norm Time used:",elapsed)