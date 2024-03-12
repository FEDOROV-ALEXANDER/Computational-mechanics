from xml.dom.minidom import Element
import matplotlib.pyplot as plt
import numpy as np
import array
import module1 as m



#enter data 
# TODO: найти свое значение J. 
L = 1 # meter 
M = 1e4
E = 2e11
J = 1.63e-6#dvutavr
J = 0.90625e-6 # tavr

# TODO: попробывать сделать автоматический выбор размера элемента
#number of elements 
element_numbers = 20
#global rigidity matrix 
K = np.zeros(((2 * element_numbers + 2), (2 * element_numbers + 2)))

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


right = m.Boundary(number = 21, type = "pinned")
K = right.boundary_conditions(K)


left = m.Boundary(number = 1, type = "pinned")
K = left.boundary_conditions(K)

#right = m.Boundary(number = 21, type = "clamped")
#K = right.boundary_conditions(K)

# forses and moments
F = np.zeros((2 * element_numbers + 2))
 
loaded = m.Forse(6, "moment", -1e4)
F  = loaded.loading(F)
#F[ 2 * 6 - 2] = -1e4


#solution of the basic equation 
U = np.linalg.solve(K, F)

x = np.linspace(0, 1, element_numbers + 1)


Moments = np.zeros(element_numbers + 1)
Forces = np.zeros(element_numbers + 1)
Displacements = U[0 : U.shape[0] - 1 : 2]
for i in  range(element_numbers ):
    u = U[2 * i: 2 * i + 4]
    f = np.matmul(k, u)
    Moments[i]  = f[1]
    Forces[i] = f[0]
    Forces[i + 1] = f[2]
    Moments[i + 1] = f[3]

Forces[-1] *=-1
Moments[-1] *=-1
Forces = np.round(Forces, 5)
Moments =  np.round(Moments, 5)

x *= 1000
for i in range(element_numbers + 1):
    print(x[i],"   ",  Moments[i],"  ",  Forces[i], "  ", Displacements[i])
m.save_data(Displacements, Forces, Moments, x)




# TODO:  Добавить сохранение данных в таблице и графики

plt.figure()
plt.plot(x, Moments) 
plt.xlabel("координата, м")
plt.ylabel("Момент, Н*м")
plt.title("Python")
plt.grid()
plt.show()


plt.figure()
plt.plot(x, Displacements) 
plt.xlabel("координата, м")
plt.ylabel("перемещение, мм")
plt.title("Python")
plt.grid()
plt.show()


plt.figure()
plt.plot(x,Forces) 
plt.xlabel("координата, м")
plt.ylabel("Сила, Н")
plt.title("Python")
plt.grid()
plt.show()

