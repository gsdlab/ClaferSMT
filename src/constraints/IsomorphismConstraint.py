'''
Created on Oct 7, 2013

@author: ezulkosk
'''

from ast import IntegerLiteral, FunExp, Exp, ClaferId, DeclPExp, \
    LocalDeclaration, Declaration
from common.Common import standard_print
from structures.ClaferSort import PrimitiveType
from visitors import VisitorTemplate, Visitor, CreateBracketedConstraints, \
    ResolveClaferIds
from z3 import ModelRef
import ast
import visitors

class IsomorphismConstraint(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    
    zero_pos = ((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
    
    def __init__(self, z3, model):
        '''
        :param z3: The Z3 instance.
        :type z3: :class:`~common.Z3Instance`
        :param model: The Z3 model produced, which we can use to get the values of each variable in the instance.
        :type model: :class: ModelRef
        '''
        self.z3 = z3
        self.model = model
        self.constraint = None
        self.topCardsConstraint = None
        self.topSome = None
        self.currSome = None
    
    def isOn(self, inst, sort):
        return int(str(inst)) != sort.parentInstances
    
    def createIsomorphicConstraint(self):
        assert isinstance(self.model, ModelRef)
        sorts = self.z3.getSorts()
        instsMap = {}
        someStrings = []
        topCardStrings = []
        otherConstraints = []
        refConstraints = []
        #create the (some's
        for i in sorts:
            insts = []
            for j in range(len(i.instances)):
                ev = self.model.eval(i.instances[j])
                if self.isOn(ev, i):
                    insts.append(str(i) + "_" + str(j))
            currSome = "(some "
            instsMap[i.element.uid] = insts
            for j in range(len(insts) - 1):
                currSome = currSome + insts[j] + " ; "
            currSome = currSome + insts[-1] + " : " + i.element.getNonUniqueID() + " | "
            localDeclList = []
            for j in insts:
                localDeclList.append(self.createLocalDecl(j))
            decl = self.createDeclaration(localDeclList, i.element.uid)
            self.createSome(decl)
            someStrings.append(currSome)
        #handle top-level clafer cardinalities
        for i in sorts:
            if i.isTopLevel:
                insts = instsMap[i.element.uid]
                topCardStrings.append("#" + i.element.getNonUniqueID() + " = " + str(len(insts)))
                if not self.topCardsConstraint:
                    self.topCardsConstraint = self.createEquals(self.createCard(self.createArg(i.element.uid)), self.createInteger(str(len(insts))))
                else:
                    self.topCardsConstraint = self.createAnd(self.topCardsConstraint, self.createEquals(self.createCard(self.createArg(i.element.uid)), self.createInteger(str(len(insts)))))
        #handle non-top level clafer cardinalities
        for i in sorts:
            for j in range(len(i.instances)):
                ev = self.model.eval(i.instances[j])
                if self.isOn(ev, i):
                    for k in i.fields:
                        currChildren = []
                        for l in range(len(k.instances)):
                            if str(self.model.eval(k.instances[l])) == str(j):
                                child = str(k) + "_" + str(l) 
                                currChildren.append(child)
                                otherConstraints.append(child \
                                      + " in " + str(i) + "_" + str(j) + "." \
                                      + k.element.getNonUniqueID())
                                self.addConstraint(self.createIn(self.createArg(child), self.createJoin(self.createArg(str(i) + "_" + str(j)), self.createArg(k.element.uid))))
                        otherConstraints.append("#" + str(i) + "_" + str(j) + "." + k.element.getNonUniqueID()\
                              + " = " + str(len(currChildren)))
                        self.addConstraint(self.createEquals(self.createCard(self.createJoin(self.createArg(str(i) + "_" + str(j)), self.createArg(k.element.uid))), self.createInteger(str(len(currChildren)))))
                        for l in currChildren:
                            for m in currChildren:
                                if l != m:
                                    otherConstraints.append(l + " != " + m)
                                    self.addConstraint(self.createNotEquals(self.createArg(l), self.createArg(m)))
        #handle ref constraints
        for i in sorts: 
            if i.refSort:
                for j in range(len(i.instances)):
                    if self.isOn(self.model.eval(i.instances[j]), i):
                        if isinstance(i.refSort, PrimitiveType) and i.refSort == "integer":
                            self.addConstraint(self.createEquals(self.createJoin(self.createArg(str(i) + "_" + str(j)), self.createArg("ref")), \
                                                                    self.createInteger(str(self.model.eval(i.refs[j])))))
                            refConstraints.append(str(i) + "_" + str(j) + ".ref = " +  str(self.model.eval(i.refs[j])))
                        else:
                            refConstraints.append(str(i) + "_" + str(j) + ".ref = " + str(i.refSort) + "_" + str(self.model.eval(i.refs[j])))
                            self.addConstraint(self.createEquals(self.createJoin(self.createArg(str(i) + "_" + str(j)), self.createArg("ref")), \
                                                                    self.createArg(str(str(i.refSort) + "_" + str(self.model.eval(i.refs[j]))))))
        '''
        print("[ !(")
        for i in topCardStrings:
            print(i + " &&")
        for i in someStrings:
            print(i)
        print(" &&\n".join(otherConstraints + refConstraints))
        print(")"*(len(someStrings) + 1))
        print("]")
        '''
        self.currSome.bodyParentExp = self.constraint
        bigConstraint = self.createAnd(self.topSome, self.topCardsConstraint)
        bigConstraint = self.createNot(bigConstraint)
        Visitor.visit(ResolveClaferIds.ResolveClaferIds(self.z3), bigConstraint)
        createBracketed = CreateBracketedConstraints.CreateBracketedConstraints(self.z3, True)
        #print(bigConstraint)
        createBracketed.isomorphismVisit(bigConstraint)
        
        
        #self.createConstraint(topCardStrings, someStrings, otherConstraints)
        
    def createArg(self, arg_id):
        #Exp.Exp()), ( iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c14_F_sort_0", isTop=True)]
        return Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=self.zero_pos, \
                       iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id=arg_id, isTop=False)]) 
    
    def createLocalDecl(self, arg):
        return LocalDeclaration.LocalDeclaration(arg)
    
    def createInteger(self, arg):
        return IntegerLiteral.IntegerLiteral(int(arg))
    
    def createDeclaration(self, locals, sort):
        return Declaration.Declaration(isDisjunct=False, localDeclarations=locals,  body=
        Exp.Exp(expType="Body", my_type="Set", parentId="", pos=self.zero_pos, iExpType="IClaferId", \
                iExp=[ClaferId.ClaferId(moduleName="", my_id=sort, isTop=True)]))
    
    def createFunExpr(self, op, elems):
        return FunExp.FunExp(operation = op, elements=elems) 
    
    def createJoin(self, left, right):
        return self.createFunExpr(".", [left,right])
     
    def createCard(self, arg):
        return self.createFunExpr("#", [arg])  
    
    def createEquals(self, left, right):
        return self.createFunExpr("=", [left,right])  
    
    def createIn(self, left, right):
        return self.createFunExpr("in", [left,right])   
    
    def createNotEquals(self, left, right):
        return self.createFunExpr("!=", [left,right])   
    
    def createAnd(self, left, right):
        return self.createFunExpr("&&", [left,right])   
    
    def createNot(self, arg):
        return self.createFunExpr("!", [arg])  
    
    def createSome(self, decl):
        some =  DeclPExp.DeclPExp(quantifier="Some", declaration=decl, bodyParentExp=None)
        if not self.topSome:
            self.topSome = some
        if self.currSome:
            self.currSome.bodyParentExp = some
        self.currSome = some
    
    def addConstraint(self, other):
        if self.constraint:
            self.constraint = self.createAnd(self.constraint, other)
        else:
            self.constraint = other
        #bottom up
        #for i in otherConstraints
        