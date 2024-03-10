import numpy as np

def getFigure():
    X= [[0, 0, 0],
   [1, 0, 0],
   [0, 1, 0],
   [0, 0, 1],
   [0.5, 0, 0], 
   [0, 0.5, 0],
   [0, 0, 0.5],
   [0.5, 0.5, 0],
   [0.5, 0, 0.5],
   [0, 0.5, 0.5]]

    return np.array( X )



def fill_form_vector(x, y, z):
   return [1+0*x, x, y, z, x ** 2, y ** 2, z ** 2, x * y, x * z, y * z]
