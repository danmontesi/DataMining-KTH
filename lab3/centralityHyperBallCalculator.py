from centralityCalculator import CentralityCalculator
import numpy as np

class CentralityHyperBallCalculator(CentralityCalculator):
    def __init__(self, graph):
        super().__init__(graph)

    def union(self, source_cardinalities, neighbor_cardinality):
        # Function that get the max from each counter

        # TODO with flajolet
        return source_cardinalities

    def calculate_hyper_balls(self):
        nodes = [n_id for n_id in range(
            self.graph.nodes)]

        # Instead of saving counters in a disk, I save in another matrix for now
        self.disk_cardinalities = np.zeros((self.graph.num_of_nodes, self.graph.num_of_nodes + 1))
        for n in nodes:
            self.hyper_ball_cardinalities[n][n] = 1

        t = 0
        while not self.has_reached_stopping_condition():

            for curr_node in self.graph.nodes:
                curr_node_card = self.hyper_ball_cardinalities[curr_node]

                # Getting the nodes whose destination is curr_node
                adjacents = self.graph.get_adjacent_nodes_transpose(curr_node)

                for el_id in adjacents:
                    curr_node_card[el_id] = self.union(curr_node_card, self.hyper_ball_cardinalities[el_id.id])

                # write new curr_counter on disk
                self.disk_cardinalities[curr_node.id] = curr_node_card

            for id in range(len(self.disk_cardinalities)):
                self.hyper_ball_cardinalities[id] = self.disk_cardinalities[id]

            t += 1

        print("Convergence reached at t = ", str(t))

    def has_reached_stopping_condition(self):
        """
        Chech that the t step is equal to the old step cardinalities
        :return:
        """
        for i in range(self.hyper_ball_cardinalities):
            for j in range(self.hyper_ball_cardinalities[i]):
                if self.hyper_ball_cardinalities[i][j] != self.disk_cardinalities[i][j]:
                    return False
        return True

