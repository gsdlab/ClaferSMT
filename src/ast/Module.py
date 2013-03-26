'''
Created on Mar 23, 2013

@author: ezulkosk
'''

class Module(object):
    '''
    IModule
    '''
    elements = []
    

    def __init__(self, mName):
        self.mName = mName
        
    def addElement(self, element):
        self.elements.append(element)
        
        
    def test(self):
        print(1)
        
    def __str__(self):
        return self.mName + " " + ', '.join(map(str, self.elements))