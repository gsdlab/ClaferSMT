'''
Created on Nov 28, 2014

@author: ezulkosk
'''
import random
import sys
import time

from z3 import sat, And, Xor, Or, Implies, Not, z3, If, Sum, BitVec, Real, Bool, Int

from common import Common
from front.ClaferModel import ClaferModel
from solvers.Z3Solver import Z3Solver, Z3Converter


class WalkZ3Solver(Z3Solver):
    
    def __init__(self, cfr):
        #TODO fix multiple instances
        self.cfr = cfr
        self.MAX_TRIES = 100000000000000000000
        self.MAX_FLIPS = 100000000000000000000
        self.solver = z3.Solver()
        self.converter = Z3Converter()
        self.goal = z3.Goal()
        self.boolean_abstraction_solver = z3.Solver()
        self.atom_hash_map = {}
        self.bool_to_atom_list = []
        self.bools = []
        self.trackers = []
        self.track_map = {}
        self.next_bool_num = 0
        self.cache_hits = 0
        self.cnf_tactic = z3.Then('simplify', 'tseitin-cnf', 'propagate-values')

    def add(self, constraint):
        self.goal.add(constraint.convert(self.converter))

    def next_bool(self):
        index = self.next_bool_num
        self.next_bool_num += 1
        b = z3.Bool("c" + str(index))
        self.bools.append(b)
        return b

    def canonize_lit(self, lit):
        decl = lit.decl().name()
        if decl == "not":
            return z3.Not(self.canonize_lit(lit.children()[0]))
        elif(decl == "="):
            #print(lit)
            (l,r) = tuple(lit.children())
            if l.hash() <= r.hash():
                return lit
            else:
                return r == l
        elif decl == "<=":
            return lit
        elif decl == ">=":
            (l,r) = tuple(lit.children())
            return r <= l
        elif decl.startswith("k!"):
            #tseitin variables
            return lit
        else:
            sys.exit("TODO canonize: " + decl)
        return lit

    def canonize_cnf(self, cnf):
        #canonical form:
        canonized_cnf = []
        for c in cnf:
            if isinstance(c.decl(),z3.FuncDeclRef) and (c.decl().name() == "or"):
                clause = []
                for i in c.children():
                    #i is a literal
                    clause.append(self.canonize_lit(i))
                canonized_cnf.append(z3.Or(clause))
            else:
                canonized_cnf.append(self.canonize_lit(c))
        return canonized_cnf
        

    def cache_atom(self, atom):
        #atom = self.canonize(atom)
        key = atom.hash()
        prev = self.atom_hash_map.get(key)
        if prev:
            #already in hash, return Not(b)
            self.cache_hits += 1
            b = prev
            return b
        else:
            #not in hash, add child0 and return next bool
            b = self.next_bool()
            self.atom_hash_map[key] = b    
            self.bool_to_atom_list.append(atom) 
            return b
            
    def T2B(self, lit):
        if isinstance(lit, z3.BoolRef):
            if(lit.decl().name() == "not"):
                b = self.cache_atom(lit.children()[0])
                return z3.Not(b)
            else:
                return self.cache_atom(lit)
        else:
            sys.exit("Unimplemented -- didn't think this could be hit.. TODO remove?")

    def add_and_track(self, solver, clause, constraint):
        #TODO: Use assert_and_track
        b = z3.Bool("track" + str(len(self.trackers)))
        self.track_map[len(self.trackers)] = clause
        self.trackers.append(b)
        solver.add(z3.Implies(b, constraint))

    ########### WALKSAT##################################
   
    def initial_assignment(self):
        conj = []
        for i in self.bools:
            asn = i if random.random() < 0.5 else z3.Not(i)
            conj.append(asn)
        return conj
        
    def c_index(self, lit):
        if str(lit.decl()) == "Not": 
            index = int(str(lit.children()[0]).replace("c",""))
        else:
            index = int(str(lit).replace("c",""))
        return index
    
    def next_truth_assignment(self, lit, asn_list):
        #TODO hard case also probabilities
        index = self.c_index(lit)
        curr_val = asn_list[index]
        if str(curr_val.decl()) == "Not":
            asn_list[index] = curr_val.children()[0]
        else:
            asn_list[index] = z3.Not(curr_val)
        return asn_list
    
    def model(self):
        return self.tsolver.model()
    
    def preprocess(self):
        #convert input to CNF
        cnf = self.cnf_tactic.apply(self.goal)[0]
        if cnf[0].decl().name() == "false":
            return False
    
        #canonize it to improve atom cache hits
        canonized_cnf = self.canonize_cnf(cnf)
        #T2B
        for c in canonized_cnf:
            decl = c.decl().name()
            if decl == "or":
                clause = []
                for i in c.children():
                    clause.append(self.T2B(i))
                self.add_and_track(self.boolean_abstraction_solver, clause, z3.Or(clause))
            else:
                h = self.T2B(c)
                self.add_and_track(self.boolean_abstraction_solver, [h], h)
        return True
    
    def walksmt(self):
        
        res = self.preprocess()
        if not res:
            return Common.UNSAT
        learned_clauses = []
        for i in range(self.MAX_TRIES):
            asn_list = self.initial_assignment()
            for i in range(self.MAX_FLIPS):
                self.boolean_abstraction_solver.push()
                self.boolean_abstraction_solver.append(z3.And(asn_list))
                for i in learned_clauses:
                    #TODO: reuse vars..
                    self.add_and_track(self.boolean_abstraction_solver, i, z3.Or(i))
                status = self.boolean_abstraction_solver.check(self.trackers)
                if status == z3.sat:
                    #TODO: can we do this more incrementally?
                    tsolver = z3.Solver()
                    tsolver_map = {}
                    for i in range(len(asn_list)):
                        c = asn_list[i]
                        if c.decl().name() == "not":
                            lit = z3.Not(self.bool_to_atom_list[i])
                        else:
                            lit = self.bool_to_atom_list[i]
                        tracker_name = 'p' + str(i)
                        tracker = Bool(tracker_name)
                        tsolver_map[tracker_name] = lit
                        tsolver.assert_and_track(lit, tracker)
                    tstatus = tsolver.check(self.trackers)
                    #TODO Cleanup trackers
                    if tstatus == z3.sat:
                        print("TSAT")
                        #TODO: Get model
                        self.tsolver = tsolver
                        return Common.SAT
                    else:
                        print("TUNSAT")
                        new_clause = []
                        for i in tsolver.unsat_core():
                            lit = tsolver_map[i.decl().name()]
                            if lit.decl().name() == "not":
                                atom = lit.children()[0]
                                is_not = True
                            else:
                                atom = lit
                                is_not = False
                            b = self.atom_hash_map[atom.hash()]
                            new_clause.append(b if is_not else z3.Not(b))
                        #print(new_clause)
                        learned_clauses.append(new_clause)
                else:
                    #boolean abstraction -- unsat case
                    #print(self.boolean_abstraction_solver.unsat_core())
                    tracker = random.choice(self.boolean_abstraction_solver.unsat_core())
                    
                    num = int(str(tracker).replace("track",""))
                    clause = self.track_map[num]
                    #print(clause)
                    lit = random.choice(clause)
                    self.next_truth_assignment(lit, asn_list)
                self.boolean_abstraction_solver.pop()
        sys.exit("Timeout for SLS. TODO: make this an exception")
    
    #####################################################
        
    def check(self, unsat_core_trackers=None):
        return self.walksmt()
        
        