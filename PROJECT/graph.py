from segment import *
from path import *

class Graph:
  # Iniciamos una clase Graph con una lista de nodos y segmentos vacíos
  def __init__(self):
      self.nodes = []
      self.segments = []

  def addNode(g, n):
      # Agrega nodos al gráfico
      # g: el gráfico al que se agregarán los nodos y n: el nodo que se agregará
      # Retorna True si el nodo se ha agregado correctamente, False si ya existe
      i = 0
      found = False
      while i < len(g.nodes) and not found:
          if g.nodes[i].name == n.name:
              found = True
          i += 1
      if not found:
          g.nodes.append(n)
          return True
      else:
          return False

  def addSegment(g, name1, name2, bidirectional=True):
      # Agrega un segmento (arista) entre dos nodos al gráfico
      # name1: nombre del primer nodo
      # name2: nombre del segundo nodo
      # bidirectional: indica si el segmento debe ser bidireccional
      n1 = g.nameNode(name1)
      n2 = g.nameNode(name2)
      if n1 and n2:
          segment = Segment(n1, n2, bidirectional)
          g.segments.append(segment)
          n1.addNeighbor(n2)
          if bidirectional:
              n2.addNeighbor(n1)
          return True
      else:
          return False

  def nameNode(g, name):
      # Obtiene el objeto del gráfico dado un nombre de nodo
      # name: el nombre del nodo a buscar
      # Retorna el objeto Node si se encuentra, None si no se encuentra
      for node in g.nodes:
          if node.name == name:
              return node
      return None

  def plot(g):
      # Función para poder hacer definitivamente el gráfico, conteniendo tanto los nodos como los segmentos entre ellos que sean necesarios.
      for segment in g.segments:
          plt.arrow(segment.n1.x, segment.n1.y, segment.n2.x - segment.n1.x, segment.n2.y - segment.n1.y,
                    length_includes_head=True, head_width=0.5, head_length=0.8, fc="cyan", ec="cyan")
          plt.text((segment.n1.x + segment.n2.x) / 2, (segment.n1.y + segment.n2.y) / 2,
                   '{:.2f}'.format(segment.cost))
      for node in g.nodes:
          plt.plot(node.x, node.y, 'ko', markersize=6)
          plt.text(node.x, node.y, node.name)
      plt.xlabel('Coordinate X')
      plt.ylabel('Coordiante Y')
      plt.title('Graph')
      plt.axis('equal')
      plt.grid(True)
      plt.show()
  def plotNode(g, name):
      # Función tal que el gráfico muestre los nodos que se quieren añadir y sus vecinos correctamente
      node = g.nameNode(name)
      for neighbor in node.neighbors:
           plt.arrow(node.x, node.y, neighbor.x - node.x, neighbor.y - node.y,
                     length_includes_head=True, head_width=0.5, head_length=0.8, fc='cyan', ec='cyan')
           plt.text((node.x + neighbor.x) / 2, (node.y + neighbor.y) / 2,'{:.2f}'.format(node.distance(neighbor)))
      for node in g.nodes:
           plt.plot(node.x, node.y, 'ko', markersize=6)
           plt.text(node.x, node.y, node.name)
      plt.plot(node.x, node.y, 'ko', markersize=6)
      plt.text(node.x, node.y, node.name, fontsize=10, weight='bold')
      plt.xlabel('Coordinate X')
      plt.ylabel('Coordinate Y')
      plt.title('Node {}'.format(name))
      plt.axis('equal')
      plt.grid(True)
      plt.show()

  def findShortestPath(self, sidOrg, sidDst):
      # Encuentra el camino más corto entre dos nodos del gráfico con el algoridmo A*
      # sidOrg: nombre del nodo de inicio
      # sidDst: nombre del nodo de destino
      # Retorna el camino más corto y su costo, o None si no se puede encontrar un camino
      start_node = self.nameNode(sidOrg)
      end_node = self.nameNode(sidDst)
      if not start_node or not end_node:
          print("Error: Start or end node not found.")
          return None, None
      paths = [[start_node]]
      path_costs = [0]
      while paths:
          min_cost = float("inf")
          min_index = -1
          for i, cost in enumerate(path_costs):
              if cost >= 0 and cost < min_cost:
                  min_cost = cost
                  min_index = i
          if min_index == -1:
              print("Error: No valid paths found.")
              return None, None
          current_path = paths.pop(min_index)
          current_cost = path_costs.pop(min_index)
          last_node = current_path[-1]
          for segment in self.segments:
              if segment.n1 == last_node:
                  neighbor = segment.n2
              elif segment.bidirectional and segment.n2 == last_node:
                  neighbor = segment.n1
              else:
                  continue
              if neighbor == end_node:
                  current_path.append(neighbor)
                  return [node.name for node in current_path], current_cost + last_node.distance(neighbor)
              if neighbor in current_path:
                  continue
              new_path = current_path + [neighbor]
              new_path_cost = current_cost + last_node.distance(neighbor)
              should_add_new_path = True
              for i, path in enumerate(paths):
                  if neighbor in path:
                      path_cost = path_costs[i]
                      if path_cost < 0 or path_cost > new_path_cost:
                          paths[i] = []
                          path_costs[i] = -1
                      else:
                          should_add_new_path = False
                          break
              if should_add_new_path:
                  paths.append(new_path)
                  path_costs.append(new_path_cost)
      print("Error: No path found.")
      return None, None

  def plotPath(self, path):
      # Función para representar el shortestPath en un grafo continuo
      plt.ion()
      plt.figure()
      plt.xlabel('Coordinate X')
      plt.ylabel('Coordinate Y')
      plt.title('Shortest Path')
      plt.axis('equal')
      plt.grid(True)
      for node in self.nodes:
          plt.plot(node.x, node.y, 'ko', markersize=6)
          plt.text(node.x, node.y, node.name)
      for i in range(len(path) - 1):
          start_node = self.nameNode(path[i])
          end_node = self.nameNode(path[i + 1])
          if start_node is not None and end_node is not None:
              print("Plotting path from", start_node.name, "to", end_node.name)
              plt.arrow(start_node.x, start_node.y, end_node.x - start_node.x, end_node.y - start_node.y,
                        length_includes_head=True, head_width=0.5, head_length=0.8, fc="cyan", ec="cyan")
              plt.text((start_node.x + end_node.x) / 2, (start_node.y + end_node.y) / 2,
                       '{:.2f}'.format(start_node.distance(end_node)), fontsize=10)
              plt.draw()
              plt.pause(1)
          else:
              print("Invalid nodes in path:", path[i], path[i + 1])
      plt.ioff()
      plt.show()

