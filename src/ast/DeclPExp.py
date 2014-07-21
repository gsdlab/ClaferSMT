'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class DeclPExp(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''
    def __init__(self, quantifier, declaration, bodyParentExp):
        self.quantifier = quantifier
        self.declaration = declaration
        self.bodyParentExp = bodyParentExp
        
    def toString(self, level):
        s = self.quantifier + " "
        if self.declaration:
            s+=  self.declaration.toString(level+1) + " | "
        s += self.bodyParentExp.toString(level+1)
        return s
    
    def __str__(self):
        return str(self.declaration)
    
    def __repr__(self):
        return str(self)