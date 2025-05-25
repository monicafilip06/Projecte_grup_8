import matplotlib.pyplot as plt
import heapq

class Path:
    def __init__(self):
        self.nodes = []
        self.costs = []
        self.totalCost = 0.0

    def addNode(P, G, name):
        if not any(node.name == name for node in G.nodes):
            print("Error: Node {} does not exist in the graph.".format(name))
            return True
        else:
            n1 = G.nodes[-1]
            n2 = G.nameNode(n1.name)
            if n2 and n2.addNeighbor(G.nameNode(name)):
                distance = n1.distance(G.nameNode(name))
                P.nodes.append(G.nameNode(name))
                P.totalCost += distance
                print("Node {} added to path.".format(name))
                return True
            else:
                return False

    def containsNode(P, name):
        if not any(node.name == name for node in P.nodes):
            print("Node {} is not in the path.".format(name))
            return False
        else:
            print("Node {} is in the path.".format(name))
            return True

    def getCostToNode(P, name):
        i = 0
        found = False
        while i < len(P.nodes) and not found:
            if P.nodes[i].name == name:
                found = True
            else:
                i += 1
        if found:
            totalCost = 0
            n = 0
            while n < i:
                d = P.nodes[n].distance(P.nodes[n + 1])
                totalCost += d
                n += 1
            return totalCost
        return -1

    def getApproxToDest(P, G, name):
        for node in P.nodes:
            if node.name == name:
                last_node = P.nodes[-1]
                return last_node.distance(node)
        return -1

    def plotPath(P, G):
        for i in range(len(P.nodes) - 1):
            n1 = P.nodes[i]
            n2 = P.nodes[i + 1]
            plt.annotate("",
                         xy=(n2.x, n2.y),
                         xytext=(n1.x, n1.y),
                         arrowprops=dict(arrowstyle="->", color='blue', lw=2))
            plt.text((n1.x + n2.x) / 2, (n1.y + n2.y) / 2,
                     '{:.2f}'.format(n1.distance(n2)), fontsize=8)

        for node in G.nodes:
            color = 'black'
            if node in P.nodes:
                color = 'blue'
            plt.plot(node.x, node.y, 'o', color=color)
            plt.text(node.x, node.y, node.name, fontsize=8)

        plt.xlabel('Coordinate X')
        plt.ylabel('Coordinate Y')
        plt.title(f'Camí òptim. Cost total = {P.totalCost:.2f}')
        plt.axis('equal')
        plt.grid(True)
        plt.show()

def findShortestPath(g, name1, name2):
    start = g.nameNode(name1)
    end = g.nameNode(name2)
    if not start or not end:
        return None, float('inf')

    distances = {node: float('inf') for node in g.nodes}
    previous = {node: None for node in g.nodes}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == end:
            break
        for neighbor in current_node.neighbors:
            if neighbor.name.upper() in g.blocked or current_node.name.upper() in g.blocked:
                continue
            segment = next((s for s in g.segments if (s.n1 == current_node and s.n2 == neighbor) or (s.bidirectional and s.n1 == neighbor and s.n2 == current_node)), None)
            if segment:
                alt = current_distance + segment.cost
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (alt, neighbor))

    path = []
    node = end
    while node:
        path.insert(0, node.name)
        node = previous[node]

    if distances[end] == float('inf'):
        return None, float('inf')
    else:
        return path, distances[end]

def findShortestPathAstar(g, name1, name2):
    start = g.nameNode(name1)
    end = g.nameNode(name2)
    if not start or not end:
        return None, float('inf')

    def heuristic(n1, n2):
        return n1.distance(n2)

    open_set = [(heuristic(start, end), 0, start)]
    came_from = {start: None}
    g_score = {node: float('inf') for node in g.nodes}
    g_score[start] = 0

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == end:
            break
        for neighbor in current.neighbors:
            if neighbor.name.upper() in g.blocked or current.name.upper() in g.blocked:
                continue
            segment = next((s for s in g.segments if (s.n1 == current and s.n2 == neighbor) or (s.bidirectional and s.n1 == neighbor and s.n2 == current)), None)
            if segment:
                tentative_g_score = g_score[current] + segment.cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    path = []
    node = end
    while node:
        path.insert(0, node.name)
        node = came_from.get(node)

    if g_score[end] == float('inf'):
        return None, float('inf')
    else:
        return path, g_score[end]

