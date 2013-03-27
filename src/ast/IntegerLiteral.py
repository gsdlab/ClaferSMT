'''
Created on Mar 26, 2013

@author: ezulkosk
'''

class IntegerLiteral(object):
    '''
    classdocs
    '''


    def __init__(self,value):
        self.value=value
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()