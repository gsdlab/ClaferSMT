'''
Created on May 1, 2013

@author: ezulkosk
'''
from z3 import Datatype

class ClaferDatatype(object):
    '''
    :var claferSort: (:mod:`~common.ClaferSort`) ClaferSort for a given Clafer object from AST.
    :var datatype: (:mod:`~common.ClaferDatatype`) The Z3 Datatype for the given clafer. Datatype constructor is named
        *new\_sortName*, where *sortName* = *claferSort.id*. The first field
        is always the same type as *self.claferSort*, and the remaining fields
        correspond to those added by :meth:`addField`. 
        If the Clafer is of type integer, an additional integer field called 
        *ref* is added.
    :var fields: ([:class:`~common.ClaferSort`]) List of all immediate subclafers.
    :var isInteger: (bool) True if the Clafer is of type integer.
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Creates the Datatype for a given ClaferSort,
    which will be used to create the hierarchy 
    of clafers.
    '''
    
    def __init__(self, z3, claferSort, isInteger=False):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        :param claferSort: ClaferSort for a given Clafer object from AST.
        :type claferSort: :mod:`~common.ClaferSort`
        :param isInteger: True if the Clafer is of type integer.
        :type isInteger: bool
        '''
        self.z3 = z3
        self.claferSort = claferSort
        self.isInteger = isInteger
        self.fields = []
        self.addField(claferSort)
        if(isInteger):
            self.addField("ref")
    
    def addField(self, claferSort):
        '''
        :param claferSort: ClaferSort for a given Clafer object from AST
        :type claferSort: :mod:`~common.ClaferSort`
        
        A new field is added for every child of the given clafer. Fields will 
        become parameters for the Datatype constructor when generated.
        '''
        self.fields.append(claferSort)
    
    def generateDatatype(self):
        '''
        Creates the actual Z3 Datatype.
        '''
        self.datatype = Datatype(self.claferSort.id)
        self.datatype.declare("new_" + self.claferSort.id)
        
    def __str__(self):
       return self.claferSort.id+"("+ "new_" + self.claferSort.id +\
           ", " + str(self.fields) + ")" 