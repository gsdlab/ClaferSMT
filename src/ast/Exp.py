'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class Exp(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''
    def __init__(self, expType, exptype, parentId, pos, iExpType ,iExp):
        self.expType = expType
        self.type = exptype
        self.parentId = parentId
        self.pos = pos
        self.iExpType = iExpType
        self.iExp = iExp

        
    def __str__(self):
        return "ExpType: " + self.expType
    
    def __repr__(self):
        print(str(self.iExp))
    
    def toString(self, level):
        print("A")