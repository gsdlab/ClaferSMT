'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class IRConstraint(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, isHard, exp):
        self.isHard = isHard
        self.exp = exp
        
    def __str__(self):
        return str(self.exp)
    
    def toString(self, level):
        return self.exp.toString(level)
    
