'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from constraints import BracketedConstraint
from visitors import VisitorTemplate
import visitors.Visitor

claferStack = [] #used to determine where the constraint is in the clafer hierarchy
inConstraint = False #true if beneath a constraint node
currentConstraint = None #holds the constraint currently being traversed


class CreateBracketedConstraints(VisitorTemplate.VisitorTemplate):
    '''
    :var CreateBracketedConstraints.currentConstraint: (:mod:`~constraints.BracketedConstraint`) Holds the constraint currently being traversed. 
    :var CreateBracketedConstraints.inConstraint: (bool) True if the traversal is currently within a constraint.
    :var claferStack: ([:mod:`~common.ClaferSort`]) Stack of clafers used primarily for debugging.
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Converts Clafer constraints to z3 syntax,
    adds constraints to z3.z3_constraints
    field.
    '''
    
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        CreateBracketedConstraints.inConstraint = False
        self.z3 = z3
    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        claferStack.append(self.z3.getSort(element.uid))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        claferStack.pop()
    
    def claferidVisit(self, element):
        if(CreateBracketedConstraints.inConstraint):
            #CreateBracketedConstraints.currentConstraint.addArg(element)
            if element.id != "ref" and element.id != "this":
                CreateBracketedConstraints.currentConstraint.addArg(([element.claferSort], [element.claferSort.instances]))
            elif element.id == "this":           
                instances = []
                for i in range(element.claferSort.numInstances):
                    instances.append([element.claferSort.parentInstances if i != j else element.claferSort.instances[j] 
                                      for j in range(element.claferSort.numInstances)])
                CreateBracketedConstraints.currentConstraint.addArg(([element.claferSort], instances))
                CreateBracketedConstraints.currentConstraint.this = element.claferSort
            else:
                CreateBracketedConstraints.currentConstraint.addArg("ref")
   
    def constraintVisit(self, element):
        CreateBracketedConstraints.inConstraint = True
        CreateBracketedConstraints.currentConstraint = BracketedConstraint.BracketedConstraint(self.z3, claferStack)
        visitors.Visitor.visit(self, element.exp)
        CreateBracketedConstraints.currentConstraint.endProcessing(None)
        CreateBracketedConstraints.currentConstraint = None
        CreateBracketedConstraints.inConstraint = False
    
    def funexpVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(CreateBracketedConstraints.inConstraint):
            CreateBracketedConstraints.currentConstraint.addOperator(element.operation)
            
    
    def localdeclarationVisit(self, element):
        #prettyPrint("element="+element.element)
        pass
    
    def integerliteralVisit(self, element):
        if(CreateBracketedConstraints.inConstraint):
            CreateBracketedConstraints.currentConstraint.addArg(([element], [element.value]))
        
    def doubleliteralVisit(self, element):
        return element
        
    def stringliteralVisit(self, element):
        return element
    