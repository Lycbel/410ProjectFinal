import sys
import pickle
import numpy as np
import scipy.sparse as sparseMatrix

# load two dicts and get dimension of the matrix
def loadDicts():
    with open("doc_word.dict", "rb") as f:
        docDict = pickle.load(f)
        f.close()
    print("doc dict loaded")

    with open("word_dict.dict", "rb") as f:
        wordDict = pickle.load(f)

        #get dimension
        dimension = 0
        for i in wordDict.items():
            if i[1] > dimension:
                dimension = i[1]
        f.close()
    print("word dict loaded")
    return docDict, wordDict, dimension

def MakeMatrix():
    docDict, wordDict, dimension = loadDicts()
    matrix = sparseMatrix.lil_matrix((dimension, dimension), dtype=np.int8)

    for docWord in docDict.items():
        print(docWord[0])
        docWordList = set(docWord[1])
        # populate the matrix
        for word1 in docWordList:
            for word2 in docWordList:
                if word1 != word2:
                    row_ind = wordDict[word1]
                    col_ind = wordDict[word2]
                    matrix[row_ind, col_ind]+=1
                    #matrix = matrix + sparseMatrix.csc_matrix((1,(row_ind, col_ind)), shape=(dimension, dimension)) data and indexes must be lists

    # save to disk
    fo = open("word_matrix.matrix", "wb")
    pickle.dump(matrix, fo)
    fo.close()
    return matrix

if __name__ == '__main__':
    matrix = MakeMatrix()



