import numpy as np
import math
import meshio
import matplotlib as plt
import pandas as pd 

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


class Boundary:

    def __init__(self, number, type):
        self.number = number
        self.type = type

    def  boundary_conditions(self, k):
        if self.type == "clamped":
            #заделка, ограничивает все степени свободы
            k[2 * self.number - 1][:] = 0 
            k[:][2 * self.number -1] = 0
            k[2 * self.number - 2][:] = 0
            k[:][2 * self.number - 2] = 0 
            k[2 * self.number - 1][2 * self.number - 1] = 1
            k[2 * self.number - 2][2 * self.number - 2] = 1 
        elif self.type == "pinned":
            #шарнирная опора,ограничивает только перемещения, разрешает повороты
            k[2 * self.number - 2][:] = 0
            k[:][2 * self.number - 2] = 0 
            k[2 * self.number - 2][2 * self.number - 2] = 1
        return k

class Forse:

    def __init__(self, number, type, load):
        self.number  = number
        self.type = type 
        self.load = load

    def loading(self, F):
        if self.type == "moment":
            F[ 2 * self.number - 1] = -self.load
        elif self.type == "concentrated force":
            F[ 2 * self.number - 2] = -self.load
    #тут в идеале добавить для распределнной нагрузки и мб еще что-то, пока хз
        return F

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


