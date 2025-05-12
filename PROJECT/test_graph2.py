from graph import *
from node import *
from path import *
try:
    # Función para mostrar el menú de la phase 2 y obtener la opción del usuario
    def menu():
        while True:
            print("1. Clear Path")
            print("2. Load and Plot Graph")
            print("3. Add Node to Path")
            print("4. Contain Node")
            print("5. Cost to Node")
            print("6. Cost to Destination")
            print("7. Plot Path")
            print("8. Shortest Path between two nodes of the Graph")
            print("0. End program")
            option = input("Option: ")
            if option.isdigit() and 0 <= int(option) <= 8:
                return int(option)
            else:
                print("Invalid option. Please enter a number between 0 and 8.")

    g = Graph()
    p = Path()
    # Función para crear un grafo de ejemplo con nodos y segmentos
    def crearGrafoEjemplo():
        g.addNode(Node("A", 1, 20))
        g.addNode(Node("B", 8, 17))
        g.addNode(Node("C", 15, 20))
        g.addNode(Node("D", 18, 15))
        g.addNode(Node("E", 2, 4))
        g.addNode(Node("F", 6, 5))
        g.addNode(Node("G", 12, 12))
        g.addNode(Node("H", 10, 3))
        g.addNode(Node("I", 19, 1))
        g.addNode(Node("J", 13, 5))
        g.addNode(Node("K", 3, 15))
        g.addNode(Node("L", 4, 10))
        g.addSegment("A", "B")
        g.addSegment("A", "E", bidirectional=False)
        g.addSegment("A", "K")
        g.addSegment("B", "A")
        g.addSegment("B", "C", bidirectional=False)
        g.addSegment("B", "F", bidirectional=False)
        g.addSegment("B", "K", bidirectional=False)
        g.addSegment("B", "G")
        g.addSegment("C", "D", bidirectional=False)
        g.addSegment("C", "G", bidirectional=False)
        g.addSegment("D", "G", bidirectional=False)
        g.addSegment("D", "H", bidirectional=False)
        g.addSegment("D", "I")
        g.addSegment("E", "F", bidirectional=False)
        g.addSegment("F", "L")
        g.addSegment("G", "B")
        g.addSegment("G", "F", bidirectional=False)
        g.addSegment("G", "H", bidirectional=False)
        g.addSegment("I", "D")
        g.addSegment("I", "J")
        g.addSegment("J", "I")
        g.addSegment("K", "A")
        g.addSegment("K", "L")
        g.addSegment("L", "K")
        g.addSegment("L", "F")
        return g

    option = -1
    grafoEjemplo_loaded = False
    while option != 0:
        option = menu()
        if option == 1:
            # Limpiar el path
            p.nodes = []
            p.costs = []
            p.totalCost = 0.0
            print("Path cleared.")
        elif option == 2:
            # Crear y graficar el grafo de ejemplo
            g = crearGrafoEjemplo()
            grafoEjemplo_loaded = True
            g.plot()
        elif option == 3:
            # Añadir un nodo al camino
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 2")
            else:
                node_name = input("Node name: ")
                if not p.nodes:
                    p.addNode(g, node_name)
                else:
                    neighbor_node = g.nameNode(node_name)
                    last_node = p.nodes[-1]
                    if neighbor_node in last_node.neighbors:
                        p.addNode(g, node_name)
                    else:
                        print(f"Node {node_name} is not connected to the last node")
        elif option == 4:
            # Verificar si el camino contiene un nodo específico
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 2")
            else:
                node_name = input("Node name: ")
                p.containsNode(node_name)
        elif option == 5:
            # Obtener el costo hasta un nodo específico
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 2")
            else:
                node_name = input("Node name: ")
                cost = p.getCostToNode(node_name)
                if cost != -1:
                    print("Cost to node {}: {}".format(node_name, cost))
                else:
                    print("Error: Node {} does not exist in the path.".format(node_name))
        elif option == 6:
            # Obtener el costo aproximado hasta el nodo de destino desde el último nodo
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 2")
            else:
                dest_node_name = input("Destination node name: ")
                cost = p.getApproxToDest(g, dest_node_name)
                if cost != -1:
                    print("Cost to Destination from last node: {}".format(cost))
                else:
                    print("Error: Destination node not found.")
        elif option == 7:
            # Graficar el path actual después de ya previamente haber añadido nodos dentro del path con la opción 3
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 2")
            else:
                p.plotPath(g)
        elif option == 8:
            # Encontrar el shortestPath entre dos nodos del grafo y hacer el plot
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 2")
            else:
                nameOrg = input("Origin node name: ")
                nameDst = input("Destination node name: ")
                path, cost = g.findShortestPath(nameOrg, nameDst)
                if path:
                    print("Path found:", path)
                    print("Cost:", cost)
                    g.plotPath(path)
                else:
                    print("No path found between", nameOrg, "and", nameDst)
    print("Program ended.")
except ValueError:
    print("Error: Data was in the wrong format.")
