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
        
    def __str__(self):
        return self.uid
    
    def toString(self, level):
        print("  " * level + "ident="+self.ident)
        print("  " * level + "absract="+self.isAbstract)
        print("  " * level + "card="+self.card)
        print("  " * level + "gcard="+self.gcard)
        print("  " * level + "glcard="+self.glcard)
        print("  " * level + "uid="+self.uid)
        print("  " * level + "supers="+self.supers)
        print("  " * level + "elements=")
        for i in self.elements:
            i.toString(level+1)
        