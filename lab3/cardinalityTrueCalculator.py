from cardinalityCalculator import CardinalityCalculator
from multiset import Multiset


class CardinalityTrueCalculator(CardinalityCalculator):

    def calculate(self, elements):
        return Multiset(elements).get_cardinality()
