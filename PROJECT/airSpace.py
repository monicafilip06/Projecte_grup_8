from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
from node import *
from graph import *
import simplekml # Importamos la libreria de simplekml para hacer algunas funciones que se tienen que crear archivos kml
class AirSpace:
  def __init__(self):
      self.points = []  # Lista de NavPoints
      self.segments = []  # Lista de NavSegments
      self.airports = []  # Lista de NavAirports

  # Función para añadir un punto de NavPoints
  def addPoint(self, point):
      self.points.append(point)

  # Función para añadir un segmento entre dos puntos
  def addSegment(self, numOrig, numDst, distance):
      orig_point = None
      dst_point = None
      for point in self.points:
          if point.num == numOrig:
              orig_point = point
          elif point.num == numDst:
              dst_point = point
          if orig_point and dst_point:
              break
      if orig_point and dst_point:
          segment = NavSegment(orig_point, dst_point, distance)
          self.segments.append(segment)
      else:
          print("Error: Uno o los dos puntos indicados no existen.")

  # Función para añadir un aeropuerto con sus respectivos SID y STAR
  def addAirport(self, name, SID, STAR):
      airport = NavAirport(name)
      airport.SID.append(SID)
      airport.STAR.append(STAR)
      self.airports.append(airport)

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
          with open(filename, 'r') as file:
              for line in file:
                  data = line.strip().split()
                  if len(data) == 4:
                      num, name, lat, lon = data
                      point = NavPoint(int(num), name, float(lat), float(lon))
                      self.addPoint(point)
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
              lines = file.readlines()
              for i in range(0, len(lines), 3):
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
      nav_filename = filename+"_nav.txt"
      seg_filename = filename+"_seg.txt"
      aer_filename = filename+"_aer.txt"
      air.loadNavPoints(nav_filename)
      air.loadSegments(seg_filename)
      air.loadAirports(aer_filename)
      return air

  # Función para construir el grafo del AirSpace
  def buildAirGraph(air):
      graph = Graph()
      # Primero añadimos todos los puntos convirtiendolos en nodos
      for point in air.points:
          node = Node(point.name, point.lon, point.lat)
          graph.nodes.append(node)
      # Segundo añadimos todos los segmentos
      for segment in air.segments:
          orig_node = None
          dst_node = None
          for node in graph.nodes:
              if node.name == segment.orig.name:
                  orig_node = node
              elif node.name == segment.dst.name:
                  dst_node = node
          if orig_node and dst_node:
              new_segment = Segment(orig_node, dst_node, segment.dist)
              graph.segments.append(new_segment)
      return graph

  # Función para poner todos los aeropuertos con sus coordenadas en un archivo KML para ejecutar goggleEarth
  def airportsToKML(air, nomFile):
      kml = simplekml.Kml()
      for point in air.points:
          kml.newpoint(name=point.name, coords=[(point.lon, point.lat)])
      kml.save(f"{nomFile}.kml")
      print(f"KML fichero {nomFile}.kml creado.")

  # Función para poner todos los segmentos con sus coordenadas en un archivo KML para ejecutar goggleEarth
  def pathToKML(path, nomFile):
      kml = simplekml.Kml()
      for segment in path.segments:
          name = f"Segment {segment.orig.name} - {segment.dst.name}"
          coords = [(segment.orig.lon, segment.orig.lat), (segment.dst.lon, segment.dst.lat)]
          kml.newlinestring(name=name, coords=coords)
      kml.save(f"{nomFile}.kml")
      print(f"KML fichero {nomFile}.kml creado.")

  # Función para obtener el SID de un aeropuerto
  def getSID(air, airport_name):
      for airport in air.airports:
          if airport.name == airport_name and airport.SID:
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
  def pathBetweenAirportsToKML(air, origin_airport_name, destination_airport_name, nomFile):
      # Comprobar si los nombres de los aeropuertos son válidos
      airport_names = [airport.name for airport in air.airports]
      if origin_airport_name not in airport_names or destination_airport_name not in airport_names:
          print("Error: Uno o los dos nombres de aeropuerto son inválidos.")
          return
      # Obtener el SID del aeropuerto de origen y el STAR del aeropuerto de destino
      SID_nameOrg = air.getSID(origin_airport_name)
      STAR_nameDst = air.getSTAR(destination_airport_name)
      if SID_nameOrg and STAR_nameDst:
          # Construir el grafo y encontrar la ruta más corta
          G = air.buildAirGraph()
          path, cost = G.findShortestPath(SID_nameOrg, STAR_nameDst)
          print("Shortest path:", path)  # Add this line for debugging
          kml = simplekml.Kml()
          if path:
              # Añadir los segmentos del shortestPath al archivo KML
              for i in range(len(path) - 1):
                  orig_name = path[i]
                  dst_name = path[i + 1]
                  for segment in air.segments:
                      if segment.orig.name == orig_name and segment.dst.name == dst_name:
                          name = f"Segment {orig_name} - {dst_name}"
                          coords = [(segment.orig.lon, segment.orig.lat), (segment.dst.lon, segment.dst.lat)]
                          kml.newlinestring(name=name, coords=coords)
                  orig_name = path[i + 1]
                  dst_name = path[i]
                  for segment in air.segments:
                      if segment.orig.name == orig_name and segment.dst.name == dst_name:
                          name = f"Segment {orig_name} - {dst_name}"
                          coords = [(segment.orig.lon, segment.orig.lat), (segment.dst.lon, segment.dst.lat)]
                          kml.newlinestring(name=name, coords=coords)
              kml.save(f"{nomFile}.kml")
              print(f"KML fichero {nomFile}.kml creado.")
          else:
              print("No hay path entre", SID_nameOrg, "i", STAR_nameDst)
      else:
          print("SID or STAR no encontrados para estos aeropuertos.")
