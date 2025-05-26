from segment import *
from path import *
import matplotlib.pyplot as plt

#Crea una estructura para representar un grafo con nodos, segmentos y posibilidad de bloquear nodos
class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []
        self.blocked = set()  # Conjunto de nodos bloqueados
#Evita nodos duplicados por nombre.
    def addNode(self, n):
        for node in self.nodes:
            if node.name == n.name:
                return False
        n.blocked = False  #Afegim la propietat bloquejat per defecte
        self.nodes.append(n)
        return True

    def addSegment(self, name1, name2, bidirectional=True):
        #Busca los nodos de origen y destino por su nombre
        n1 = self.nameNode(name1)
        n2 = self.nameNode(name2)
        if n1 and n2:
            segment = Segment(n1, n2, bidirectional)  #Si ambos nodos existen, crea un segmento y lo agrega. 
                                                     #Si es bidireccional, conecta en ambas direcciones.
            self.segments.append(segment)
            n1.addNeighbor(n2)
            if bidirectional:
                n2.addNeighbor(n1)
            return True
        return False
    #busca un nodo por su nombre
    def nameNode(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    #Elimina completamente un nodo del grafo, incluyendo todas sus conexiones con otros nodos
    def deleteNode(self, name):
        node_to_remove = self.nameNode(name)
        #Si no existe ese nodo, termina 
        if not node_to_remove:
            return False
        self.nodes = [n for n in self.nodes if n.name != name]
        self.segments = [s for s in self.segments if s.n1 != node_to_remove and s.n2 != node_to_remove]
        #También lo quita de las listas de vecinos de los demás nodos
        for node in self.nodes:
            if node_to_remove in node.neighbors:
                node.neighbors.remove(node_to_remove)
        return True

    def deleteSegment(self, name1, name2):
        n1 = self.nameNode(name1)
        n2 = self.nameNode(name2)
        if not n1 or not n2:
            return False
        self.segments = [s for s in self.segments if not ((s.n1 == n1 and s.n2 == n2) or (s.bidirectional and s.n1 == n2 and s.n2 == n1))]
        #También elimina cada uno del listado de vecinos del otro.
        if n2 in n1.neighbors:
            n1.neighbors.remove(n2)
        if n1 in n2.neighbors:
            n2.neighbors.remove(n1)
        return True

    def getClosest(self, x, y):
        if not self.nodes:
            return None
        #Devuelve el nodo más cercano a una coordenada (x, y), usando distance_coords.
        #Supone que el primer nodo es el más cercano y guarda su distancia al punto (x, y)
        closest = self.nodes[0]
        min_dist = closest.distance_coords(x, y)
        for node in self.nodes[1:]:
            d = node.distance_coords(x, y)
            #Calcula su distancia a (x, y) 
            #Si encuentra uno más cercano, actualiza closest
            if d < min_dist:
                closest = node
                min_dist = d
        return closest
# funcion para bloquear o desbloquear nodos,hacer que no puedan ser usados al calcular rutas
    def blockNode(self, name):
        node = self.nameNode(name)
        if node:
            node.blocked = True
            print(f"Node {name} bloquejat.")
            return True
        print(f"Node {name} no trobat.")
        return False
#Sirve para reactivar un nodo para que pueda usarse en una ruta (hace ecatamente lo contrario)
    def unblockNode(self, name):
        node = self.nameNode(name)
        if node:
            node.blocked = False
            print(f"Node {name} desbloquejat.")
            return True
        print(f"Node {name} no trobat.")
        return False
#Comprueba si un nodo está bloqueado,Usa la función getattr, que sirve para obtener un atributo de un objeto
    def isBlocked(self, node):
        return getattr(node, 'blocked', False)
#Devuelve una lista de vecinos del nodo que no estén bloqueados
    def getUnblockedNeighbors(self, node):
        return [n for n in node.neighbors if not self.isBlocked(n)]

    #Función permite al usuario bloquear nodos manualmente con el teclado
    def interactiveBlockNodes(self):
        print("\n✈️  Introdueix els noms dels waypoints que vols bloquejar (separats per comes):")
        resposta = input("Blocar waypoints: ")
        noms = [n.strip().upper() for n in resposta.split(',') if n.strip()]
        #Llama a blockNode() para cada nombre ingresado
        for nom in noms:
            self.blockNode(nom)
        print("Waypoints bloquejats: ", noms)

#Función dibuja el grafo completo con todos sus nodos y conexiones
def Plot(g):
    #extrae las coordenadas del nodo (origen/destino)
    for seg in g.segments:
        x1, y1 = seg.n1.x, seg.n1.y
        x2, y2 = seg.n2.x, seg.n2.y
        #Dibuja una flecha desde el nodo de origen hasta el de destino
        plt.annotate("",
                     xy=(x2, y2),
                     xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color='cyan', lw=1.5))
        #Escribe el coste del segmento
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, f"{seg.cost:.2f}", fontsize=7)

    for node in g.nodes:
        color = 'red' if g.isBlocked(node) else 'black'   #si nodo esta bloqueado rojo sino negro
        plt.plot(node.x, node.y, 'o', color=color)
        plt.text(node.x, node.y, node.name, fontsize=8)

    plt.axis('equal')
    plt.grid(True) #cuadricula
    plt.title("Graf amb fletxes des de origen fins a destí")
    plt.show()

def PlotNode(g, nameOrigin):
    #Buscar el nodo con nombre nameOrigin.
    origin = g.nameNode(nameOrigin)
    if not origin:
        return False
#Dibuja los segmentos (flechas) 
    for seg in g.segments:
        x1, y1 = seg.n1.x, seg.n1.y
        x2, y2 = seg.n2.x, seg.n2.y
        color = 'gray'
        #Si el segmento va desde el nodo origen a un vecino, se pinta de rojo
        if seg.n1 == origin and seg.n2 in origin.neighbors:
            color = 'red'
        #Dibuja la flecha enre nodos y escribe el coste
        plt.annotate("",
                     xy=(x2, y2),
                     xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, f"{seg.cost:.2f}", fontsize=7)
#Establece el color según el tipo de nodo
    for node in g.nodes:
        if node == origin:
            color = 'blue'
        elif node in origin.neighbors:
            color = 'green'
        elif g.isBlocked(node):
            color = 'red'
        else:
            color = 'gray'
        plt.plot(node.x, node.y, 'o', color=color)
        plt.text(node.x, node.y, node.name, fontsize=8)

    plt.axis('equal')
    plt.grid(True)
    plt.title(f"Veïns del node {nameOrigin}")
    plt.show()
    return True
# función permite interactuar con el grafo en una ventana gráfica
def interactivePlotNode(g):
    #escribes el nombre de un nodo en una caja de texto (hace una figura y area de dibujo)
    from matplotlib.widgets import TextBox
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    ax.set_title("Introdueix el nom del node per mostrar els seus veïns")
#Función que se llama cada vez que escribes un nombre en la caja
    def draw_node(nameOrigin):
        ax.clear()

        #Busca el nodo ingresado
        origin = g.nameNode(nameOrigin.upper())
        if not origin:
            ax.set_title(f"Node '{nameOrigin}' no trobat.")
            fig.canvas.draw_idle()
            return
        #Recorre los segmentos y resalta en rojo los que van del nodo origen a sus vecinos
        for seg in g.segments:
            x1, y1 = seg.n1.x, seg.n1.y
            x2, y2 = seg.n2.x, seg.n2.y
            color = 'gray'
            if seg.n1 == origin and seg.n2 in origin.neighbors:
                color = 'red'
            # Dibuja las flechas
            ax.annotate("",
                        xy=(x2, y2),
                        xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{seg.cost:.2f}", fontsize=7)
        #Asignar colores a los nodos
        for node in g.nodes:
            if node == origin:
                color = 'blue'
            elif node in origin.neighbors:
                color = 'green'
            elif g.isBlocked(node):
                color = 'red'
            else:
                color = 'gray'
            ax.plot(node.x, node.y, 'o', color=color)
            ax.text(node.x, node.y, node.name, fontsize=8)
        # Mostrar grafico con cuadricula 
        ax.set_title(f"Veïns del node {nameOrigin.upper()} amb fletxes")
        ax.axis('equal')
        ax.grid(True)
        fig.canvas.draw_idle()
    # Crea una area para la caja de texto abajo
    #Al presionar enter se llama a drawnode
    axbox = plt.axes([0.3, 0.05, 0.4, 0.075])
    text_box = TextBox(axbox, 'Nom del node: ')
    text_box.on_submit(draw_node)
    plt.show()
