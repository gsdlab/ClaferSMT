'''
Created on May 31, 2013

@author: ezulkosk
'''
from common.Common import standard_print
from visitors import VisitorTemplate
import ast
import visitors

class PrintHierarchy(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Creates the Clafer hierarchy using Z3 Datatypes and Sorts.
    The fields will need to be changed to lists ASAP.
    '''
    
    def __init__(self, z3, model):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.model = model
        self.parentStack = [0] #used to determine the parent of each clafer
    
    def claferVisit(self, element):
        indent = "  " * (len(self.parentStack) - 1)
        sort = self.z3.z3_sorts[element.uid]
        for j in range(sort.numInstances):
            isOn = str(self.model.eval(sort.instances[j])) == str(self.parentStack[-1]) 
            if isOn:
                if not sort.refs:
                    standard_print(str(indent) + str(sort.instances[j]))
                else:
                    standard_print(str(indent) + str(sort.instances[j]) + " = " + str(self.model.eval(sort.refs[j])))
                self.parentStack.append(j)
                for i in element.elements:
                    visitors.Visitor.visit(self, i)
                self.parentStack.pop()
        
         
    
    