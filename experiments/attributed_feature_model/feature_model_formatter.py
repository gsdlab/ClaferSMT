import sys
from bintrees.avltree import AVLTree



def traverseTree(root, tree, features, metricsMap):
    stack = [root]
    while stack:
        currNode = stack.pop()
        print(features[currNode])
        (indent, metrics) = metricsMap[currNode]
        for i in metrics:
            print(indent + i)
            
        nextNodes = [child  for (par,child) in tree if par == currNode]
        stack = stack + nextNodes
        

def run(fname):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
    root = ""
    tree = []

    with open(fname) as f:
        content = f.readlines()
    content = [i.rstrip().replace("$","__") for i in content]
    #content = [i.rstrip() for i in content]
        
    currFeature = ""
    currCard = ""
    currGCard = ""
    indent = "  "
    currCon = ""
    currConLeft = ""
    currConRight = ""
    currConOp = ""
    currLevel = ""

    mostRecentFeature = ""
    currParent = ""

    polarity =""
    metric =""
    func =""
    objnum = 0

    features = { }
    metricsMap = { }
    constraints = []
    parentConstraints = []
    objectives = []
    
    currMetrics = []
    
    while content:
        i = content.pop(0)
        if i.startswith("Feature"):
            currFeature = i
        elif "type" in i:
            if "Optional" in i:
                currCard = " 0..1"
            else:
                currCard = " 1..1"
        elif "gcard" in i:
            if "Xor" in i:
                currGCard = "1..1"
            elif "Some" in i:
                currGCard = "1..*"
            else:
                currGCard = "0..*"
        elif "conType" in i:
            if "Include" in i:
                currConPrefix = ""
                currConOp = " => "
                currConSuffix = ""
            else:
                currConPrefix = "!("
                currConOp = " && "
                currConSuffix = ")"
        elif "parent_feature" in i:
            s = i.split(" = ")
            currParent = s[1]
        elif "left" in i:
            s = i.split(" = ")
            currConLeft = s[1]
        elif "right" in i:
            s = i.split(" = ")
            currConRight = s[1]
        elif "level" in i:
            s = i.split(" = ")
            currLevel = int(s[1])
        
        elif i.strip().startswith("metric") and currFeature != "":
            line = i.split(" = ")[1]
            line = line.split("__")[1]
            currMetrics.append("[ Metric" + line + " = @metric ]")
            #print("Metricasdf" + line)

        elif i.startswith("Objective"):
            #print("A" + i)
            #line = i.split("$")
            #print(line)
            metric = i#[1].strip()
        elif "objType" in i:
            polarity = i.split(" = ")[1].split("$")[0]
            polarity = polarity.split("__")[0].lower()
            if polarity == "maximize":
                polarity = "max"
            else:
                polarity = "min"

        if polarity != "":
            #print("metric: " + metrics
            objnumstr = str(objnum)
            objectives.append("ObjectiveInt" + objnumstr + " -> int")
            objectives.append("[ " + "ObjectiveInt" + objnumstr + " = " + "(sum AbsFeature.Metric"+objnumstr+")"+ " ]")
            func = "ObjectiveInt" + objnumstr
            objectives.append("<<" + polarity + " " + func + ">>")
            polarity =""
            func =""
            metric=""
            objnum = objnum + 1
                
        if(currConLeft != "" and currConRight != "" and currConOp != ""):
            constraints.append("[" + currConPrefix + currConLeft + currConOp + currConRight + currConSuffix + "]")
            currConLeft = ""
            currConRight = ""
            currConOp = ""
        
        if(currCard != "" and currGCard != "" and currFeature != ""  and currLevel != "" and (currLevel == 0 or currParent != "")):
            #print(indent)
            #print(currLevel)
            #print(currLevel)
            if currLevel == 0:
                root = currFeature
                #print(root)
            currIndent = indent * currLevel
            features[currFeature] = currIndent + currGCard + " " + currFeature + " : AbsFeature " + currCard
            metricsMap[currFeature] = (indent*(currLevel+1), currMetrics)
            if currParent != "":
                parentConstraints.append("[" + currFeature + " => " + currParent + "]") 
                tree.append((currParent, currFeature))
                currParent = ""
            currFeature = ""
            currCard = ""
            currGCard = ""
            currLevel = ""
            currMetrics = []

    print("abstract AbsFeature " + str(len(features)))
    mets = list(metricsMap.values())[0][1]
    for i in range(len(mets)):
        print("  Metric" + str(i) + " ->> int")

    print("// Features\n")
    traverseTree(root, tree, features, metricsMap)
    
    #for i in features:
    #    print(i)
    print("\n// Constraints\n")
    for i in constraints:
        print(i) 
    #print("\n// Parent Constraints")
    #for i in parentConstraints:
    #    print(i)
    for i in objectives:
        print(i)
   
if __name__ == '__main__':
    run(sys.argv[1])
