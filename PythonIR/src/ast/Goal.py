'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class Goal(object):
    '''
    classdocs
    '''


    def __init__(self, isMaximize, exp):
        self.isMaximize = isMaximize
        self.exp = exp
        
    def __str__(self):
        return self.isMaximize + self.exp