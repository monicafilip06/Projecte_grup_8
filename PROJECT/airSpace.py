from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
#Importa todo lo que esté definido en el módulo node
from node import *
from graph import *
from path import findShortestPath
import simplekml # Importamos la libreria de simplekml para hacer algunas funciones que se tienen que crear archivos kml
class AirSpace:
  def __init__(self):
      self.points = []  # Lista de NavPoints donde se almacenan los puntos de navegación 
      self.segments = []  # Lista de NavSegments
      self.airports = []  # Lista de NavAirports

  # Función para añadir un punto de NavPoints
  def addPoint(self, point):
      self.points.append(point) # Añade un objeto NavPoint a la lista de puntos
 
  # Función para añadir un segmento entre dos puntos
  def addSegment(self, numOrig, numDst, distance):
    #Inicializa variables para guardar el punto de origen y destino.
      orig_point = None
      dst_point = None
    #Busca entre los puntos cuál tiene el número de origen y destino
      for point in self.points:
          if point.num == numOrig:
              orig_point = point
          elif point.num == numDst:
              dst_point = point
          if orig_point and dst_point:
              #si los encuentra rompe el bucle
              break
      #Si se encontraron ambos puntos, se crea un nuevo segmento y se guarda en self.segments
      if orig_point and dst_point:
          segment = NavSegment(orig_point, dst_point, distance)
          self.segments.append(segment)
      else:
          print("Error: Uno o los dos puntos indicados no existen.")

  # Función para añadir un aeropuerto con sus respectivos SID y STAR
  def addAirport(self, name, SID, STAR):
      airport = NavAirport(name)     # Crea el aeropuerto con su nombre
      airport.SID.append(SID)        # Añade un SID a su lista
      airport.STAR.append(STAR)      # Añade un STAR a su lista
      self.airports.append(airport)  # Añade el aeropuerto a la lista general

  # Función para añadir un SID a un aeropuerto específico
  def addSID(self, nameAirport, nameSID):
      for airport in self.airports:
          if airport.name == nameAirport:
              airport.SID.append(nameSID)
              break
      else:
          print("Error: Airport no encontrado.")

  # Función para añadir un STAR a un aeropuerto específico
  def addSTAR(self, nameAirport, nameSTAR):
      for airport in self.airports:
          if airport.name == nameAirport:
              airport.STAR.append(nameSTAR)
              break
      else:
          print("Error: Airport no encontrado.")

  # Función para cargar NavPoints desde un archivo
  def loadNavPoints(self, filename):
      try:
          #Usa with para que el archivo se cierre automáticamente después de usarlo.
          with open(filename, 'r') as file:
              for line in file:
                  data = line.strip().split()
                  #Si hay exactamente 4 elementos, se guardan en variables.
                  if len(data) == 4:
                      num, name, lat, lon = data
                      point = NavPoint(int(num), name, float(lat), float(lon))
                      self.addPoint(point)
                  #si no tiene 4 elementos
                  else:
                      print(f"Error: Datos inválidos de la línea: {line}")
      except FileNotFoundError:
          print("Error: Fichero no encontrado.")

  # Función para cargar segmentos desde un archivo
  def loadSegments(self, filename):
      try:
          with open(filename, 'r') as file:
              for line in file:
                  data = line.strip().split()
                  if len(data) == 3:
                      numOrig, numDst, distance = data
                      self.addSegment(int(numOrig), int(numDst), float(distance))
                  else:
                      print(f"Error: Datos inválidos de la línea: {line}")
      except FileNotFoundError:
          print("Error: Fichero no encontrado.")

  # Función para cargar aeropuertos desde un archivo
  def loadAirports(self, filename):
      try:
          with open(filename, 'r') as file:
              #lee todas las líneas de golpe usando readlines().
              lines = file.readlines()
            #Recorre las líneas de 3 en 3, porque cada aeropuerto está definido por 3 líneas
              for i in range(0, len(lines), 3):
                #Verifica que haya suficientes líneas
                #Limpia cada línea (quita saltos de línea y espacios)
                  if i + 2 < len(lines):
                      name = lines[i].strip()
                      sid = lines[i + 1].strip()
                      star = lines[i + 2].strip()
                      self.addAirport(name, sid, star)
                  else:
                      print(f"Error: Datos incompletos en líneas: {i + 1}")
      except FileNotFoundError:
          print("Error: Fichero no enocntrado.")

  # Método para construir el AirSpace a partir de archivos
  def buildAirSpace(air, filename):
    #Toma un filename base y construye los nombres de archivo
      nav_filename = filename+"_nav.txt"
      seg_filename = filename+"_seg.txt"
      aer_filename = filename+"_aer.txt"
    #Llama a los tres métodos de carga anteriores para construir el espacio aéreo completo
      air.loadNavPoints(nav_filename)
      air.loadSegments(seg_filename)
      air.loadAirports(aer_filename)
      return air

  # Función para construir el grafo del AirSpace
  def buildAirGraph(air):
    #Se crea un objeto Graph() vacío donde se irán añadiendo nodos y segmentos
      graph = Graph()
      # Primero añadimos todos los puntos convirtiendolos en nodos
      for point in air.points:
          node = Node(point.name, point.lon, point.lat)
          graph.nodes.append(node)
      # Segundo recorre todos los segmentos
      for segment in air.segments:
        #Inicializa los nodos origen y destino 
          orig_node = None
          dst_node = None
        #Busca en los nodos del grafo cuáles corresponden al origen y destino del segmento
          for node in graph.nodes:
              if node.name == segment.orig.name:
                  orig_node = node
              elif node.name == segment.dst.name:
                  dst_node = node
              #Si se encontraron ambos nodos, se crea un Segment 
          if orig_node and dst_node:
              new_segment = Segment(orig_node, dst_node, segment.dist)
              graph.segments.append(new_segment)
      return graph

  # Función para poner todos los aeropuertos con sus coordenadas en un archivo KML para ejecutar goggleEarth
  def airportsToKML(air, nomFile):
    #Crea un objeto Kml usando la librería simplekml.
      kml = simplekml.Kml()
      for point in air.points:
        #Para cada punto, crea un marcador en el KML
          kml.newpoint(name=point.name, coords=[(point.lon, point.lat)])
      #Guardamos el archivo
      kml.save(f"{nomFile}.kml")
      print(f"KML fichero {nomFile}.kml creado.")

  # Función para poner todos los segmentos con sus coordenadas en un archivo KML para ejecutar goggleEarth
  def pathToKML(path, nomFile):
    #Crea un objeto Kml usando la librería simplekml.
      kml = simplekml.Kml()
      for segment in path.segments:
          name = f"Segment {segment.orig.name} - {segment.dst.name}"
          coords = [(segment.orig.lon, segment.orig.lat), (segment.dst.lon, segment.dst.lat)]
          #Añade una línea al archivo KML que conecta esos dos puntos
          kml.newlinestring(name=name, coords=coords)
      kml.save(f"{nomFile}.kml")
      print(f"KML fichero {nomFile}.kml creado.")

  # Función para obtener el SID de un aeropuerto
  def getSID(air, airport_name):
    #Busca en la lista de aeropuertos un aeropuerto con ese nombre
      for airport in air.airports:
          if airport.name == airport_name and airport.SID:
            #Si lo encuentra devuelve la primera SID
              return airport.SID[0]
      return None

  # Función para obtener el STAR de un aeropuerto
  def getSTAR(air, airport_name):
      for airport in air.airports:
          if airport.name == airport_name and airport.STAR:
              return airport.STAR[0]
      return None

  # Función para encontrar el shortestPath entre dos aeropuertos y guardarlo en un fichero
  def AirSpaceRouting(self, airport1, airport2, nomFile):
      # Comprobar si los nombres de los aeropuertos son válidos
      airport_names = [airport.name for airport in self.airports]
      if airport1 not in airport_names or airport2 not in airport_names:
          print("Error: Uno o los dos nombres de aeropuerto son inválidos.")
          return
      # Obtener el SID del aeropuerto de origen y el STAR del aeropuerto de destino
      SID_nameOrg = self.getSID(airport1)
      STAR_nameDst = self.getSTAR(airport2)
      if SID_nameOrg and STAR_nameDst:
          # Construir el grafo y encontrar la ruta más corta
          G = self.buildAirGraph()
          path, cost = G.findShortestPath(SID_nameOrg, STAR_nameDst)

        # si hay una ruta abre el archivo para escribir guardar la ruta y su coste
          if path:
              F = open(nomFile, 'w')
              F.write(f"Ruta de {airport1} a {airport2}\n")
              F.write(f"Path: {path}\n")
              F.write(f"Cost: {cost}\n")
              print(f"Ruta de {airport1} a {airport2} guardado en {nomFile}.")
          else:
              print("No hay path entre", SID_nameOrg, "i", STAR_nameDst)
      else:
          print("SID o STAR no encontrados para estos aeropuertos.")

  # Función para exportar a KML la ruta entre dos aeropuertos
  def pathBetweenAirportsToKML(self, origin_airport_name, destination_airport_name, nomFile):
    # Verifica que los aeropuertos existan
      airport_names = [airport.name for airport in self.airports]
      if origin_airport_name not in airport_names or destination_airport_name not in airport_names:
          print("Error: Uno o los dos nombres de aeropuerto son inválidos.")
          return
      # Obtiene SID Y STAR 
      SID_nameOrg = self.getSID(origin_airport_name)
      STAR_nameDst = self.getSTAR(destination_airport_name)
      # Construye el grafo y busca la ruta
      if SID_nameOrg and STAR_nameDst:
          G = self.buildAirGraph()
          path, cost = findShortestPath(G, SID_nameOrg, STAR_nameDst)
          # Si hay una ruta, recorre el camino paso a paso, crea líneas (LineString) entre cada
           # par de nodos consecutivos y las añade al archivo kml
          if path:
              kml = simplekml.Kml()
              for i in range(len(path) - 1):
                  n1 = G.nameNode(path[i])
                  n2 = G.nameNode(path[i + 1])
                  if n1 and n2:
                      coords = [(n1.x, n1.y), (n2.x, n2.y)]
                      kml.newlinestring(name=f"{n1.name} to {n2.name}", coords=coords)
              kml.save(f"{nomFile}.kml")
              print(f"KML fichero {nomFile}.kml creado.")
          else:
              print("No hay path entre", SID_nameOrg, "y", STAR_nameDst)
      else:
          print("SID o STAR no encontrados para estos aeropuertos.")
