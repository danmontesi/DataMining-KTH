from centralityTrueCalculator import CentralityTrueCalculator
from edge import Edge
from graph import Graph

graph = Graph(7)
graph.add_edge(Edge(graph.get_node(1), graph.get_node(0)))
graph.add_edge(Edge(graph.get_node(2), graph.get_node(1)))
graph.add_edge(Edge(graph.get_node(3), graph.get_node(1)))
graph.add_edge(Edge(graph.get_node(4), graph.get_node(3)))
graph.add_edge(Edge(graph.get_node(1), graph.get_node(5)))
graph.add_edge(Edge(graph.get_node(5), graph.get_node(6)))

centralityTrueCalculator = CentralityTrueCalculator(graph)
centralityTrueCalculator.calculate_hyper_balls()
print("Closeness centrality: ")
for i in range(7):
    print("Node " + str(i) + ": " + str(centralityTrueCalculator.calculate_closeness(graph.get_node(i))))
print("Lin centrality: ")
for i in range(7):
    print("Node " + str(i) + ": " + str(centralityTrueCalculator.calculate_lin(graph.get_node(i))))
print("Harmonic centrality: ")
for i in range(7):
    print("Node " + str(i) + ": " + str(centralityTrueCalculator.calculate_harmonic(graph.get_node(i))))