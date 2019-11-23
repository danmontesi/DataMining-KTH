from centrality.centralityHyperBallCalculator import CentralityHyperBallCalculator
from centrality.centralityTrueCalculator import CentralityTrueCalculator
from graph_dir.edge import Edge
from graph_dir.graph import Graph
from graph_reader import GraphReader
from hashers.hasher2 import Hasher2



num_of_nodes = 400

"""graph = Graph(num_of_nodes)
graph.add_edge(Edge(graph.get_node(1), graph.get_node(2)))
graph.add_edge(Edge(graph.get_node(2), graph.get_node(3)))
graph.add_edge(Edge(graph.get_node(3), graph.get_node(4)))
graph.add_edge(Edge(graph.get_node(4), graph.get_node(5)))
graph.add_edge(Edge(graph.get_node(5), graph.get_node(6)))
graph.add_edge(Edge(graph.get_node(6), graph.get_node(0)))"""

"""graph = Graph(num_of_nodes)
graph.add_edge(Edge(graph.get_node(1), graph.get_node(0)))
graph.add_edge(Edge(graph.get_node(2), graph.get_node(1)))
graph.add_edge(Edge(graph.get_node(3), graph.get_node(1)))
graph.add_edge(Edge(graph.get_node(4), graph.get_node(3)))
graph.add_edge(Edge(graph.get_node(1), graph.get_node(5)))
graph.add_edge(Edge(graph.get_node(5), graph.get_node(6)))"""


graph_r = GraphReader("airport_graph_dataset.txt")
graph = graph_r.read_graph()
centralityTrueCalculator = CentralityTrueCalculator(graph)
centralityTrueCalculator.calculate_hyper_balls()

centralityHyperBallCalculator = CentralityHyperBallCalculator(graph, 2**32-1, 32, Hasher2(2**32))
centralityHyperBallCalculator.calculate_hyper_balls()

print("Closeness centrality: ")
for i in range(7):
    print("Node " + str(i) + ": " + str(centralityTrueCalculator.calculate_closeness(graph.get_node(i))) + " approximate with " + str(centralityHyperBallCalculator.calculate_closeness(graph.get_node(i))))
print("Lin centrality: ")
for i in range(7):
    print("Node " + str(i) + ": " + str(centralityTrueCalculator.calculate_lin(graph.get_node(i))) + " approximate with " + str(centralityHyperBallCalculator.calculate_lin(graph.get_node(i))))
print("Harmonic centrality: ")
for i in range(7):
    print("Node " + str(i) + ": " + str(centralityTrueCalculator.calculate_harmonic(graph.get_node(i))) + " approximate with " + str(centralityHyperBallCalculator.calculate_harmonic(graph.get_node(i))))

"""closeness_correct = []
closeness_approximated = []
for i in range(num_of_nodes):
    closeness_correct.append((centralityTrueCalculator.calculate_closeness(graph.get_node(i)), i))
    closeness_approximated.append((centralityHyperBallCalculator.calculate_closeness(graph.get_node(i)), i))

closeness_correct.sort(reverse=True)
closeness_approximated.sort(reverse=True)

print(closeness_correct)
print(closeness_approximated)"""

harmonic_correct = []
harmonic_approximated = []
for i in range(num_of_nodes):
    harmonic_correct.append((centralityTrueCalculator.calculate_closeness(graph.get_node(i)), i))
    harmonic_approximated.append((centralityHyperBallCalculator.calculate_closeness(graph.get_node(i)), i))

harmonic_correct.sort(reverse=True)
harmonic_approximated.sort(reverse=True)

print(harmonic_correct)
print(harmonic_approximated)

for i in range(num_of_nodes):
    print(str(centralityTrueCalculator.hyper_ball_cardinalities[2][i]) + " " + str(centralityHyperBallCalculator.hyper_ball_cardinalities[2][i]))
