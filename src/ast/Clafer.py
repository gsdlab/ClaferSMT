'''
Created on Mar 23, 2013

@author: ezulkosk
'''

class Clafer(object):
    elements = []

    def __init__(self, pos, isAbstract, gcard, ident, uid, my_supers, card, glCard):
        self.pos = pos
        self.isAbstract = isAbstract
        self.gcard = gcard
        self.ident = ident
        self.uid = uid
        self.supers = my_supers
        self.card = card
        self.glCard = glCard
        
    def addElement(self, element):
        self.elements.append(element)
        
    def __str__(self):
        return self.uid