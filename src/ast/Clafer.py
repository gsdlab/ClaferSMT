'''
Created on Mar 23, 2013

@author: ezulkosk
'''


class Clafer(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, pos, isAbstract, gcard, ident, uid, my_supers, card, glCard):
        self.pos = pos
        self.isAbstract = isAbstract
        self.gcard = gcard
        self.ident = ident
        self.uid = uid
        self.supers = my_supers
        self.card = card
        self.glCard = glCard
        self.elements = []
        
    def addElement(self, element):
        #print(self.elements)
        self.elements.append(element)
       
    def nonUniqueID(self):
        return self.uid.split("_")[1]
        
    def __str__(self):
        return self.uid
    
    def toString(self, level):
        self.uid.split("_",1)[1]
        