import string
import findspark
import pyspark
import numpy as np

from LSH import LSH
from Shingling import Shingling


def cleanDocument(document):
    """
    Given a document in String format, remove the punctuation
    :param document:
    :return:
    """
    document = document.lower()
    document = document.translate(str.maketrans('', '', string.punctuation))
    return document

if __name__ == '__main__':

    findspark.init()
    sc = pyspark.SparkContext("local", "lhs")

    numberOfDocuments = 10

    # Read documents to analyze
    documents = []
    for i in range(numberOfDocuments):
        documents.append(sc.textFile("../data/" + str(i) + ".txt"))
        documents[i] = documents[i].map(lambda x: cleanDocument(x))

    # Create class shinglings to convert document into shingles and then into number
    shinglingSize = 7
    shingler = Shingling(shinglingSize)

    data = []
    for d in range(numberOfDocuments):
        document = ""
        for s in documents[d].collect():
            document = document + s
        shinglings = []
        for i in range(shinglingSize - 1, len(document)):
            # get the hash of the shingling and append to the new vector of integers
            shinglings.append(shingler.hashShingling(document[i - shinglingSize + 1:i]))
        data.append(shinglings)

    data = np.array(data)

    # create RDD and create LSH class
    dataRDD = sc.parallelize(data)
    dataWithIndex = dataRDD.zipWithIndex().map(lambda x: (x[1], x[0]))

    lsh = LSH(dataWithIndex, 25, 100, numberOfDocuments)

    lsh.run()