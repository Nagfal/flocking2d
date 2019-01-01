import numpy
from numpy import linalg

def distance(pointA=[0,0], pointB=[0,0]):
    assert type(pointA) == list and type(pointB) == list
    assert len(pointA) == 2 and len(pointB) == 2
    vector = numpy.array(pointA) - numpy.array(pointB)
    dist = linalg.norm(vector)
    return dist

