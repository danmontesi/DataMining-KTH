from abc import ABC
import random
from random import randint

class Graph(ABC):
    """
    Graph having nodes and edges as sets
    @:param
    node: set of tuples (id, value)
    edges: set of tuples (id_source, id_dest)
    """
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_nodes(self, node):
        if len(node) == 2 and isinstance(node[0], int) and isinstance(node[1], int):
            self.nodes.add(node)
        else:
            print("Not correct format")

    def generate_random(self, nodes_num, edges_num):
        for i in range(nodes_num):
            self.add_nodes((randint(0,4023345), randint(0,4023345)))

        nodes_list = list(self.nodes)
        for i in range(edges_num):
            self.edges.add((nodes_list[randint(0,len(nodes_list))][1],
                            nodes_list[randint(0,len(nodes_list))][1]))
