import xml.etree.ElementTree as ET

dictionary = {}

def readXML(dic, file):
    tree = ET.parse(file)
    print("Finish reading XML file.")
    root = tree.getroot()
    count =0
    for report in root:
        count+=1
        print(count)
        patient = next(report.iter("patient"))
        reactions = patient.iter("reaction")
        drugs = patient.iter("drug")
        reactionList = []
        drugList = []

        for r in reactions:
            effect = next(r.iter("reactionmeddrapt")).text
            reactionList.append(effect)

        for d in drugs:
            drug = next(d.iter("medicinalproduct")).text
            try:
                activesubstancename = next(d.iter("activesubstancename")).text
            except:
                activesubstancename = "unknown"
            drugList.append(drug+"{"+activesubstancename+"}")

        rowList = []
        for d in drugList:
            for r in reactionList:
                row = d + "==>" + r
                rowList.append(row)

        for row in set(rowList):
            if row not in dic.keys():
                dic[row] = 1
            else:
                dic[row] += 1

if __name__ == '__main__':
    dictionary = {}
    readXML(dictionary, "DATA/xml/raw.xml")
    print(len(dictionary))
    fo = open("out.txt", "w")
    for i in dictionary.items():
        fo.write(str(i)+"\n")
    fo.close()