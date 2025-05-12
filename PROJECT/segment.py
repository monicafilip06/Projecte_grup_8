class Segment:
   def __init__(self, n1, n2, bidirectional=True):
       # Inicializa un segmento entre dos nodos
       # Calcula la distancia entre los dos nodos y la almacena como el costo del segmento
       # Bidirectional indica si el segmento debe ser bidireccional o no
       self.n1 = n1
       self.n2 = n2
       self.cost = n1.distance(n2)
       self.bidirectional = bidirectional
       self.update_neighbors_n1 = n1.addNeighbor(n2)
       self.update_neighbors_n2 = n2.addNeighbor(n1)

