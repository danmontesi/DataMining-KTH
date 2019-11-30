

class CompareSets():
    """
    Class CompareSets:
    It computes the Jaccard similarity of two sets of integers – two sets of hashed shingles.
    """


    def computeJaccard(self, set1, set2):
        #To be sure that the user inputted a set:
        a = set(set1)
        b = set(set2)

        union = a.union(b)
        intersection = a.intersection(b)
        print("Similarity between the 2 sets is " + str(round(len(intersection)/len(union), 2)))




if __name__ == '__main__':
    cs = CompareSets()
    cs.computeJaccard([1,2,3,3,4], [1,2,5])