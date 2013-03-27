'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class FunExp(object):
    '''
    classdocs
    '''


    def __init__(self, operation, elements):
        self.operation = operation
        self.elements = elements
        
        
    def __str__(self):
        return self.operation + self.elements
    
    def toString(self, level):
        print("A")