﻿#Эта программа просто переписывает данные из таблицы и строит графики

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dataY = pd.read_excel(r"C:\Users\Alexander\source\Studying\3 course\Computational mechanical\МКЭ\Finite_element_method\DynamicBending\Abaqus.xlsx", sheet_name="Прогибы")

x = list(dataY['coordinate'])
deflection0 = list(dataY['zero'])
deflection1 = list(dataY['first'])
deflection2 = list(dataY['second'])
deflection3 = list(dataY['third'])
deflection4 = list(dataY['fourth'])
deflection5 = list(dataY['fifth'])
deflection6 = list(dataY['sixth'])
deflection7 = list(dataY['seventh'])
deflection8 = list(dataY['eighth'])
deflection9 = list(dataY['ninth'])
deflection10 = list(dataY['tenh'])

plt.figure(1)
plt.plot(x, deflection0, label = '0,c')
plt.plot(x, deflection1, label = '0.1,c') 
plt.plot(x, deflection2, label = '0.2,c') 
plt.plot(x, deflection3, label = '0.3,c') 
plt.plot(x, deflection4, label = '0.4,c') 
plt.plot(x, deflection5, label = '0.5,c') 
plt.legend()
plt.xlabel("Координата, м")
plt.ylabel("Прогибы, м")
plt.title("Перемещения 0 - 0.5, с")
plt.grid()
plt.savefig('Перемещения(0-0.5) Abaqus.png')

plt.figure(2)
plt.plot(x, deflection6, label = '0.6,c')
plt.plot(x, deflection7, label = '0.7,c') 
plt.plot(x, deflection8, label = '0.8,c') 
plt.plot(x, deflection9, label = '0.9,c') 
plt.plot(x, deflection10, label = '0.10,c') 
plt.legend()
plt.xlabel("Координата, м")
plt.ylabel("Прогибы, м")
plt.title("Перемещения 0.6 - 1, с")
plt.grid()
plt.savefig('Перемещения(0.6-1) Abaqus.png')


dataV = pd.read_excel(r"C:\Users\Alexander\source\Studying\3 course\Computational mechanical\МКЭ\Finite_element_method\DynamicBending\Abaqus.xlsx", sheet_name="Скорости")

x = list(dataV['координата'])
speed0 = list(dataV['zero'])
speed1 = list(dataV['first'])
speed2 = list(dataV['second'])
speed3 = list(dataV['third'])
speed4 = list(dataV['fourth'])
speed5 = list(dataV['fifth'])
speed6 = list(dataV['sixth'])
speed7 = list(dataV['seventh'])
speed8 = list(dataV['eighth'])
speed9 = list(dataV['ninth'])
speed10 = list(dataV['tenh'])


plt.figure(3)
plt.plot(x, speed0, label = '0,c')
plt.plot(x, speed1, label = '0.1,c') 
plt.plot(x, speed2, label = '0.2,c') 
plt.plot(x, speed3, label = '0.3,c') 
plt.plot(x, speed4, label = '0.4,c') 
plt.plot(x, speed5, label = '0.5,c') 
plt.legend()
plt.xlabel("Координата, м")
plt.ylabel("Скорость,  м/с")
plt.title("Скорости 0 - 0.5, с")
plt.grid()
plt.savefig('Скорости(0-0.5) Abaqus.png')

plt.figure(4)
plt.plot(x, speed6, label = '0.6,c')
plt.plot(x, speed7, label = '0.7,c') 
plt.plot(x, speed8, label = '0.8,c') 
plt.plot(x, speed9, label = '0.9,c') 
plt.plot(x, speed10, label = '0.10,c') 
plt.legend()
plt.xlabel("Координата, м")
plt.ylabel("Скорость,  м/с")
plt.title("Скорости 0.6 - 1, с")
plt.grid()
plt.savefig('Скорости(0.6-1) Abaqus.png')

dataA = pd.read_excel(r"C:\Users\Alexander\source\Studying\3 course\Computational mechanical\МКЭ\Finite_element_method\DynamicBending\Abaqus.xlsx", sheet_name="Ускорения")
x = list(dataA['координата'])
acceleration0 = list(dataA['zero'])
acceleration1 = list(dataA['first'])
acceleration2 = list(dataA['second'])
acceleration3 = list(dataA['third'])
acceleration4 = list(dataA['fourth'])
acceleration5 = list(dataA['fifth'])
acceleration6 = list(dataA['sixth'])
acceleration7 = list(dataA['seventh'])
acceleration8 = list(dataA['eighth'])
acceleration9 = list(dataA['ninth'])
acceleration10 = list(dataA['tenh'])


plt.figure(5)
plt.plot(x, acceleration0, label = '0,c')
plt.plot(x, acceleration1, label = '0.1,c') 
plt.plot(x, acceleration2, label = '0.2,c') 
plt.plot(x, acceleration3, label = '0.3,c') 
plt.plot(x, acceleration4, label = '0.4,c') 
plt.plot(x, acceleration5, label = '0.5,c') 
plt.legend()
plt.xlabel("Координата, м")
plt.ylabel("Ускорение,  м/с^2")
plt.title("Ускорения 0 - 0.5, с")
plt.grid()
plt.savefig('Ускорения(0-0.5) Abaqus.png')

plt.figure(6)
plt.plot(x, acceleration6, label = '0.6,c')
plt.plot(x, acceleration7, label = '0.7,c') 
plt.plot(x, acceleration8, label = '0.8,c') 
plt.plot(x, acceleration9, label = '0.9,c') 
plt.plot(x, acceleration10, label = '0.10,c') 
plt.legend()
plt.xlabel("Координата, м")
plt.ylabel("Ускорение,  м/с^2")
plt.title("Ускорения 0.6 - 1, с")
plt.grid()
plt.savefig('Ускорения(0.6-1) Abaqus.png')