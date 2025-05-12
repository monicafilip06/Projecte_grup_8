from airSpace import *
try:
    # Función para hacer un menú del proyecto donde el usuario puede elegir alguna de las opciones
    def menu():
        while True:
            print("1. Load simple graph")
            print("2. Plot Graph")
            print("3. Plot node")
            print("4. Plot path")
            print("5. Plot min path")
            print("-------------------------------------------------------------")
            print("6. Load airspace")
            print("7. List airports")
            print("8. Create airports.kml")
            print("9. Create segments.kml")
            print("10. Create route.kml")
            print("11. Find a route between 2 airports and save it in a file")
            print("-------------------------------------------------------------")
            print("12. Plot Graph of an airspace")
            print("13. Plot Node of an airspace")
            print("14. PLot min path of an airspace")
            print("-------------------------------------------------------------")
            print("0. End program")
            option = input("Option: ")
            if option.isdigit() and 0 <= int(option) <= 14:
                return int(option)
            else:
                print("Invalid option. Please enter a number between 0 and 14.")

    g = Graph()
    p = Path()
    air = AirSpace()

    # Crea un grafo de ejemplo con nodos y segmentos
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
    airspace_loaded = False
    airSpace_name = ""
    while option != 0:
        option = menu()
        if option == 1:
            # Crea un grafo de ejemplo con nodos y segmentos
            g = crearGrafoEjemplo()
            grafoEjemplo_loaded = True
        elif option == 2:
            # Dibuja el grafo
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                g.plot()
        elif option == 3:
            # Dibuja un nodo específico del grafo
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
            else:
                node_name = input("Node name: ")
                node_names = [node.name for node in g.nodes]
                if node_name not in node_names:
                    print("Error: The node name is not valid.")
                else:
                    g.plotNode(node_name)
        elif option == 4:
            # Trazar un camino y luego dibujarlo, cada vez que eliges la opción vas añadiendo nodos para hacer el path.
            # Si el nodo que añades no está conectado con el último no se dibuja.
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
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
                p.plotPath(g)
        elif option == 5:
            # Encontrar el camino más corto entre dos nodos y luego dibujarlo
            if not grafoEjemplo_loaded:
                print("El grafo de ejemplo no està cargado aún, haz la opción 1")
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
        elif option == 6:
            # Cargar un airSpace
            airSpace_name = input("AirSpace name: ")
            if airSpace_name == "Cat" or airSpace_name == "ECAC" or airSpace_name == "Spain":
                air = air.buildAirSpace(airSpace_name)
                airspace_loaded = True
                print("AirSpace loaded.")
            else:
                print("Couldn't load AirSpace.")
        elif option == 7:
            # Listar aeropuertos del airSpace cargado
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                filename = f"{airSpace_name}_aer.txt"
                try:
                    with open(filename, 'r') as f:
                        lines = f.readlines()
                    i = 0
                    listAirports = []
                    while i < len(lines):
                        airport_name = lines[i].strip()
                        listAirports.append(airport_name)
                        i += 3  # Skip SIDs and STARs for this function
                    print("Airports:", listAirports)
                except FileNotFoundError:
                    print(f"File {filename} not found.")
        elif option == 8:
            # Crear un archivo KML de aeropuertos con sus SIDs y STARs
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                kml_filename = input("Output KML file name: ")
                air.airportsToKML(kml_filename)
                print(f"Airports KML file created: {kml_filename}")
                print("Para ver el archivo poner opción 0 y elegir el archivo que se ha generado dentro de la carpeta PROJECT.")
                print("Para ver en goggle Earth subir manualmente desde goggle Earth en internet, importar archivos KML.")
        elif option == 9:
            # Crear un archivo KML de todos los segmentos del airSpace
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                route_filename = input("Output route KML file name: ")
                air.pathToKML(route_filename)
                print(f"Airports KML file created: {route_filename}")
                print("Para ver el archivo poner opción 0 y elegir el archivo que se ha generado dentro de la carpeta PROJECT.")
                print("Para ver en goggle Earth subir manualmente desde goggle Earth en internet, importar archivos KML.")
        elif option == 10:
            # Crear un archivo KML del shortestPath entre dos aeropuertos
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                nameOrg = input("Origin airport name: ")
                nameDst = input("Destination airport name: ")
                path_filename = input("Output route text file name: ")
                air.pathBetweenAirportsToKML(nameOrg, nameDst, path_filename)
                print("Para ver el archivo poner opción 0 y elegir el archivo que se ha generado dentro de la carpeta PROJECT.")
                print("Para ver en goggle Earth subir manualmente desde goggle Earth en internet, importar archivos KML.")
        elif option == 11:
            # Encontrar el shortestPath entre dos aeropuertos y guardarla en un fichero
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                nameOrg = input("Origin airport name: ")
                nameDst = input("Destination airport name: ")
                route_filename = input("Output route text file name: ")
                air.AirSpaceRouting(nameOrg, nameDst, route_filename)
        elif option == 12:
            # Trazar el grafo del airSpace
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                G = air.buildAirGraph()
                G.plot()
        elif option == 13:
            # Trazar el grafo de un nodo del airSpace
            point_name = input("SID or STAR name: ")
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                point_names = [point.name for point in air.points]
                if point_name not in point_names:
                    print("Error: The SID or STAR name is not valid.")
                else:
                    G = air.buildAirGraph()
                    G.plotNode(point_name)
        elif option == 14:
            # Trazar el shortestpath entre dos aeropuertos del airSpace
            airport1 = input("Name of origin Airport: ")
            airport2 = input("Name of Destination Airport: ")
            if not airspace_loaded:
                print("Airspace wasn't loaded.")
            else:
                airport_names = [airport.name for airport in air.airports]
                if airport1 not in airport_names or airport2 not in airport_names:
                    print("Error: One or both airport names are not valid or Airspace wasn't loaded.")
                else:
                    SID_nameOrg = air.getSID(airport1)
                    STAR_nameDst = air.getSTAR(airport2)
                    if SID_nameOrg and STAR_nameDst:
                        G = air.buildAirGraph()
                        path, cost = G.findShortestPath(SID_nameOrg, STAR_nameDst)
                        if path:
                            print("Path found:", path)
                            print("Cost:", cost)
                            G.plotPath(path)
                        else:
                            print("No path found between", SID_nameOrg, "and", STAR_nameDst)
                    else:
                        print("SID or STAR not found for the given airports.")
    print("Program ended.")
except ValueError:
    print("Error: Data was in the wrong format.")
