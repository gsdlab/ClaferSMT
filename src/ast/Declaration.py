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
        print("A")