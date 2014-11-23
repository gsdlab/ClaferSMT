'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class Declaration(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, isDisjunct, localDeclarations, body):
        self.isDisjunct = isDisjunct
        self.localDeclarations = localDeclarations
        self.body = body
        
    def __str__(self):
        return self.body
    
    def toString(self, level):
        s = ""
        if self.isDisjunct:
            s = "disj "
        return s + " ".join([i.toString(level+1) for i in self.localDeclarations]) + " : " + self.body.toString(level+1)
        
    def __repr__(self):
        return self.__str__()