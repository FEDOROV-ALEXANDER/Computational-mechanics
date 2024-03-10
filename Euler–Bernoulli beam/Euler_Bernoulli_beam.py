import matplotlib.pyplot as plt
import numpy as np


#enter data 
L = 1 # meter 
M = 1e4
E = 1.63e-6
J = 9.0625

#number of elements 
element_numbers = 10 
#global rigidity matrix 
K = np.zeros(((2 * element_numbers + 2), (2 * element_numbers + 2)))

#local rigidity matrix 
l = L / element_numbers


k = E * J / l ** 3 * np.array([[12, 6 * l, -12, 6 * l],
[6 * l, 4 * l * l, -6 * l, 2 * l * l],
[-12, -6 * l, 12, -6 * l],
[6 * l, 2 * l * l, -6 * l, 4 * l * l]])

for i in range(element_numbers): 
    sub = [2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3]
    K[np.ix_(sub, sub)] += k


# forses and moments 

node_forced = 1
F = np.zeros((2 * element_numbers + 2))
F[ 2 * node_forced - 1] = - M

#boundary conditions
bounded_node = 11

K[2 * bounded_node - 1][:] = 0 
K[:][2 * bounded_node -1] = 0
K[2 * bounded_node - 2][:] = 0
K[:][2 * bounded_node - 2] = 0 
K[2 * bounded_node - 1][2 * bounded_node - 1] = 1
K[2 * bounded_node - 2][2 * bounded_node - 2] = 1 
U = np.linalg.solve(K, F)


u2 = U[0: -1 : 2]

sf = np.zeros(2 * element_numbers)
sm = np.zeros(2 * element_numbers)

for i in range(element_numbers):
    q = U[2 * i : 2 * i + 4]
    r = np.matmul(k, q) 
    sf[2 * i] = r[0]
    sf[2 * i +1 ] = r[2] 

    sm[2 * i] = r[1]
    sm[2 * i + 1]  = r[3]


print("хуй")



