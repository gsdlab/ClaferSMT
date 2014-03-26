'''
Created on Mar 15, 2014

@author: ezulkosk
'''
from common import Options
from common.Clock import Clock
from common.Common import preventSameModel
from gia.npGIAforZ3 import GuidedImprovementAlgorithmOptions, \
    GuidedImprovementAlgorithm
from visitors import PrintHierarchy, Visitor
import multiprocessing
import z3



          
def model_to_string(z3, model):
    ph = PrintHierarchy.PrintHierarchy(z3, model)
    Visitor.visit(ph, z3.module)
    ph.printTree()
    return ph.get_pickled()

class GIAConsumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, z3, totalTime, index, outputFileParentName, num_consumers, s, metrics_variables, metrics_objective_direction, consumerConstraints):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
#         self.CurrentNotDomConstraints_queuelist = CurrentNotDomConstraints_queuelist
        self.totalTime = totalTime 
        self.z3 = z3
        self.solver = s
        self.consumerConstraints = consumerConstraints
        self.index = index
        self.num_consumers = num_consumers
        self.ParetoFront = []
        self.clock = Clock()
        self.GIAOptions = GuidedImprovementAlgorithmOptions(verbosity=0, \
                        incrementallyWriteLog=False, \
                        writeTotalTimeFilename="timefile.csv", \
                        writeRandomSeedsFilename="randomseed.csv", useCallLogs=False)    
        
        self.GIAAlgorithm = GuidedImprovementAlgorithm(s, metrics_variables, \
                    metrics_objective_direction, [], options=self.GIAOptions)
        
    def addParetoPoints(self, point):
        self.ParetoFront.append(point)
            
    def run(self):
        num_solutions = 0
        self.clock.tick("Consumer " + str(self.index))
        while True:
            next_task = self.task_queue.get()
            try:
                if next_task == "Poison" or (num_solutions == Options.NUM_INSTANCES):
                    self.task_queue.task_done()
                    break
            except:
                pass    
            self.solver.push()
            self.solver.add(self.consumerConstraints[int(next_task)])
            self.clock.tick("Constraint " + str(next_task))
            while True:
                if self.GIAAlgorithm.s.check() != z3.sat or num_solutions == Options.NUM_INSTANCES:
                    self.task_queue.task_done()
                    
                    self.clock.tock("Constraint " + str(next_task))
                    self.solver.pop()
                    break
                else:  
                    prev_solution = self.GIAAlgorithm.s.model()
                    self.GIAAlgorithm.s.push()
                    NextParetoPoint, local_count_sat_calls, local_count_unsat_calls = self.GIAAlgorithm.ranToParetoFront(prev_solution)
                    self.addParetoPoints(NextParetoPoint)
                    metric_values = self.GIAAlgorithm.get_metric_values(NextParetoPoint)
                    self.result_queue.put((model_to_string(self.z3, NextParetoPoint), metric_values))

                    self.GIAAlgorithm.s.pop()
                    tmpNotDominatedByNextParetoPoint = self.GIAAlgorithm.ConstraintNotDominatedByX(NextParetoPoint)
                    self.GIAAlgorithm.s.add(tmpNotDominatedByNextParetoPoint)
                    
                    num_solutions = num_solutions +  1
        self.clock.tock("Consumer " + str(self.index))
        print(self.clock)
        return 0
    
class StandardConsumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, z3, totalTime, index, outputFileParentName, num_consumers, s, consumerConstraints):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
#         self.CurrentNotDomConstraints_queuelist = CurrentNotDomConstraints_queuelist
        self.totalTime = totalTime 
        self.z3 = z3
        self.solver = s
        self.consumerConstraints = consumerConstraints
        self.index = index
        self.num_consumers = num_consumers
        self.clock = Clock()
        
    def run(self):
        num_solutions = 0
        self.clock.tick("Consumer " + str(self.index))
        while True:
            next_task = self.task_queue.get()
            try:
                if next_task == "Poison" or (num_solutions == Options.NUM_INSTANCES):
                    self.task_queue.task_done()
                    break
            except:
                pass    
            self.solver.push()
            self.solver.add(self.consumerConstraints[int(next_task)])
            self.clock.tick("Constraint " + str(next_task))
            while self.solver.check() == z3.sat and num_solutions != Options.NUM_INSTANCES:
                model = self.solver.model()
                self.result_queue.put(model_to_string(self.z3, model))
                num_solutions = num_solutions +  1
                preventSameModel(self.solver, model)
            self.task_queue.task_done()                    
            self.clock.tock("Constraint " + str(next_task))
            self.solver.pop()
            break
        self.clock.tock("Consumer " + str(self.index))
        print(self.clock)
        return 0

