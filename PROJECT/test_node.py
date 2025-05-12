from node import *
print("Probando nodo...")

n1 = Node("A", 1, 20)
n2 = Node("B", 8, 17)
n3 = Node("C", 15, 20)

# Añadir nodos n1 y n2 como vecinos del nodo n3
n3.addNeighbor(n1)
n3.addNeighbor(n2)

# Obtener los nombres de los vecinos del nodo n3
neighbor_names = [n.name for n in n3.neighbors]

# Imprimir la información del nodo n3, incluyendo su nombre, coordenadas y vecinos
print("Node n3: ")
print("Node Name:", n3.name, " Coordinate X:", n3.x, " Coordiante Y:", n3.y, " Neighbors:{}".format(neighbor_names))
print("OK")
