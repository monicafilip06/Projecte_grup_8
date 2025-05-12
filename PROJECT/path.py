import matplotlib.pyplot as plt


class Path:
    # Iniciamos una clase Path definida con vectores vacíos de nodos, costes y costes totales
    def __init__(self):
        self.nodes = []
        self.costs = []
        self.totalCost = 0.0

    def addNode(P, G, name):
        # Añade un nodo al camino. Verifica si el nodo existe en el grafo G y si no está ya en el camino P.
        # Si el nodo puede añadirse, se actualiza el costo total y se agrega el nodo al camino.
        if not any(node.name == name for node in G.nodes):
            print("Error: Node {} does not exist in the graph.".format(name))
            return True
        else:
            n1 = G.nodes[-1]
            n2 = G.nameNode(n1.name)
            if n2 and n2.addNeighbor(G.nameNode(name)):
                distance = n1.distance(G.nameNode(name))
                P.nodes.append(G.nameNode(name))
                P.totalCost += distance
                print("Node {} added to path.".format(name))
                return True
            else:
                return False

    def containsNode(P, name):
        # Comprueba si un nodo con el nombre dado ya está en el camino P.
        # Devuelve True si el nodo está en el camino, de lo contrario devuelve False.
        if not any(node.name == name for node in P.nodes):
            print("Node {} is not in the path.".format(name))
            return False
        else:
            print("Node {} is in the path.".format(name))
            return True

    def getCostToNode(P, name):
        # Calcula el costo total para llegar a un nodo específico en el camino P.
        # Devuelve el costo total si el nodo se encuentra en el camino, de lo contrario devuelve -1.
        i = 0
        found = False
        while i < len(P.nodes) and not found:
            if P.nodes[i].name == name:
                found = True
            else:
                i += 1
        if found:
            totalCost = 0
            position = i
            n = 0
            while n < i:
                d = P.nodes[n].distance(P.nodes[n + 1])
                totalCost = totalCost + d
                n += 1
            return totalCost
        if not found:
            return -1

    def getApproxToDest(P, G, name):
        # Obtiene una distancia aproximada desde el último nodo en el camino hasta el nodo con el nombre dado.
        # Devuelve la distancia si el nodo se encuentra en el grafo, de lo contrario devuelve -1.
        for node in P.nodes:
            if node.name == name:
                last_node = P.nodes[-1]
                return last_node.distance(node)
        return -1

    def plotPath(P, G):
        # Dibuja el camino en el grafo utilizando matplotlib.
        # Los nodos en el camino se representan con puntos negros, y los nodos no en el camino con puntos rojos.
        for i in range(len(P.nodes) - 1):
            n1 = P.nodes[i]
            n2 = P.nodes[i + 1]
            plt.plot([n1.x, n2.x], [n1.y, n2.y], color='cyan')
            plt.text((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, '{:.2f}'.format(n1.distance(n2)), fontsize=10)
        for node in G.nodes:
            if node in P.nodes:
                plt.plot(node.x, node.y, 'ko', markersize=6)
                plt.text(node.x, node.y, node.name)
            else:
                plt.plot(node.x, node.y, 'ro', markersize=6)
                plt.text(node.x, node.y, node.name)
        plt.xlabel('Coordinate X')
        plt.ylabel('Coordinate Y')
        plt.title('Graph with Path')
        plt.axis('equal')
        plt.grid(True)
        plt.show()

