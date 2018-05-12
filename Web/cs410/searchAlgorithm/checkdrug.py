import pickle
import numpy as np
import scipy.sparse as sparseMatrix

def loadFiles():
    durgDict = {}
    drugidx = 0

    with open("word_dict.dict", "rb") as f:
        wordDict = pickle.load(f)
        #get dimension
        dimension = 0
        for i in wordDict.items():
            if i[1] > dimension:
                dimension = i[1]
        f.close()

    print("word dict loaded.")

    print("word dict inverse loaded.")

    with open("drug_adr.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    for i in subDict.keys():
        durgDict[i.strip().lower()] = drugidx
        drugidx += 1

    with open("/data/work/huaminz2/CS410/project/GuoShijie/word_matrix.matrix", "rb") as f:
        matrix = pickle.load(f)
        f.close()
    print("doc dict loaded.")
    print("matrix shape: " + str(matrix.shape))
    print("=======Initialization completed========")
    return matrix, wordDict, durgDict, dimension

def getDegree(matrix,drugDict,wordDict):
    rs = {}
    drugDegree = {}
    for drug in drugDict:
        idx = wordDict[drug]
        degree = len(matrix[idx].nonzero()[1])
        if degree >= 0:
            rs[drug] = idx
            drugDegree[drug] = degree
    rs = rs.items()
    drugDegree = drugDegree.items()
    rs = sorted(rs, key=lambda x: x[1])
    drugDegree = sorted(drugDegree, key=lambda x: x[1])
    return rs,drugDegree


if __name__ == '__main__':
    matrix, wordDict, durgDict, dimension = loadFiles()
    rs, drugDegree = getDegree(matrix,durgDict,wordDict)
    #l = len(rs)
    rs = rs[0:99]
    drugDegree = drugDegree[0:99]
    for i in rs:
        print(i)
    fo = open("drug_degree.dict", "wb")
    pickle.dump(drugDegree, fo)
    fo.close()
