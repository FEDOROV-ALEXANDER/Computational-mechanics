import numpy as np
import math
import meshio
import matplotlib as plt
import pandas as pd 

def save_data(U,F, elements, nodes): 

    Ux = np.zeros(len(U)//2)
    Uy = np.zeros(len(U)//2)
    j = 0
    k = 0

    for i in range(len(U)):
        if i%2 == 0:
            Ux[j] = U[i]
            j += 1
        else:
            Uy[k] = U[i]
            k += 1

    displacement = np.zeros((len(nodes), 2))
    displacement[:, 0] = Ux
    displacement[:, 1] = Uy
    forces = np.zeros((len(elements), 1)) 
    forces[:, 0] = F

    data_forces = pd.DataFrame(forces, index=elements ,columns=[ "Сила, Н"]) 
    data_displacemet = pd.DataFrame(displacement, index = nodes,  columns =[ "Ux, м", "Uy, м"] )
    data_displacemet.index.name = "Номер шарнира"
    data_forces.index.name = "Номер стержня"
    data_displacemet.to_excel(r'C:\Users\Alexander\source\Учеба\3 курс\Вычислительная механика\МКЭ\Finite_element_method\Euler–Bernoulli beam\Bending.xlsx') 
    data_forces.to_excel(r'C:\Users\Alexander\source\Учеба\3 курс\Вычислительная механика\МКЭ\Finite_element_method\Euler–Bernoulli beam\Bending.xlsx')




def J():
    return 


def mesh():
    return

def save_data():
    return




g = 9.81 # ускорение свободного падения
J = 7.87e-9 # момент инерции
A = 144e-6 # Площадь поперечного сечения
E = 2e11 # модуль упругости Юнга
rho = 7900 # плотность (сталь)
nodes_num = 21 # число узлов
elements_num = nodes_num - 1 # число отрезков
L = 1 # длина всей балки
l = L / elements_num # длина конечных элементов балки


def calc_deflection(u):
    xsi = np.array[-1, 1]
    ni = 1 / 4 * (1 - xsi) ** 2 * (2 + xsi)
    ni_theta = 1 / 8 * l * (1 - xsi) ** 2 * (1 + xsi)
    nj = 1 / 4 * (1 + xsi) ** 2 * (2 - xsi)
    nj_theta = -1 / 8 * l * (1 + xsi) ** 2 * (1 - xsi)
    n = np.array([ni, ni_theta, nj, nj_theta])
    v = n.T.dot(u)
    return v


def calc_curvature(u):
    xsi = np.linspace(-1, 1)
    b = 1 / l * np.array([6 * xsi / l, 3 * xsi - 1, -6 * xsi / l, 3 * xsi + 1])
    return b.T.dot(u)


def calc_force(u):
    b = 1 / l * np.array([6 / l, 3, -6 / l, 3])
    return b.dot(u)


k = E * J / (l * l * l) * np.array([[12, 6 * l, -12, 6 * l],
[6 * l, 4 * l * l, -6 * l, 2 * l * l],
[-12, -6 * l, 12, -6 * l],
[6 * l, 2 * l * l, -6 * l, 4 * l * l]])


k_global = np.zeros((2 * nodes_num, 2 * nodes_num))


for i in range(elements_num):
    k_global[2 * i, 2 * i: 2 * i + 4] += k[0, :]
    k_global[2 * i + 1, 2 * i: 2 * i + 4] += k[1, :]
    k_global[2 * i + 2, 2 * i: 2 * i + 4] += k[2, :]
    k_global[2 * i + 3, 2 * i: 2 * i + 4] += k[3, :]
    k_global[2 * nodes_num - 2, :] = 0
    4
    k_global[:, 2 * nodes_num - 2] = 0
    k_global[2 * nodes_num - 2, 2 * nodes_num - 2] = 1
    k_global[0, :] = 0
    k_global[:, 0] = 0
    k_global[0, 0] = 1


F1 = np.zeros((42, 1))
F2 = np.zeros((42, 1))
Pl = -2942
F_local1 = -l / 2 * rho * A * g * np.array([[1], [l / 6], [1], [-l / 6]])
F_local2 = l * Pl / 2 * np.array([[1], [l / 6], [1], [-l / 6]])
F1[0:2] = F_local1[0:2]
F1[0] = 0
F1[40:42] = F_local1[2:4]
F1[40] = 0
F2[10:12] = F_local2[0:2]
F2[20:22] = F_local2[2:4]


for i in range(5, 9):
    F2[2 * i + 2:2 * i + 4] = F_local2[0:2] + F_local2[2:4]
for i in range(19):
    F1[2 * i + 2:2 * i + 4] = F_local1[0:2] + F_local1[2:4]


u = np.linalg.solve(k_global, F1 + F2)
x = np.linspace(0, 1, nodes_num)
vs = []
moments = []
forces = []
vs.extend(calc_deflection(u[0:4]))
forces.append(-E * J * calc_force(u[0:4]))
moments.extend(-E * J * calc_curvature(u[0:4]))
for i in range(2, u.shape[0] - 2, 2):
    vs.extend(calc_deflection(u[i:i + 4])[1:])
    moments.extend(-E * J * calc_curvature(u[i:i + 4])[1:])
    forces.append(-E * J * calc_force(u[i:i + 4]))


plt.figure(0)
plt.plot(x, u) 
plt.xlabel("координата, м")
plt.ylabel("перемещение, мм")
plt.title("Beam")
plt.grid()

