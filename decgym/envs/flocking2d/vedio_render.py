
#-*- coding: UTF-8 -*-  

 

import imageio

 

def create_gif(image_list, gif_name):

 

    frames = []

    for image_name in image_list:

        frames.append(imageio.imread(image_name))

    # Save them as frames into a gif 

    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.1)

 

    return

 

def main():

    #image_list = ['test_gif-0.png', 'test_gif-2.png', 'test_gif-4.png', 

                  #'test_gif-6.png', 'test_gif-8.png', 'test_gif-10.png']
    image_list=[]
    for i in range(0,400):
        image_list.append('g:\\flocking2d_resualt\snapshot\example3\episode0\\timestep'+str(i+1)+'.png')

    gif_name = 'e3e0.gif'

    create_gif(image_list, gif_name)

 

if __name__ == "__main__":

    main()
