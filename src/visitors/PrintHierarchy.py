'''
Created on May 31, 2013

@author: ezulkosk
'''

from common import Options
from structures.ClaferSort import PrimitiveType
from structures.SimpleTree import SimpleTree
from visitors import VisitorTemplate
import visitors



def hashtag(string):
    if string.find("__"):
        arr = string.split("__",1)
        return(arr[0] + "$" + arr[1])
    else:
        return string

def removePrefix(string):
    #print(string)
    if Options.UNIQUE_NAMES:
        return hashtag(string)
    if string.startswith("c"):
        newStr = string.split("_",1)
        newStr = newStr[1]
    else:
        newStr = string
    return hashtag(newStr)

class PrintHierarchy(VisitorTemplate.VisitorTemplate):
    '''
    :var cfr: (:class:`~common.Z3Instance`) The Z3 solver.
    
    '''
    
    def __init__(self, cfr, model):
        '''
        :param cfr: The Z3 solver.
        :type cfr: :class:`~common.Z3Instance`
        '''
        self.cfr = cfr
        self.model = model
        self.tree = SimpleTree()
        self.pickledInstance = []
    
    
    
    def findEndRef(self, node):
        #print("A" + str(node))
        while True:
            #print(node)
            ref = self.tree.findParentInList(node, self.tree.refs)
            if ref:
                #
                #print("FOUND: ")
                #print(ref)
                #print(ref[1][0][1])#[1])
                ref = ref[1][0]
                #print("FOUND: ")
                #print(ref)
                (sort, val) = ref
                if isinstance(sort, PrimitiveType):
                    return str(ref[1])
                else:
                    #print("FOUND: ")
                    #print(ref)
                    if sort.subs:
                        for i in sort.subs:
                            #print(str(i.indexInSuper) + " <= " + str(val) + " < " + str(i.indexInSuper + i.numInstances) + " " + str(i.indexInSuper <= val))
                            if i.indexInSuper <= int(str(val)) and int(str(val)) < i.indexInSuper + i.numInstances:
                                ref = str(i.instances[int(str(val)) - i.indexInSuper])
                        #print("Done")
                    else:
                        ref = str(sort.instances[int(str(val))])
                    return removePrefix(ref)
            node = self.tree.findParentInList(node, self.tree.abstractRefs)
            if not node:
                return None
            else:
                (_, node) =  node
       
    def get_pickled(self):
        return '\n'.join(self.pickledInstance)      
        
    def show_inheritance(self, sort):
        '''
        Displays the super clafer. Useful for ClaferIDE.
        '''
        if Options.SHOW_INHERITANCE:
            if sort.superSort:
                sup = str(sort.superSort)[:-5]
            else:
                sup = "clafer"
            return " : " + sup + " "
        else:
            return ""
        
    def instance_print(self, str):
        if Options.CORES == 1:
            print(str)
        else:
            self.pickledInstance.append(str)
            
        
    def recursivePrint(self, node, level, thisIsAbstract=False):
        #print(node)
        #print(self.tree.abstractRefs)
        (sort, instance) = node
        indent = Options.INDENTATION * level
        abs_ref = self.tree.findParentInList(node, self.tree.abstractRefs)
        #print(abs_ref)
        #if abs_ref:
        #    print("TRUE")
        if not thisIsAbstract:
            #print(node)
            #print(self.findEndRef(node))
            nodeStr = removePrefix(str(instance))
            currRef = self.findEndRef(node)#self.tree.findParentInList(node, self.tree.refs)
            if currRef: # self.tree.refs.get(node):
                #print()
                #(_, refs) = currRefs
                #refs = refs[0]
                ref = " = " + str(currRef) #self.tree.refs.get(node)[0] #removePrefix(str(self.tree.refs[node]))
            else:
                ref = ""
            
            self.instance_print(indent + nodeStr + self.show_inheritance(sort) + ref)
        if abs_ref:
            (_, real_abs_ref) = abs_ref
            self.recursivePrint(real_abs_ref, level, True)
        (_, children) = self.tree.findParentInList(node, self.tree.nodes)
        #print(children)
        for i in children:
            self.recursivePrint(i, level + 1)
        
    
    def printTree(self):
        #print(self.tree.refs)
        #print(self.tree.nodes)
        #print(self.tree.roots)
        for i in self.tree.roots:
            #print(i)
            self.recursivePrint(i, 0)
            pass
        
    def claferVisit(self, element):
        if not self.cfr.isUsed(str(element)):
            return 
        sort = self.cfr.cfr_sorts[element.uid]
        if sort.parent:
            parent = sort.parent.element.uid#getNonUniqueID()
        else:
            parent = None
        for j in range(sort.numInstances):
            #if element.isAbstract and not parent:
            #    continue
            isOn = str(self.model.eval(sort.instances[j].var)) != str(sort.parentInstances)
            if isOn:
                if not parent and not element.isAbstract:
                    self.tree.addRoot((sort,sort.instances[j]))
                    parentInstance = None 
                if parent:
                    parentInstance = (sort.parent, sort.parent.instances[int(str(self.model.eval(sort.instances[j].var)))])
                    
                else:
                    parentInstance = None
                if element.isAbstract:
                    #print(element)
                    #print(sort.subs)
                    #print(element)
                    for k in sort.subs:
                        if not self.cfr.isUsed(str(k.element)):
                            continue 
                        if k.indexInSuper <= j and j < k.indexInSuper + k.numInstances:
                            #self.tree.addRef(str(sort.instances[j]), str(k.instances[j - k.indexInSuper]))
                            #print(k)
                            self.tree.addAbstractRef((k, k.instances[j - k.indexInSuper]), (sort, sort.instances[j]))
                #print("-----------")
                #print(str((sort, sort.instances[j])) + str(parentInstance))
                self.tree.addNode((sort, sort.instances[j]), parentInstance)
                if sort.refSort:
                    if isinstance(sort.refSort, PrimitiveType) and (sort.refSort == "integer" or sort.refSort == "string" or sort.refSort == "real"):
                        self.tree.addRef((sort, sort.instances[j]), (sort.refSort, self.model.eval(sort.refs[j].var)))
                    else:
                        self.tree.addRef((sort, sort.instances[j]),(sort.refSort, self.model.eval(sort.refs[j].var))) #str(sort.refSort.element.getNonUniqueID()) + 
                        # "__"+ str(self.model.eval(sort.refs[j])))

        for i in element.elements:
            visitors.Visitor.visit(self, i)
