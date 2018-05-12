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

    with open("drug_adr.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    for i in subDict.keys():
        durgDict[i.strip().lower()] = drugidx
        drugidx += 1

    #server path： /data/work/huaminz2/CS410/project/GuoShijie/word_matrix.matrix
    with open("word_matrix.dict", "rb") as f:
        matrix = pickle.load(f)
        f.close()
    print("doc dict loaded.")
    print("matrix shape: " + str(matrix.shape))
    print("=======Initialization completed========")
    return matrix, wordDict, durgDict, dimension

def getDegree(matrix,drugDict,wordDict):
    drugDegree = {}
    for drug in drugDict:
        idx = wordDict[drug]
        degree = len(matrix[idx].nonzero()[1])
        if degree >= 10:
            drugDegree[drug] = degree
    drugDegree = drugDegree.items()
    drugDegree = sorted(drugDegree, key=lambda x: x[1])
    return drugDegree

def toDict(lst):
    rs = {}
    for i in lst:
        rs[i[0]] = i[1]
    return rs

def strategyTwo():
    rs = {}
    with open("FDA_processed.dict", "rb") as f:
        adrCount = pickle.load(f)
        f.close()
        print("load1")
    for i in adrCount.items():
        if i[1] > 6000:
            rs[i[0]] = i[1]
    return rs

def makePairDict(samples):
    rs = {}
    for sample in samples.keys():
        temp = sample.split("==>")
        drug = temp[0]
        adr = temp[1]
        rs[drug] = adr
    return rs

if __name__ == '__main__':
    matrix, wordDict, durgDict, dimension = loadFiles()
    drugDegree = getDegree(matrix,durgDict,wordDict)
    #l = len(rs)
    drugDegree = drugDegree[0:99]
    for i in drugDegree:
        print(i)

    # drugDegreeDict = toDict(drugDegree)
    fo = open("drug_degree.dict", "wb")
    pickle.dump(drugDegree, fo)
    fo.close()
    '''
    samples = strategyTwo()
    rs = makePairDict(samples)
    fo = open("drug_degree.dict", "wb")
    pickle.dump(rs, fo)
    fo.close()
    for i in rs.items():
        print(i)
    '''

