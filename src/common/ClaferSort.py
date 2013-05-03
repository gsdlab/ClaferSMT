'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from z3 import *

class ClaferSort(object):
    '''
    :var consts: ([Z3_Consts]) The list of Z3 Consts associated with this Sort.
    :var id: (str) The string ID of the Sort
    :var numConsts: The number of Z3 consts of this sort required to
            specify constraints over this Sort.
    :var sort: Z3 Sort associated with the clafer, declared when Z3Instance is ran.
    
    Contains necessary information for each clafer,
    and declares a Z3 Sort associated with it
    '''
    
    def __init__(self, name):
        '''
        :param name: The ID of the sort.
        :type name: str
        '''
        self.id = name
        self.numConsts = 0
    
     
    def addConsts(self, newconsts):
        '''
        :param newconsts: The number of Z3 consts of this sort required to
            specify the constraint that called this method. e.g. A lower bound 
            cardinality constraint *c* with card (5,10) would call addConsts(11)
            to specify the upper bound.  
        :type newconsts: int
        '''
        self.numConsts = max(self.numConsts, newconsts)
             
    def __str__(self):
        return self.id + "_sort"
    
    def __repr__(self):
        return self.__str__()