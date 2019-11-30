class Multiset():
    """
    Class for maintaining a series of repeated elements.
    (multi: duplicate elements in the set)
    """

    def __init__(self, elements):
        self.elements = elements
        self.set = set(elements)

    def add_element(self, el):
        self.elements.append(el)
        self.set.add(el)

    def add_element_with_replication(self, el, occurrences):
        for i in range(occurrences):
            self.add_element(el)

    def get_cardinality(self):
        return len(self.set)