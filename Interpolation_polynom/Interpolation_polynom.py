from ctypes import sizeof
import numpy as np
import matplotlib.pyplot as plt
import element as f
import sympy as sp


def get_x_matrix(variables):
    dimension = len(variables)
    X = np.zeros( (dimension, dimension) )

    for i in range(0, dimension):
        current_set = variables[i, :]
        X[i, : ] = f.fill_form_vector(current_set[0], current_set[1], current_set[2])
    X = np.linalg.inv(X) 
    X = X.T
    return X

def graph(F, step, title, xlabel, ylabel, projection):
    xl = np.linspace(0, 1, step)
    xgrid, ygrid = np.meshgrid(xl, xl)
    fig, ax = plt.subplots()
    cs = ax.contourf(xgrid, ygrid, F, levels = 10)
    cbar = plt.colorbar(cs)
    ax.set_xlabel("{}".format(xlabel))
    ax.set_ylabel("{}".format(ylabel))
    ax.set_title("{0}({1}, {2}) при {3} = 0" .format(title, xlabel, ylabel, projection))
    ax.grid()
    plt.savefig("fileout/Функция формы({}).png".format(title))


def main():
    varis = f.getFigure()
    X = get_x_matrix(varis)
    print(X)
    step = 101
    step1 = 101
    N1 = np.zeros((step, step))
    N2 = np.zeros((step, step))
    N3 = np.zeros((step, step))
    N4 = np.zeros((step, step))
    N5 = np.zeros((step, step))
    N6 = np.zeros((step, step))
    N7 = np.zeros((step, step))
    N8 = np.zeros((step, step))
    N9 = np.zeros((step, step))
    N10 = np.zeros((step, step))
    xcoord = np.linspace(0, 1, step)
    ycoord = np.linspace(0, 1, step)
    zcoord = np.linspace(0, 1, step)
    for i in range(step):
        for j in range(step1):
            N1[i][j] = 1 - 3 * xcoord[i] - 3 * ycoord[j] + 2 * xcoord[i] ** 2 + 2 * ycoord[j] ** 2 + 4 * xcoord[i] * ycoord[j]
            N2[i][j] = -xcoord[i] + 2 * xcoord[i] ** 2 
            N3[i][j] = -ycoord[j] + 2 * ycoord[j] ** 2
            N4[i][j] = -zcoord[j] + 2 * zcoord[j] ** 2
            N5[i][j] = 4 * xcoord[i] - 4 * xcoord[i] ** 2 - 4 * xcoord[i] * ycoord[j]
            N6[i][j] = 4 * ycoord[j] - 4 * ycoord[j] ** 2 - 4 * xcoord[i] * ycoord[j]
            N7[i][j] = 4 * zcoord[j] - 4 * zcoord[j] ** 2 - 4 * ycoord[i] * zcoord[j]
            N8[i][j] = 4 * xcoord[i] * ycoord[j]
            N9[i][j] = 4 * zcoord[i] * xcoord[j] 
            N10[i][j] = 4 * ycoord[i] * zcoord[j] 
            
        step1 = step1 - 1
    graph(N1, step,'N1', 'x', 'y', 'z')
    graph(N2, step,'N2', 'x', 'y', 'z')
    graph(N3, step,'N3', 'x', 'y', 'z')
    graph(N4, step,'N4', 'y', 'z', 'x')
    graph(N5, step,'N5', 'x', 'y', 'z')
    graph(N6, step,'N6', 'x', 'y', 'z')
    graph(N7, step,'N7', 'y', 'z', 'x')
    graph(N8, step,'N8', 'x', 'y', 'z')
    graph(N9, step,'N9', 'z', 'x', 'y')
    graph(N10, step,'N10', 'y', 'z', 'x')


if __name__ == "__main__": 
    main()


#def graphics(A):
#    n=11
#    x = np.linspace(0, 1, n)
#    y = np.linspace(0, 1, n)
#    z = np.linspace(0, 1, n)
#    X, Y, Z = np.meshgrid(x, y, z)
#    for k in range(10):
#        N = form_function_for_node(x, y, z, A, k)
#        fig = plt.figure() 
#        ax = plt.axes(projection = '3d')
#        scatter = ax.scatter3D(X, Y,Z, c =N, cmap = "hot", alpha = 0.5)
#        fig.colorbar(scatter, shrink = 0.5, aspect = 10)
#        ax.set_title("Распределение {} функции формы".format(k))
#        plt.show()
#    return

#def form_function_for_node (x: np.array, y: np.array, z:np.array, A:np.array, number):
#    length = len(x)
#    N = np.zeros((length, length, length), float)

#    for i in range(length):
#        for j in range(length):
#            for k in range(length):
#                vec = f.fill_form_vector(x[i], y[j], z[k])
#                for m in range(10):
#                    N[i, j, k] = A[number, m]*vec[m]+N[i, j, k]
#    return N
#def graphics(A, number, label, label1, label2, label3):
    
#    x1 = np.linspace(0, 1, number) 
#    xgrid, ygrid = np.meshgrid(x1, x1)
#    fig, ax = plt.subplots()
#    cs = ax.contourf(xgrid, ygrid, F, levels = 10)
#    cbar = plt.colorbar(cs)
#    ax.set_xlabel('%s' % label1)
#    ax.set_ylabel('%s' % label2)
#    ax.set_title('%s(%s, %s) при %s = 0' % (label, label1, label2, label3)) 
#    ax.grid() 
#    plt.show()

#    return
#def shape_func(A, p, number) : 
#    x = np.linspace(0, 1, number) 
#    y = np.linspace(0, 1, number)
#    z = np.linspace(0, 1, number)
#    for i in range(number):
#        for j in range(number):
#            for k in range(number):
#                vec = f.fill_form_vector(x[i], y[i], z[i])
#                for m in range (len(A)):
#                    n[m] = A[p, m] * vec[m] 
#                N[i, j, k] = np.sum(n, axis = 0)
#    return N
