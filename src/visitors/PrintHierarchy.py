'''
Created on May 31, 2013

@author: ezulkosk
'''

from structures.ClaferSort import PrimitiveType
from structures.SimpleTree import SimpleTree
from visitors import VisitorTemplate
import visitors



class PrintHierarchy(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    '''
    
    def __init__(self, z3, model):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.model = model
        self.tree = SimpleTree()
    
    def recursivePrint(self, node, level):
        indent = "  " * level
        if self.tree.refs.get(node):
            ref = " = " + str(self.tree.refs[node])
        else:
            ref = ""
        print(indent + node + ref)
        for i in self.tree.nodes.get(node, []):
            self.recursivePrint(i, level + 1)
    
    def printTree(self):
        for i in self.tree.roots:
            self.recursivePrint(i, 1)
    
    def claferVisit(self, element):
        sort = self.z3.z3_sorts[element.uid]
        if sort.parent:
            parent = sort.parent.element.uid#getNonUniqueID()
        else:
            parent = None
        for j in range(sort.numInstances):
            isOn = str(self.model.eval(sort.instances[j])) != str(sort.parentInstances)
            if isOn:
                if not parent:
                    self.tree.addRoot(str(sort.instances[j]))
                    parentInstance = None 
                else:
                    parentInstance = parent + "__" + str(self.model.eval(sort.instances[j])) 
                if element.isAbstract:
                    for k in sort.subs:
                        if k.indexInSuper <= j and j < k.indexInSuper + k.numInstances:
                            self.tree.addRef(str(sort.instances[j]), str(k.instances[j - k.indexInSuper]))
                if not sort.refs:
                        self.tree.addNode(str(sort.instances[j]), parentInstance)
                else:
                    if isinstance(sort.refSort, PrimitiveType) and (sort.refSort == "integer" or sort.refSort == "string"):
                        self.tree.addNode(str(sort.instances[j]), parentInstance)
                        self.tree.addRef(str(sort.instances[j]), str(self.model.eval(sort.refs[j])))
                    else:
                        self.tree.addNode(str(sort.instances[j]), parentInstance)
                        self.tree.addRef(str(sort.instances[j]), str(sort.refSort.element.getNonUniqueID()) + 
                                       "__"+ str(self.model.eval(sort.refs[j])))

        for i in element.elements:
            visitors.Visitor.visit(self, i)
    