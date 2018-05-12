
infileName = 'desc2018.xml'
f1 = 'descrip.txt'
f2 = 'qua.txt'
f3 = 'term.txt'
patterns =[ ['<DescriptorUI>','</DescriptorUI>',len('<DescriptorUI>')],
 ['<QualifierUI>','</QualifierUI>',len('<QualifierUI>')],
  ['<TermUI>','</TermUI>',len('<TermUI>')]]
patternString = ['<String>','</String>',len('<String>')]


hash1 = {};
hash2= {};
hash3 = {};
hashs = [hash1,hash2,hash3]

f = open(infileName,'r',encoding='utf-8');
ff1 = open(f1,'w+',encoding='utf-8');
ff2 = open(f2,'w+',encoding='utf-8');
ff3 = open(f3,'w+',encoding='utf-8');
fs = [ff1,ff2,ff3];


def handelKeyPair(key,value,code):
            hashs[code][key] = value;

def getPatternCode(string):
    for i in range(0,3):
        result = getPattern(patterns[i],string)
        if(result!=-1):
            return (result,i)
    return -1

def getPattern(pattern,string):
     
     pos1 = line.find(pattern[0]);
     pos2 = -1;
     if(pos1!=-1):
         pos2 = line.find(pattern[1],pos1+1)
     else:
         return -1;
     return string[pos1+pattern[2]:pos2]
 
waitStart = True;
patterninfo = -1;
for line in f:

    if(waitStart):
        content = getPatternCode(line)
        if(content != -1):
            waitStart = False;
            patterninfo = content;
    else:
        result =getPattern(patternString,line);
        if(result!=-1):
            waitStart = True;
            handelKeyPair(patterninfo[0],result,patterninfo[1])
            
for i in range(0,3):
    for key,value in hashs[i].items():
        fs[i].write(key+'\n');    
        fs[i].write(value+'\n');

for i in range(0,3):
    fs[i].flush();
    fs[i].close();
