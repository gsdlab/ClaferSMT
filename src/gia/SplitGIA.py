'''
Created on Nov 21, 2013

@author: ezulkosk
'''



from common import Options
from gia import consts
from gia.consts import METRICS_MINIMIZE, METRICS_MAXIMIZE
from gia.npGIAforZ3 import GuidedImprovementAlgorithmOptions, \
    GuidedImprovementAlgorithm
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
import sys
import time




#from Z3ModelEmergencyResponseUpdateAllMin import *
#from Z3ModelWebPortal import *

RECORDPOINT = False

class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, z3, totalTime, index, outputFileParentName, num_consumers, s, metrics_variables, metrics_objective_direction, extraConstraint):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
#         self.CurrentNotDomConstraints_queuelist = CurrentNotDomConstraints_queuelist
        self.totalTime = totalTime 
        self.z3 = z3
        self.index = index
        self.outputFileParentName = outputFileParentName
        self.num_consumers = num_consumers
        self.ParetoFront = []
        self.GIAOptions = GuidedImprovementAlgorithmOptions(verbosity=0, \
                        incrementallyWriteLog=False, \
                        writeTotalTimeFilename="timefile.csv", \
                        writeRandomSeedsFilename="randomseed.csv", useCallLogs=False)    
        ''' add extra constraint'''
        #print extraConstraint
        s.add(extraConstraint)
        
        self.GIAAlgorithm = GuidedImprovementAlgorithm(s, metrics_variables, \
                    metrics_objective_direction, [], options=self.GIAOptions)
        
        self.count_sat_calls = 0
        self.count_unsat_calls = 0
        self.count_paretoPoints = 0
        self.startTime = time.time()
        
    def addParetoPoints(self, point):
        self.ParetoFront.append(point)
          
    def model_to_string(self, model):
        ph = PrintHierarchy.PrintHierarchy(self.z3, model)
        Visitor.visit(ph, self.z3.module)
        ph.printTree()
        return ph.get_pickled()
            
    def run(self):
        num_solutions = 0
        while True:
            if self.task_queue[self.index].empty() == True:
                break
            else:
                next_task = self.task_queue[self.index].get(False)
                if next_task is None or (num_solutions == self.options.num_models):
                    self.task_queue[self.index].task_done()
                    self.totalTime.put(str(time.time()-self.startTime))
                    self.result_queue.put("Done")
                    
                    
                    break
                
            
                if self.GIAAlgorithm.s.check() != sat:
                    self.count_unsat_calls += 1
                    self.task_queue[self.index].put(None)
                else:
                    self.count_sat_calls += 1
                    self.task_queue[self.index].put("Task")      
                    prev_solution = self.GIAAlgorithm.s.model()
                    self.GIAAlgorithm.s.push()
                    NextParetoPoint, local_count_sat_calls, local_count_unsat_calls = self.GIAAlgorithm.ranToParetoFront(prev_solution)
                    self.addParetoPoints(NextParetoPoint)
                    metric_values = self.GIAAlgorithm.get_metric_values(NextParetoPoint)
                    self.result_queue.put((self.model_to_string(NextParetoPoint), metric_values))
                    #print(self.ParetoFront)
                    
                    end_time = time.time()
                    self.count_sat_calls += local_count_sat_calls
                    self.count_unsat_calls += local_count_unsat_calls
                    self.count_paretoPoints += 1
                 
                    self.GIAAlgorithm.s.pop()
                    tmpNotDominatedByNextParetoPoint = self.GIAAlgorithm.ConstraintNotDominatedByX(NextParetoPoint)
                    self.GIAAlgorithm.s.add(tmpNotDominatedByNextParetoPoint)
                    
                    # picklize and store Pareto point and constraints
                    strNextParetoPoint = list((d.name(), str(NextParetoPoint[d])) for d in NextParetoPoint.decls())
                    self.task_queue[self.index].task_done()
                    num_solutions = num_solutions +  1
        return 0


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

class SplitGIA():
    def __init__(self, z3, solver, metrics_variables, metrics_objective_direction):
        self.consumerConstraints = self.splitter()
        self.solvers = replicateSolver(solver, Options.CORES)
        self.metrics_variables = metrics_variables
        self.metrics_objective_direction = metrics_objective_direction
        self.z3 = z3
    
    def run(self):
        outfile = "out"
        mgr = multiprocessing.Manager()
        taskQueue = []
        for i in range(Options.CORES):
            taskQueue.append(mgr.Queue())
        ParetoFront = mgr.Queue()
        totalTime = mgr.Queue()
        
        # Enqueue initial tasks
        for i in range(Options.CORES):
            taskQueue[i].put("Task")
        
        # Start consumers
        self.consumers = [ Consumer(taskQueue, ParetoFront, self.z3, totalTime, i, "out", Options.CORES, j, self.metrics_variables, self.metrics_objective_direction, k)
                        for i,j,k in zip(range(Options.CORES), self.solvers,  self.consumerConstraints)]
        
        for w in self.consumers:
            w.start()            
        for w in self.consumers:
            w.join()  
        
        runningtime = 0.0
        
        while totalTime.qsize() > 0:
            time = totalTime.get()
            if (float(time) > runningtime): 
                runningtime = float(time)
        
        num_jobs = Options.CORES
        
        results = []
        while num_jobs != 0:
            result = ParetoFront.get()
            try:
                if result == "Done":
                    num_jobs = num_jobs - 1
                    continue
            except:
                pass
            results.append(result)
            #print ("\n INSTANCE: \n\n" + str(result))
        #print(results)
        return self.merge(results)
        
        
    def merge(self, results):
        
        results = self.removeDominatedAndEqual(results)
        return [i for (i,_) in results]
        
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
            return [True for _ in range(Options.CORES)]
        else: 
            return [True for _ in Options.CORES]
    
    
    
    
