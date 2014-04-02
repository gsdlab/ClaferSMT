'''
Created on Nov 21, 2013

@author: ezulkosk
'''



from common import Options
from common.Clock import Clock
from gia import consts
from gia.consts import METRICS_MINIMIZE, METRICS_MAXIMIZE
from gia.npGIAforZ3 import GuidedImprovementAlgorithmOptions, \
    GuidedImprovementAlgorithm
from parallel import Consumer
from parallel.heuristics import SAP
from visitors import PrintHierarchy, Visitor
from z3 import *
import argparse
import csv
import importlib
import itertools
import math
import multiprocessing
import operator
import os
import random
import sys
import time






#from Z3ModelEmergencyResponseUpdateAllMin import *
#from Z3ModelWebPortal import *




def replicateSolver(solver, num_consumers):
    solvers = []
    for _ in range(num_consumers):
        newSolver = Solver()
        for j in solver.assertions():
            newSolver.add(j)
        solvers.append(newSolver)
    return solvers    


def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

def getZ3Feature(feature, expr):
    #print("B")
    if(str(expr) == feature):
        return expr
    for child in expr.children():
        result = getZ3Feature(feature, child)
        if result:
            return result
    return []

class ParSolver():
    def __init__(self, z3, module, solver, metrics_variables, metrics_objective_direction):
        self.z3 = z3
        self.module = module
        self.solvers = replicateSolver(solver, Options.CORES)
        self.metrics_variables = metrics_variables
        self.metrics_objective_direction = metrics_objective_direction
        self.clock = Clock()
        self.consumerConstraints = self.splitter()
    
    def run(self):
        mgr = multiprocessing.Manager()
        taskQueue = mgr.Queue()
        #for i in range(Options.CORES):
        #    taskQueue.append(mgr.Queue())
        solutions = mgr.Queue()
        totalTime = mgr.Queue()
        
        # Enqueue initial tasks
        for i in range(Options.NUM_SPLIT):
            taskQueue.put(i)
        for i in range(Options.CORES):
            taskQueue.put("Poison")
        
        # Start consumers 
        #case: objectives
        if self.metrics_variables:
            self.consumers = [ Consumer.GIAConsumer(taskQueue, solutions, self.z3, totalTime, i, "out", Options.CORES, j, self.metrics_variables, self.metrics_objective_direction, self.consumerConstraints)
                            for i,j in zip(range(Options.CORES), self.solvers)]
        #case: no objectives
        else:
            self.consumers = [ Consumer.StandardConsumer(taskQueue, solutions, self.z3, totalTime, i, "out", Options.CORES, j, self.consumerConstraints)
                            for i,j in zip(range(Options.CORES), self.solvers)]
        
        
        self.clock.tick("ParSolver")
        for w in self.consumers:
            w.start()            
        for w in self.consumers:
            w.join()  
        num_jobs = Options.CORES
        results = []
        
        while not solutions.empty():
            result = solutions.get()
            results.append(result)
        merged_results = self.merge(results)
        #print(merged_results)
        self.clock.tock("ParSolver")
        self.clock.printParEvents()
        return merged_results
        
        
    def merge(self, results):
        if self.metrics_variables:
            results = self.removeDominatedAndEqual(results)
            return [i for (i,_) in results]
        else:
            return list(set(results))
        
        
    def checkDominated(self, l, r):
        worseInOne = False
        betterInOne = False
        for i in range(len(l)):
            ml = l[i]
            mr = r[i]

            if self.metrics_objective_direction == consts.METRICS_MAXIMIZE:
                if  ml < mr:
                    worseInOne = True
                elif ml > mr:
                    betterInOne = True
            elif self.metrics_objective_direction == consts.METRICS_MINIMIZE:
                if  ml > mr:
                    worseInOne = True
                elif ml < mr:
                    betterInOne = True
        if worseInOne and not betterInOne:
            return True
        return False
    
    def removeDominatedAndEqual(self, results):
        count = len(results)
        removalList = [False for _ in range(count)]
        for i in range(count):
            for j in range(count):
                if i < j:
                    if self.checkDominated(results[i][1], results[j][1]):
                        removalList[i] = True
                    elif results[i][0] == results[j][0]:
                        removalList[i] = True
        nonDominated = []
        for i in removalList:
            if not i:
                nonDominated.append(results[i])
        return nonDominated
    
            
                 
    
    def splitter(self):
        if Options.SPLIT == Options.SAP:
            print(self.z3.z3_sorts)
            server =  self.z3.getSort("c0_" + Options.SERVER)
            service = self.z3.getSort("c0_" + Options.SERVICE)
            print(server)
            print(service)
            sap = SAP.SAP(self.solvers[0], server, service)
            jobs = sap.random_unique_service_random_server()
            #print(jobs)
            print(jobs)
            jobs = sap.random_unique_service_random_server_range()
            #print(jobs)
            #jobs = sap.turn_off_servers(self.module)
            print(jobs)
            return jobs
        else: 
            return [True for _ in range(Options.NUM_SPLIT)]
    
    
    
    
