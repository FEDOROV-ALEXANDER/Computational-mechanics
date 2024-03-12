import matplotlib.pyplot as plt
import numpy as np
import array
import module1 as m



#enter data 
# TODO: найти свое значение J. 
L = 1 # meter 
M = 1e4
E = 2e11
J = 1.63e-6#9.0625


# TODO: попробывать сделать автоматический выбор размера элемента
#number of elements 
element_numbers = 10
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

#bounded_node = 11


##K[2 * bounded_node - 2][:] = 0
#K[:][2 * bounded_node - 2] = 0 

#K[2 * bounded_node - 2][2 * bounded_node - 2] = 1 
#bounded_node = 1

#bounded_node  = 1
#K[2 * bounded_node - 2][:] = 0
#K[:][2 * bounded_node - 2] = 0 

#K[2 * bounded_node - 2][2 * bounded_node - 2] = 1 
#L = K
#print(np.linalg.det(L))

right = m.Boundary(number = 11, type = "pinned")
K = right.boundary_conditions(K)


left = m.Boundary(number = 1, type = "pinned")
K = left.boundary_conditions(K)

# forses and moments
F = np.zeros((2 * element_numbers + 2))
 
#loaded = m.Forse(1, "concentrated force", M)
#F  = loaded.loading(F)
F[ 2 * 5 - 2] = -1e4


#solution of the basic equation 
U = np.linalg.solve(K, F)



#вывод данных (функции которые здесь используются просто взяты и пособия,
# в принципе можно было и основным уравнением МКЭ для элемента тоже самое получить)
x = np.linspace(0, 1, element_numbers)
vs = []
moments = []
forces = []
vs.extend(m.calc_deflection(U[0:4], l))
forces.append(-E * J * m.calc_force(U[0:4], l))
moments.extend(-E * J * m.calc_curvature(U[0:4], l))
for i in range(2, U.shape[0] - 2, 2):
    vs.extend(m.calc_deflection(U[i:i + 4], l))
    moments.extend(-E * J * m.calc_curvature(U[i:i + 4], l))
    forces.append(-E * J * m.calc_force(U[i:i + 4], l))


Moments = array.array('f', moments)
Forces = array.array('f', forces)
Displacements = array.array('f', vs)


for i in range(element_numbers):
    print(x[i],"   ",  Moments[i],"  ",  Forces[i], "  ", Displacements[i], "   ", forces[i])
m.save_data(Displacements, Forces, Moments, x)




# TODO:  Добавить сохранение данных в таблице и графики
plt.figure()
plt.plot(x, Moments) 
plt.xlabel("координата, м")
plt.ylabel("Момент, Н*м")
plt.title("Beam")
plt.grid()
plt.show()


plt.figure()
plt.plot(x, Displacements) 
plt.xlabel("координата, м")
plt.ylabel("перемещение, мм")
plt.title("Beam")
plt.grid()
plt.show()


plt.figure()
plt.plot(x,Forces) 
plt.xlabel("координата, м")
plt.ylabel("Сила, Н")
plt.title("Beam")
plt.grid()
plt.show()


print("хуй")