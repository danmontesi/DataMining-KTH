import numpy as np


class CentralityCalculator:

    def __init__(self, graph):
        self.graph = graph
        self.hyper_ball_cardinalities = np.zeros((self.graph.num_of_nodes, self.graph.num_of_nodes + 1)) #a matrix that store, for each node x and for each radius r, the cardinality of the HyperBall B(x,r)

    def calculate_closeness(self, node):
        return

    def calculate_lin(self, node):
        return

    def calculate_harmonic(self, node):
        return

