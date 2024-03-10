from pickle import TRUE 
import numpy as np 
import math as m 
from openpyxl import load_workbook
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d 
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
    data_displacemet.to_excel(r'C:\Users\Alexander\source\Учеба\3 курс\Вычислительная механика\МКЭ\Finite_element_method\tension-compression of elastic rods\Таблица1.xlsx') 
    data_forces.to_excel(r'C:\Users\Alexander\source\Учеба\3 курс\Вычислительная механика\МКЭ\Finite_element_method\tension-compression of elastic rods\Таблица2.xlsx')
