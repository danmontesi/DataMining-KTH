from cardinality.cardinalityCalculator import CardinalityCalculator
from testers.multiset import Multiset


class CardinalityTrueCalculator(CardinalityCalculator):

    def calculate(self, elements):
        return Multiset(elements).get_cardinality()
