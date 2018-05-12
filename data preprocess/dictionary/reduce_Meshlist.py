path = ""

# mesh:
meshList = makeMESHList()
meshHash = {}
for i in meshList:
    meshHash[i.lower()] = 0

#goterm&ID
with open(path + "Go_term.dict", "rb") as f:
    subDict = pickle.load(f)
    f.close()

goHash = {}
for w in subDict.keys():
    goHash[w.lower()] = 0
    goHash[subDict[w].lower()] = 0

###deal with drug
with open(path + "drug_adr.dict", "rb") as f:
    drug_tmp = pickle.load(f)
    f.close()

drug_go = []
# ['cell', 'reflex', 'sleep', 'aster']
drug_mesh = []
for i in drug_tmp.keys():
    if i.lower() in meshHash.keys():
        drug_mesh.append(i.lower())
    if i.lower() in goHash.keys():
        drug_go.append(i.lower())

l = len(meshList) - 1
while l >= 0:
    if meshList[l] in drug_mesh:
        del meshList[l]
    l -= 1

###deal with adr
with open(path + "adr_drug.dict", "rb") as f:
    adr_tmp = pickle.load(f)
    f.close()

adr_go = []
# ['type ii hypersensitivity', 'hypersensitivity', 'cell death', 'platelet aggregation', 'macrophage activation', 'detoxification', 'muscle atrophy', 'menopause', 'muscle hypertrophy', 'vasoconstriction', 'type i hypersensitivity', 'fibrinolysis']

adr_mesh = []
for i in adr_tmp.keys():
    if i.lower() in meshHash.keys():
        adr_mesh.append(i.lower())
    if i.lower() in goHash.keys():
        adr_go.append(i.lower())

l = len(meshList) - 1
while l >= 0:
    if meshList[l] in adr_mesh:
        del meshList[l]
    l -= 1

### deal with active
with open(path + "activeSubstance.dict", "rb") as f:
    subDict = pickle.load(f)
    f.close()

activeList = []

for i in subDict.items():
    for active in i[1]:
        if not active in activeList:
            activeList.append(active)

active_go = []
# 
active_mesh = []
for i in activeList:
    if i.lower() in meshHash.keys():
        active_mesh.append(i.lower())
    if i.lower() in goHash.keys():
        active_go.append(i.lower())

l = len(meshList) - 1
while l >= 0:
    if meshList[l] in active_mesh:
        del meshList[l]
    l -= 1

#>>> len(meshList)
#31418
#>>> len(active_mesh)
#2448
#>>> len(drug_mesh)
#2277
#>>> len(adr_mesh)
#1321
