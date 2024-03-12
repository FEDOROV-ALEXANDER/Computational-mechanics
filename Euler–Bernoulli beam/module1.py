import numpy as np
import math
import meshio
import matplotlib as plt
import pandas as pd 

def calc_deflection(u, l):
    xsi = np.arange(-1, 1, 2)
    ni = 1 / 4 * (1 - xsi) ** 2 * (2 + xsi)
    ni_theta = 1 / 8 * l * (1 - xsi) ** 2 * (1 + xsi)
    nj = 1 / 4 * (1 + xsi) ** 2 * (2 - xsi)
    nj_theta = -1 / 8 * l * (1 + xsi) ** 2 * (1 - xsi)
    n = np.array([ni, ni_theta, nj, nj_theta])
    v = n.T.dot(u)
    return v


def calc_curvature(u, l):
    xsi = np.arange(-1, 1, 2)
    b = 1 / l * np.array([6 * xsi / l, 3 * xsi - 1, -6 * xsi / l, 3 * xsi + 1])
    return b.T.dot(u)


def calc_force(u, l):
    b = 1 / l * np.array([6 / l, 3, -6 / l, 3])
    return b.dot(u)


class Boundary:

    def __init__(self, number, type):
        self.number = number
        self.type = type

    def  boundary_conditions(self, k):
        if self.type == "clamped":
            #заделка, ограничивает все степени свободы
            k[2 * self.number - 1, :] = 0 
            k[:,2 * self.number -1] = 0
            k[2 * self.number - 2, :] = 0
            k[:,2 * self.number - 2] = 0 
            k[2 * self.number - 1, 2 * self.number - 1] = 1
            k[2 * self.number - 2, 2 * self.number - 2] = 1 
        elif self.type == "pinned":
            #шарнирная опора,ограничивает только перемещения, разрешает повороты
            k[2 * self.number - 2, :] = 0
            k[:, 2 * self.number - 2] = 0 
            k[2 * self.number - 2, 2 * self.number - 2] = 1
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

def save_data(U, F,  M,  x): 

    data_result = pd.DataFrame({'Coordinate, m' : x,   'Displacements Y, mm' : U, 'Forses, N' : F, 'Moments N*m': M})
    with pd.ExcelWriter(r"C:\Users\Alexander\source\Учеба\3 курс\Вычислительная механика\МКЭ\Finite_element_method\Euler–Bernoulli beam\Bending.xlsx") as writer:
        data_result.to_excel(writer, sheet_name ="Python", index = "False")


