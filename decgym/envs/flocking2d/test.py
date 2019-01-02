import sys
sys.path.append('D:\PyProject\flocking2d')
import numpy

import get_speed as gs
import get_speed_f as gsf
from operator import itemgetter
import para_iterator as p_iter
import flocking2d_env as fe

import time
if __name__ == '__main__':
    env = fe.flocking2d_env()

    sample_num = 50
    sample_repeat = 20
    bestsample_num = 10
    #print(observations)

    avg_reward_cov =[]
    iter_times = 20

    parameters_range = {
        'p_rep':[0.0,100.0],
        'd_rep':[0.0,100.0],
        'p_ali':[0.0,100.0],
        'd_ali':[0.0,100.0],
        'p_att':[0.0,100.0],
        'd_att':[0.0,100.0],
        'p_obstacal':[0.0,100.0],
        'v_obstacal':[0.0,100.0],
        'd_obstacal':[0.0,100.0]
    }

    for iter in range(0,iter_times):
        #sampling
        parameters ={
            'p_rep':0.0,
            'd_rep':0.0,
            'p_ali':0.0,
            'd_ali':0.0,
            'p_att':0.0,
            'd_att':0.0,
            'p_obstacal':0.0,
            'v_obstacal':0.0,
            'd_obstacal':0.0,
            'avg_reward':0.0   
        }
        samples = []
        rewards = []
        avg_reward = []
        for j in range(0,sample_num):
            for i in parameters_range:
                parameters[i] = fe.np_random.uniform(parameters_range[i][0],parameters_range[i][1])
            samples.append(parameters.copy())

        #sim
        
        for parameter in samples:
            reward_sample_list = []
            #init_start = time.clock()
            if iter == iter_times-1:
                sample_repeat = 5
            for i in range(0,sample_repeat):
                observations, reward, done, info = env.reset()
                reward_sample = 0.0
                #t = 0
                time_step=0
                
                while not done:
                
                    action=[]
                    for j in range(0,len(observations)):
                        #action.append([1,1])
                          
                        #action.append(gs.velocity(observations[j],parameter,info['target_loc'], 5.0 ,8.0))
                        action.append(gsf.velocity(observations[j],parameter,info['target_loc'], 5,8))
                    observations, reward, done, info = env.step(action)
                    filepath='d:\\flocking2d_resualt\snapshot\episode'+str(i)
                    if iter == iter_times-1:
                        env.render(filepath='g:\\flocking2d_resualt\snapshot\example'+str(samples.index(parameter))+'\episode'+str(i))
                    time_step+=1
                    reward_sample +=reward['team']
                reward_sample_list.append(reward_sample)
                
                #print('value:'+str(reward_sample)+'||reach_num:'+str(info['reach_num']))
            #lapsed = (time.clock() - init_start)
           # print("Init action Time used:",elapsed)
            rewards.append(reward_sample_list)
            parameter['avg_reward'] = numpy.mean(reward_sample_list)
            print('para_avg_value = ' + str(parameter['avg_reward']))
            avg_reward.append(numpy.mean(reward_sample_list))
        #env.render() 
        avg_reward_cov.append(avg_reward)
        #iteration
        best_samples = []
        samples.sort(key = itemgetter('avg_reward'),reverse=True)
        best_samples = samples[:bestsample_num-1].copy()
        print('the best in this epoc is:******************************',best_samples[0])
        print('the avg in this epoc is:******************************',numpy.mean(avg_reward))
        parameters_range = p_iter.next_parameters(best_samples, parameters_range)
    print(parameters_range)

#print(observations)

