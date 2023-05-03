from tkinter import *
import random
import networkx as nx
import matplotlib.pyplot as plt
from distinctipy import distinctipy

graph_instances = []
# Generating random colors to assign FirstFit vertices
available_colors = distinctipy.get_colors(100)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////
########### --------------------------- Graph Generator [START] ------------------------- #############
def diffset(i, j, setlist):
    for s in setlist:
        if i in s and j in s:
            return False
        if i in s or j in s:
            return True
    return False


def kcgg(n, k, p):
    graph = [set() for i in range(n)]
    v = list(range(n))
    random.shuffle(v)
    setlist = [set() for i in range(k)]
    for i in range(k):
        newset = set()
        val = i
        while val < n:
            newset.add(v[val])
            val += k
        setlist[i] = newset
    # for i in setlist:
    #     print(i)
    for i in range(n):
        for j in range(i + 1, n):
            if diffset(i, j, setlist) and random.random() < p:
                graph[i].add(j)
                graph[j].add(i)
    return convert(graph)


def convert(graph):
    newgraph = []
    for i in range(len(graph)):
        newgraph.append(list(graph[i]))
    return newgraph


########### --------------------------- Graph Generator [END] ------------------------- #############
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
########### ---------------------------    FirstFit [START]   ------------------------- #############
class FirstFit:
    colors = {}
    color_count = 1

    def __init__(self):
        self.colors = {}
        self.color_count = 1

    def add_vertex(self, vertex, sub_graph):
        used_colors = {self.colors[neighbor] for neighbor in sub_graph[vertex] if neighbor in self.colors}
        for i in range(self.color_count):
            if i not in used_colors:
                self.colors[vertex] = i
                # print("vertex = " + str(vertex) + " color = " + str(self.colors[vertex]))
                break
        if vertex not in self.colors:
            self.colors[vertex] = self.color_count
            # print("vertex = " + str(vertex) + " color = " + str(self.colors[vertex]))
            self.color_count += 1

    def get_unique_colors(self):
        unique_used_colors = {}
        for v in self.colors:
            unique_used_colors[self.colors[v]] = 1
        return len(unique_used_colors)

    def get_colors(self):
        return self.colors


########### ---------------------------     FirstFit [END]    ------------------------- #############
# /////////////////////////////////////////////////////////////////////////////////////////////////////////

# /////////////////////////////////////////////////////////////////////////////////////////////////////////
########### ---------------------------    CBIP [START]   ------------------------- #############
class cbipAlgo:
    def __init__(self, graph):
        self.sets = [set(), set()]
        self.graph = graph
        self.colors = []
        self.visited = []
        self.part_graph = []

    def possibleBipartition(self, V, G):
        # To store graph as adjacency list in edges
        edges = [[] for _ in range(V + 1)]
        for u, v in G:
            edges[u].append(v)
            edges[v].append(u)

        visited = [False] * (V + 1)
        res = True
        for i in range(1, V + 1):
            if not visited[i]:
                res = res and self.bipartite(edges, V, i, visited)

        return res

    def bipartite(self, edges, V, i, visited):
        if V == 0:
            return True

        pending = []

        # Inserting source vertex in U(set[0])
        self.sets[0].add(i)

        # Enqueue source vertex
        pending.append(i)
        while pending:

            # Dequeue current vertex
            current = pending.pop()

            # Mark the current vertex true
            visited[current] = True

            # Finding the set of
            # current vertex(parent vertex)
            currentSet = 0 if current in self.sets[0] else 1

            for neighbor in edges[current]:

                # If not present
                # in any of the set
                if neighbor not in self.sets[0] and neighbor not in self.sets[1]:

                    # Inserting in opposite
                    # of current vertex
                    self.sets[1 - currentSet].add(neighbor)
                    pending.append(neighbor)

                # Else if present in the same
                # current vertex set the partition
                # is not possible
                elif neighbor in self.sets[currentSet]:
                    return False

        return True

    def generate_sets(self, vertex, size, edge_graph):
        self.sets[0] = set()
        self.sets[1] = set()
        flag = 1
        result = []
        if self.possibleBipartition(len(self.part_graph), edge_graph):
            new_set = set()
            for elem in self.sets[0]:
                new_set.add(elem - 1)

            result.append(new_set)

            new_set = set()

            for s in self.sets[1]:
                new_set.add(s - 1)
                if s - 1 == vertex: flag = 0
            result.append(new_set)
        return result[flag]

    def convert_to_edges(self, part_graph):
        edge_graph = []
        for u in range(len(part_graph)):
            for v in part_graph[u]:
                if u <= v:
                    edge_graph.append([u + 1, v + 1])
        return edge_graph

    def setup(self, vertices):
        self.colors = list(range(vertices))

        for i in range(0, vertices):
            self.colors[i] = float('inf')
        self.visited = [False] * vertices

    def getMinColor(self, color):
        n = len(color)
        for i in range(1, n + 2):
            if i not in color:
                return i
        return -1

    def assignColor(self, vertex, part):
        colors_x = set()
        for i in part:
            colors_x.add(self.colors[i])
        self.colors[vertex] = self.getMinColor(colors_x)

    def generatePartialGraph(self, vertex, nbrs):
        self.visited[vertex] = True
        hashset = set()
        for nbr in nbrs:
            if self.visited[nbr]:
                hashset.add(nbr)
                old = self.part_graph[nbr]
                old.add(vertex)
                self.part_graph[nbr] = old
        self.part_graph.insert(vertex, hashset)

    def total_colours(self, color):
        max = 0
        for i in color:
            if i > max:
                max = i
        return max

    def cbip(self, vertex, nbrs):
        self.generatePartialGraph(vertex, nbrs)
        edge_graph = self.convert_to_edges(self.part_graph)
        required_partition = self.generate_sets(vertex, len(self.part_graph), edge_graph)

        self.assignColor(vertex, required_partition)

    def get_unique_colors(self):
        return len(set(self.colors))

    def get_colors(self):
        return self.colors


########### ---------------------------    CBIP [END]   ------------------------- #############
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
########### ----------    Display Graph (k-colorable + FirstFit) [START]   ----------- #############
def display_graph(graph):
    plt.close()

    # Displaying graph generated by graph generator
    global available_colors
    visual = []
    for u in range(len(graph)):
        for v in graph[u]:
            visual.append([u, v])
    G = nx.Graph()
    G.add_nodes_from([i for i in range(len(graph))])
    G.add_edges_from(visual)
    plt.figure("Graph generated by graph generator")
    nx.draw(G, with_labels=True)

    # Displaying graph generated by FirstFit
    visited = {}
    sub_graph = [[] for _ in range(len(graph))]
    first_fit = FirstFit()

    for u in range(len(graph)):
        visited[u] = 1
        for v in graph[u]:
            if v in visited:
                sub_graph[u].append(v)
                sub_graph[v].append(u)
        first_fit.add_vertex(u, sub_graph)
    colors = first_fit.get_colors()
    color_map = []

    G = nx.Graph()
    G.add_nodes_from([i for i in range(len(graph))])
    G.add_edges_from(visual)
    for i in range(len(graph)):
        color_map.append(available_colors[colors[i]])
    plt.figure("Total colors (FirstFit): " + str(first_fit.get_unique_colors()))
    nx.draw(G, node_color=color_map, with_labels=True)

    # Displaying graph generated by CBIP
    color_map = []
    cbip = cbipAlgo(graph)
    cbip.setup(len(graph))
    for j in range(len(graph)):
        cbip.cbip(j, graph[j])
    colors = cbip.get_colors()

    G = nx.Graph()
    G.add_nodes_from([i for i in range(len(graph))])
    G.add_edges_from(visual)
    for i in range(len(graph)):
        color_map.append(available_colors[colors[i]])
    plt.figure("Total colors (CBIP): " + str(cbip.get_unique_colors()))
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()


########### ---------   Display Graph (k-colorable + FirstFit) [END]  ------ #############
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
########### ----------    Main GUI Logic [START]   ------------- #############
def callback_generate_graph():
    global graph_instances
    graph_instances = []
    k = int(input_k.get())
    n = int(input_n.get())
    N = int(input_N.get())
    for _ in range(N):
        p = random.random()
        graph_instances.append(kcgg(n, k, p).copy())


def callback_firstfit():
    global label_result_firstfit, graph_instances
    if (len(graph_instances) == 0):
        label_result_firstfit.config(text="Please generate the graph first")
        return
    k = int(input_k.get())
    N = int(input_N.get())
    total_sum = 0

    # Passing graph in online fashion to FirstFit
    for i in range(N):
        graph = graph_instances[i]
        visited = {}
        sub_graph = [[] for _ in range(len(graph))]
        first_fit = FirstFit()

        for u in range(len(graph)):
            visited[u] = 1
            for v in graph[u]:
                if v in visited:
                    sub_graph[u].append(v)
                    sub_graph[v].append(u)
            # Adding each vertex with it's subgraph to FirstFit
            first_fit.add_vertex(u, sub_graph)

        unique_used_colors = first_fit.get_unique_colors()
        total_sum += (unique_used_colors / k)
    label_result_firstfit.config(text="Average Competitive ratio for FirstFit: " + str(total_sum / N))


def callback_cbip():
    global label_result_cbip, graph_instances
    if (len(graph_instances) == 0):
        label_result_firstfit.config(text="Please generate the graph first")
        return
    k = int(input_k.get())
    n = int(input_n.get())
    N = int(input_N.get())
    if (k != 2):
        label_result_cbip.config(text="Cannot run cbip on " + str(k) + " colourable graph")
        return
    total_sum = 0
    for i in range(N):
        graph = graph_instances[i]
        cbip = cbipAlgo(graph)
        cbip.setup(n)
        for j in range(len(graph)):
            cbip.cbip(j, graph[j])
        unique_used_colors = cbip.get_unique_colors()
        # print(unique_used_colors)
        total_sum += (unique_used_colors / k)
    label_result_cbip.config(text="Average Competitive ratio for CBIP: " + str(total_sum / N))


def callback_display_graph():
    global graph_instances, label_result_display_graph
    n = int(input_n.get())
    if (n > 100):
        label_result_display_graph.config(text="Please select n <= 100 for better visual")
        return
    label_result_display_graph.config(text="")
    graph = graph_instances[0]
    display_graph(graph)


master = Tk()
master.wm_title("Online Graph Coloring")

label_k = Label(master, text="Enter k", height=4)
label_k.pack()
input_k = Entry(master, width=50)
input_k.pack()

label_n = Label(master, text="Enter n", height=4)
label_n.pack()
input_n = Entry(master, width=50)
input_n.pack()

label_N = Label(master, text="Enter N", height=4)
label_N.pack()
input_N = Entry(master, width=50)
input_N.pack()

label_result_firstfit = Label(master, text="", height=4)
label_result_cbip = Label(master, text="", height=4)
label_result_display_graph = Label(master, text="", height=4)
label_result_firstfit.pack()
label_result_cbip.pack()
label_result_display_graph.pack()

b1 = Button(master, text="Online coloring by FirstFit", command=callback_firstfit)
b2 = Button(master, text="Online coloring by CBIP", command=callback_cbip)
b3 = Button(master, text="Generate graph", command=callback_generate_graph)
b4 = Button(master, text="Display graph", command=callback_display_graph)

b3.pack()
b4.pack()
b1.pack()
b2.pack()

master.mainloop()
########### ------------    Main GUI Logic [END]   ------------ #############
