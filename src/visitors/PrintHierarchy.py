'''
Created on May 31, 2013

@author: ezulkosk
'''
from common import ClaferDatatype
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
        self.partition = [0] #used to determine the parent of each clafer
        

    '''
    def printVars(self, model):
        print("Model: " + str(self.count))
        self.count = self.count + 1
        for i in self.z3_sorts.values():
            for j in range(len(i.bits)):
                if str(model.eval(i.bits[j])) == "1" and not i.refs:
                    print(i.bits[j])
                elif str(model.eval(i.bits[j])) == "1" and i.refs:
                    print(str(i.bits[j]) + " = " + str(model.eval(i.refs[j])))
        print("\n")
    '''
    
    def claferVisit(self, element):
        indent = "  " * (len(self.partition) - 1)
        sort = self.z3.z3_sorts[element.uid]
        if self.partition[-1] == 0:
            lowBit = 0
            highBit = len(sort.bits)
        else:
            lowBit = sort.partitionSize * (self.partition[-1] - 1)
            highBit = sort.partitionSize * self.partition[-1]
        for j in range(lowBit,highBit):
            isOn = str(self.model.eval(sort.bits[j])) == "1" 
            if isOn:
                if not sort.refs:
                    print(str(indent) + str(sort.bits[j]))
                else:
                    print(str(indent) + str(sort.bits[j]) + " = " + str(self.model.eval(sort.refs[j])))
                if(self.partition[-1] == 0):
                    self.partition.append(j+1)
                else:
                    self.partition.append(self.partition[-1] * j)
                for i in element.elements:
                    visitors.Visitor.visit(self, i)
                self.partition.pop()
        
         
    
    