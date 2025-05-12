from node import *
from segment import *

n1 = Node("A", 1, 20)
n2 = Node("B", 8, 17)
n3 = Node("C", 15, 20)

# Crear segmentos entre los nodos
segment1 = Segment(n1, n2)
segment2 = Segment(n2, n3)

print("Segment 1 distance:", segment1.cost)
print("Segment 2 distance:", segment2.cost)

# Obtener los nombres de los vecinos del nodo n1 y nodo n2
neighbor_names_n1 = [neighbor.name for neighbor in n1.neighbors]
neighbor_names_n2 = [neighbor.name for neighbor in n2.neighbors]

print("Neighbors of node 1:", neighbor_names_n1)
print("Neighbors of node 2:", neighbor_names_n2)
