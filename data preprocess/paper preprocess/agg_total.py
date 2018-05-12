import pickle
doc_word = {}

f = open('doc_lower_word.dict','rb')
doc_lower_word = pickle.load(f)
f.close()
f = open('doc_upper_word.dict','rb')
doc_upper_word = pickle.load(f)
f.close()
f = open('doc_source_node.dict','rb')
doc_source_node = pickle.load(f)
f.close()

for key in doc_lower_word.keys():
    tmp = []
    tmp1 = doc_lower_word[key]
    tmp2 = doc_upper_word[key]
    tmp3 = doc_source_node[key]
    tmp.extend(tmp1)
    tmp.extend(tmp2)
    tmp.extend(tmp3)
    final = []
    for i in tmp:
        final.append(i.lower())
    final = list(set(final))
    doc_word[key] = final

f = open('doc_word.dict','wb')
pickle.dump(doc_word, f)
f.close()

    