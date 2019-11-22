from cardinalityTrueCalculator import CardinalityTrueCalculator
from flajoletMartin import FlajoletMartin
from hasher import Hasher
from hasher2 import Hasher2
from hyperloglog import HyperLogLog
from multisetGenerator import MultisetGenerator
import numpy as np

class CardinalityTester():

    def __init__(self, multiset_size, max_value):
        self.multiset_size = multiset_size
        self.max_value = max_value
        self.multiset = self.generate_multiset()

    def generate_multiset(self):
        """
        Generate a multiset having size self.multiset_size containing randomic elements
        :return: list[int]
        """
        multiset_generator = MultisetGenerator(self.multiset_size, self.max_value)
        multiset_generator.generate()
        multiset = multiset_generator.multiset
        return multiset

    def test(self):
        cardinality_true_calculator = CardinalityTrueCalculator()
        print("Real cardinality: " + str(cardinality_true_calculator.calculate(self.multiset.elements)))
        #flajolet_martin = FlajoletMartin(50, 20, max_value)
        #print("Approximate cardinality flajolet: " + str(flajolet_martin.calculate(self.multiset.elements)))
        hyperloglog = HyperLogLog(self.max_value, 32, Hasher2(2**32))
        print("Approximate cardinality loglog: " + str(hyperloglog.calculate(self.multiset.elements)))

if __name__ == "__main__":
    multiset_size = 5000
    max_value = 2**32 - 1
    CardinalityTester(multiset_size, max_value).test()