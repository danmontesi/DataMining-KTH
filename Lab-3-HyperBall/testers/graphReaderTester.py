from abc import ABC

from graph_reader import GraphReader
from testers import multiset


class GraphReaderTester(ABC):

    def __init__(self, path):
        self.path = path


    def test(self):
        """
        Generate a multiset having size self.multiset_size containing randomic elements
        :return: list[int]
        """
        graph_reader = GraphReader(self.path)
        test_graph = graph_reader.read_graph()

        print("The graph has {} nodes and {} edges".format(len(test_graph.nodes), len(test_graph.edges) ))
        return multiset




gt = GraphReaderTester("../airport_graph_dataset.txt")
gt.test()