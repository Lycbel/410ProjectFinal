
infileName = 'pa2018.xml'
f1 = 'paC.txt'

pattern =['<RecordUI>','</RecordUI>',len('<RecordUI>')]

patternString = ['<String>','</String>',len('<String>')]


hash1 = {};

f = open(infileName,'r',encoding='utf-8');
ff1 = open(f1,'w+',encoding='utf-8');



def handelKeyPair(key,value):
    hash1[key] = value;


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
        content = getPattern(pattern,line)
        if(content != -1):
            waitStart = False;
            patterninfo = content;
    else:
        result =getPattern(patternString,line);
        if(result!=-1):
            waitStart = True;
            if(patterninfo[0:1]!='D'):
                handelKeyPair(patterninfo,result)
            

for key,value in hash1.items():
    ff1.write(key+'\n');    
    ff1.write(value+'\n');


ff1.flush();
ff1.close();
