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
        self.nonUniqueID = self.uid.split("_")[1]
        self.elements = []
       
        
    def addElement(self, element):
        #print(self.elements)
        self.elements.append(element)
       
    def getNonUniqueID(self):
        """
        :returns: string
        
        Obtains the simple name of the clafer
        
        >>> nonUniqueID(c1_A) => "A"
        """
        return self.nonUniqueID
        
    def __str__(self):
        return str(self.uid)
    
    def __repr__(self):
        return self.__str__()
    
    def toString(self, level):
        return str(self.glCard) + " " + self.uid + " " + str(self.card)
        