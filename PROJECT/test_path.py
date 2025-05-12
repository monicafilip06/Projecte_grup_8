from graph import *
from node import *

print("Path empty:")
# Crear path vacío
path_empty = Path()
# Imprimir el costo total del path vacío
print("{} ->".format(path_empty.totalCost))

# Indicando que se está probando con un camino con un solo nodo
print("Path with one Node:")
g = Graph()
g.addNode(Node("B", 8, 17))
p = Path()
p.addNode(g, "B")
print("{} -> {}".format(p.totalCost, p.nodes))

# Indicando que se está probando con un camino con más de un nodo
print("Path with more than one Node:")
g.addNode(Node("C", 15, 20))
g.addNode(Node("G", 12, 12))
p.addNode(g, "C")
p.addNode(g, "G")
g.addSegment("B", "C")
g.addSegment("C", "G")
print("{} -> {}".format(p.totalCost, p.nodes))

# Indicando que se está probando el error de agregar un nodo ya existente en el camino
print("Error: Node already exists in the Path:")
# Intentar añadir el nodo "B" al camino y comprobar si falla
if not p.addNode(g, "B"):
    print("Error in pathAddNode: Node B already exists in path")

# Indicando que se está probando el error de no poder añadir un nodo al camino
print("Error: Not able to add node B to path:")
# Intentar añadir el nodo "B" al camino nuevamente y comprobar si falla
if not p.addNode(g, "B"):
    print("Error: Not able to add node B to path")
