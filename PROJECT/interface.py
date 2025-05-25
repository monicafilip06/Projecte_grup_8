import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from graph import Graph
from node import Node
import pickle

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualizer")
        self.master.geometry("700x500")

        self.graph = Graph()
        self.mode = None
        self.selected_node = None
        self.shortest_path_edges = []
        self.reachable_nodes = []

        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.LEFT, padx=5, pady=5)

        buttons = [
            ("Show Example Graph", self.show_example_graph),
            ("Show Custom Graph", self.show_custom_graph),
            ("Load from File", self.load_graph_from_file),
            ("Save to File", self.save_graph_to_file),
            ("Add Node", self.add_node_mode),
            ("Add Segment", self.add_segment_mode),
            ("Delete Node", self.delete_node_mode),
            ("Delete Segment", self.delete_segment_mode),
            ("Find Shortest Path", self.find_shortest_path),
            ("Show Reachability", self.activate_reachability_mode),
            ("Clear Graph", self.clear_graph),
        ]

        for text, cmd in buttons:
            tk.Button(button_frame, text=text, command=cmd, width=25).pack(pady=2)

        self.canvas = tk.Canvas(master, width=500, height=450, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=5)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_graph(self):
        self.canvas.delete("all")
        for s in self.graph.segments:
            x1, y1 = s.origin.x * 20, s.origin.y * 20
            x2, y2 = s.destination.x * 20, s.destination.y * 20
            color = "red" if (s.origin.name, s.destination.name) in self.shortest_path_edges else "black"
            self.canvas.create_line(x1, y1, x2, y2, fill=color)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(round(s.cost, 2)), fill="blue")

        for n in self.graph.nodes:
            x, y = n.x * 20, n.y * 20
            color = "green" if n.name in self.reachable_nodes else "gray"
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color)
            self.canvas.create_text(x+10, y, text=n.name, anchor=tk.W)

    def on_canvas_click(self, event):
        x, y = event.x / 20, event.y / 20
        if self.mode == "add_node":
            name = simpledialog.askstring("Node Name", "Enter name:")
            if name:
                self.graph.AddNode(Node(name, x, y))
                self.draw_graph()
        elif self.mode == "add_segment":
            node = self.graph.getClosest(x, y)
            if self.selected_node:
                self.graph.AddSegment(self.selected_node.name, node.name)
                self.selected_node = None
                self.draw_graph()
            else:
                self.selected_node = node
        elif self.mode == "delete_node":
            node = self.graph.getClosest(x, y)
            self.graph.deleteNode(node.name)
            self.draw_graph()
        elif self.mode == "delete_segment":
            node = self.graph.getClosest(x, y)
            if self.selected_node:
                self.graph.deleteSegment(self.selected_node.name, node.name)
                self.selected_node = None
                self.draw_graph()
            else:
                self.selected_node = node
        elif self.mode == "reachability":
            node = self.graph.getClosest(x, y)
            self.reachable_nodes = self.graph.reachability(node.name)
            self.draw_graph()

    def add_node_mode(self):
        self.mode = "add_node"

    def add_segment_mode(self):
        self.mode = "add_segment"
        self.selected_node = None

    def delete_node_mode(self):
        self.mode = "delete_node"

    def delete_segment_mode(self):
        self.mode = "delete_segment"
        self.selected_node = None

    def activate_reachability_mode(self):
        self.mode = "reachability"
        self.reachable_nodes = []
        self.shortest_path_edges = []

    def find_shortest_path(self):
        start = simpledialog.askstring("Start", "Start node name:")
        end = simpledialog.askstring("End", "End node name:")
        if start and end:
            path = self.graph.findShortestPath(start, end)
            if path:
                self.shortest_path_edges = [(path[i].name, path[i+1].name) for i in range(len(path)-1)]
                self.draw_graph()
            else:
                messagebox.showinfo("Info", "No path found.")

    def clear_graph(self):
        self.graph = Graph()
        self.draw_graph()

    def show_example_graph(self):
        self.graph = self.graph.createGraph_1()
        self.draw_graph()

    def show_custom_graph(self):
        self.graph = self.graph.createGraph_2()
        self.draw_graph()

    def save_graph_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pkl")
        if filename:
            with open(filename, 'wb') as f:
                pickle.dump(self.graph, f)

