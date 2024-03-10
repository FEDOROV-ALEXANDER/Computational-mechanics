from calendar import leapdays
import numpy as np
import math
import meshio
import matplotlib.pyplot as plt
from module import save_data


S = 1 * 10 ** (-4) #cross-sectional area (m^2)
E = 2 * 10 ** 11 # Young's module (Pa)
absF = 1 * 10 **(3) # Forse N
forsed_hinges = [11,10,9,8,7] #hinges where force impact
sealed_hinges = [1, 6] # hinges wich are sealed

####coordinates of nodes in the truss (x, y)
nodes = [
    (0,0),(3,0),(6,0),
    (18,0),(21,0),
    (24,0),(21,2.25),(18,4.5),
    (12,9),(6,4.5),(3,2.25)
    ]

#forsed_hinges = [7, 8, 3] #hinges where force impact
#sealed_hinges = [4, 9] # hinges wich are sealed
#nodes = [
#    (15,-6),(21,-6),(18,0),
#    (24,0), (9, -6), (3, -6), 
#    (6, 0), (12, 0), (0, 0)
#    ]

#elements = [
#    (1,1,2),(2,2,3),
#    (3,3,4),(4,4,2),(5,5,1), 
#    (6,6,5), (7,7,6), (8,7,5), 
#    (9,5,8), (10,8,7),(11,9,7),
#    (12,6,9), (13,3,1), (14,1,8),
#    (15, 8, 3)
#    ]

 ###connection between rods and hinges (number of rod, number of first hinge, number of the second hinge)
elements = [
    (1,1,2),(2,2,3),(3,3,4),(4,4,5),
    (5,5,6),(6,6,7),(7,7,8),
    (8,8,9),(9,9,10),(10,10,11),(11,11,1),
    (12,2,11),(13,11,3),(14,3,10),(15,8,10),
    (16,8,3),(17,4,8),(18,4,7),(19, 5, 7)
    ]

#number degrees of freedom
number = len(nodes) * 2
#array for forses
F = np.zeros(number )
#system stiffness matrix
K = np.zeros((number , number ))
F_in = np.zeros((len(elements)))

for node in forsed_hinges:
    F[2 * (node-1)+1] = -absF


for element in elements:
    element_number, hinge1, hinge2 = element
    x1, y1 = nodes[hinge1-1]
    x2, y2 = nodes[hinge2-1]
    le = np.sqrt((x2 - x1) ** 2 +(y2 - y1) ** 2)
    l = ((x2 - x1))/le 
    m = ((y2 - y1))/le
    transform_matrix = np.array([[l, m, 0, 0], 
         [0, 0, l, m]]) 
    B = np.array([[1, -1], [-1, 1]])
    k = (transform_matrix.T @ B @ transform_matrix) * E * S / le
    place = [2 * hinge1-2 , 2 * hinge1 - 1, 2  * hinge2 -2 , 2 * hinge2 - 1]
    K[np.ix_(place, place)] +=k 

#hecking the fulfillment of conditions for K
print(np.linalg.det(K), "determinant K")
print(np.amax(abs(K-K.T)))

for node in sealed_hinges:
    F[2 * (node-1)] = 0
    F[2 * (node-1) + 1] = 0
    K[2 * (node-1), :] = 0
    K[2 * (node-1)+1, :] = 0
    K[:, 2 * (node-1)] = 0
    K[:, 2 * (node-1)+1] = 0
    K[2 * (node-1), 2 * (node-1)] = 1
    K[2 * (node-1) + 1, 2 * (node-1) + 1] = 1


print(np.linalg.det(K), "determinant K")
print(np.amax(abs(K-K.T)))

U = np.zeros(number, float )
U = np.linalg.solve(K, F)

print(U)
print("-------------------------------------------------------------")

elementnum = np.zeros(len(elements))
nodenum = np.linspace(0,len(nodes)-1, len(nodes))
nodenum += 1
nodenum = nodenum.astype(int)
for i in range(len(elements)):
    elementnum[i] = i+1

for element in elements:
    element_number, hinge1, hinge2 = element
    x1, y1 = nodes[hinge1-1]
    x2, y2 = nodes[hinge2-1]
    le = np.sqrt((x2 - x1) ** 2 +(y2 - y1) ** 2)
    Ux1 = U[2*(hinge1-1)]
    Uy1 = U[2*(hinge1-1)+1]
    Ux2 = U[2*(hinge2-1)]
    Uy2 = U[2*(hinge2-1)+1]
    x1 += Ux1
    x2 += Ux2
    y1 += Uy1 
    y2 += Uy2
    L = np.sqrt((x2-x1)**2 + (y2-y1) ** 2)
    F_in[element_number-1] = E * S * (L/le-1)
print(F_in)
 
save_data(U, F_in, elementnum, nodenum)