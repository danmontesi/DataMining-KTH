from abc import ABC
import pandas as pd

from graph_dir.edge import Edge
from graph_dir.graph import Graph
from graph_dir.node import Node


class GraphReader(ABC):
    def __init__(self, path, is_undirected=True):
        self.path = path
        self.is_undirected = is_undirected

    def read_graph(self):
        """
        Dataset is in txt each line is in the format "id_src, id_dst, edge-weigth"
        Since we are not interested on the weight, we get only the first two attributes
        We remove the last element in the list splitted [:-1]
        :return:
        """
        filename = self.path
        edges = []
        with open(filename) as f:
            for line in f:
                edges.append([int(n) for n in line.strip().split()[:-1]])

        nodes = []
        for e in edges[:-1]:
            nodes.append(e[0])
            nodes.append(e[1])

        nodes = list(set(nodes))

        myGraph = Graph(len(nodes))
        for el in edges[:-1]:
            curr_edge = Edge(Node(el[0]), Node(el[1]))
            myGraph.add_edge(curr_edge)

            if self.is_undirected:
                curr_edge_inv = Edge(Node(el[1]), Node(el[0]))
                myGraph.add_edge(curr_edge_inv)

        return myGraph