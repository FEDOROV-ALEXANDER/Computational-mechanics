import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

def implicit_method_solution(K, M, F, steps, t):
    Deflections = np.zeros((steps + 1, len(F)))
    Velocities = np.zeros((steps + 1, len(F)))
    Accelerations = np.zeros((steps + 1, len(F)))

    dt = t/steps
    #Это константы метода Ньюмарка
    beta = 0.26
    gamma = 0.53

    for i in range(1, steps + 1):
        accelerations = np.zeros(len(F))
        velocities = np.zeros(len(F))
        deflections = np.zeros(len(F))

        deflections = Deflections[i-1, :] + dt * Velocities[i-1, :] + (0.5 - beta) * dt * dt * Accelerations[i-1, :]
        velocities = Velocities[i - 1, :] + (1 - gamma) * dt * Accelerations[i-1, :]
        if(i <=int(steps / 2)):
            accelerations = (np.linalg.inv(M + beta * (dt **2) * K)) @ (F * 2 * i / steps- K @ deflections)
        else:
            accelerations = (np.linalg.inv(M + beta * (dt **2) * K)) @ (- K @ deflections)
        deflections += (0.5 - beta) * dt * dt * accelerations
        velocities += gamma * dt * accelerations

        Accelerations[i, :] = accelerations
        Velocities[i, :]  = velocities
        Deflections[i, :]  = deflections

    return Deflections, Velocities, Accelerations

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

def save_data(Deflections, Velocities,  Accelerations,  x): 

    data_deflections = pd.DataFrame({'Координата, м' : x,   'zero' : Deflections[0][0::2], 'first' : Deflections[1][0::2], 
                                'second': Deflections[2][0::2], 'third': Deflections[3][0::2]  ,
                               'fourth' : Deflections[4][0::2],'fifth': Deflections[5][0::2],	'sixth': Deflections[6][0::2],	
                               'seventh':	Deflections[7][0::2],'eighth':	Deflections[8][0::2],
                               'ninth':	Deflections[9][0::2],'tenh': Deflections[10][0::2]})
    
        

    data_velocities = pd.DataFrame({'Координата, м' : x,   'zero' : Velocities[0][0::2], 'first' : Velocities[1][0::2], 
                                'second': Velocities[2][0::2], 'third': Velocities[3][0::2]  ,
                               'fourth' : Velocities[4][0::2],'fifth': Velocities[5][0::2],	'sixth': Velocities[6][0::2],	
                               'seventh':	Velocities[7][0::2],'eighth':	Velocities[8][0::2],
                               'ninth':	Velocities[9][0::2],'tenh': Velocities[10][0::2]})
    
      

    data_accelerations = pd.DataFrame({'Координата, м' : x,   'zero' : Accelerations[0][0::2], 'first' : Accelerations[1][0::2], 
                                'second': Accelerations[2][0::2], 'third': Accelerations[3][0::2]  ,
                               'fourth' : Accelerations[4][0::2],'fifth': Accelerations[5][0::2],	'sixth': Accelerations[6][0::2],	
                               'seventh':	Accelerations[7][0::2],'eighth':	Accelerations[8][0::2],
                               'ninth':	Accelerations[9][0::2],'tenh': Accelerations[10][0::2]})

    with pd.ExcelWriter(r"C:\Users\Alexander\source\Studying\3 course\Computational mechanical\МКЭ\Finite_element_method\DynamicBending\Python.xlsx") as writer:
        data_deflections.to_excel(writer, sheet_name ="Прогибы", index = "False")
        data_velocities.to_excel(writer, sheet_name ="Скорости", index = "False")
        data_accelerations.to_excel(writer, sheet_name ="Ускорения", index = "False")

def plots(Deflections, Velocities, Accelerations, x):
    
    plt.figure(1)
    for i in(range(0, 6)):
        plt.plot(x, Deflections[i][0::2], label = f'{i/10}c')
    plt.legend()
    plt.xlabel("Координата, м")
    plt.ylabel("Прогибы, м")
    plt.title("Перемещения 0 - 0.5 с")
    plt.grid()
    plt.savefig('Перемещения(0-0.5) Python.png')

    plt.figure(2)
    for i in(range(6, 11)):
        plt.plot(x, Deflections[i][0::2], label = f'{i/10}c')
    plt.legend()
    plt.xlabel("Координата, м")
    plt.ylabel("Прогибы, м")
    plt.title("Перемещения 0.6 - 1 с")
    plt.grid()
    plt.savefig('Перемещения(0.6-1) Python.png')


    plt.figure(3)
    for i in(range(0, 6)):
        plt.plot(x, Velocities[i][0::2], label = f'{i/10}c')
    plt.legend()
    plt.xlabel("Координата, м")
    plt.ylabel("Скорость,  м/с")
    plt.title("Скорости 0 - 0.5 с")
    plt.grid()
    plt.savefig('Скорости(0-0.5) Python.png')

    plt.figure(4)
    for i in(range(6, 11)):
        plt.plot(x, Velocities[i][0::2], label = f'{i/10}c')
    plt.legend()
    plt.xlabel("Координата, м")
    plt.ylabel("Скорость,  м/с")
    plt.title("Скорости 0.6 - 1 с")
    plt.grid()
    plt.savefig('Скорости(0.6-1) Python.png')


    plt.figure(5)
    for i in(range(0, 6)):
        plt.plot(x, Accelerations[i][0::2], label = f'{i/10}c')
    plt.legend()
    plt.xlabel("Координата, м")
    plt.ylabel("Ускорение,  м/с^2")
    plt.title("Ускорения 0 - 0.5 с")
    plt.grid()
    plt.savefig('Ускорения(0-0.5) Python.png')

    plt.figure(6)
    for i in(range(6, 11)):
        plt.plot(x, Accelerations[i][0::2], label = f'{i/10}c')
    plt.legend()
    plt.xlabel("Координата, м")
    plt.ylabel("Ускорение,  м/с^2")
    plt.title("Ускорения 0.6 - 1 с")
    plt.grid()
    plt.savefig('Ускорения(0.6-1) Python.png')

    #return