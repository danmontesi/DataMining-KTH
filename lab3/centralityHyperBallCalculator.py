from centralityCalculator import CentralityCalculator
from hyperloglog import HyperLogLog
import numpy as np

class CentralityHyperBallCalculator(CentralityCalculator):
    def __init__(self, graph, max_value, num_buckets, hasher):
        super().__init__(graph)
        self.max_value = max_value
        self.num_buckets = num_buckets
        self.hasher = hasher
        self.hyperloglog_balls = []
        self.hyperloglog_balls_diff = [None]*self.graph.num_of_nodes
        for node in self.graph.nodes:
            self.hyperloglog_balls.append(HyperLogLog(max_value, num_buckets, hasher))
            self.hyperloglog_balls_diff[node.id] = []
            self.hyperloglog_balls_diff[node.id].append(HyperLogLog(max_value, num_buckets, hasher))
        for node in self.graph.nodes:
            adjacent_nodes = graph.get_adjacent_nodes_transpose(node)
            adjacent_nodes_id = []
            for adjacent_node in adjacent_nodes:
                adjacent_nodes_id.append(adjacent_node.id)
            self.hyperloglog_balls[node.id].calculate_with_buckets(adjacent_nodes_id)
            self.hyper_ball_cardinalities[node.id][1] = self.hyperloglog_balls[node.id].count()
            self.hyperloglog_balls_diff[node.id][0].calculate_with_buckets(adjacent_nodes_id)
            #print(self.hyper_ball_cardinalities[node.id][0])

    def calculate_hyper_balls(self):
        for t in range(2, self.graph.num_of_nodes):
            for node in self.graph.nodes:
                self.hyperloglog_balls_diff[node.id].append(HyperLogLog(self.max_value, self.num_buckets, self.hasher))
            for node in self.graph.nodes:
                for neighbor in self.graph.get_adjacent_nodes_transpose(node):
                    self.hyperloglog_balls_diff[node.id][1].union(self.hyperloglog_balls_diff[neighbor.id][0])
                self.hyperloglog_balls[node.id].union(self.hyperloglog_balls_diff[node.id][1])
                self.hyper_ball_cardinalities[node.id][t] = self.hyperloglog_balls[node.id].count()
            for node in self.graph.nodes:
                self.hyperloglog_balls_diff[node.id].pop(0)



