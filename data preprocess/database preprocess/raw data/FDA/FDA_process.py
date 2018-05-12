import pickle
f = open('FDA.dict','rb')
fda_dict = pickle.load(f)
f.close()
# extract fda information
drug_count = {}
drug_adr = {}
adr_drug = {}
for key in fda_dict.keys():
    string = key.strip().split('==>')
    drug = string[0].strip()
    adr = string[1].strip()
    count = fda_dict[key]
    if drug in drug_count.keys():
        drug_count[drug].append(count)
    else:
        drug_count[drug] = [count]
    if drug in drug_adr.keys():
        drug_adr[drug].append(adr)
    else:
        drug_adr[drug] = [adr]
    if adr in adr_drug.keys():
        adr_drug[adr].append(drug)
    else:
        adr_drug[adr] = [drug]

# process active Substance
import pickle
f = open('activeSubstance.dict','rb')
drug_ingredient = pickle.load(f)
f.close()

# conbine (#drug_ingredient = #drug_adr)
for i in drug_adr.keys():
    if i in drug_ingredient.keys():
        continue;
    else:
        drug_ingredient[i] = []

# 规范化key(strip())
tmp = {}
for i in drug_ingredient.keys():
    k = i.strip()
    if k in tmp.keys():
        tmp[k].extend(drug_ingredient[i])
    else:
        tmp[k] = drug_ingredient[i]
drug_ingredient = tmp

import heapq
drug_threshold = {}
for key in drug_count.keys():
    list = drug_count[key]
    threshold = heapq.nsmallest(int(len(list) * 0.05)+1, list)[-1]
    drug_threshold[key] = threshold

#re-extract
drug_adr = {}
adr_drug = {}
new_fda_dict = {}
for key in fda_dict.keys():
    string = key.strip().split('==>')
    drug = string[0].strip()
    adr = string[1].strip()
    count = fda_dict[key]
    if count >= drug_threshold[drug] and count != 1:
        new_fda_dict['==>'.join([drug,adr])] = count
        if drug in drug_adr.keys():
            drug_adr[drug].append(adr)
        else:
            drug_adr[drug] = [adr]
        if adr in adr_drug.keys():
            adr_drug[adr].append(drug)
        else:
            adr_drug[adr] = [drug]

f1 = open("activeSubstance.dict","wb")
pickle.dump(drug_ingredient, f1)
f1.close()
f1 = open("FDA_processed.dict","wb")
pickle.dump(new_fda_dict, f1)
f1.close()
f1 = open("drug_adr.dict","wb")
pickle.dump(drug_adr, f1)
f1.close()
f1 = open("adr_drug.dict","wb")
pickle.dump(adr_drug, f1)
f1.close()