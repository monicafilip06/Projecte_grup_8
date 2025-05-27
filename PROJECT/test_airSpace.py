from airSpace import *

# Creamos la base de datos de Cat
airSpace = AirSpace()
air_space = airSpace.buildAirSpace("Cat")

# Añadimos los SID y los STAR de cada aeropuerto.
air_space.addSID("LEBL", "BCN.D")
air_space.addSTAR("LEZG", "ZAR.A")

G = air_space.buildAirGraph()

# Hacemos el plot general de grafo
G.plot()

# Hcaemos el plot de un nodo
G.plotNode("GODOX")

# Para buscar el shortest path cogemos dos aeropuertos primero
nameOrg = "LEBL"  # Airport name
nameDst = "LEZG"  # Airport name

# De cada aeropuerto buscamos su SID y STAR
SID_nameOrg = air_space.getSID(nameOrg)
STAR_nameDst = air_space.getSTAR(nameDst)

# Hacemos el plot con plotPath i buscamos el shortest path con la función findShortestPath
if SID_nameOrg and STAR_nameDst:
    path, cost = G.findShortestPath(SID_nameOrg, STAR_nameDst)
    if path:
        print("Path found:", path)
        print("Cost:", cost)
        G.plotPath(path)
    else:
        print("No path found between", SID_nameOrg, "and", STAR_nameDst)
else:
    print("SID or STAR not found for the given airports.")

