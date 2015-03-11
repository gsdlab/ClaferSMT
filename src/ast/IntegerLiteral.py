'''
Created on Mar 26, 2013

@author: ezulkosk
'''

class IntegerLiteral(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self,value):
        self.value=value
        
    def __str__(self):
        return str(self.value)
    
    def toString(self, level):
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()