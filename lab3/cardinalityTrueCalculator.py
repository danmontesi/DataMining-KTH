from cardinalityCalculator import CardinalityCalculator
from multiset import Multiset


class CardinalityTrueCalculator(CardinalityCalculator):

    def __init__(self, elements):
        super().__init__(elements)

    def calculate(self):
        return Multiset(self.elements).get_cardinality()
