from lsh.MinHashing import MinHashing
import numpy as np


class LSH():
    """
    Bonus task:
    Class LSH that implements the LSH technique: given a collection of minhash signatures
    (integer vectors) and a similarity threshold t, the LSH class (using banding and hashing)
    finds all candidate pairs of signatures that agree on at least fraction t of their components.
    """
    def __init__(self, signatures_lists, bands_num, signatures, doc_num):
        """
        :param signatures_lists: collection of minhash signatures (integer vectors) in the form of a RDD
        """
        self.signatures_lists = signatures_lists
        self.bands_num = bands_num
        self.signatures = signatures
        self.doc_num = doc_num

    def vectorHash(self, vector):
        """
        Computes an hash value given a vector
        :return: hashed value
        """
        return np.sum(vector) % 2 ** 32 - 1

    def generateCandidates(self, vector):
        """
        Given a vector, states whether it is a candidate or not
        """

        candidates = []
        for x in vector:
            for y in vector:
                if x[0] < y[0] and x[1] == y[1]:
                    candidates.append((x[0], y[0]))
        return candidates

    def run(self):

        # Computer threshold from given bands_num and signatures
        t = (1 / self.bands_num) ** (self.bands_num / self.signatures)
        print("Threshold is set to " + str(t))
        hasher = MinHashing(self.signatures)

        # Generate signatures of a given list of integers
        min_hash_lists = self.signatures_lists.map(lambda x: (x[0], hasher.generateSignatures(x[1])))

        # Create a tuples having as elements (bandId, (documentId, hashOverTheBand))
        bands0 = min_hash_lists.flatMap(lambda x: np.arange(self.bands_num))
        bands1 = min_hash_lists.flatMap(lambda x: np.ones(self.bands_num, dtype=int) * x[0])
        bands2 = min_hash_lists.flatMap(lambda x: np.array(np.split(x[1], self.bands_num)))
        bands2Hashed = bands2.map(lambda x: self.vectorHash(x))
        bands12Hashed = bands1.zip(bands2Hashed)
        bands = bands0.zip(bands12Hashed)

        bandsInGroup = bands.groupByKey()

        candidates = bandsInGroup.flatMap(lambda x: self.generateCandidates(x[1])).map(
            lambda x: (x[0] * len(self.doc_num) + x[1], x)).values().distinct()
        print("Candidates are: " + candidates.collect())






