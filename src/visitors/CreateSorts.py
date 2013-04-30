'''
Created on Apr 28, 2013

@author: ezulkosk
'''

import common.Common
import visitors.Visitor

class CreateSorts(object):
    '''
    adds sorts to the Z3Instance for each clafer
    fields:
        z3(Z3Instance): the Z3Instance object
    '''

    uid_stack = []    
    __TAB__ = "  "
    level = 0
    
    def __init__(self, z3instance):
        self.z3 = z3instance
    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        self.uid_stack.append(element.uid)
        #create fully qualified ID of clafer
        sortID = ".".join(CreateSorts.uid_stack)
        self.z3.addSort(sortID)
        element.sortID = sortID
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.uid_stack.pop()