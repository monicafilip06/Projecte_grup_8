from airSpace import AirSpace
from graph import Plot, PlotNode, interactivePlotNode
from path import findShortestPath, findShortestPathAstar
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
import simplekml

# Carregar espai aeri
air = AirSpace()
air.buildAirSpace("Cat")
G = air.buildAirGraph()

# GRÀFIC 1
Plot(G)

# GRÀFIC 2
interactivePlotNode(G)

# GRÀFIC 3 – Funció per dibuixar el camí
def plotShortestPath(G, path, cost, name1, name2, alg='Dijkstra'):
    fig, ax = plt.subplots()
    ax.set_title(f"Camí {alg} entre {name1} i {name2} - Cost: {cost:.2f}")

    for seg in G.segments:
        ax.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)

    for node in G.nodes:
        if hasattr(G, 'blocked') and node.name.upper() in G.blocked:
            color = 'red'
        elif node.name in path:
            color = 'blue'
        else:
            color = 'gray'
        ax.plot(node.x, node.y, 'o', color=color, markersize=3)
        ax.text(node.x, node.y, node.name, fontsize=6)

    for i in range(len(path) - 1):
        n1, n2 = G.nameNode(path[i]), G.nameNode(path[i + 1])
        ax.annotate("",
                    xy=(n2.x, n2.y),
                    xytext=(n1.x, n1.y),
                    arrowprops=dict(arrowstyle="->", color='cyan', lw=2))
        mid_x = (n1.x + n2.x) / 2
        mid_y = (n1.y + n2.y) / 2
        ax.text(mid_x, mid_y, f"{n1.distance(n2):.2f}", fontsize=7)

    ax.axis('equal')
    plt.grid(True)
    plt.show()

# GRÀFIC 3 + 4 – Tot en una sola finestra
def interactiveFull():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.5)
    ax.set_title("Selecciona aeroports i punts a bloquejar")

    axbox1 = plt.axes([0.2, 0.4, 0.6, 0.07])
    tb1 = TextBox(axbox1, "Origen (ex: LEBL)")
    axbox2 = plt.axes([0.2, 0.3, 0.6, 0.07])
    tb2 = TextBox(axbox2, "Destí (ex: LEVC)")
    axbox3 = plt.axes([0.2, 0.2, 0.6, 0.07])
    tb3 = TextBox(axbox3, "Punts a bloquejar (ex: SABAS, EDUIL)")

    # RadioButtons per escollir l'algorisme
    ax_radio = plt.axes([0.05, 0.05, 0.15, 0.15])
    radio = RadioButtons(ax_radio, ('Dijkstra', 'A*'))

    btn_calc_ax = plt.axes([0.3, 0.08, 0.2, 0.07])
    btn_calc = Button(btn_calc_ax, "Calcular camí")
    btn_exp_ax = plt.axes([0.55, 0.08, 0.2, 0.07])
    btn_exp = Button(btn_exp_ax, "Exportar KML")

    state = {
        'path_dijkstra': None,
        'cost_dijkstra': 0,
        'path_astar': None,
        'cost_astar': 0,
        'origin': '',
        'dest': '',
        'selected': 'Dijkstra'
    }

    def on_radio(label):
        state['selected'] = label

    radio.on_clicked(on_radio)

    def on_click(event):
        origin = tb1.text.strip().upper()
        dest = tb2.text.strip().upper()
        blocked = [x.strip().upper() for x in tb3.text.split(',') if x.strip()]

        SID = air.getSID(origin)
        STAR = air.getSTAR(dest)
        if not SID or not STAR:
            ax.set_title("SID o STAR invàlid.")
            fig.canvas.draw_idle()
            return

        if hasattr(G, 'blocked'):
            G.blocked.clear()
        else:
            G.blocked = set()

        for b in blocked:
            G.blocked.add(b)

        path_d, cost_d = findShortestPath(G, SID, STAR)
        path_a, cost_a = findShortestPathAstar(G, SID, STAR)

        if not path_d or not path_a:
            ax.set_title("No hi ha camí.")
        else:
            plotShortestPath(G, path_d, cost_d, origin, dest, alg="Dijkstra")
            plotShortestPath(G, path_a, cost_a, origin, dest, alg="A*")
            state['path_dijkstra'] = path_d
            state['cost_dijkstra'] = cost_d
            state['path_astar'] = path_a
            state['cost_astar'] = cost_a
            state['origin'] = origin
            state['dest'] = dest

    def on_export(event):
        path = state['path_dijkstra'] if state['selected'] == 'Dijkstra' else state['path_astar']
        if not path:
            print("❌ No hi ha cap camí a exportar.")
            return

        kml = simplekml.Kml()
        for i in range(len(path) - 1):
            n1 = G.nameNode(path[i])
            n2 = G.nameNode(path[i + 1])
            if n1 and n2:
                coords = [(n1.x, n1.y), (n2.x, n2.y)]
                kml.newlinestring(name=f"{n1.name}-{n2.name}", coords=coords)
        alg_name = state['selected'].replace("*", "Astar")
        nomFitxer = f"Ruta_{state['origin']}_a_{state['dest']}_{alg_name}"
        kml.save(f"{nomFitxer}.kml")
        print(f"✅ Ruta exportada a {nomFitxer}.kml")

    btn_calc.on_clicked(on_click)
    btn_exp.on_clicked(on_export)
    plt.show()

interactiveFull()

