import pickle
# load dict
f = open("drug_adr.dict","rb")
drug_adr = pickle.load(f)
f.close()
f = open("adr_drug.dict","rb")
adr_drug = pickle.load(f)
f.close()
f = open("activeSubstance.dict","rb")
active = pickle.load(f)
f.close()

active_list = []
for key in active.keys():
    active_list.extend(active[key])

###################Create a dictionary of node#######################
dict_list = {};
active_list = set(active_list)

dict_list = {};
for element1 in active_list:
    dict_list[element1.strip().lower()]=0;

for element1 in drug_adr.keys():
    dict_list[element1.strip().lower()]=0;

for element2 in adr_drug.keys():
    dict_list[element2.strip().lower()]=0;

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
    out_file = './result/doc_source_node.dict' + str(i)
    f = open(out_file,"wb")
    pickle.dump(pair, f)
    f.close()