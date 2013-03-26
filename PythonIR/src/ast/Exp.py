'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class Exp(object):
    '''
    classdocs
    '''


    def __init__(self, expType, my_type, parentId, pos, iExpType ,iExp):
        self.expType = expType
        self.type = my_type
        self.parentId = parentId
        self.pos = pos
        self.iExpType = iExpType
        self.iExp = iExp

        
    def __str__(self):
        return "ExpType: " + self.expType