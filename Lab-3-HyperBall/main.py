from centrality.centralityHyperBallCalculator import CentralityHyperBallCalculator
from centrality.centralityTrueCalculator import CentralityTrueCalculator
from graph_reader import GraphReader
from hashers.hasher2 import Hasher2
from testers.centralityTester import CentralityTester

path = "airport_graph_dataset.txt"
graph_reader = GraphReader(path)
graph = graph_reader.read_graph()

centralityTester = CentralityTester(graph)
centralityTester.print_similarities()
