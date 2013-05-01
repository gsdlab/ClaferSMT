'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from z3 import *

class ClaferSort(object):
    '''
    Contains necessary information for each clafer,
    and declares a Z3 Sort associated with it
    
    id (str): fully qualified name of the clafer
    sort (Sort): Z3 Sort associated with the clafer, declared when Z3Instance is ran
    numConsts (int): the number of z3_constants associated with this sort
    consts ([Consts]): the list of z3 Consts associated with this sort
    --TODO?: subclafers([]): lists clafers that declare this clafer as a super
      --may be useful when handling cardinalities, but not sure yet
    '''
    def __init__(self, name):
        self.id = name
        self.numConsts = 0
    
    '''
    sets the number of consts of this sort needed to construct our model 
    ''' 
    def addConsts(self, newconsts):
        self.numConsts = max(self.numConsts, newconsts)
             
    def __str__(self):
        return self.id + "_sort"
    
    def __repr__(self):
        return self.__str__()