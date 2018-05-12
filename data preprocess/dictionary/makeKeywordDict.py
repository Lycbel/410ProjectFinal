import pickle

####################################
# Notes: dicts used
# activeSubstance.dict:     key: drug,            value: list of actives        231092
# adr_drug.dict:            key: adr,             value: list of drugs          13544
# doc_word.dict:            key: ??
# drug_adr.dict:            key: drug,            value: list of adrs           63707
# FDA_processed.dict:       key: drug==>adr,      value: count                  3507300
# GO_term.dict:             key: gotermID,        value: goterm                 47131
# Go_term.txt:              same as above
# Mesh_descrip.txt:         1st part of MESH keywords
# Mesh_paC.txt:             2nd part of MESH keywords
#####################################

def readTXT(f):
    file = open(f, "r")
    file.readline()
    line = file.readline()
    count = 0
    out = []
    while line:
        out.append(line[:-1].strip().lower())
        file.readline()
        line = file.readline()
        count+=1
    return out

def makeMESHList():
    out1 = readTXT("Mesh_descrip.txt")
    out2 = readTXT("Mesh_paC.txt")
    MeshList = out1+out2
    return MeshList

def reverse_dict(dict):
    result = {}
    for key in dict.keys():
        if dict[key] not in result.keys():
            result[dict[key]] = [key]
        else:
            result[dict[key]].append(key)
    return result
###
# order: mesh + goterm&ID + drug + adr + actives
###
def makeWordDict():
    dict = {}
    index = 0
    path = "dict/"

    # mesh:
    meshList = makeMESHList()
    #### reduceMesh.py
    for w in meshList:
        dict[w.lower()] = index
        index+=1

    #goterm&ID
    with open(path + "Go_term.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    subDict = reverse_dict(subDict)
    for i in subDict.items():
        if i[0] not in dict.keys():
            dict[i[0]] = index # map go term & ID onto the same index
            index+=1
        for key in i[1]:
            dict[key] = dict[i[0]]

    #drug
    with open(path + "drug_adr.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    for i in subDict.keys():
        if i.lower() not in dict.keys():
            dict[i.lower()] = index
            index += 1
        else:
            print(i)

    #adr
    with open(path + "adr_drug.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    for i in subDict.keys():
        if i.lower() not in dict.keys():
            dict[i.lower()] = index
            index += 1
        else:
            print(i)

    #actives
    with open(path + "activeSubstance.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    activeList = []
    for i in subDict.items():
        for active in i[1]:
            if not active in activeList:
                activeList.append(active)
    print(len(activeList))
    for i in activeList:
        if i.lower() not in dict.keys():
            dict[i.lower()] = index
            index += 1
        else:
            print(i)

    fo = open("word_dict.dict", "wb")
    pickle.dump(dict, fo)
    fo.close()

    f2 = open("word_dict.txt", "w")
    for i in dict.items():
        f2.write(str(i) + "\n")
    f2.close()
    
    return dict, index


if __name__ == '__main__':
    dict, index = makeWordDict()
    print(index)