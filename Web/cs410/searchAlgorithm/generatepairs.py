import pickle
import numpy as np
import scipy.sparse as sparseMatrix

def loadFiles():

    with open("drug_adr.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()

    with open("FDA_processed.dict", "rb") as f:
        adrCount = pickle.load(f)
        f.close()
        print("load1")

    with open("drug_degree.dict",'rb') as f:
        drugDegree = pickle.load(f)
        f.close()
        print('load2')
        drugs = []
        for i in drugDegree:
            drugs.append(i)

    return subDict,adrCount,drugDegree,drugs

if __name__ == '__main__':
    drugList = {}
    subDict, adrCount, drugDegree, drugs = loadFiles()
    for drug in drugDegree:
        drugtemp = {}
        currentCount = 0
        for element in adrCount:
            if (drug in drugs) == True:
                currentCount = adrCount[element]
                drugtemp[element] = currentCount
                if adrCount[element] > currentCount:
                    drugtemp.clear()
                    currentCount = adrCount[element]
                    drugtemp[element] = currentCount
        drugList.update(drugtemp)

    print(drugList)
