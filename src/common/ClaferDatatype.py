'''
Created on May 1, 2013

@author: ezulkosk
'''
from z3 import Datatype

class ClaferDatatype(object):
    '''
    creates the datatype for a given ClaferSort,
    which will be used to create the hierarchy 
    of clafers
    
    datatype (Datatype): the actual Z3 datatype
    fields ([]): sorts of the fields in the constructor of the z3 datatype
    
    z3 (Z3Instance)
    claferSort (ClaferSort)
    isInteger (bool): true if the clafer is of type integer
    '''
    def __init__(self, z3, claferSort, isInteger=False):
        self.z3 = z3
        self.claferSort = claferSort
        self.isInteger = isInteger
        self.fields = []
        self.addField(claferSort)
        if(isInteger):
            self.addField("ref")
    
    def addField(self, claferSort):
        self.fields.append(claferSort)
    
    def generateDatatype(self):
        self.datatype = Datatype(self.claferSort.id)
        self.datatype.declare("new_" + self.claferSort.id)
        
    def __str__(self):
       return self.claferSort.id+"("+ "new_" + self.claferSort.id +\
           ", " + str(self.fields) + ")" 