import pickle
doc_upper_word = {}

for i in range(400):
    tmp = {}
    file =  './result/doc_upper_word.dict' + str(i)
    f = open(file,'rb')
    tmp = pickle.load(f)
    f.close()
    for key in tmp.keys():
        index_key = str(i) + '_' + str(key)
        if index_key in doc_upper_word.keys():
            print('error: %s\n' % index_key)
        else:
            doc_upper_word[index_key] = tmp[key]

f = open('doc_upper_word.dict','wb')
pickle.dump(doc_upper_word, f)
f.close()

tmp = {}
for key in doc_upper_word.keys():
    if len(doc_upper_word[key]) != 0:
        tmp[key] = doc_upper_word[key]