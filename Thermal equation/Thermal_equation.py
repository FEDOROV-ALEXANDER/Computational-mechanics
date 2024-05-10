import numpy as np
import pandas as pd
from openpyxl.workbook import Workbook
import meshio
import data_helper as dh
T_water = 5
T_air = 25
#transcalency1 = 1.5
#transcalency2 = 1.75

#elements = np.loadtxt("elements.txt", dtype=int, comments="#", delimiter=",", 
#unpack=False)
#nodes = np.loadtxt("nodes.txt", dtype=float, comments="#", delimiter=",", 
#unpack=False)
#nodes_water = np.loadtxt("nodes_water.txt", dtype=int, comments="#", 
#delimiter=",", unpack=False)
#nodes_air = np.loadtxt("nodes_air.txt", dtype=int, comments="#", delimiter=",", 
#unpack=False)



nodes, elements, nodes_air, nodes_water,indexes1, indexes2, transcalency1, transcalency2= dh.input("Thermal.inp")


elements1 = np.arange(indexes1(0), indexes1(1), indexes1(2))
elements2 = np.arange(indexes2(0), indexes2(1), indexes2(2))

materials = {
 "array": [elements1, elements2],
 "property": [transcalency1, transcalency2]
}
boundary = {
 "array": [nodes_water, nodes_air],
 "property": [T_water, T_air]
}
n_el = len(elements)
n_nod = len(nodes)
n_mat = len(materials["array"])
n_bound = len(boundary["array"])
j = np.array([[-1, 0, 1], [-1, 1, 0]])
j1 = np.array([-1, -1])
j2 = np.array([0, 1])
j3 = np.array([1, 0])
K = np.zeros((n_nod, n_nod))
for i in range(n_mat):
     for element in materials["array"][i]:
         nod = elements[element - 1][1:4]
         coord = np.array([nodes[nod[0] - 1][1:3], nodes[nod[1] - 1][1:3], 
        nodes[nod[2] - 1][1:3]])
         J = j @ coord
         J_inv = np.linalg.inv(J)
         B = np.array([J_inv @ j1, J_inv @ j2, J_inv @ j3])
         k = 0.5 * materials["property"][i] * np.linalg.det(J) * B @ B.T
         sub = [nod[0] - 1, nod[1] - 1, nod[2] - 1]
         K[np.ix_(sub, sub)] += k
R = np.zeros(n_nod)
for i in range(n_bound):
     T_b = boundary["property"][i]
     for node in boundary["array"][i]:
         nod = node - 1
         K[nod][:] = 0
         K[:][nod] = 0
         K[nod][nod] = 1
         R[nod] = T_b
T = np.linalg.solve(K, R)
df = pd.DataFrame(T)
df.to_excel('T.xlsx', index=False)
nod = nodes[np.ix_(np.arange(0, n_nod, 1), np.arange(1, 3, 1))]
element = elements[np.ix_(np.arange(0, n_el, 1), np.arange(1, 4, 1))] - 1
cells = [('triangle', np.array(element))]
point_data = {"temperature": T.reshape(-1,1)}
mesh = meshio.Mesh(nod, cells, point_data=point_data)
meshio.write('temp.vtk', mesh, file_format ='vtk')