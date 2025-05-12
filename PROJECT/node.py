import math


class Node:
   def __init__(self, name, x, y):
       #Iniciamos una función de Node con un nombre y unas coordenadas
       self.name = name
       self.x = x
       self.y = y
       self.neighbors = []

   # Agrega un nodo vecino a la lista de vecinos de la Node
   # n1 es el nodo actual, n2 es el nodo vecino a agregar
   def addNeighbor(n1, n2):
       i = 0
       found = False
       while i < len(n1.neighbors) and not found:
           if n1.neighbors[i] == n2:
               found = True
           i += 1
       if not found:
           n1.neighbors.append(n2)
           return True
       else:
           return False

   # Calcula la distancia euclidiana entre dos nodos
   # n1 y n2 son los nodos entre los cuales se calcula la distancia
   def distance(n1, n2):
#Cálculo de la distancia euclídea entre nodos
       distance = math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)
       return distance
