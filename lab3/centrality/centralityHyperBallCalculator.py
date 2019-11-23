from centrality.centralityCalculator import CentralityCalculator
from cardinality.hyperloglog import HyperLogLog


class CentralityHyperBallCalculator(CentralityCalculator):
    def __init__(self, graph, max_value, num_buckets, hasher):
        super().__init__(graph)
        self.max_value = max_value
        self.num_buckets = num_buckets
        self.hasher = hasher

        # Cardinality of a node at instant t
        self.hyperloglog_balls_cumulative = []

        # List of lists of 2 elements [ [count_t, count_t+1]_1,  [count_t, count_t+1]_2, ... [count_t, count_t+1]_num_nodes]
        # Registers the counters of a node at instant t and t+1 respectively in pos 0 and pos 1 in the list
        self.hyperloglog_balls_diff = [None]*self.graph.num_of_nodes

        for node in self.graph.nodes:
            self.hyperloglog_balls_cumulative.append(HyperLogLog(max_value, num_buckets, hasher))
            self.hyperloglog_balls_diff[node.id] = []
            # Append 1 empty counter per every node in list hyperloglog_balls_diff, in position 0 of the list
            self.hyperloglog_balls_diff[node.id].append(HyperLogLog(max_value, num_buckets, hasher))
        for node in self.graph.nodes:
            adjacent_nodes = graph.get_adjacent_nodes_transpose(node)
            adjacent_nodes_id = []
            for adjacent_node in adjacent_nodes:
                adjacent_nodes_id.append(adjacent_node.id)
            self.hyperloglog_balls_cumulative[node.id].calculate_with_buckets(adjacent_nodes_id)

            # Fill the cardinality matrix to be used for centrality computation, for every node.
            # Here we fill the cardinality at instant t=1
            self.hyper_ball_cardinalities[node.id][1] = self.hyperloglog_balls_cumulative[node.id].count()
            self.hyperloglog_balls_diff[node.id][0].calculate_with_buckets(adjacent_nodes_id)
            #print(self.hyper_ball_cardinalities[node.id][0])

    def calculate_hyper_balls(self):
        t = 2
        while t < self.graph.num_of_nodes and not self.has_reached_convergence(t):
            for node in self.graph.nodes:
                # Append in position 1 an empty counter for every node list in the list self.hyperloglog_balls_diff
                self.hyperloglog_balls_diff[node.id].append(HyperLogLog(self.max_value, self.num_buckets, self.hasher))
            for node in self.graph.nodes:
                for neighbor in self.graph.get_adjacent_nodes_transpose(node):
                    self.hyperloglog_balls_diff[node.id][1].union(self.hyperloglog_balls_diff[neighbor.id][0])

                self.hyperloglog_balls_cumulative[node.id].union(self.hyperloglog_balls_diff[node.id][1])

                self.hyper_ball_cardinalities[node.id][t] = self.hyperloglog_balls_cumulative[node.id].count()
            for node in self.graph.nodes:
                self.hyperloglog_balls_diff[node.id].pop(0) # Makes the counter at pos t+1 -> pos t,

            t += 1
        print("Reached convergence in " + str(t) + " iterations")

    def has_reached_convergence(self, t):
        for i in range(len(self.hyper_ball_cardinalities)):
            if self.hyper_ball_cardinalities[i][t-1] != self.hyper_ball_cardinalities[i][t-2]:
                return False

        return True
