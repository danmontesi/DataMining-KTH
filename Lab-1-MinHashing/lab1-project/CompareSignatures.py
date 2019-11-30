
import numpy as np

class CompareSignatures():

    """
    A class CompareSignatures that estimates similarity of two integer vectors – minhash signatures –
    as a fraction of components, in which they agree.
    """

    def getSimilarity(self, list1, list2):
        comparison = np.dstack((list1, list2))[0]
        print("Similarity between the 2 vectors is " + str(
        len(list(filter(lambda x: x[0] == x[1], comparison))) / len(comparison)))