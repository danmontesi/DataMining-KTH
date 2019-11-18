import numpy as np
class Hasher:
    def __init__(self, w1, w0, mod):
        self.w1 = w1
        self.w0 = w0
        self.mod = mod

    def hash_value(self, value):
        return (self.w1 * value + self.w0) % self.mod

    def hash_vector(self, vector):
        hasher = np.vectorize(self.hash_value)
        return hasher(vector)
