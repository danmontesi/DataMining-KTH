from cardinalityCalculator import CardinalityCalculator
import numpy as np

from hasher import Hasher


class FlajoletMartin(CardinalityCalculator):
    def __init__(self, elements, k, l, max_value):
        """
        :param elements: Elements of the multiset
        :param k:
        :param l:
        :param max_value: maximum value allowed to be inside the multiset representation
        """
        super().__init__(np.array(elements, dtype=np.int64))
        self.k = k
        self.l = l
        self.maxValue = max_value
        self.L = np.ceil(np.log2(max_value)) #Maximum number of zeros allowed

    def lsb(self, value):
        """
        lsb: least significant bit position
        :param hasher:
        :return:
        """
        if value == 0:
            return self.L
        k = 0
        while value%2 == 0:
            k += 1
            value /= 2
        return k

    def max_lsb_slow(self, hasher):
        r = 0
        for el in self.elements:
            r = max(r, self.lsb(hasher.hash_value(el)))
        return r

    def max_lsb_fast(self, hasher):
        lsb_vectorize = np.vectorize(self.lsb)
        return np.max(lsb_vectorize(hasher.hash_vector(self.elements)))

    def calculate(self):
        averages = np.zeros(self.k)
        for k in range(self.k):
            medians = np.zeros(self.l)
            for l in range(self.l):
                # Create k*l hash functions with different factors
                # h(x) = (w1 * value + w0) % mod
                w1 = np.random.randint(1, 2**self.L - 1)
                w0 = np.random.randint(1, 2**self.L - 1)
                mod = 2**self.L - 1
                hasher = Hasher(w1, w0, mod)
                medians[l] = self.max_lsb_fast(hasher)
            averages[k] = np.median(np.array(medians))
        return int(2**np.mean(np.array(averages)))





