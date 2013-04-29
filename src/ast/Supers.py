'''
Created on Mar 23, 2013

@author: ezulkosk
'''

class Supers(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, isOverlapping, elements):
        self.isOverlapping = isOverlapping
        self.elements = elements
        
    def __str__(self):
        return self.elements
    