from centrality.centralityHyperBallCalculator import CentralityHyperBallCalculator
from centrality.centralityTrueCalculator import CentralityTrueCalculator
from graph_dir.edge import Edge
from graph_dir.graph import Graph
from graph_reader import GraphReader
from hashers.hasher2 import Hasher2


class CentralityTester():

    def __init__(self, graph):
        self.graph = graph
        self.num_of_nodes = len(self.graph.nodes)

        self.centralityTrueCalculator = CentralityTrueCalculator(self.graph)
        self.centralityTrueCalculator.calculate_hyper_balls()

        self.centralityHyperBallCalculator = CentralityHyperBallCalculator(self.graph, 2 ** 32 - 1, 32, Hasher2(2 ** 32))
        self.centralityHyperBallCalculator.calculate_hyper_balls()


    def print_similarities(self):
        print("Closeness centrality: ")
        for i in range(self.num_of_nodes):
            print("Node " + str(i) + ": " + str(self.centralityTrueCalculator.calculate_closeness(self.graph.get_node(i))) + " approximate with " + str(self.centralityHyperBallCalculator.calculate_closeness(self.graph.get_node(i))))
        print("Lin centrality: ")
        for i in range(self.num_of_nodes):
            print("Node " + str(i) + ": " + str(self.centralityTrueCalculator.calculate_lin(self.graph.get_node(i))) + " approximate with " + str(self.centralityHyperBallCalculator.calculate_lin(self.graph.get_node(i))))
        print("Harmonic centrality: ")
        for i in range(self.num_of_nodes):
            print("Node " + str(i) + ": " + str(self.centralityTrueCalculator.calculate_harmonic(self.graph.get_node(i))) + " approximate with " + str(self.centralityHyperBallCalculator.calculate_harmonic(self.graph.get_node(i))))

    def compare_sorted_closeness(self):
        closeness_correct = []
        closeness_approximated = []
        for i in range(self.num_of_nodes):
            closeness_correct.append((self.centralityTrueCalculator.calculate_closeness(self.graph.get_node(i)), i))
            closeness_approximated.append((self.centralityHyperBallCalculator.calculate_closeness(self.graph.get_node(i)), i))

        closeness_correct.sort(reverse=True)
        closeness_approximated.sort(reverse=True)

        print(closeness_correct)
        print(closeness_approximated)

    def compate_sorted_harmonic(self):
        harmonic_correct = []
        harmonic_approximated = []
        for i in range(self.num_of_nodes):
            harmonic_correct.append((self.centralityTrueCalculator.calculate_closeness(self.graph.get_node(i)), i))
            harmonic_approximated.append((self.centralityHyperBallCalculator.calculate_closeness(self.graph.get_node(i)), i))

        harmonic_correct.sort(reverse=True)
        harmonic_approximated.sort(reverse=True)

        print(harmonic_correct)
        print(harmonic_approximated)

    def compare_sorted_lin(self):
        lin_correct = []
        lin_approximated = []
        for i in range(self.num_of_nodes):
            lin_correct.append((self.centralityTrueCalculator.calculate_lin(self.graph.get_node(i)), i))
            lin_approximated.append((self.centralityHyperBallCalculator.calculate_lin(self.graph.get_node(i)), i))

        lin_correct.sort(reverse=True)
        lin_approximated.sort(reverse=True)

        print(lin_correct)
        print(lin_approximated)

    def compare_cumulative_cardinalities(self, node):
        for i in range(self.num_of_nodes):
            if self.centralityTrueCalculator.hyper_ball_cardinalities[node][i] == 0:
                break
            print(str(self.centralityTrueCalculator.hyper_ball_cardinalities[node][i]) + " " + str(self.centralityHyperBallCalculator.hyper_ball_cardinalities[node][i]))


def test():
    num_of_nodes = 7

    graph = Graph(num_of_nodes)
    graph.add_edge(Edge(graph.get_node(1), graph.get_node(2)))
    graph.add_edge(Edge(graph.get_node(2), graph.get_node(3)))
    graph.add_edge(Edge(graph.get_node(3), graph.get_node(4)))
    graph.add_edge(Edge(graph.get_node(4), graph.get_node(5)))
    graph.add_edge(Edge(graph.get_node(5), graph.get_node(6)))
    graph.add_edge(Edge(graph.get_node(6), graph.get_node(0)))

    """graph = Graph(num_of_nodes)
    graph.add_edge(Edge(graph.get_node(1), graph.get_node(0)))
    graph.add_edge(Edge(graph.get_node(2), graph.get_node(1)))
    graph.add_edge(Edge(graph.get_node(3), graph.get_node(1)))
    graph.add_edge(Edge(graph.get_node(4), graph.get_node(3)))
    graph.add_edge(Edge(graph.get_node(1), graph.get_node(5)))
    graph.add_edge(Edge(graph.get_node(5), graph.get_node(6)))"""

    centralityTester = CentralityTester(graph)
    centralityTester.print_similarities()
    centralityTester.compare_sorted_closeness()
    centralityTester.compare_sorted_lin()
    centralityTester.compate_sorted_harmonic()
    centralityTester.compare_cumulative_cardinalities(2)


#test()