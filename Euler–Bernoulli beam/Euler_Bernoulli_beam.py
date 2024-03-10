import matplotlib.pyplot as plt
import numpy as np
import array


#enter data 
L = 1 # meter 
M = 1e4
E = 2e11
J = 1.63e-6#9.0625

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

node_forced = 1
F = np.zeros((2 * element_numbers + 2))
F[ 2 * node_forced - 1] = - M

#boundary conditions
bounded_node = 21

K[2 * bounded_node - 1][:] = 0 
K[:][2 * bounded_node -1] = 0
K[2 * bounded_node - 2][:] = 0
K[:][2 * bounded_node - 2] = 0 
K[2 * bounded_node - 1][2 * bounded_node - 1] = 1
K[2 * bounded_node - 2][2 * bounded_node - 2] = 1 


U = np.linalg.solve(K, F)

def calc_deflection(u):
    xsi = np.arange(-1, 1, 2)
    ni = 1 / 4 * (1 - xsi) ** 2 * (2 + xsi)
    ni_theta = 1 / 8 * l * (1 - xsi) ** 2 * (1 + xsi)
    nj = 1 / 4 * (1 + xsi) ** 2 * (2 - xsi)
    nj_theta = -1 / 8 * l * (1 + xsi) ** 2 * (1 - xsi)
    n = np.array([ni, ni_theta, nj, nj_theta])
    v = n.T.dot(u)
    return v


def calc_curvature(u):
    xsi = np.arange(-1, 1, 2)
    b = 1 / l * np.array([6 * xsi / l, 3 * xsi - 1, -6 * xsi / l, 3 * xsi + 1])
    return b.T.dot(u)


def calc_force(u):
    b = 1 / l * np.array([6 / l, 3, -6 / l, 3])
    return b.dot(u)


x = np.linspace(0, 1, element_numbers)
vs = []
moments = []
forces = []
vs.extend(calc_deflection(U[0:4]))
forces.append(-E * J * calc_force(U[0:4]))
moments.extend(-E * J * calc_curvature(U[0:4]))
for i in range(2, U.shape[0] - 2, 2):
    vs.extend(calc_deflection(U[i:i + 4]))
    moments.extend(-E * J * calc_curvature(U[i:i + 4]))
    forces.append(-E * J * calc_force(U[i:i + 4]))

Moments = array.array('f', moments)
for i in range(element_numbers):
    print(x[i], Moments[i])

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