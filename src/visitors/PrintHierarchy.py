'''
Created on May 31, 2013

@author: ezulkosk
'''
from common.Common import standard_print
from lxml.builder import basestring
from visitors import VisitorTemplate
import ast
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
        self.indentCount = 0
        self.parentStack = [0] #used to determine the parent of each clafer
    
    def claferVisit(self, element):
        sort = self.z3.z3_sorts[element.uid]
        if element.isAbstract and self.parentStack == [0]:
            for i in sort.subs:
                for j in range(i.numInstances):
                    isOn = str(self.model.eval(i.instances[j])) != str(i.parentInstances)
                    if isOn:
                        standard_print(element.getNonUniqueID() + "__" + str(i.indexInSuper + j)
                            + " = " + str(i.instances[j]))
        if not element.isAbstract:
            self.indentCount = self.indentCount + 1 
        indent = "  " * (self.indentCount)
        
        for j in range(sort.numInstances):
            if not element.isAbstract:
                isOn = str(self.model.eval(sort.instances[j])) == str(self.parentStack[-1])
            else:
                isOn = str(self.model.eval(sort.instances[j])) != str(sort.parentInstances) and \
                    str(j) == str(self.parentStack[-1])
            if isOn:
                if not sort.refs and not element.isAbstract:
                    standard_print(str(indent) + str(sort.instances[j]))
                elif not element.isAbstract:
                    if isinstance(sort.refSort, basestring) and (sort.refSort == "integer" or sort.refSort == "string"):
                        standard_print(str(indent) + str(sort.instances[j]) + " = " + str(self.model.eval(sort.refs[j])))
                    else:
                        standard_print(str(indent) + str(sort.instances[j]) + " = " + 
                                       str(sort.refSort.element.getNonUniqueID()) + 
                                       "__"+ str(self.model.eval(sort.refs[j])))
                self.parentStack.append(j)
                for i in element.elements:
                    visitors.Visitor.visit(self, i)
                if sort.superSort:
                    self.parentStack.append(j + sort.indexInSuper)
                    visitors.Visitor.visit(self, sort.superSort.element)
                    self.parentStack.pop()
                self.parentStack.pop()
        if not element.isAbstract:
            self.indentCount = self.indentCount - 1   
    