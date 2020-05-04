import findspark
findspark.init()

import numpy as np


class VectorWrapper():
    def __init__(self, vector):
        self.vector = vector

class MinHashing():
    """
    A class MinHashing that builds a minHash signature (in the form of a vector or a set)
    of a given length n from a given set of integers (a set of hashed shingles).
    """

    def __init__(self, n):
        self.n = n
        self.coefficient = np.random.randint(2 ** 32 - 1, size=self.n)
        self.bias = np.random.randint(2 ** 32 - 1, size=self.n)
        self.mod = np.ones(self.n) * 2 ** 32 - 1

    def hashValue(self, value, signature):
        return (value * self.coefficient[signature] + self.bias[signature]) % self.mod[signature]

    def hashVector(self, vector, signature):
        return np.vectorize(self.hashValue)(vector, signature)

    def minHashVector(self, signature, vectorWrapper):
        return np.amin(self.hashVector(vectorWrapper.vector, signature))

    def generateSignatures(self, vector):
        return np.vectorize(self.minHashVector)(np.arange(self.n), VectorWrapper(vector))