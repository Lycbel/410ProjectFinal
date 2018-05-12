import pickle

with open("drug_degree.dict", "rb") as f:
    dic = pickle.load(f)
    f.close()

with open("FDA_processed.dict", "rb") as f:
    adrCount = pickle.load(f)
    f.close()

drug = 'clebopride'.upper() + "==>"
print(drug)
adrList = []
for i in adrCount.keys():
    if i.find(drug) >= 0:
        adrList.append(i)

print(adrList)


