import numpy as np

from multiset import Multiset


class MultisetGenerator:
    def __init__(self, length, max_value):
        self.multiset = Multiset([])
        self.length = length
        self.max_value = max_value

    def generate(self):
        """
        Generate #self.length samples of randomic elements,
        having random number of duplicates i.e. generate random number n.
        Then, insert n into the set m random number times.
        [n,n,n, ... n] = [n]*m
        """
        temp_length = self.length
        while temp_length > 0:
            el = np.random.randint(0, self.max_value)
            occurrences = 1 + np.random.randint(0, 1 + int(self.length ** 0.5))
            self.multiset.add_element_with_replication(el, occurrences)
            temp_length -= occurrences

