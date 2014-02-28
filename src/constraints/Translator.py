'''
Created on Feb 18, 2014

@author: ezulkosk
'''
from z3 import And, Exists, ForAll, Implies, Not, Function, Int
import z3

class Translator():
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    
    
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 instance.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.relations = {}
        self.sorts_of_relations = {}
        self.oneNames = {}
        
    
    def addRelation(self, *sorts):
        sorts_l = list(sorts)[0]
        rid = ".".join([str(i) for i in sorts_l])
        sorts_l.append(z3.BoolSort())
        if rid in self.relations:
            return self.relation[rid]
        #print("adding " + rid)
        f = z3.Function(rid, *sorts_l)
        self.relations[rid] = f
        self.sorts_of_relations[rid] = sorts
        
        #print(f) 
        #print(f.arity())
        for i in sorts:
            pass#print(i)
        return f
    
    
    def oneName(self, sorts):
        rid = ".".join([str(i) for i in sorts])
        if self.oneNames.get(rid):
            return self.oneNames[rid]
        else:
            #print("B")
            #print(sorts)
            oneNameF = Function('oneName_'+rid, *sorts) 
            self.oneNames[rid] = oneNameF
            return oneNameF
        
    def lone(self, claferSorts, sorts):
        rid = ".".join([str(i) for i in sorts])
        #print(rid)
        #print(self.relations)
        oneNameF =  self.oneName(sorts)
        func = self.relations[rid]
        firstSort = claferSorts[0]
        consts = [sort.consts[0] for sort in claferSorts]
        constsMinusLast = [consts[i] for i in range(len(consts)-1)]
        firstSort.constraints.addCardConstraint(ForAll(consts, Implies(func(*consts), consts[-1] == oneNameF(*constsMinusLast))))
        
    def some(self, claferSorts, sorts):
        rid = ".".join([str(i) for i in sorts])
        #print(rid)
        #print(self.relations)
        oneNameF =  self.oneName(sorts)
        func = self.relations[rid]
        firstSort = claferSorts[0]
        consts = [sort.consts[0] for sort in claferSorts]
        constsMinusLast = [consts[i] for i in range(len(consts)-1)]
        #print(constsMinusLast)
        constsMinusLastPlusOneName = constsMinusLast + [oneNameF(*constsMinusLast)]
        #print(constsMinusLastPlusOneName)
        firstSort.constraints.addCardConstraint(ForAll(constsMinusLast, func(*constsMinusLastPlusOneName)))
        
    
    def addParentChildRelation(self, child, parent,lowerCard, upperCard,  *sorts):
        func = self.addRelation([child.sort,parent.sort])
        self.lone([child,parent],[child.sort,parent.sort])
        self.some([child,parent],[child.sort,parent.sort])
        c = child.consts[0]
        p = parent.consts[0]
        i = z3.Int('i')
        #print(str(lowerCard) + " " + str(upperCard))
        #child.constraints.addCardConstraint(ForAll([c], )
        rid = ".".join([str(i) for i in sorts])
        is_sort = Function('is_' + rid, parent.sort, child.sort, z3.BoolSort())
        child.constraints.addCardConstraint(ForAll([p,c], is_sort(p,c) == func(c,p) )) #inverse
        card = Function('crd_' + rid, parent.sort, z3.IntSort())
        ord = Function('ord_' + rid, parent.sort, child.sort, z3.IntSort())
        inv0 = Function('inv0_' + rid, z3.IntSort(), parent.sort, child.sort)
        inv1 = Function('inv1_' + rid, z3.IntSort(), child.sort)
        trig = Function('trig_' + rid, z3.IntSort(), z3.BoolSort())
        c = child.consts[0]
        p = parent.consts[0]
        i = z3.Int('i')
        child.constraints.addCardConstraint(ForAll([p], And(card(p) >= 0, Implies(card(p) == 0, ForAll([c], Not(is_sort(p,c))))))) #5
        child.constraints.addCardConstraint(ForAll([p,c], Implies(is_sort(p,c), And(1 <= ord(p,c), ord(p,c) <= card(p))))) #6
        child.constraints.addCardConstraint(ForAll([p,c], Implies(is_sort(p,c), inv0(ord(p,c), p) == c)))#, inv1(ord(p,c)) == c)))) #7
        #child.constraints.addCardConstraint(ForAll([p,i], Implies(And(1 <= i, i <= card(p)), ord(inv0(i), inv1(i)) == i))) #8
        child.constraints.addCardConstraint(ForAll([p,i], Implies(And(1 <= i, i <= card(p)), ord(p,inv0(i,p)) == i))) #8
        child.constraints.addCardConstraint(ForAll([i], ForAll([p], Implies(And(1 <= i, i <= card(p)), is_sort(p, inv0(i,p)))), patterns=[trig(i)])) #9
        for j in range(3):
            k = max(1, 20*j)
            child.constraints.addCardConstraint(ForAll([i,p], Implies(0 < card(p), trig(k)))) #10
        child.constraints.addCardConstraint(ForAll([i], ForAll([p], Implies(And(1 <= i, i < card(p)), trig(i+1))),patterns=[trig(i)])) #11
        #cards
        print(lowerCard)
        print(upperCard)
        child.constraints.addCardConstraint(ForAll([p], And(lowerCard <= card(p), card(p) <= upperCard)))
        '''
        parent to child relation flip flop cards bleh bleh bleh
        '''
        