'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class FunExp(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, operation, elements):
        self.operation = operation
        self.elements = elements
        
        
    def __str__(self):
        return self.operation + str(self.elements)
    
    def __repr__(self):
        return str(self.operation) + str(self.elements)
    
    