import numpy as np



""" 1 - 
 Create a class Shingling that constructs k–shingles of a given length k (e.g., 10) from a given document, 
 computes a hash value for each unique shingle, and represents the document in the form of an ordered set of 
 its hashed k-shingles.
"""
class Shingling():

    def __init__(self, k):
        """
        :param k: length of the shingles
        """

        self.k = k




    def hashShingling(self, shingle, mod=2 ** 32 - 1):
        """
        Given a shingle, returns its hashed value
        the hash function is defined as below.
        hash(char) = val*26 + getAscii(char)%mod

        :param shingle: input characters sequence
        :return val: hashed value for the string
        """

        val = 0
        for c in shingle:
            val = (val * 26 + ord(c)) % mod
        return val



    def get_shinglings(self, document):
        """
        Get list of shinglings from a document as a list
        :param document: Document in form of String
        """

        shinglings = []
        for i in range(self.k - 1, len(document)):
            shinglings.append(self.hashShingling(document[i - self.k + 1:i]))

        return np.array(shinglings)


