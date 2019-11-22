from cardinalityCalculator import CardinalityCalculator
import numpy as np

from flajoletMartin import FlajoletMartin


class HyperLogLog(FlajoletMartin):

    def __init__(self, max_value, num_buckets, hasher):
        self.L = np.ceil(np.log2(max_value))
        self.bucket_leading_bits = np.ceil(np.log2(num_buckets))
        self.num_buckets = int(2 ** self.bucket_leading_bits)
        self.hasher = hasher
        self.buckets = np.zeros(self.num_buckets)
        self.alpha = {16: 0.673, 32: 0.697, 64: 0.709}

    def get_bucket_id(self, value):
        bucket_id = 0
        k = 0
        while k < self.bucket_leading_bits:
            bucket_id = bucket_id * 2 + int(value/(2**(self.L-k-1)))
            value %= 2**(self.L-k-1)
            k += 1
        return int(bucket_id)

    def calculate_with_buckets(self, elements):
        for el in elements:
            hashed = self.hasher.hash_value(el)
            bucket = self.get_bucket_id(hashed)
            self.buckets[bucket] = max(self.buckets[bucket], 1 + self.lsb(hashed))


    def linear_counting(self, V):
        """
        :param V: number of register equal to zero
        :return:
        """
        return self.num_buckets*np.log(self.num_buckets/V)

    def count_buckets_with_zeros(self):
        cont = 0
        for b in self.buckets:
            if b == 0:
                cont += 1
        return cont

    def count(self):
        Z = np.sum(np.exp2(self.buckets * -1)) ** -1
        E = self.alpha[self.num_buckets] * Z * self.num_buckets ** 2
        if E <= 5/2*self.num_buckets:
            V = self.count_buckets_with_zeros()
            if V != 0:
                return np.ceil(self.linear_counting(V))
            else:
                return np.ceil(E)
        elif E <= (1/30)*2**32:
            return np.ceil(E)
        else:
            return np.ceil((-2**32)*np.log(1-E/(2**32)))

    def calculate(self, elements):
        self.calculate_with_buckets(elements)
        return self.count()

    def union(self, hyperLogLog2):
        self.buckets = np.maximum(self.buckets, hyperLogLog2.buckets)
