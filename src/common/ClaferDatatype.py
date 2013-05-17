'''
Created on May 1, 2013

@author: ezulkosk
'''
from gi.overrides.keysyms import a
from z3 import Datatype, IntSort

class ClaferDatatype(object):
    '''
    :var claferSort: (:mod:`~common.ClaferSort`) ClaferSort for a given Clafer object from AST.
    :var datatype: (:mod:`~common.ClaferDatatype`) The Z3 Datatype for the given clafer. Datatype constructor is named
        *new\_sortName*, where *sortName* = *claferSort.id*. The first field
        is always the same type as *self.claferSort*, and the remaining fields
        correspond to those added by :meth:`addField`. 
        If the Clafer is of type integer, an additional integer field called 
        *ref* is added.
    
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
        #self.addField(claferSort)
        self.datatype = Datatype("$" + self.claferSort.id + "$")
        if(isInteger):
            self.addField("ref")
    
    
    
    def generateDatatype(self):
        '''
        Creates the actual Z3 Datatype.
        '''
        fieldList =  [(i.id, self.z3.z3_datatypes[i].datatype) for i in self.fields] 
        #print(fieldList)
        self.datatype.declare("new_"+ self.claferSort.id, (self.claferSort.id, self.claferSort.sort) ,*fieldList ) #("A", IntSort()))
        #print(self.datatype)
        
    def __str__(self):
       return self.claferSort.id+"("+ "new_" + self.claferSort.id +\
           ", " + str(self.fields) + ")" 