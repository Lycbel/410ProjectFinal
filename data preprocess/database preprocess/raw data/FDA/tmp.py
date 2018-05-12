import pickle
f = open('FDA.dict','rb')
tmp = pickle.load(f)
f.close()
fda_dict = {}
for key in tmp.keys():
    string = key.strip().split('==>')
    drug = string[0].strip()
    adr = string[1].strip()
    string = '==>'.join([drug,adr])
    if string in fda_dict.keys():
        fda_dict[string] += tmp[key]
    else:
        fda_dict[string] = tmp[key]

f1 = open("FDA2.dict","wb")
pickle.dump(fda_dict, f1)
f1.close()

fo = open("FDA2.txt", "w")
for i in fda_dict.items():
    fo.write(str(i)+"\n")

fo.close()