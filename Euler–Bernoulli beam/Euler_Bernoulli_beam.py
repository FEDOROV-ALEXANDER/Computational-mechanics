﻿import matplotlib.pyplot as plt
import numpy as np
import array
import module1 as m


#enter data 
# TODO: найти сове значение J. 
L = 1 # meter 
M = 1e4
E = 2e11
J = 1.63e-6#9.0625


# TODO: попробывать сделать автоматический выбор размера элемента
#number of elements 
element_numbers = 20 
#global rigidity matrix 
K = np.zeros(((2 * element_numbers + 2), (2 * element_numbers + 2)))

#local rigidity matrix 
l = L / element_numbers
x = np.arange(0, L + l, l)


k = E * J / l ** 3 * np.array([[12, 6 * l, -12, 6 * l],
                            [6 * l, 4 * l * l, -6 * l, 2 * l * l],
                            [-12, -6 * l, 12, -6 * l],
                            [6 * l, 2 * l * l, -6 * l, 4 * l * l]])

for i in range(element_numbers): 
    sub = [2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3]
    K[np.ix_(sub, sub)] += k

# forses and moments
F = np.zeros((2 * element_numbers + 2))
 


loaded = m.Forse(1, "moment", M)
F  = loaded.loading(F)

right = m.Boundary(number = 21, type = "clamped")
K = right.boundary_conditions(K)

U = np.linalg.solve(K, F)




x = np.linspace(0, 1, element_numbers)
vs = []
moments = []
forces = []
vs.extend(m.calc_deflection(U[0:4]))
forces.append(-E * J * m.calc_force(U[0:4]))
moments.extend(-E * J * m.calc_curvature(U[0:4]))
for i in range(2, U.shape[0] - 2, 2):
    vs.extend(m.calc_deflection(U[i:i + 4]))
    moments.extend(-E * J * m.calc_curvature(U[i:i + 4]))
    forces.append(-E * J * m.calc_force(U[i:i + 4]))

Moments = array.array('f', moments)
for i in range(element_numbers):
    print(x[i], Moments[i])


# TODO:  Добавить сохранение данных в таблице и графики
plt.figure()
plt.plot(x, Moments) 
plt.xlabel("координата, м")
plt.ylabel("Момент, кН*м")
plt.title("Beam")
plt.grid()
plt.show()


plt.figure()
plt.plot(x, vs) 
plt.xlabel("координата, м")
plt.ylabel("перемещение, мм")
plt.title("Beam")
plt.grid()
plt.show()


plt.figure()
plt.plot(x, forces) 
plt.xlabel("координата, м")
plt.ylabel("Сила, кН")
plt.title("Beam")
plt.grid()
plt.show()


print("хуй")