'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from z3 import *

class ClaferSort(object):
    '''
    Contains necessary information for each clafer,
    and declares a Z3 Sort associated with it
    
    name (str): fully qualified name of the clafer
    sort (Sort): Z3 Sort associated with the clafer
    --subclafers([]): lists clafers that declare this clafer as a super
      --may be useful when handling cardinalities, but not sure yet
    
    '''
    
    def __init__(self, name):
        self.name = name
        self.sort = DeclareSort(name)
        
        
    
    def __str__(self):
        return self.name + "_sort"
    
    def __repr__(self):
        return self.__str__()