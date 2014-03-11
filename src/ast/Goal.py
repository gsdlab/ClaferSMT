'''
Created on Mar 24, 2013

@author: ezulkosk
'''

MAX=True
MIN=False

class Goal(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, isMaximize, exp):
        self.isMaximize = isMaximize
        self.exp = exp
        
    def __str__(self):
        return str(self.isMaximize) + str(self.exp)
    
    def toString(self, level):
        print("Goal")