import tkinter as tk
from tkinter import simpledialog, messagebox

from graph import Graph
from node import Node

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualizer")
        self.master.geometry("600x500")

        self.graph = Graph()
        self.mode = None
        self.selected_node = None
        self.shortest_path_edges = []
        self.reachable_nodes = []

        # Botones en vertical a la izquierda
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.LEFT, padx=5, pady=5)

        buttons = [
            ("Add Node", self.add_node_mode),
            ("Add Segment", self.add_segment_mode),
            ("Delete Node", self.delete_node_mode),
            ("Find Shortest Path", self.find_shortest_path),
            ("Show Reachability", self.activate_reachability_mode),
            ("Clear Graph", self.clear_graph),
        ]

        for text, cmd in buttons:
            tk.Button(button_frame, text=text, command=cmd, width=20).pack(pady=2)

        # Canvas a la derecha
        self.canvas = tk.Canvas(master, width=450, height=400, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=5)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def add_node_mode(self):
        self.mode = "add_node"

    def add_segment_mode(self):
        self.mode = "add_segment"
        self.selected_node = None

    def delete_node_mode(self):
        self.mode = "delete_node"

    def activate_reachability_mode(self):
        self.mode = "reachability"
        self.reachable_nodes = []
        self.shortest_path_edges = []

    def clear_graph(self):
        self.graph = Graph()
        self.draw_graph()

    def find_shortest_path(self):
        start = simpledialog.askstring("Start", "Start node name:")
        end = simpledialog.askstring("End", "End node name:")
        if start and end:
            result = self.graph.findShortestPath(start, end)
            if result:
                path_names, cost = result
                self.shortest_path_edges = []
                for i in range(len(path_names) - 1):
                    src = self.graph.nameNode(path_names[i])
                    dst = self.graph.nameNode(path_names[i + 1])
                    self.shortest_path_edges.append((src.name, dst.name))
                msg = " → ".join(path_names)
                messagebox.showinfo("Path Found", f"{msg}\nTotal Cost: {round(cost, 2)}")
                self.draw_graph()
            else:
                messagebox.showwarning("No Path", "No path found between nodes.")

    def reachable_from(self, origin):
        node = next((n for n in self.graph.nodes if n.name == origin), None)
        if not node:
            return []
        visited = set()
        stack = [node]
        while stack:
            current = stack.pop()
            if current.name not in visited:
                visited.add(current.name)
                stack.extend(current.neighbors)
        return [n for n in self.graph.nodes if n.name in visited]

    def on_canvas_click(self, event):
        scale, margin = 40, 40
        x = (event.x - margin) / scale
        y = (event.y - margin) / scale

        if self.mode == "add_node":
            name = f"N{len(self.graph.nodes)}"
            node = Node(name, x, y)
            self.graph.addNode(node)
            self.draw_graph()

        elif self.mode == "add_segment":
            clicked = self.get_node_at(x, y)
            if clicked:
                if not self.selected_node:
                    self.selected_node = clicked
                else:
                    self.graph.addSegment(self.selected_node.name, clicked.name)
                    self.selected_node = None
                    self.draw_graph()

        elif self.mode == "delete_node":
            clicked = self.get_node_at(x, y)
            if clicked:
                self.graph.nodes = [n for n in self.graph.nodes if n != clicked]
                self.graph.segments = [
                    s for s in self.graph.segments
                    if s.n1 != clicked and s.n2 != clicked
                ]
                self.draw_graph()

        elif self.mode == "reachability":
            clicked = self.get_node_at(x, y)
            if clicked:
                self.reachable_nodes = self.reachable_from(clicked.name)
                names = ", ".join(n.name for n in self.reachable_nodes)
                messagebox.showinfo("Reachable Nodes", f"From {clicked.name} you can reach:\n{names}")
                self.draw_graph()

    def get_node_at(self, x, y, threshold=0.5):
        for node in self.graph.nodes:
            if abs(node.x - x) < threshold and abs(node.y - y) < threshold:
                return node
        return None

    def draw_graph(self):
        self.canvas.delete("all")
        scale, margin = 40, 40
        r = 5

        for seg in self.graph.segments:
            x1 = seg.n1.x * scale + margin
            y1 = seg.n1.y * scale + margin
            x2 = seg.n2.x * scale + margin
            y2 = seg.n2.y * scale + margin

            # Comparación doble dirección por nombre
            is_shortest = (seg.n1.name, seg.n2.name) in self.shortest_path_edges or \
                          (seg.n2.name, seg.n1.name) in self.shortest_path_edges

            color = "red" if is_shortest else "gray"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, arrow=tk.LAST)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my - 10, text=f"{round(seg.cost, 2)}", fill=color)

        for node in self.graph.nodes:
            x = node.x * scale + margin
            y = node.y * scale + margin
            fill = "green" if node in self.reachable_nodes else "black"
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill)
            self.canvas.create_text(x + 10, y, text=node.name, anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
