import numpy as np

from centralityCalculator import CentralityCalculator


class CentralityTrueCalculator(CentralityCalculator):
    """
    This class implements methods to compute the exact values of Closeness, Lin and Harmonic centrality.
    """

    def __init__(self, graph):
        super().__init__(graph)

    def calculate_closeness(self, node):
        res = 0
        t = 1
        while self.hyper_ball_cardinalities[node.id][t] > 0:
            res += t*(self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        if res == 0:
            res = 1
        return 1/res


    def calculate_lin(self, node):
        res = 0
        cont = 0
        t = 1
        while self.hyper_ball_cardinalities[node.id][t] > 0:
            cont += self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1]
            res += t * (self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        if res == 0:
            res = 1
        return cont **2 / res

    def calculate_harmonic(self, node):
        res = 0
        t = 1
        while self.hyper_ball_cardinalities[node.id][t] > 0:
            res += (1/t)*(self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        return res

    def bfs(self, start):
        """
        Breadth-first search algorithm to find the HyperBalls centered in start.
        :param start: Starting Node of the BFS
        """
        queue = []
        queue.append(start)
        dist = np.ones(self.graph.num_of_nodes, dtype=int)*(self.graph.num_of_nodes + 1)
        dist[start.id] = 0
        while len(queue) > 0:
            current_node = queue.pop()
            adjacent_nodes = self.graph.get_adjacent_nodes_transpose(current_node)
            for node in adjacent_nodes:
                if dist[node.id] == self.graph.num_of_nodes + 1:
                    dist[node.id] = dist[current_node.id] + 1
                    if self.hyper_ball_cardinalities[start.id][dist[node.id]] == 0: #From the definition of HyperBall, the HyperBall of radius r contains also all the nodes of the Hyperball of radius r - 1
                        self.hyper_ball_cardinalities[start.id][dist[node.id]] = self.hyper_ball_cardinalities[start.id][dist[node.id] - 1]
                    self.hyper_ball_cardinalities[start.id][dist[node.id]] += 1
                    queue.append(node)



    def calculate_hyper_balls(self):
        for node in self.graph.nodes:
            self.bfs(node)
