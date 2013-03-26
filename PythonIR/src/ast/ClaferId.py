'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class ClaferId(object):
    '''
    classdocs
    '''


    def __init__(self, moduleName, my_id, isTop):
        self.moduleName = moduleName
        self.my_id = my_id
        self.isTop = isTop
        
        
    def __str__(self):
        return self.my_id