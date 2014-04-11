import sys
from bintrees.avltree import AVLTree



def traverseTree(root, tree, features):
    stack = [root]
    while stack:
        currNode = stack.pop()
        print(features[currNode])
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

    features = {}
    constraints = []
    parentConstraints = []
    
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
                currGCard = "0..*" #"0..*"
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
            features[currFeature] = currIndent + currGCard + " " + currFeature + currCard
            if currParent != "":
                parentConstraints.append("[" + currFeature + " => " + currParent + "]") 
                tree.append((currParent, currFeature))
                currParent = ""
            currFeature = ""
            currCard = ""
            currGCard = ""
            currLevel = ""
            
    print("// Features\n")
    traverseTree(root, tree, features)
    
    #for i in features:
    #    print(i)
    print("\n// Constraints\n")
    for i in constraints:
        print(i) 
    #print("\n// Parent Constraints")
    #for i in parentConstraints:
    #    print(i)
   
if __name__ == '__main__':
    run(sys.argv[1])
