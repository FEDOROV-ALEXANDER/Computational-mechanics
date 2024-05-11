import numpy as np
import pandas as pd

#� ���� ����� � ������ �������� ��� ��������� � ����� ��������
def input(file_name):
	transcalency1 = found_string('*Material, name=B20', file_name) +1
	transcalency2 = found_string('*Material, name=B30', file_name) +1
	first_node = found_string('*Node', file_name)
	first_element = found_string('*Element, type=', file_name)
	second_element = found_string('*Nset, nset', file_name) - 1
	first_node_material = found_string('*Elset, elset=B20, generate', file_name) 
	second_node_material = found_string('*Elset, elset=B30, generate', file_name)  
	nodes_air = found_string('*Nset, nset=AIR',file_name) 
	nodes_water  = found_string('*Nset, nset=WATER',file_name)
	print(first_node, first_element, first_node_material, second_node_material, nodes_air, nodes_water)
	nodes = np.array(read_diapazone_from_file(file_name, first_node, first_element - 1))
	elements = np.array(read_diapazone_from_file(file_name, first_element, second_element))
	nodes_air = np.array(read_diapazone_from_file(file_name, nodes_air,  nodes_air+1))
	nodes_water = np.array(read_diapazone_from_file(file_name, nodes_water,  nodes_water+1))
	elements1 = np.array(read_diapazone_from_file(file_name, first_node_material,  first_node_material+1))
	elements2 = np.array(read_diapazone_from_file(file_name, second_node_material,  second_node_material+1))
	transcalency1 = read_diapazone_from_file(file_name, transcalency1, transcalency1 + 1)
	transcalency2 = read_diapazone_from_file(file_name, transcalency2, transcalency2 + 1)
	print(elements1[0])

	return nodes, elements, nodes_air, nodes_water, elements1, elements2, transcalency1, transcalency2
def found_string(search_string, file_name):
	with open(file_name) as f:
		n = 0
		for line in f:
			n += 1
			if search_string in line:
				break
	return n
search_string = '*Node'

def read_diapazone_from_file(file_name, first, last):
	lines = []
	with open(file_name) as f:
		for i, line in enumerate(f):
			if ((i >= first) and (i < last)):
				lines.append(line.strip())
	return lines

nodes, elements, nodes_air, nodes_water, elements1, elements2, transcalency1, transcalency2 = input("Thermal.inp")