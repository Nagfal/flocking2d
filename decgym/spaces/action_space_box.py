import sys
sys.path.append('D:\PyProject')
from decgym.spaces import space
from decgym.spaces import np_random

class action_space_box(space.space):

    def __init__(self, low = None, high = None, shape = None, dtype = None):
        import numpy as np

        if shape is None:
            assert low.shape == high.shape
            shape = low.shape
        else:
            assert np.isscalar(low) and np.isscalar(high)
            low = low + np.zeros(shape)
            high = high + np.zeros(shape)
        if dtype is None:  # Autodetect type
            if (high == 255).all():
                dtype = np.uint8
            else:
                dtype = np.float32
            raise('Sutodetected dtype as %s. Please provide explicit dtype.' % dtype)
            #logger.warn("gym.spaces.Box autodetected dtype as %s. Please provide explicit dtype." % dtype)
        self.low = low.astype(dtype)
        self.high = high.astype(dtype)
        space.space.__init__(self,shape,dtype)
        pass
    
    def sample(self):
        return np_random.uniform(low = self.low, high = self.high + (0 if self.dtype.kind == 'f' else 1), size=self.low.shape).astype(self.dtype)
    
    def contains(self,x):
        return x.shape == self.shape and (x >= self.low).all() and (x <= self.high).all()
