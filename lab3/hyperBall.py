from abc import ABC

from flajoletMartin import FlajoletMartin
import numpy as np
from Graph import Graph

from hasher import Hasher


class HyperBall(ABC):
    def __init__(self, graph, k, l, max_value, t = 100):
        """
        :param graph: Graph object
        :param k: functions k for the Flajolet Martin algorithm
        :param l: number l for the Flajolet Martin algorithm
        :param max_value: maximum value allowed to be inside counter representation
        :param t: maximum radius of the balls to be computed
        """
        self.graph = graph
        self.k = k
        self.l = l
        self.maxValue = max_value
        self.L = np.ceil(np.log2(max_value)) #Maximum number of zeros allowed
        self.t = t

    def union(self, counter1, counter2):
        # Function that get the max from each counter
        print("To implement")
        return counter1

    def compute(self):
        nodes = [node[0] for node in self.graph.get_nodes()] #save only ids, not the values

        counters = {} # dictionary containing the counters
        disk_counters = {} # Instead of saving them in disk, I suppose to save them in memory for now
        for n in nodes:
            #Inialize the counters with the element itself
            counters[n] = set(n)
            disk_counters[n] = set()

        t = 0

        while not self.has_reached_stopping_condition(counters, disk_counters):

            for curr_node in nodes:
                curr_counter = counters[curr_node]

                # for each node in counter, get the destination edge's counters ID having this element id as source
                dest_node_id = []
                for el in curr_counter:
                    dest_node_id += [edge[1] for edge in self.graph.get_edges() if edge[0] == el]

                for el_id in list(set(dest_node_id)):
                    curr_counter = self.union(curr_counter, counters[el_id])

                # write curr_counter on disk
                disk_counters[curr_node] = curr_counter



    def has_reached_stopping_condition(self, counters, disk_counters):
        """
        Chech that the t pass is equal to the old pass
        :param counters:
        :param disk_counters:
        :return:
        """
        set_c = set()
        set_old_c = set()
        for item, key in counters.items():
            set_c.add((item, key))

        for item, key in disk_counters.items():
            set_old_c.add((item, key))

        if set_c.difference(set_old_c) == set_old_c.difference(set_c) and set_old_c.difference(set_c) == 0:
            return True

        return False



