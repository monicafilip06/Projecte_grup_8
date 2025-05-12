from graph import *
from node import *

try:
    # Función para mostrar el menú de la phase 1 y obtener la opción del usuario
    def menu():
        while True:
            print("1. Load the initial Graph")
            print("2. Add a Node to the Graph")
            print("3. Add a new Segment to the Graph")
            print("4. Add a Segment between two existing nodes in the Graph")
            print("5. Plot Graph")
            print("6. Plot Node")
            print("0. End program")
            option = input("Option: ")
            if option.isdigit() and 0 <= int(option) <= 6:
                return int(option)
            else:
                print("Invalid option. Please enter a number between 0 and 6.")


    g = Graph()
    # Función para crear un grafo de ejemplo con nodos y segmentos
    def crearGrafoEjemplo ():
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
        g.addSegment("A", "E")
        g.addSegment("A", "K")
        g.addSegment("B", "A")
        g.addSegment("B", "C")
        g.addSegment("B", "F")
        g.addSegment("B", "K")
        g.addSegment("B", "G")
        g.addSegment("C", "D")
        g.addSegment("C", "G")
        g.addSegment("D", "G")
        g.addSegment("D", "H")
        g.addSegment("D", "I")
        g.addSegment("E", "F")
        g.addSegment("F", "L")
        g.addSegment("G", "B")
        g.addSegment("G", "F")
        g.addSegment("G", "H")
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
            g = crearGrafoEjemplo()
            grafoEjemplo_loaded = True
        elif option == 2:
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                n1 = input("Name:")
                if not any(node.name == n1 for node in g.nodes):
                    x = float(input("Coordinate X:"))
                    y = float(input("Coordiante Y:"))
                    g.addNode(Node(n1, x, y))
                    g.plot()
                else:
                    print("Node {} is already in the Graph.".format(n1))
        elif option == 3:
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                n1 = input("Origin node name that already exists in the Graph: ")
                if not any(node.name == n1 for node in g.nodes):
                    print("Error: Origin Node {} not found in the Graph.".format(n1))
                else:
                    n2 = input("Destination node name that doesn't exist in the Graph:")
                    if not any(node.name == n2 for node in g.nodes):
                        x = float(input("Coordinate X:"))
                        y = float(input("Coordiante Y:"))
                        g.addNode(Node(n2, x, y))
                        g.addSegment(n1, n2)
                        g.plot()
                    else:
                        print("Destination node {} already exists in the Graph".format(n2))
        elif option == 4:
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                n1 = input("Origin node name that already exists in the Graph: ")
                if not any(node.name == n1 for node in g.nodes):
                    print("Error: Origin node {} not found in the Graph.".format(n1))
                else:
                    n2 = input("Destination node name that already exists in the Graph: ")
                    if not any(node.name == n2 for node in g.nodes):
                        print("Error: Destination node {} not found in the Graph.".format(n2))
                    else:
                        g.addSegment(n1, n2)
                        g.plot()
        elif option == 5:
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                g.plot()
        elif option == 6:
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                node_name = input("Node name that already exists in the Graph: ")
                if not any(node.name == node_name for node in g.nodes):
                    print("Error: Node {} not found in the Graph.".format(node_name))
                else:
                    g.plotNode(node_name)
    print("Program ended.")
except ValueError:
    print("Error: Data was in the wrong format.")
