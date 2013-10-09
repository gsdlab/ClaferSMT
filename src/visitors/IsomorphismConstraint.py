'''
Created on Oct 7, 2013

@author: ezulkosk
'''

from common.Common import standard_print
from lxml.builder import basestring
from visitors import VisitorTemplate
import ast
import visitors

class IsomorphismConstraint(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    
    '''
    
    def __init__(self, z3, model):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.cardStrings = []
        self.returnStr = ""
        self.refString = ""
        self.someString = ""
        self.model = model
        self.parentStack = [0] #used to determine the parent of each clafer
        self.stringStack = []
        self.localDeclCounter = 0
    
    def createLocalSort(self, sort):
        rstr = ""
        for i in self.stringStack:
            rstr = rstr + i + "."
        rstr = rstr + str(sort.element.nonUniqueID())
        return rstr
    
    def createRefSome(self, sort):
        #need to "resolve" "sort"
        card = 0
        for i in sort.instanceIsReffed:
            if i != 0:
                card = card + 1
                
        if card == 0: 
            return ""
        if sort.isTopLevel:
            rstr = "(some "
        localStrings = []
        for i in range(sort.numInstances):
            if(sort.instanceIsReffed[i] != 0 and card != 1):
                rstr = rstr + ("r" + str(sort.instanceIsReffed[i])+ "; " )
                card = card - 1
                localStrings.append("r" + str(sort.instanceIsReffed[i]))
            elif sort.instanceIsReffed[i] != 0 and card == 1:
                rstr = rstr + ("r" + str(sort.instanceIsReffed[i]))
                localStrings.append("r" + str(sort.instanceIsReffed[i]))
            
        #fixme
        rstr = rstr + (" : " + self.createLocalSort(sort) + " | ")
        self.localDeclCounter = self.localDeclCounter + 1
        #unique instances
        for i in range(len(localStrings)-1):
            for j in range(i+1, len(localStrings)):
                if i != len(localStrings)-2 or j != len(localStrings):
                    rstr = rstr + localStrings[i] + " != " + localStrings[j] +  " && "
                else :
                    rstr = rstr + localStrings[i] + " != " + localStrings[j]
        return rstr
    
    
    def createSome(self, sort, card):
        #need to "resolve" "sort"
        if self.someString == "":
            if card == 0:
                return "(no " + self.createLocalSort(sort)
            rstr = "(some "
        else:
            if card == 0: 
                #fixme
                return "&& (no " + self.createLocalSort(sort)
            rstr = "&& (some "
        for i in range(card - 1):
            rstr = rstr + ("d" + str(self.localDeclCounter)+ "; " )
            
            self.localDeclCounter = self.localDeclCounter + 1
        #fixme
        rstr = rstr + ("d" + str(self.localDeclCounter)+ " : " + self.createLocalSort(sort) + " | ")
        self.localDeclCounter = self.localDeclCounter + 1
        #unique instances
        for i in range(self.localDeclCounter - card, self.localDeclCounter - 1):
            for j in range(i+1, self.localDeclCounter):
                if i != self.localDeclCounter -2 or j != self.localDeclCounter -1:
                    rstr = rstr + "d" + str(i) + " != " + "d" + str(j)  + " && "
                else:
                    rstr = rstr + "d" + str(i) + " != " + "d" + str(j)
        return rstr
    
    def appendStr(self, s):
        self.returnStr = self.returnStr + s + "\n"
        
    def prependStr(self, s):
        self.returnStr = s  + "\n" + self.returnStr
    
    def claferVisit(self, element):
        sort = self.z3.z3_sorts[element.uid]
        fromRefStr = ""
        if sort.isReffed:
            fromRefStr = self.createRefSome(sort)
            if fromRefStr != "":
                self.refString = (fromRefStr) + self.refString
        if element.isAbstract and self.parentStack == [0]:
            return
        
        card = 0
        for j in range(sort.numInstances):
            if not element.isAbstract:
                isOn = str(self.model.eval(sort.instances[j])) == str(self.parentStack[-1])
            else:
                isOn = str(self.model.eval(sort.instances[j])) != str(sort.parentInstances) and \
                    str(j) == str(self.parentStack[-1])
            if isOn:
                card = card + 1
        #print("#"str(sort.element.nonUniqueID()) + " " + str(card))
        if sort.isTopLevel:
            self.cardStrings.append("[#" + str(sort.element.nonUniqueID()) + " = " + str(card) + "]")
        else:
            self.appendStr(" && #"+ self.createLocalSort(sort) + " = " + str(card))
        self.appendStr(self.createSome(sort, card))
        localStrings = []
        for i in range(self.localDeclCounter - card, self.localDeclCounter):
            localStrings.append("d" + str(i))
        for j in range(sort.numInstances):
            if str(self.model.eval(sort.instances[j])) != str(sort.parentInstances) and \
                    str(j) == str(self.parentStack[-1]):#str(self.model.eval(sort.instances[j])) == str(self.parentStack[-1]):
                currLocal = localStrings.pop(0)
            else:
                continue
            if not sort.refs and not element.isAbstract:
                pass#standard_print(str(indent) + str(sort.instances[j]))
            elif not element.isAbstract:
                if isinstance(sort.refSort, basestring) and sort.refSort == "integer":
                    if str(self.model.eval(sort.instances[j])) == str(self.parentStack[-1]):
                        self.appendStr("&& " + currLocal + ".ref = " + str(self.model.eval(sort.refs[j])))#standard_print(str(indent) + str(sort.instances[j]) + " = " + str(self.model.eval(sort.refs[j])))
                else:   
                    self.appendStr(("&& " + currLocal + " = r" 
                          + str(sort.refSort.instanceIsReffed[int(str(self.model.eval(sort.refs[j])))])))
                    pass#standard_print(str(indent) + str(sort.instances[j]) + " = " + 
                        #           str(sort.refSort.element.uid.split("_",1)[1]) + 
                        #           "__"+ str(self.model.eval(sort.refs[j])))
            if str(self.model.eval(sort.instances[j])) == str(self.parentStack[-1]):
                self.parentStack.append(j)
                self.stringStack.append(currLocal)
                for i in element.elements:
                    visitors.Visitor.visit(self, i)
                if sort.superSort:
                    self.parentStack.append(j + sort.indexInSuper)
                    #for i in sort.superSort.element.elements:
                    #    visitors.Visitor.visit(self, i)
                    visitors.Visitor.visit(self, sort.superSort.element)
                    self.parentStack.pop()
                self.parentStack.pop()
                self.stringStack.pop()
        #close some
        self.returnStr = self.returnStr + ")"
        #if fromRefStr != "":
        #    self.returnStr = self.returnStr + ")"
        if sort.isTopLevel:
            self.someString = self.someString + (self.returnStr)
            self.returnStr = ""
    
    def moduleVisit(self, element):
        '''
        :param element: A Module AST node
        :type element: :class:`~ast.Module`
        '''
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        bigString = ""
        
        for i in self.cardStrings:
            bigString = bigString + i
        print("[")
        print(self.refString)
        print(self.someString)
        print("]")
        print(bigString)
        
class HandleRefs(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    
    def __init__(self, z3, model):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.returnStr = ""
        self.model = model
        self.parentStack = [0] #used to determine the parent of each clafer
        self.stringStack = []
        self.localDeclCounter = 1
    
    def claferVisit(self, element):
        sort = self.z3.z3_sorts[element.uid]
        
        if sort.refSort:
            for i in range(len(sort.refs)):
                if int(str(self.model.eval(sort.instances[i]))) != int(sort.parentInstances) and  \
                    sort.refSort.instanceIsReffed[int(str(self.model.eval(sort.refs[i])))] == 0:
                    sort.refSort.instanceIsReffed[int(str(self.model.eval(sort.refs[i])))] = self.localDeclCounter
                    self.localDeclCounter = self.localDeclCounter + 1
                    
        
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        
    