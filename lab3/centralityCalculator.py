import numpy as np


class CentralityCalculator:

    def __init__(self, graph):
        self.graph = graph
        self.hyper_ball_cardinalities = np.zeros((self.graph.num_of_nodes, self.graph.num_of_nodes + 1)) #a matrix that store, for each node x and for each radius r, the cardinality of the HyperBall B(x,r)
        for x in range(self.graph.num_of_nodes):
            self.hyper_ball_cardinalities[x][0] = 1

    def calculate_closeness(self, node):
        res = 0
        t = 1
        while t <= self.graph.num_of_nodes and self.hyper_ball_cardinalities[node.id][t] > 0:
            res += t*(self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        if res == 0:
            res = 1
        return 1/res


    def calculate_lin(self, node):
        res = 0
        cont = 0
        t = 1
        while t <= self.graph.num_of_nodes and self.hyper_ball_cardinalities[node.id][t] > 0:
            cont += self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1]
            res += t * (self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        if res == 0:
            res = 1
        return cont **2 / res

    def calculate_harmonic(self, node):
        res = 0
        t = 1
        while t <= self.graph.num_of_nodes and self.hyper_ball_cardinalities[node.id][t] > 0:
            res += (1/t)*(self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        return res

