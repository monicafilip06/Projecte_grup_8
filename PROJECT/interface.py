import tkinter as tk                                            #per finestres de diàleg
from tkinter import simpledialog, messagebox, filedialog
import matplotlib.pyplot as plt                                #mostra gràfics
from matplotlib.widgets import TextBox, Button, RadioButtons
import simplekml                                               #per exportar resultats a kml
from airSpace import AirSpace
from path import findShortestPath, findShortestPathAstar


# Inicialitzar una ventana principal tkinter per als diàlegs
root = tk.Tk()
root.withdraw()

#Dibuixa un graf amb nodes i connexions
def Plot(G, titol="Espai aeri"):
    fig, ax = plt.subplots(figsize=(16, 10))  # Aumentamos el tamaño de la figura
    ax.set_title(titol, fontsize=18, fontweight='bold')  # Título más grande
    #Dibuja una flecha por cada segmento
    for seg in G.segments:
        ax.annotate("",
                    xy=(seg.n2.x, seg.n2.y),
                    xytext=(seg.n1.x, seg.n1.y),
                    arrowprops=dict(arrowstyle="->", color='cyan', lw=0.7))
    #dibuja cada nodo con su nombre
    for n in G.nodes:
        ax.plot(n.x, n.y, 'o', color='black', markersize=3)
        ax.text(n.x, n.y, n.name, fontsize=7)  # Tamaño más grande para el texto
    ax.axis('equal')
    plt.grid(True)
    plt.tight_layout()  # Optimiza uso del espacio
    plt.show()

#Exporta el graf G en format kml per visualitzar a Google Earth
def export_to_kml(G):
    filepath = filedialog.asksaveasfilename(        #abre dialogo para elegir nombre del archivo
        defaultextension=".kml",
        filetypes=[("KML files", "*.kml")],
        title="Guardar espai aeri com a KML"
    )
    if not filepath:
        print("❌ Exportació cancel·lada.")
        return

    kml = simplekml.Kml()

    # 🔹 Afegim segments com a línies
    for seg in G.segments:
        coords = [(seg.n1.x, seg.n1.y), (seg.n2.x, seg.n2.y)]
        ls = kml.newlinestring(name=f"{seg.n1.name}-{seg.n2.name}", coords=coords)
        ls.style.linestyle.color = simplekml.Color.white
        ls.style.linestyle.width = 2

    # 🔸 Afegim nodes com a punts vermells amb etiqueta
    for node in G.nodes:
        pnt = kml.newpoint(name=node.name, coords=[(node.x, node.y)])
        pnt.style.iconstyle.color = simplekml.Color.red
        pnt.style.iconstyle.scale = 1
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'
        pnt.style.labelstyle.scale = 1  # mida del text

    kml.save(filepath)
    print(f"✅ Exportat a {filepath}")

# Càrrega de dades i construccio dels espais aeris (cat,spain...)
air_cat = AirSpace()
air_cat.buildAirSpace("Cat")           #carrega informacio dels punts i rutes
G_cat = air_cat.buildAirGraph()        #genera un graf , converteix aixo en un graf de nodes...
for seg in G_cat.segments:             # asegura que cada nodo tenga una lista de vecinos
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

air_spain = AirSpace()
air_spain.buildAirSpace("Spain")
G_spain = air_spain.buildAirGraph()
for seg in G_spain.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

air_eur = AirSpace()
air_eur.buildAirSpace("ECAC")
G_eur = air_eur.buildAirGraph()
for seg in G_eur.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

# Crea la ventana principal de la interfaz
fig, ax = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(left=0.35)
ax.set_title("Selecciona l'espai aeri a visualitzar", fontsize=16, fontweight='bold')
ax.axis('off')

# Radio buttons més grans i para escoger la region
ax_radio = plt.axes([0.05, 0.6, 0.25, 0.25], facecolor='#f0f0f0')
radio = RadioButtons(ax_radio, ('Catalunya', 'Espanya', 'Europa'))
[lab.set_fontsize(12) for lab in radio.labels]

# Botó Mostrar
btn_plot_ax = plt.axes([0.05, 0.45, 0.25, 0.08], facecolor='#d0eaff')
btn_plot = Button(btn_plot_ax, 'Mostrar', color='#80bfff', hovercolor='#3399ff')
btn_plot.label.set_fontsize(12)

# Botó Exportar a KML
btn_kml_ax = plt.axes([0.05, 0.35, 0.25, 0.08], facecolor='#d0ffd0')
btn_kml = Button(btn_kml_ax, 'Exportar a KML', color='#80ff80', hovercolor='#33cc33')
btn_kml.label.set_fontsize(12)

# Control d'estat, guarda la seleccion actual del usuario
current_state = {'selected': 'Catalunya'}

#Mitjançant botons i selecció de regió, podem mostrar o exportar l’espai aeri que vulguem. 
#Aquestes funcions gestionen l’estat de l’aplicació."
#Aquesta funció actualitza l’estat intern de la selecció de regió (Catalunya, Espanya o Europa) quan l’usuari prem un dels RadioButtons.
def on_radio_change(label):            
    current_state['selected'] = label

def on_show_click(event):        #S’activa quan l’usuari fa clic al botó “Mostrar”.
                                #Segons la regió escollida, crida la funció Plot(G) corresponent
    seleccio = current_state['selected']
    if seleccio == 'Catalunya':
        Plot(G_cat, titol="Espai aeri de Catalunya")
    elif seleccio == 'Espanya':
        Plot(G_spain, titol="Espai aeri d’Espanya")
    elif seleccio == 'Europa':
        Plot(G_eur, titol="Espai aeri d’Europa")

def on_export_click(event):                #S’activa quan es fa clic al botó “Exportar a KML”.
    seleccio = current_state['selected']    #i exporta el grafo correspondiente
    if seleccio == 'Catalunya':
        export_to_kml(G_cat)            
    elif seleccio == 'Espanya':
        export_to_kml(G_spain)
    elif seleccio == 'Europa':
        export_to_kml(G_eur)

radio.on_clicked(on_radio_change)
btn_plot.on_clicked(on_show_click)
btn_kml.on_clicked(on_export_click)

plt.show()

# === FUNCIO PLOT PERSONALITZADA ===
#Aquesta versió s’utilitza dins d’algunes de les interfaces (com reachability o càlcul de rutes)
#per fer gràfics més clars
def Plot(G, titol="Graf amb fletxes des de l'origen fins al destí"):
    fig, ax = plt.subplots()
    ax.set_title(titol)
    for seg in G.segments:
        ax.annotate("",
                    xy=(seg.n2.x, seg.n2.y),
                    xytext=(seg.n1.x, seg.n1.y),
                    arrowprops=dict(arrowstyle="->", color='cyan', lw=0.7))
    for n in G.nodes:
        ax.plot(n.x, n.y, 'o', color='black', markersize=3)
        ax.text(n.x, n.y, n.name, fontsize=5)
    ax.axis('equal')
    plt.grid(True)
    plt.show()

# === CÀRREGA DE REGIONS ===
air_cat = AirSpace()
air_cat.buildAirSpace("Cat")
G_cat = air_cat.buildAirGraph()
for seg in G_cat.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

air_spain = AirSpace()
air_spain.buildAirSpace("Spain")
G_spain = air_spain.buildAirGraph()
for seg in G_spain.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

air_eur = AirSpace()
air_eur.buildAirSpace("ECAC")
G_eur = air_eur.buildAirGraph()
for seg in G_eur.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

def interactiveReachability():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    ax.set_title("Reachability des d'un node")

    axbox = plt.axes([0.25, 0.15, 0.5, 0.07])
    text_box = TextBox(axbox, "Nom del node:")

    ax_radio = plt.axes([0.05, 0.05, 0.2, 0.1])
    radio = RadioButtons(ax_radio, ('Catalunya', 'Espanya', 'Europa'))

    btn_ax = plt.axes([0.75, 0.05, 0.2, 0.1])
    btn = Button(btn_ax, "Mostrar reachability")

    airspaces = {
        'Catalunya': G_cat,
        'Espanya': G_spain,
        'Europa': G_eur
    }

    state = {'region': 'Europa'}

    def set_region(label):
        state['region'] = label

    radio.on_clicked(set_region)

    def show_reachability(event):
        G = airspaces[state['region']]
        node_name = text_box.text.strip().upper()
        node = G.nameNode(node_name)
        if not node:
            ax.set_title(f"Node {node_name} no trobat a {state['region']}")
            fig.canvas.draw_idle()
            return

        reachable = G.reachability(node.name)

        fig2, ax2 = plt.subplots(figsize=(16, 10))
        for seg in G.segments:
            ax2.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)
        for n in G.nodes:
            color = 'green' if n.name in reachable else 'gray'
            if n == node:
                color = 'blue'
            ax2.plot(n.x, n.y, 'o', color=color, markersize=3)
            ax2.text(n.x, n.y, n.name, fontsize=5)

        ax2.set_title(f"Nodes accessibles des de {node_name} a {state['region']} ({len(reachable)} trobats)")
        ax2.axis('equal')
        plt.grid(True)
        plt.show()

    btn.on_clicked(show_reachability)
    plt.show()


def interactiveFull():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.6)
    ax.set_title("Selecciona espai aeri, aeroports i punts a bloquejar")

    tb1 = TextBox(plt.axes([0.2, 0.45, 0.6, 0.05]), "Origen (ex: LEBL)")
    tb2 = TextBox(plt.axes([0.2, 0.38, 0.6, 0.05]), "Destí (ex: LEVC)")
    tb3 = TextBox(plt.axes([0.2, 0.31, 0.6, 0.05]), "Nodes a bloquejar")

    radio_alg = RadioButtons(plt.axes([0.05, 0.05, 0.15, 0.15]), ('Ruta més curta', 'A*'))
    radio_map = RadioButtons(plt.axes([0.8, 0.05, 0.15, 0.15]), ('Catalunya', 'Espanya', 'Europa'))

    btn_calc = Button(plt.axes([0.3, 0.18, 0.2, 0.06]), "Calcular camí")
    btn_exp = Button(plt.axes([0.55, 0.18, 0.2, 0.06]), "Exportar KML")

    #Podem calcular la millor ruta entre dos aeroports. 
    #També podem bloquejar punts i escollir l’algorisme: Dijkstra o A*
    state = {
        'path_dijkstra': None,        #ruta mes curta (utilitza dijkstra)
        'cost_dijkstra': 0,
        'path_astar': None,           #A* es mes eficient en certs casos
        'cost_astar': 0,
        'origin': '',
        'dest': '',
        'selected_alg': 'Ruta més curta',
        'selected_map': 'Catalunya'
    }

    airspaces = {
        'Catalunya': (air_cat, G_cat),
        'Espanya': (air_spain, G_spain),
        'Europa': (air_eur, G_eur)
    }

    radio_alg.on_clicked(lambda label: state.update({'selected_alg': label}))
    radio_map.on_clicked(lambda label: state.update({'selected_map': label}))

    def plotShortestPath(G, path, cost, name1, name2, alg):
        fig, ax = plt.subplots()
        ax.set_title(f"{alg} entre {name1} i {name2} - Cost: {cost:.2f}")
        for seg in G.segments:
            ax.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)
        for node in G.nodes:
            color = 'red' if hasattr(G, 'blocked') and node.name.upper() in G.blocked else (
                'blue' if node.name in path else 'gray')
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

    def on_click(event):
        origin = tb1.text.strip().upper()
        dest = tb2.text.strip().upper()
        blocked = [x.strip().upper() for x in tb3.text.split(',') if x.strip()]
        air, G = airspaces[state['selected_map']]

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

        alg = state['selected_alg']
        if alg == "Ruta més curta":
            path, cost = findShortestPath(G, SID, STAR)
        else:
            path, cost = findShortestPathAstar(G, SID, STAR)

        if not path:
            ax.set_title("No hi ha camí.")
            fig.canvas.draw_idle()
            return

        plotShortestPath(G, path, cost, origin, dest, alg)

        if alg == "Ruta més curta":
            state.update({'path_dijkstra': path, 'cost_dijkstra': cost})
        else:
            state.update({'path_astar': path, 'cost_astar': cost})

        state.update({'origin': origin, 'dest': dest})

    def on_export(event):
        _, G = airspaces[state['selected_map']]
        path = state['path_dijkstra'] if state['selected_alg'] == 'Ruta més curta' else state['path_astar']
        if not path:
            print("❌ No hi ha cap camí a exportar.")
            return
        kml = simplekml.Kml()
        for i in range(len(path) - 1):
            n1, n2 = G.nameNode(path[i]), G.nameNode(path[i + 1])
            kml.newlinestring(name=f"{n1.name}-{n2.name}", coords=[(n1.x, n1.y), (n2.x, n2.y)])
        alg_name = state['selected_alg'].replace("*", "Astar").replace("Ruta més curta", "cami_mes_curta")
        nomFitxer = f"Ruta_{state['origin']}_a_{state['dest']}_{alg_name}.kml"
        kml.save(nomFitxer)
        print(f"✅ Ruta exportada a {nomFitxer}")

    btn_calc.on_clicked(on_click)
    btn_exp.on_clicked(on_export)
    plt.show()
def interactivePlotNodeRegion():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.35)
    ax.set_title("Veïns del node (segons la regió seleccionada)")

    axbox = plt.axes([0.25, 0.25, 0.5, 0.07])
    text_box = TextBox(axbox, "Nom del node:")

    ax_radio = plt.axes([0.05, 0.05, 0.2, 0.15])
    radio = RadioButtons(ax_radio, ('Catalunya', 'Espanya', 'Europa'))

    btn_ax = plt.axes([0.75, 0.1, 0.2, 0.1])
    btn = Button(btn_ax, "Mostrar veïns")

    airspaces = {
        'Catalunya': G_cat,
        'Espanya': G_spain,
        'Europa': G_eur
    }

    state = {'region': 'Europa'}

    def set_region(label):
        state['region'] = label

    radio.on_clicked(set_region)

    def show_neighbors(event):
        G = airspaces[state['region']]
        node_name = text_box.text.strip().upper()
        node = G.nameNode(node_name)
        if not node:
            ax.set_title(f"Node {node_name} no trobat a {state['region']}")
            fig.canvas.draw_idle()
            return

        fig2, ax2 = plt.subplots(figsize=(16, 10))
        count = 0
        neighbor_names = getattr(node, 'neighbors', [])

        for seg in G.segments:
            ax2.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)
        for n in G.nodes:
            color = 'gray'
            if n == node:
                color = 'blue'
            elif n.name in neighbor_names:
                color = 'green'
            ax2.plot(n.x, n.y, 'o', color=color, markersize=3)
            ax2.text(n.x, n.y, n.name, fontsize=5)

        for n_name in neighbor_names:
            neighbor = G.nameNode(n_name)
            if not neighbor:
                continue
            ax2.annotate("",
                         xy=(neighbor.x, neighbor.y),
                         xytext=(node.x, node.y),
                         arrowprops=dict(arrowstyle="->", color='red', lw=1.5))
            mid_x = (node.x + neighbor.x) / 2
            mid_y = (node.y + neighbor.y) / 2
            ax2.text(mid_x, mid_y, f"{node.distance(neighbor):.2f}", fontsize=6, color='red')
            count += 1

        ax2.set_title(f"Veïns del node {node_name} a {state['region']} ({count} trobats)")
        ax2.axis('equal')
        plt.grid(True)
        plt.show()

    btn.on_clicked(show_neighbors)
    plt.show()

# === Llançament ===
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from matplotlib.widgets import TextBox, Button, RadioButtons
import matplotlib.pyplot as plt
import simplekml
from airSpace import AirSpace
from path import findShortestPath, findShortestPathAstar

# === FUNCIO PLOT PERSONALITZADA ===
def Plot(G, titol="Graf amb fletxes des de l'origen fins al destí"):
    fig, ax = plt.subplots()
    ax.set_title(titol)
    for seg in G.segments:
        ax.annotate("",
                    xy=(seg.n2.x, seg.n2.y),
                    xytext=(seg.n1.x, seg.n1.y),
                    arrowprops=dict(arrowstyle="->", color='cyan', lw=0.7))
    for n in G.nodes:
        ax.plot(n.x, n.y, 'o', color='black', markersize=3)
        ax.text(n.x, n.y, n.name, fontsize=5)
    ax.axis('equal')
    plt.grid(True)
    plt.show()

# === CÀRREGA DE REGIONS ===
air_cat = AirSpace()
air_cat.buildAirSpace("Cat")
G_cat = air_cat.buildAirGraph()
for seg in G_cat.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

air_spain = AirSpace()
air_spain.buildAirSpace("Spain")
G_spain = air_spain.buildAirGraph()
for seg in G_spain.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

air_eur = AirSpace()
air_eur.buildAirSpace("ECAC")
G_eur = air_eur.buildAirGraph()
for seg in G_eur.segments:
    if seg.n2.name not in seg.n1.neighbors:
        seg.n1.neighbors.append(seg.n2.name)

def interactiveReachability():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    ax.set_title("Reachability des d'un node")

    axbox = plt.axes([0.25, 0.15, 0.5, 0.07])
    text_box = TextBox(axbox, "Nom del node:")

    ax_radio = plt.axes([0.05, 0.05, 0.2, 0.1])
    radio = RadioButtons(ax_radio, ('Catalunya', 'Espanya', 'Europa'))

    btn_ax = plt.axes([0.75, 0.05, 0.2, 0.1])
    btn = Button(btn_ax, "Mostrar reachability")

    airspaces = {
        'Catalunya': G_cat,
        'Espanya': G_spain,
        'Europa': G_eur
    }

    state = {'region': 'Europa'}

    def set_region(label):
        state['region'] = label

    radio.on_clicked(set_region)

    def show_reachability(event):
        G = airspaces[state['region']]
        node_name = text_box.text.strip().upper()
        node = G.nameNode(node_name)
        if not node:
            ax.set_title(f"Node {node_name} no trobat a {state['region']}")
            fig.canvas.draw_idle()
            return

        reachable = G.reachability(node.name)

        fig2, ax2 = plt.subplots(figsize=(16, 10))
        for seg in G.segments:
            ax2.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)
        for n in G.nodes:
            color = 'green' if n.name in reachable else 'gray'
            if n == node:
                color = 'blue'
            ax2.plot(n.x, n.y, 'o', color=color, markersize=3)
            ax2.text(n.x, n.y, n.name, fontsize=5)

        ax2.set_title(f"Nodes accessibles des de {node_name} a {state['region']} ({len(reachable)} trobats)")
        ax2.axis('equal')
        plt.grid(True)
        plt.show()

    btn.on_clicked(show_reachability)
    plt.show()


def interactiveFull():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.6)
    ax.set_title("Selecciona espai aeri, aeroports i punts a bloquejar")

    tb1 = TextBox(plt.axes([0.2, 0.45, 0.6, 0.05]), "Origen (ex: LEBL)")
    tb2 = TextBox(plt.axes([0.2, 0.38, 0.6, 0.05]), "Destí (ex: LEVC)")
    tb3 = TextBox(plt.axes([0.2, 0.31, 0.6, 0.05]), "Punts a bloquejar")

    radio_alg = RadioButtons(plt.axes([0.05, 0.05, 0.15, 0.15]), ('Ruta més curta', 'A*'))
    radio_map = RadioButtons(plt.axes([0.8, 0.05, 0.15, 0.15]), ('Catalunya', 'Espanya', 'Europa'))

    btn_calc = Button(plt.axes([0.3, 0.18, 0.2, 0.06]), "Calcular camí")
    btn_exp = Button(plt.axes([0.55, 0.18, 0.2, 0.06]), "Exportar KML")

    state = {
        'path_dijkstra': None,
        'cost_dijkstra': 0,
        'path_astar': None,
        'cost_astar': 0,
        'origin': '',
        'dest': '',
        'selected_alg': 'Ruta més curta',
        'selected_map': 'Catalunya'
    }

    airspaces = {
        'Catalunya': (air_cat, G_cat),
        'Espanya': (air_spain, G_spain),
        'Europa': (air_eur, G_eur)
    }

    radio_alg.on_clicked(lambda label: state.update({'selected_alg': label}))
    radio_map.on_clicked(lambda label: state.update({'selected_map': label}))

    def plotShortestPath(G, path, cost, name1, name2, alg):
        fig, ax = plt.subplots()
        ax.set_title(f"{alg} entre {name1} i {name2} - Cost: {cost:.2f}")
        for seg in G.segments:
            ax.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)
        for node in G.nodes:
            color = 'red' if hasattr(G, 'blocked') and node.name.upper() in G.blocked else (
                'blue' if node.name in path else 'gray')
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

    def on_click(event):
        origin = tb1.text.strip().upper()
        dest = tb2.text.strip().upper()
        blocked = [x.strip().upper() for x in tb3.text.split(',') if x.strip()]
        air, G = airspaces[state['selected_map']]

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

        alg = state['selected_alg']
        if alg == "Ruta més curta":
            path, cost = findShortestPath(G, SID, STAR)
        else:
            path, cost = findShortestPathAstar(G, SID, STAR)

        if not path:
            ax.set_title("No hi ha camí.")
            fig.canvas.draw_idle()
            return

        plotShortestPath(G, path, cost, origin, dest, alg)

        if alg == "Ruta més curta":
            state.update({'path_dijkstra': path, 'cost_dijkstra': cost})
        else:
            state.update({'path_astar': path, 'cost_astar': cost})

        state.update({'origin': origin, 'dest': dest})

    def on_export(event):
        _, G = airspaces[state['selected_map']]
        path = state['path_dijkstra'] if state['selected_alg'] == 'Ruta més curta' else state['path_astar']
        if not path:
            print("❌ No hi ha cap camí a exportar.")
            return
        kml = simplekml.Kml()
        for i in range(len(path) - 1):
            n1, n2 = G.nameNode(path[i]), G.nameNode(path[i + 1])
            kml.newlinestring(name=f"{n1.name}-{n2.name}", coords=[(n1.x, n1.y), (n2.x, n2.y)])
        alg_name = state['selected_alg'].replace("*", "Astar").replace("Ruta més curta", "cami_mes_curta")
        nomFitxer = f"Ruta_{state['origin']}_a_{state['dest']}_{alg_name}.kml"
        kml.save(nomFitxer)
        print(f"✅ Ruta exportada a {nomFitxer}")

    btn_calc.on_clicked(on_click)
    btn_exp.on_clicked(on_export)
    plt.show()
def interactivePlotNodeRegion():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.35)
    ax.set_title("Veïns del node (segons la regió seleccionada)")

    axbox = plt.axes([0.25, 0.25, 0.5, 0.07])
    text_box = TextBox(axbox, "Nom del node:")

    ax_radio = plt.axes([0.05, 0.05, 0.2, 0.15])
    radio = RadioButtons(ax_radio, ('Catalunya', 'Espanya', 'Europa'))

    btn_ax = plt.axes([0.75, 0.1, 0.2, 0.1])
    btn = Button(btn_ax, "Mostrar veïns")

    airspaces = {
        'Catalunya': G_cat,
        'Espanya': G_spain,
        'Europa': G_eur
    }

    state = {'region': 'Europa'}

    def set_region(label):
        state['region'] = label

    radio.on_clicked(set_region)

    def show_neighbors(event):
        G = airspaces[state['region']]
        node_name = text_box.text.strip().upper()
        node = G.nameNode(node_name)
        if not node:
            ax.set_title(f"Node {node_name} no trobat a {state['region']}")
            fig.canvas.draw_idle()
            return

        fig2, ax2 = plt.subplots(figsize=(16, 10))
        count = 0
        neighbor_names = getattr(node, 'neighbors', [])

        for seg in G.segments:
            ax2.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)
        for n in G.nodes:
            color = 'gray'
            if n == node:
                color = 'blue'
            elif n.name in neighbor_names:
                color = 'green'
            ax2.plot(n.x, n.y, 'o', color=color, markersize=3)
            ax2.text(n.x, n.y, n.name, fontsize=5)

        for n_name in neighbor_names:
            neighbor = G.nameNode(n_name)
            if not neighbor:
                continue
            ax2.annotate("",
                         xy=(neighbor.x, neighbor.y),
                         xytext=(node.x, node.y),
                         arrowprops=dict(arrowstyle="->", color='red', lw=1.5))
            mid_x = (node.x + neighbor.x) / 2
            mid_y = (node.y + neighbor.y) / 2
            ax2.text(mid_x, mid_y, f"{node.distance(neighbor):.2f}", fontsize=6, color='red')
            count += 1

        ax2.set_title(f"Veïns del node {node_name} a {state['region']} ({count} trobats)")
        ax2.axis('equal')
        plt.grid(True)
        plt.show()

    btn.on_clicked(show_neighbors)
    plt.show()

def interactiveRutaPersonalitzada():
    import matplotlib.pyplot as plt
    from matplotlib.widgets import TextBox, Button, RadioButtons    #widgets per interectuar
    import simplekml
    from tkinter import filedialog        #obre una finestra per guardar el fitxer kml
    #creacio de la finestra principal
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.55)
    ax.set_title("Crea la teva pròpia ruta")
    #creacio de caixes de text per introduir dades
    ax_origen = plt.axes([0.2, 0.45, 0.6, 0.05])
    tb_origen = TextBox(ax_origen, "Aeroport origen")

    ax_desti = plt.axes([0.2, 0.38, 0.6, 0.05])
    tb_desti = TextBox(ax_desti, "Aeroport destí")

    ax_intermedis = plt.axes([0.2, 0.31, 0.6, 0.05])
    tb_intermedis = TextBox(ax_intermedis, "Nodes intermedis (separats per comes)")

    ax_color = plt.axes([0.2, 0.24, 0.6, 0.05])
    tb_color = TextBox(ax_color, "Color de la ruta (en minúscula i en català)")
    
    #botons per escollir regió
    ax_radio = plt.axes([0.05, 0.05, 0.2, 0.15])
    radio = RadioButtons(ax_radio, ('Catalunya', 'Espanya', 'Europa'))

    ax_btn_plot = plt.axes([0.35, 0.13, 0.25, 0.06])
    btn_plot = Button(ax_btn_plot, "Mostrar ruta")

    ax_btn_export = plt.axes([0.65, 0.13, 0.25, 0.06])
    btn_export = Button(ax_btn_export, "Exportar a KML")
    #diccionari de dades
    #relaciona els noms de les regions amb els objectes Airspace corresponents
    airspaces = {'Catalunya': G_cat, 'Espanya': G_spain, 'Europa': G_eur}
    airlogics = {'Catalunya': air_cat, 'Espanya': air_spain, 'Europa': air_eur}
    
    #guarda l'estat actual(regió, camí trobat, color)
    state = {'region': 'Catalunya', 'path': [], 'color': 'blue'}
    #diccionari que converteix colors en catala a color de phyton
    colors_dict = {
        'vermell': 'red',
        'blau': 'blue',
        'groc': 'yellow',
        'verd': 'green',
        'negre': 'black',
        'gris': 'gray',
        'taronja': 'orange',
        'rosa': 'pink'
    }
    #guarda la regió triada pels Radiobuttons
    def on_region_select(label):
        state['region'] = label
    # es crida quan es fa clic a "Mostrar ruta"
    def on_plot_click(event):

        #llegeix l'origen, destí, nodes intermedis...
        region = state['region']
        G = airspaces[region]
        air = airlogics[region]

        origen = tb_origen.text.strip().upper()
        desti = tb_desti.text.strip().upper()
        intermedis = [n.strip().upper() for n in tb_intermedis.text.split(',') if n.strip()]
        color_input = tb_color.text.strip().lower()
        color = colors_dict.get(color_input, color_input)  # convierte si está en català

        #converteix l'origen i destí en nodes reals del graf
        sid = air.getSID(origen)
        star = air.getSTAR(desti)
        if not sid or not star:
            print("❌ SID o STAR invàlids")
            return
            
        #calcula la ruta cmpleta, es crea una llista amb tots els trams(origen/punts intermedis/desti)
        ruta = [sid] + intermedis + [star]
        path_total = []
        total_cost = 0
        #per cada parell de punts consecutius es calcula el cami i s'afegeix al cami total
        for i in range(len(ruta) - 1):
            subpath, cost = findShortestPath(G, ruta[i], ruta[i + 1])
            if not subpath:
                print(f"❌ No es pot connectar {ruta[i]} amb {ruta[i+1]}")
                return
            if i > 0:
                subpath = subpath[1:]
            path_total += subpath
            total_cost += cost
#Dibuixa la ruta
        state['path'] = path_total
        state['color'] = color

        fig2, ax2 = plt.subplots()
        ax2.set_title(f"Ruta personalitzada de {origen} a {desti} - Cost: {total_cost:.2f}")

        for seg in G.segments:
            ax2.plot([seg.n1.x, seg.n2.x], [seg.n1.y, seg.n2.y], color='lightgray', lw=0.5)

        for node in G.nodes:
            color_node = color if node.name in path_total else 'gray'
            ax2.plot(node.x, node.y, 'o', color=color_node, markersize=3)
            ax2.text(node.x, node.y, node.name, fontsize=6)

        for i in range(len(path_total) - 1):
            n1, n2 = G.nameNode(path_total[i]), G.nameNode(path_total[i + 1])
            ax2.annotate("", xy=(n2.x, n2.y), xytext=(n1.x, n1.y), arrowprops=dict(arrowstyle="->", color=color, lw=2))

        ax2.axis('equal')
        plt.grid(True)
        plt.show()
#Funció exporta la ruta guardada com a kml
    def on_export_click(event):
        region = state['region']
        G = airspaces[region]
#si no hi ha ruta calculada no fa res
        path = state['path']
        if not path:
            print("❌ No hi ha ruta per exportar")
            return
        #Crea les linies al fitxer kml
        kml = simplekml.Kml()
        for i in range(len(path) - 1):
            n1, n2 = G.nameNode(path[i]), G.nameNode(path[i + 1])
            kml.newlinestring(name=f"{n1.name}-{n2.name}", coords=[(n1.x, n1.y), (n2.x, n2.y)])
        #obre finestra per desar el fitxer i l'exporta
        filepath = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")], title="Guardar ruta personalitzada")
        if filepath:
            kml.save(filepath)
            print(f"✅ Ruta personalitzada exportada a {filepath}")
    #afegeix la funcionalitat als botons i mostra la interface
    radio.on_clicked(on_region_select)
    btn_plot.on_clicked(on_plot_click)
    btn_export.on_clicked(on_export_click)
    plt.show()
#Llança una interfaz una darrere l'altre, primero vecinos, accesibilidad, calculo de rutas...
# === Llançament (ordre desitjat) ===
interactivePlotNodeRegion()
interactiveReachability()
interactiveFull()
interactiveRutaPersonalitzada()
