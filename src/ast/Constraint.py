'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class Constraint(object):
    '''
    classdocs
    '''


    def __init__(self, isHard, exp):
        self.isHard = isHard
        self.exp = exp
        
    def __str__(self):
        return self.exp