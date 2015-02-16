'''
Created on Jul 10, 2014

@author: ezulkosk
'''
'''
TODO:
    Implement my own ForAll or declare sort to incorporate QFLIA approach
'''

import z3


def declareSort(clafer):
    if not clafer.super_clafer:
        return z3.DeclareSort(clafer.name)
    return None

def declareBoundedSort(claferSort):
    if not claferSort.superSort:
        (s,consts) = z3.EnumSort(claferSort.element.uid, [claferSort.element.uid + "_" + str(i) for i in range(4)])
        #print(s)
        return (s,consts)
    return (None,None)

def isOn(claferSort):
    if not claferSort.superSort:
        return z3.Function("isOn_" + claferSort.element.uid, claferSort.sort, z3.BoolSort())
    
def T(clafer):
    if not clafer.super_clafer:
        return clafer
    else:
        curr_clafer = clafer.super_clafer
        while curr_clafer:
            if curr_clafer.super_clafer:
                curr_clafer = curr_clafer.super_clafer
            else:
                return curr_clafer

def isName(clafer):
    return z3.Function("isName_" + str(clafer.name), T(clafer).sort, z3.BoolSort())

def isA(model, s1, s2):
    i = T(s1).consts[0]
    model.assertions.append(z3.ForAll(i, z3.Implies(s1.isName(i), s2.isName(i))))


def getRelationName(s1, s2):
    return "r$" + s1.name + "$" + s2.name

#for hierarchy, s1 = child, s2 = parent
def relation(model, s1, s2, lone=False, some=False):
    rname = getRelationName(s1, s2)
    r = model.relations.get(rname)
    c1 = T(s1).consts[0]
    p1 = T(s2).consts[0]
    p2 = T(s2).consts[1]
    if not r:
        r = z3.Function(rname, T(s1).sort, T(s2).sort, z3.BoolSort())
        model.relations[rname] = r
        constraint = z3.ForAll([c1,p1], z3.Implies(r(c1,p1), z3.And(s1.isName(c1), s2.isName(p1))))
        model.assertions.append(constraint)
    if lone:
        constraint = z3.ForAll([c1,p1,p2], z3.Implies(z3.And(r(c1,p1), r(c1,p2)), p1 == p2))
        model.assertions.append(constraint)
    if some:
        #constraint = z3.ForAll(c1, z3.And(z3.Implies(T(s1).isOn(c1), z3.Exists(p1, r(c1,p1))),
        #                                  z3.Implies(z3.Exists(p1, r(c1,p1)), T(s1).isOn(c1))))
        constraint = z3.ForAll(c1, z3.Exists(p1, r(c1,p1)))
        model.assertions.append(constraint)
    return r

def And(s1, s2):
    return z3.And(s1, s2)
    
#TODO ensure 0 upper bound case?
def setCard(model, s):
    #print(str(s) + ": " + str(s.card))
    (lcard, ucard) = s.card
    if lcard <= 0 and ucard < 0:
        return

    if s.parent:
        #TODO:
        return
        p = s.parent.getNewConst()
        r = model.relations[getRelationName(s, s.parent)]
    else:
        s.createIntFunctions()
        i = z3.Int('i')
        c = s.get_const(0)
        c5 = z3.And(s.crd() >= 0, z3.Implies(s.crd() == 0, z3.ForAll([c], z3.Not(s.isName(c)))))
        c6 = z3.ForAll([c], z3.Implies(s.isName(c), And(1 <= s.ord(c), s.ord(c) <= s.crd()))) 
        c7 = z3.ForAll([c], z3.Implies(s.isName(c), s.inv(s.ord(c)) == c))
        c8 = z3.ForAll([i], z3.Implies(And(1 <= i, i <= s.crd()), s.ord(s.inv(i)) == i)) 
        c9 = z3.ForAll([i], z3.Implies(And(1 <= i, i <= s.crd()), s.isName(s.inv(i))), patterns=[s.trg(i)]) 
        c10 = z3.Implies(0 < s.crd(), s.trg(1)) 
        c11 = z3.ForAll([i], z3.Implies(And(1 <= i, i < s.crd()), s.trg(i+1)),patterns=[s.trg(i)]) 
        if lcard == ucard:
            card = s.crd() == lcard
        elif ucard > lcard:
            card = z3.And(s.crd() >= lcard, s.crd <= ucard)
        else:
            card = z3.And(s.crd() >= lcard)
        model.assertions.extend([c5,c6,c7,c8,c9,c10,c11,card])
        
            
def noOverlappingSubs(model, s):
    subs = s.subs
    p = s.consts[0]
    cons = z3.ForAll(p, z3.And(*[z3.Not(z3.And(subs[i].isName(p), subs[j].isName(p))) for i in range(len(subs) - 1) for j in range(i+1, len(subs))]))
    
    model.assertions.append(cons)
