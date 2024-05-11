import numpy as np
import pandas as pd
import meshio


properties = {
     "name": ["concrete20", "concrete30", "rock"],
     "density": [2500, 2500, 0],
     "Young's modulus": [27500e6, 32500e6, 2.3e10],
     "Poisson's ratio": [0.14, 0.14, 0.25]
}
density_water = 1000
depth = 130
g = 9.8
elements = np.loadtxt("el.txt", dtype=int, comments="#", delimiter=",", unpack=False)
nodes = np.loadtxt("nodes.txt", dtype=float, comments="#", delimiter=",", unpack=False)

el_concrete20 = np.arange(409, 432, 1)
el_concrete_30 = np.arange(366, 408, 1)
el_rock = np.arange(1, 365, 1)

bcs_x = np.loadtxt("bcs_x.txt", dtype=int, comments="#", delimiter=",", unpack=False)
bcs_y = np.loadtxt("bcs_y.txt", dtype=int, comments="#", delimiter=",", unpack=False)

npu_x = np.loadtxt("npu_x.txt", dtype=int, comments="#", delimiter=",", unpack=False)
npu_y = np.loadtxt("npu_y.txt", dtype=int, comments="#", delimiter=",", unpack=False)

materials = [el_concrete20, el_concrete_30, el_rock]
n_el = len(elements)
n_nod = len(nodes)
n_mat = len(materials)
j = np.array([[-1, 0, 1], [-1, 1, 0]])
j1 = np.array([-1, -1])
j2 = np.array([0, 1])
j3 = np.array([1, 0])
K = np.zeros((2 * n_nod, 2 * n_nod))

for i in range(n_mat):
     E = properties["Young's modulus"][i]
     nu = properties["Poisson's ratio"][i]
     D = E * (1 - nu) * np.array([[1, nu / (1 - nu), 0], [nu / (1 - nu), 1, 0], 
[0, 0, (1 - 2 * nu) / (2 - 2 * nu)]]) / ((1 + nu) * (1 - 2 * nu))
     for element in materials[i]:
         nod = elements[element - 1][1:4]
         coord = np.array([nodes[nod[0] - 1][1:3], nodes[nod[1] - 1][1:3], 
nodes[nod[2] - 1][1:3]])
         J = j @ coord
         J_inv = np.linalg.inv(J)
         dN_1 = J_inv @ j1
         dN_2 = J_inv @ j2
         dN_3 = J_inv @ j3
         B = np.array([[dN_1[0], 0, dN_2[0], 0, dN_3[0], 0], [0, dN_1[1], 0, 
dN_2[1], 0, dN_3[1]], [dN_1[1], dN_1[0], dN_2[1], dN_2[0], dN_3[1], dN_3[0]]])
         k = 0.5 * np.abs(np.linalg.det(J)) * B.T @ D @ B
         sub = [2 * nod[0] - 2, 2 * nod[0] - 1, 2 * nod[1] - 2, 2 * nod[1] - 1, 2 
* nod[2] - 2, 2 * nod[2] - 1]
         K[np.ix_(sub, sub)] += k
F = np.zeros(2 * n_nod)


for i in range(n_mat - 1):
     p = -properties["density"][i] * g
     P = np.array([0, p, 0, p, 0, p])
     for element in materials[i]:
         nod = elements[element - 1][1:4]
         coord = np.array([nodes[nod[0] - 1][1:3], nodes[nod[1] - 1][1:3], 
nodes[nod[2] - 1][1:3]])
         J = j @ coord
         f = np.abs(np.linalg.det(J)) * P / 6
         sub = [2 * nod[0] - 2, 2 * nod[0] - 1, 2 * nod[1] - 2, 2 * nod[1] - 1, 2 
* nod[2] - 2, 2 * nod[2] - 1]
         F[sub] += f
         
side_id = [[1, 2], [2, 3], [3, 1]]
p = -density_water * g * depth
P = np.array([0, p, 0, p])
for element in npu_y:
     nod = elements[element[0] - 1][side_id[element[1] - 1]]
     coord = np.array([nodes[nod[0] - 1][1], nodes[nod[1] - 1][1]])
     length = np.abs(coord[0] - coord[1])
     f = length * P / 2
     sub = [2 * nod[0] - 2, 2 * nod[0] - 1, 2 * nod[1] - 2, 2 * nod[1] - 1]
     F[sub] += f
     
def pressure(y):
     return density_water * g * (depth - y)

for element in npu_x:
     nod = elements[element[0] - 1][side_id[element[1] - 1]]
     coord = np.array([nodes[nod[0] - 1][2], nodes[nod[1] - 1][2]])
     length = np.abs(coord[0] - coord[1])
     p1 = pressure(coord[1])
     p2 = pressure(coord[0])
     f = length * np.array([p1 / 6 + p2 / 3, 0, p1 / 3 + p2 / 6, 0])
     sub = [2 * nod[0] - 2, 2 * nod[0] - 1, 2 * nod[1] - 2, 2 * nod[1] - 1]
     F[sub] += f
     
for node in bcs_x:
     K[2 * node - 2][:] = 0
     K[:][2 * node - 2] = 0
     K[2 * node - 2][2 * node - 2] = 1
     
for node in bcs_y:
     K[2 * node - 1][:] = 0
     K[:][2 * node - 1] = 0
     K[2 * node - 1][2 * node - 1] = 1
     
U = np.linalg.solve(K, F)
Deform = np.zeros(3 * n_el)
Stress = np.zeros(3 * n_el)
for i in range(n_mat):
     E = properties["Young's modulus"][i]
     nu = properties["Poisson's ratio"][i]
     D = E * (1 - nu) * np.array([[1, nu / (1 - nu), 0], [nu / (1 - nu), 1, 0], 
[0, 0, (1 - 2 * nu) / (2 - 2 * nu)]]) / ((1 + nu) * (1 - 2 * nu))
     
     for element in materials[i]:
         nod = elements[element - 1][1:4]
         coord = np.array([nodes[nod[0] - 1][1:3], nodes[nod[1] - 1][1:3], nodes[nod[2] - 1][1:3]])
         J = j @ coord
         J_inv = np.linalg.inv(J)
         dN_1 = J_inv @ j1
         dN_2 = J_inv @ j2
         dN_3 = J_inv @ j3
         B = np.array([[dN_1[0], 0, dN_2[0], 0, dN_3[0], 0], [0, dN_1[1], 0, 
dN_2[1], 0, dN_3[1]], [dN_1[1], dN_1[0], dN_2[1], dN_2[0], dN_3[1], dN_3[0]]])
         sub = [2 * nod[0] - 2, 2 * nod[0] - 1, 2 * nod[1] - 2, 2 * nod[1] - 1, 2 * nod[2] - 2, 2 * nod[2] - 1]
         u = U[sub]
         d = B @ u
         s = D @ d
         sub = [3 * element - 3, 3 * element - 2, 3 * element - 1]
         Deform[sub] = d
         Stress[sub] = s
     

U_x = []
U_y = []

for i in range(len(U)):
     if i%2 == 0:
         U_x.append(U[i])
     else:
         U_y.append(U[i])
         
data1 = pd.DataFrame(U_x)
data2 = pd.DataFrame(U_y)
writer = pd.ExcelWriter('results.xlsx')
data1.to_excel(writer, 'page_1', float_format='%.5f')
data2.to_excel(writer, 'page_2', float_format='%.5f')
writer.close()
nod = nodes[np.ix_(np.arange(0, n_nod, 1), np.arange(1, 3, 1))]
element = elements[np.ix_(np.arange(0, n_el, 1), np.arange(1, 4, 1))] - 1
cells = [('triangle', np.array(element))]
point_data = {"U_x": U_x}
mesh = meshio.Mesh(nod, cells, point_data=point_data)
meshio.write("U_x.vtk", mesh, file_format='vtk')
point_data = {"U_y": U_y}
mesh = meshio.Mesh(nod, cells, point_data=point_data)
meshio.write("U_y.vtk", mesh, file_format='vtk')
cell_data = {"S11": [Stress[0:-1:3]]}
mesh = meshio.Mesh(nod, cells, cell_data=cell_data)
meshio.write("S11.vtk", mesh, file_format='vtk')
cell_data = {"S22": [Stress[1:-1:3]]}
mesh = meshio.Mesh(nod, cells, cell_data=cell_data)
meshio.write("S22.vtk", mesh, file_format='vtk')
cell_data = {"E11": [Deform[0:-1:3]]}
mesh = meshio.Mesh(nod, cells, cell_data=cell_data)
meshio.write("E11.vtk", mesh, file_format='vtk')
cell_data = {"E22": [Deform[1:-1:3]]}
mesh = meshio.Mesh(nod, cells, cell_data=cell_data)
meshio.write("E22.vtk", mesh, file_format='vtk')
