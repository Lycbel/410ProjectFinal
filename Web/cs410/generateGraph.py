import pickle
import sys
import time 
import os.path
import searchAlgorithm.IDDFS as idf
def log(content):
    f = open('log.txt','a+')
    f.write(str(content)+"\n");
    f.flush();
    f.close();
def process(drug,adr,path):
    return idf.webAppSearch(drug,adr,path);
def check(drug,adr):
    log('p1');
    fs = open('word_dict.dict','rb')
    log('p2');
    try:
        dic = pickle.load(fs);
        log('p3');
    except Exception as e:
        log(e);
    
    fs.close();
    if((drug in dic.keys()) and (adr in dic.keys())):
        return True;
    else:
        print("-1")
        return False;

if __name__ == "__main__":
    drug = str(sys.argv[1]);
    adr = str(sys.argv[2]);
    drug = drug.replace('_',' ');
    adr = adr.replace('_',' ');
    
    drugo = drug.lower().strip();
    adro = adr.lower().strip();
    if(check(drug,adr)):
        log('correct2')
        drug = drugo.replace(" ","_");
        adr = adro.replace(" ","_");
        filename = "data\\"+drug+"_"+adr;
        
        if(os.path.isfile(filename) ):
            print("1")
        else:
            time.sleep(2) 
            path =(os.path.abspath(".")+"\\"+filename)
            result = process(drugo,adro,path);
            log(result)
            print(result);
            
    else:
        log('error2')
        pass;
    

    