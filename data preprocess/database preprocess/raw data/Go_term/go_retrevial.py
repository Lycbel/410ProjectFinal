import re
flag = 0
go_term = {}
pattern = re.compile(r'^\[Term\]')
pattern1 = re.compile(r'^id:')
pattern2 = re.compile(r'^name:')
count = 0
file = open('go-basic.obo','r')
for line in file.readlines():
    if pattern.match(line):
        flag = 1
        count += 1
    if flag == 1 and pattern1.match(line):
        l = line.strip().split('id:')
        go_id = l[1].strip()
        if go_id in go_term.keys():
            print(go_id)
        else:
            go_term[go_id] = 0
    if flag == 1 and pattern2.match(line):
        l = line.strip().split('name:')
        if go_term[go_id] == 0:
            go_term[go_id] = l[1].strip()
        else:
            print(go_id)
        flag = 0
        go_id = None

import pickle
# save dict
f1 = open("Go_term.dict","wb")
pickle.dump(go_term, f1)
f1.close()
# load dict
f2 = open("Go_term.dict","rb")
go_term = pickle.load(f2)
f2.close()