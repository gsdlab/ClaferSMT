'''
Created on May 1, 2013

@author: ezulkosk
'''
import abc


class Constraint(object):
    '''
    Abstract superclass for all constraints
    '''
    __metaclass__ = abc.ABCMeta
     
    
    @abc.abstractproperty
    def comment(self):
        '''
        :returns: str -- Used for debugging constraints.
        '''
        return 'comment not implemented'
    
    @abc.abstractproperty
    def stringValue(self):
        '''
        :returns: str -- Contains the string representation of the constraint.
        '''
        return 'stringValue not implemented'
    
    @abc.abstractproperty
    def value(self):
        '''
        :returns: str -- The actual z3 constraint passed to the solver.
        '''
        return 'value not implemented'
    
    
    @abc.abstractmethod
    def generateConstraint(self):
        '''
        Creates the Z3 constraint to be handled by the solver.
        '''
        raise NotImplementedError("generateConstraint() not implemented")
    
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError("__str__ not implemented")

        