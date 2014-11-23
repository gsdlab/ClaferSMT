'''
Created on Nov 21, 2013

@author: ezulkosk
'''



from common import Options, Common
from common.Clock import Clock
from common.Common import METRICS_MAXIMIZE, METRICS_MINIMIZE
from parallel import Consumer
from parallel.heuristics import GeneralHeuristics
from solvers import BaseSolver
import multiprocessing

def replicateSolver(solver, num_consumers):
    solvers = []
    for _ in range(num_consumers):
        newSolver = BaseSolver.getSolver()
        for j in solver.assertions():
            newSolver.addRaw(j)
        solvers.append(newSolver)
    return solvers    


def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

def getZ3Feature(feature, expr):
    if(str(expr) == feature):
        return expr
    for child in expr.children():
        result = getZ3Feature(feature, child)
        if result:
            return result
    return []

class ParSolver():
    def __init__(self, cfr, module, solver, metrics_variables, metrics_objective_direction):
        self.cfr = cfr
        self.module = module
        self.solvers = replicateSolver(solver, Options.CORES)
        self.metrics_variables = metrics_variables
        self.metrics_objective_direction = metrics_objective_direction
        self.clock = Clock()
        self.consumerConstraints = self.splitter()
    
    def run(self):
        if not self.consumerConstraints:
            self.cfr.metric = Common.BOUND
            return []
            
        mgr = multiprocessing.Manager()
        taskQueue = mgr.Queue()
        solutions = mgr.Queue()
        timeQueue = mgr.Queue()
        
        # Enqueue initial tasks
        for i in range(Options.NUM_SPLIT):
            taskQueue.put(i)
        for i in range(Options.CORES):
            taskQueue.put("Poison")
        
        # Start consumers 
        #case: objectives
        if self.metrics_variables:
            self.consumers = [ Consumer.GIAConsumer(taskQueue, solutions, self.cfr, timeQueue, i, "out", Options.CORES, j, self.metrics_variables, self.metrics_objective_direction, self.consumerConstraints)
                            for i,j in zip(range(Options.CORES), self.solvers)]
        #case: no objectives
        else:
            self.consumers = [ Consumer.StandardConsumer(taskQueue, solutions, self.cfr, timeQueue, i, "out", Options.CORES, j, self.consumerConstraints)
                            for i,j in zip(range(Options.CORES), self.solvers)]
        
        
        self.clock.tick("ParSolver")
        for w in self.consumers:
            w.start()          
        TERMINATED = False
        for w in self.consumers:
            if Options.TIME_OUT != 0:
                w.join(Options.TIME_OUT) 
            else:
                w.join()
            if w.is_alive():
                TERMINATED = True
                w.terminate() 
        if TERMINATED:
            GeneralHeuristics.safe_raise_heuristic_failure_exception("Heuristic Timed Out")
        results = []
        
        while not solutions.empty():
            result = solutions.get()
            results.append(result)
        while not timeQueue.empty():
            clock = timeQueue.get()
            self.clock = self.clock.combineClocks(clock)
        
        self.clock.tick("Merge")
        merged_results = self.merge(results)
        self.clock.tock("Merge")
        self.clock.tock("ParSolver")
        self.clock.getParallelStats(self.cfr)
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
            if self.metrics_objective_direction[i] == METRICS_MAXIMIZE:
                if  ml < mr:
                    worseInOne = True
                elif ml > mr:
                    betterInOne = True
            elif self.metrics_objective_direction[i] == METRICS_MINIMIZE:
                if  ml > mr:
                    worseInOne = True
                elif ml < mr:
                    betterInOne = True
        if (worseInOne and not betterInOne): 
            return True
        return False
    
    def removeDominatedAndEqual(self, results):
        count = len(results)
        removalList = [False for _ in range(count)]
        for i in range(count):
            for j in range(count):
                if i != j:
                    if self.checkDominated(results[i][1], results[j][1]):
                        removalList[i] = True
                    elif i < j and (results[i][0] == results[j][0] or results[i][1] == results[j][1]):
                        removalList[i] = True
                    
        nonDominated = []
        for i in range(len(removalList)):
            if not removalList[i]:
                nonDominated.append(results[i])
        return nonDominated
    
    
    def splitter(self): 
        heuristic = GeneralHeuristics.heuristics[Options.SPLIT]
        return heuristic(self.cfr, self.module, Options.NUM_SPLIT)
    
    
    
    
