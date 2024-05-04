import matplotlib.pyplot as plt
import numpy as np
import array
import moduledynamics as md

L = 1 # meter 
Momemnt = 1e4
E = 2e11
J = 3.75e-7
density = 7800
S = 0.00075
steps = 10
#number of elements 
element_numbers = 20
#global rigidity matrix 
K = np.zeros(((2 * element_numbers + 2), (2 * element_numbers + 2)))
M = np.zeros(((2 * element_numbers + 2), (2 * element_numbers + 2)))
#local rigidity matrix 
l = L / element_numbers

k = E * J / l ** 3 * np.array([[12, 6 * l, -12, 6 * l],
                            [6 * l, 4 * l * l, -6 * l, 2 * l * l],
                            [-12, -6 * l, 12, -6 * l],
                            [6 * l, 2 * l * l, -6 * l, 4 * l * l]])
#creating global rigidity matrix 
for i in range(element_numbers): 
    sub = [2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3]
    K[np.ix_(sub, sub)] += k


right = md.Boundary(number = 21, type = "pinned")
K = right.boundary_conditions(K)


left = md.Boundary(number = 1, type = "pinned")
K = left.boundary_conditions(K)

# Матрица масс
m = (density*S*l/420)*np.array([[156,       22*l,       54,     -13*l    ],
                             [22*l,     4*l**2,     13*l,   -3*l**2  ],
                             [54,       13*l,       156,    -22*l    ],
                             [-13*l,    -3*l**2,    -22*l,  4*l**2   ]])

for i in range(element_numbers): 
    sub = [2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3]
    M[np.ix_(sub, sub)] += m

    
right = md.Boundary(number = 21, type = "pinned")
M = right.boundary_conditions(M)


left = md.Boundary(number = 1, type = "pinned")
M = left.boundary_conditions(M)

F = np.zeros((2 * element_numbers + 2))
 
loaded = md.Forse(6, "moment", -1e4)
F  = loaded.loading(F)

Deflections, Velocities, Accelerations = md.implicit_method_solution(K, M, F, steps, 1)

x = np.linspace(0, 1, element_numbers + 1)
md.plots(Deflections, Velocities, Accelerations, x)
md.save_data(Deflections, Velocities,  Accelerations,  x)
print("хуй")















