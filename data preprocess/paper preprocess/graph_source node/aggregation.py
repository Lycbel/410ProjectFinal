import pickle
doc_source_node = {}

for i in range(400):
    tmp = {}
    file =  './result/doc_source_node.dict' + str(i)
    f = open(file,'rb')
    tmp = pickle.load(f)
    f.close()
    for key in tmp.keys():
        index_key = str(i) + '_' + str(key)
        if index_key in doc_source_node.keys():
            print('error: %s\n' % index_key)
        else:
            doc_source_node[index_key] = tmp[key]

f = open('doc_source_node.dict','wb')
pickle.dump(doc_source_node, f)
f.close()

tmp = {}
for key in doc_source_node.keys():
    if len(doc_source_node[key]) != 0:
        tmp[key] = doc_source_node[key]
