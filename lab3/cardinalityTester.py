from cardinalityTrueCalculator import CardinalityTrueCalculator
from flajoletMartin import FlajoletMartin
from multisetGenerator import MultisetGenerator

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
        cardinality_true_calculator = CardinalityTrueCalculator(self.multiset.elements)
        print("Real cardinality: " + str(cardinality_true_calculator.calculate()))
        flajolet_martin = FlajoletMartin(self.multiset.elements, 50, 20, max_value)
        print("Approximate cardinality: " + str(flajolet_martin.calculate()))

if __name__ == "__main__":
    multiset_size = 5000
    max_value = 2**32 - 1
    CardinalityTester(multiset_size, max_value).test()