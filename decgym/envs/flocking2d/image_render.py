import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path as mtpath
import matplotlib.patches as patches

loc_color=[
    'navy',
    'mediumblue',
    'blue',
    'aqua',
    'springgreen',
    'lime',
    'lawngreen'
    'greenyyellow',
    'yellowgreen',
    'yellow',
    'gold',
    'orange',
    'orangered',
    'red',
    'red'
]

def render(episode, timestep, collision_num, target,target_dtst=100,value=0,trajectory = True, loc_history = [], image_path='',map_size=[],fpath=''):
    assert len(loc_history) != 0
    #assert image_path != ''

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_xlim(0,map_size[0])
    ax.set_ylim(0,map_size[1])
    title = 'timestep = '+str(timestep)+'    collision = '+str(collision_num) + '    value = ' +str(value)
    ax.set_title(title)
    
    target_aera = patches.Circle(
            target,
            radius=target_dtst,
            fc='y',
            ec='b',
            ls='-.',
            lw=1,
            alpha=0.3)
    ax.add_patch(target_aera)
    
    for tra in loc_history:
        trajec =[]
        path_code=[]
        #path_code.append(mtpath.MOVETO)
        for loc in tra:
            path_code.append(mtpath.LINETO)
            trajec.append((loc[0],loc[1]))
        path_code[0] = mtpath.MOVETO
        path = mtpath(trajec,path_code)
        patch = patches.PathPatch(path,facecolor='white', edgecolor='orange',  lw=2 , alpha=0.5)
        ax.add_patch(patch)
        ax.plot(tra[len(tra)-1][0],tra[len(tra)-1][1],'k.')
    ax.plot(target[0],target[1],'b*')
    #patch = patches.PathPatch(path, edgecolor='orange', lw=2)
    if fpath == '':
        filepath='d:\\flocking2d_resualt\episode'+str(episode)
    else:
        filepath = fpath
    import os
    isExists=os.path.exists(filepath)
    if not isExists:
        os.makedirs(filepath) 
    fig.savefig(filepath+'\\timestep'+str(timestep))
    plt.close(fig)