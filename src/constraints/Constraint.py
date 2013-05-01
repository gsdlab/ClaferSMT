'''
Created on May 1, 2013

@author: ezulkosk
'''
import abc

'''
Abstract superclass for all constraints
'''
class Constraint(object):
    __metaclass__ = abc.ABCMeta
     
    '''
    comment(str): used for debugging constraints
    stringValue(str): contains the string representation of the constraint
    value(Z3 Expr): the actual z3 constraint passed to the solver
    '''
    @abc.abstractproperty
    def comment(self):
        return 'comment not implemented'
    
    @abc.abstractproperty
    def stringValue(self):
        return 'stringValue not implemented'
    
    @abc.abstractproperty
    def value(self):
        return 'value not implemented'
    
    '''
    returns the constraint in Z3 syntax
    '''
    @abc.abstractmethod
    def generateConstraint(self):
        raise NotImplementedError("generateConstraint() not implemented")
    
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError("__str__ not implemented")

        