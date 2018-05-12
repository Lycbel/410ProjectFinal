###################Deal with Go term#######################
import re
#flag = 0
#go_term = {}
#pattern = re.compile(r'^\[Term\]')
#pattern1 = re.compile(r'^id:')
#pattern2 = re.compile(r'^name:')
#count = 0
#file = open('go-basic.obo','r')
#for line in file.readlines():
#    if pattern.match(line):
#        flag = 1
#        count += 1
#    if flag == 1 and pattern1.match(line):
#        l = line.strip().split('id:')
#        go_id = l[1].strip()
#        if go_id in go_term.keys():
#            print(go_id)
#        else:
#            go_term[go_id] = 0
#    if flag == 1 and pattern2.match(line):
#        l = line.strip().split('name:')
#        if go_term[go_id] == 0:
#            go_term[go_id] = l[1].strip()
#        else:
#            print(go_id)
#        flag = 0
#        go_id = None

import pickle
# save dict
#f1 = open("Go_term.txt","wb")
#pickle.dump(go_term, f1)
#f1.close()
# load dict
f2 = open("Go_term.dict","rb")
go_term = pickle.load(f2)
f2.close()

###################Deal with Mesh headings#######################
file2 = open('Mesh_descrip.txt','r')
descrip_list = []
for line in file2.readlines():
    line = line.strip()
    is_node = 'D0' not in line
    if is_node == 1:
        descrip_list.append(line.lower())

file3 = open('Mesh_paC.txt','r')
pac_list = []
count = 1
for line in file3.readlines():
    line = line.strip()
    if count % 2 == 1:
        count = count + 1
    else:
        pac_list.append(line.lower())
        count = count + 1

###################Create a dictionary of node#######################
# store all medical nodes into one list
go_list = []
for key in go_term.keys():
    go_list.append(key)
    go_list.append(go_term[key])

dict_list = {};
for element1 in go_list:
    dict_list[element1.replace("\n",'').lower()]=0;

for element2 in descrip_list:
    dict_list[element2.replace("\n",'').lower()]=0;

for element3 in pac_list:
    dict_list[element3.replace("\n",'').lower()]=0;

#######################N gram##############################
import metapy
maxGram = 10;
minGram = 1;
def generatePair(value,ng,line,dict_list,doc):
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=False)
    tok = metapy.analyzers.LowercaseFilter(tok)
    #tok = metapy.analyzers.LengthFilter(tok, min=2, max=5)
    tok.set_content(doc.content())
    #tokens = [token for token in tok]
    #print(tokens)
    ana = metapy.analyzers.NGramWordAnalyzer(ng, tok)
    try:
        trigrams = ana.analyze(doc)
    except Exception :
        #print("ex");
        return [];
    for key in trigrams:
        m='';
        if(ng==1):
            m =key;
            # print(m)
        else:
            for i in range(0,ng):
                if(i==(ng-1)):
                    m=m+key[i];
                else:
                    m=m+key[i]+" ";
        if(m in dict_list):
            value.append(m);

def pairs(line,dict_list):
    doc = metapy.index.Document()
    doc.content(line)
    values =[];
    for i in range(minGram,maxGram+1):
        generatePair(values,i,line,dict_list,doc);
    return values;

######### Process paper#############################
import datetime
import sys
intervals = sys.argv
start = int(intervals[1])
end = int(intervals[2])
file_index = list(range(start,end))

for i in file_index:
    file_name = './data/pmid2meta_autophrase.chunk' + str(i)
    docfile = open(file_name, 'r')
    starttime = datetime.datetime.now()
    pair ={};
    index = 1
    for line in docfile.readlines():
        line = line.strip().replace('_','')
        va = pairs(line,dict_list);
        pair[index] = va
        index = index + 1
    endtime = datetime.datetime.now()
    time =(endtime - starttime)
    print(file_name, time.seconds);
    # save dict
    out_file = './result/doc_word.dict' + str(i)
    f = open(out_file,"wb")
    pickle.dump(pair, f)
    f.close()