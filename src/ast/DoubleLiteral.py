'''
Created on Mar 26, 2013

@author: ezulkosk
'''

class DoubleLiteral(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self,value):
        self.value=value
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)