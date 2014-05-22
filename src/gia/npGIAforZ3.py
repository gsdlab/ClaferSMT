
from common import Common
from common.Common import preventSameModel
from time import time
from z3 import *
import random



#Modified by Jianmei for EPOAL
# count #ParetoPoints
# count #satcalls and #unsatcalls
# print every found Pareto point (especially for Eshop)

OUTPUT_PARETO_FRONT = False
RECORDPOINT = False

def setRecordPoint(b):
    global RECORDPOINT
    RECORDPOINT = b


class GuidedImprovementAlgorithmOptions(object):
    def __init__(self, verbosity=False, useSummaryStatsFile=False, \
                  SummaryStatsFilename="", incrementallyWriteLog=False, \
                  writeLogFilename="", writeTotalTimeFilename="timefile.csv", \
         writeRandomSeedsFilename="randomseed.csv",  \
         exclude_variables_in_printout=[],\
         incrementallyprintparetopoints=False,
         useCallLogs=False, num_models=-1, magnifying_glass=False):
        self.verbosity = verbosity
        self.useSummaryStatsFile = useSummaryStatsFile
        self.SummaryStatsFilename = SummaryStatsFilename
        self.exclude_variables_in_printout = exclude_variables_in_printout        
        self.incrementallyWriteLog = incrementallyWriteLog
        self.writeLogFilename = writeLogFilename
        self.writeTotalTimeFilename = writeTotalTimeFilename
        self.useCallLogs = useCallLogs
        if self.writeLogFilename != "":
            self.logfile = open(self.writeLogFilename, "w")
        self.incrementallyprintparetopoints = incrementallyprintparetopoints
        self.writeRandomSeedsFilename = writeRandomSeedsFilename
        self.magnifying_glass = magnifying_glass
        self.num_models = num_models
        
        
                    
     
class GuidedImprovementAlgorithm(object):
    def __init__(self, z3inst, s,  metrics_variables, metrics_objective_direction, decision_variables=[], options=GuidedImprovementAlgorithmOptions()):
        self.z3 = z3inst
        self.s = s
        self.metrics_variables = metrics_variables
        self.metrics_objective_direction = metrics_objective_direction
        self.decision_variables = decision_variables
        self.options = options
        self.verbosity = self.options.verbosity

    def _setAndLogZ3RandomSeeds(self):
        """ 
        Will set random seeds for z3 and store them on the file
        """
        random.seed()
        z3_random_seed_val = random.randint(0, 500000000)
        z3_arith_random_seed_val = random.randint(0, 500000000)        
        #set_option(random_seed=z3_random_seed_val)
        #set_option(arith_random_seed=z3_arith_random_seed_val)
        
        self.options.randomSeedsFil =  open(self.options.writeRandomSeedsFilename, "a")            
        self.options.randomSeedsFil.write("%s, %s, %s\n" % \
          ( self.options.writeLogFilename ,"random_seed", z3_random_seed_val ))
        self.options.randomSeedsFil.write("%s, %s, %s\n" % \
          ( self.options.writeLogFilename ,"arith_random_seed", z3_arith_random_seed_val ))
        
        self.options.randomSeedsFil.close()
          
    '''
    CAUTION: REMOVED FUNCTIONALITY FOR OUTPUT E.G RECORDPOINT STUFF BELOW
    '''
    def genEquivalentSolutions(self, point, count):
        self.s.push()
        equivalentSolutions = []
        equalConstraint = self.ConstraintEqualToX(point)
        self.s.add(equalConstraint)
        #print(count)
        preventSameModel(self.z3, self.s, point)
        #print(self.s.check()==sat)
        while(self.s.check() == sat and not(len(equivalentSolutions) + count == self.options.num_models)):
            #print("in")
            #count_sat_calls += 1
#                 self.GIALogger.logEndCall(True, model = self.s.model(), statistics = self.s.statistics())                              
            solution = self.s.model()
            preventSameModel(self.z3, self.s, solution)
            equivalentSolutions.append(solution)
            
        self.s.pop()
        return equivalentSolutions
#           
          

    def addParetoPoints(self, ParetoFront, point):
        ParetoFront.append(point)
        return ParetoFront


    def replicateSolver(self, solver, num_consumers):
        solvers = []
        for i in range(num_consumers):
            newSolver =Solver()
            for j in solver.assertions():
                newSolver.add(j)
            solvers.append(newSolver)
        return solvers   

    def ExecuteGuidedImprovementAlgorithm(self, outfilename):
        """ 
        Ran the Guided Improvement Algorithm.
        """
        self._setAndLogZ3RandomSeeds()
        count_paretoPoints = 0
        ParetoFront = []
        initial_start_time = time()
        start_time = time()
        count_sat_calls = 0
        count_unsat_calls = 0
        if self.options.magnifying_glass:
            self.s.push()
        #self.GIALogger.logStartCall()
        if self.s.check() == sat:
            count_sat_calls += 1
            prev_solution = self.s.model()
            #self.GIALogger.logEndCall(True, model=prev_solution, statistics = self.s.statistics())            
            self.s.push()
            FirstParetoPoint, local_count_sat_calls, local_count_unsat_calls = self.ranToParetoFront(prev_solution)
            end_time = time()
            count_sat_calls += local_count_sat_calls
            count_unsat_calls += local_count_unsat_calls
            count_paretoPoints += 1
            
            ParetoFront = self.addParetoPoints(ParetoFront, FirstParetoPoint)
            #ParetoFront.append(FirstParetoPoint)
            # RecordPoint
            strNextParetoPoint = list((d.name(), str(FirstParetoPoint[d])) for d in FirstParetoPoint.decls())
            if RECORDPOINT:
                outputFile = open(outfilename, 'a')
                try:
                    outputFile.writelines(str(count_paretoPoints) + ',' +
                                          str(count_sat_calls) + ',' +
                                          str(end_time - start_time) + ',' +
                                          str(strNextParetoPoint) + ',' +
                                          '\n')
                finally:
                    outputFile.close()
                ##    
                    
            self.s.pop()

            tmpNotDominatedByFirstParetoPoint = self.ConstraintNotDominatedByX(FirstParetoPoint)
#             self.GIALogger.logStartCall(tmpNotDominatedByFirstParetoPoint)
            self.s.add(tmpNotDominatedByFirstParetoPoint)
            start_time = time()
            while(self.s.check() == sat and not(len(ParetoFront) == self.options.num_models)):
                count_sat_calls += 1
#                 self.GIALogger.logEndCall(True, model = self.s.model(), statistics = self.s.statistics())                              
                prev_solution = self.s.model()
                self.s.push()
                NextParetoPoint, local_count_sat_calls, local_count_unsat_calls = self.ranToParetoFront(prev_solution)
                end_time = time()
                count_sat_calls += local_count_sat_calls
                count_unsat_calls += local_count_unsat_calls
                count_paretoPoints += 1
                #ParetoFront.append(NextParetoPoint)
                ParetoFront = self.addParetoPoints(ParetoFront, NextParetoPoint)
                
                # RecordPoint
                strNextParetoPoint = list((d.name(), str(FirstParetoPoint[d])) for d in FirstParetoPoint.decls())
                if RECORDPOINT:
                    outputFile = open(outfilename, 'a')
                    try:
                        outputFile.writelines(str(count_paretoPoints) + ',' +
                                              str(count_sat_calls) + ',' +
                                              str(end_time - start_time) + ',' +
                                              str(strNextParetoPoint) + ',' +
                                              '\n')
                    finally:
                        outputFile.close()
                ##    
                self.s.pop()
#                 ParetoFront.append(NextParetoPoint)
#                 if self.options.incrementallyprintparetopoints == True:
#                     self.print_solution(NextParetoPoint)
                tmpNotDominatedByNextParetoPoint = self.ConstraintNotDominatedByX(NextParetoPoint)
#                 self.GIALogger.logStartCall(tmpNotDominatedByNextParetoPoint)
                self.s.add(tmpNotDominatedByNextParetoPoint)
                start_time = time()
#             self.GIALogger.logEndCall(False, statistics = self.s.statistics())                
#         else :
        count_unsat_calls += 1
            #self.GIALogger.logEndCall(False, statistics = self.s.statistics())            
            
        end_time = time()
        
        if self.options.magnifying_glass:
            self.s.pop()
            for i in ParetoFront:
                equivalentSolutions = self.genEquivalentSolutions(i, len(ParetoFront))
                ParetoFront = ParetoFront + equivalentSolutions
        
        
#         print count_paretoPoints, count_sat_calls, count_sat_calls, end_time - start_time
        outputFile = open(outfilename, 'a')
        try:
            outputFile.writelines(str(count_paretoPoints) + ',' +
                                  str(count_sat_calls) + ',' +
                                  str(count_unsat_calls) + ',' +
                                  str(end_time - initial_start_time) + ',' +
                                  '\n')
        finally:
            outputFile.close()
        return ParetoFront
              
    def print_stats_info(self, end_time, start_time, ParetoFront):
        statsfile_fd = open(self.args.statsfile, "a")   
        self.print_header_if_file_is_empty(statsfile_fd)   
        statsfile_fd.write( "%s, %s,%s\n" % (self.optimizationmodelname , (end_time - start_time), len(ParetoFront)))
        statsfile_fd.close()
        
    def print_header_if_file_is_empty(self, statsfile_fd):
        if statsfile_fd.tell() == 0:
            statsfile_fd.write("%s, %s, %s\n" % ('model name' , 'time to compute pareto front', 'length of pareto front'))
                
    def print_solution(self, solution):
        """
        Prints the objective value for the solution in one line, followed by the decision variables in the next line.
        """        
        SolutionSpacePoint = []
        for metric in self.metrics_variables:
            SolutionSpacePoint.append(solution[metric])
        print(SolutionSpacePoint)
                
        DecisionSpacePoint = []
        for instVariable in solution.decls()  :
            if instVariable.name() not in self.exclude_variables_in_printout:
                DecisionSpacePoint.append("%s=%s" % (instVariable.name(),  solution[instVariable]))
        print(DecisionSpacePoint)
    
    
    def ranToParetoFront(self, prev_solution):
        """
        Iterates until a pareto optimal solution is found.
        """
        local_count_sat_calls = 0
        local_count_unsat_calls = 0
        tmpConstraintMustDominateX= self.ConstraintMustDominatesX(prev_solution)
        self.s.add(tmpConstraintMustDominateX)
        while (self.s.check() == sat):
            local_count_sat_calls += 1
            prev_solution = self.s.model()     
            tmpConstraintMustDominateX = self.ConstraintMustDominatesX(prev_solution)
            self.s.add(tmpConstraintMustDominateX)
        local_count_unsat_calls += 1
        return prev_solution, local_count_sat_calls, local_count_unsat_calls

    def ConstraintNotDominatedByX(self, model):
        """
        Creates a constraint preventing search in dominated regions.
        """
        DisjunctionOrLessMetrics  = list()
        for i in range(len(self.metrics_variables)):
            if self.metrics_objective_direction[i] == Common.METRICS_MAXIMIZE:
                DisjunctionOrLessMetrics.append(self.metrics_variables[i].convert(self.z3.solver_converter) >  model.eval(self.metrics_variables[i].convert(self.z3.solver_converter)))#model[self.metrics_variables[i]])
            else :
                DisjunctionOrLessMetrics.append(self.metrics_variables[i].convert(self.z3.solver_converter) <  model.eval(self.metrics_variables[i].convert(self.z3.solver_converter)))#model[self.metrics_variables[i]])
        return Or(DisjunctionOrLessMetrics)


    def ConstraintEqualToX(self, model):
        """
        Returns a Constraint that a  new instance, can't be dominated by the instance represented by model. 
        (it can't be worst in any objective).
        """
        EqualMetrics  = list()
        for i in range(len(self.metrics_variables)):
            EqualMetrics.append(self.metrics_variables[i] ==  model.eval(self.metrics_variables[i]))
        return And(EqualMetrics)

    def get_metric_values(self, model):
        metrics  = list()
        for i in range(len(self.metrics_variables)):
            strval = str(model.eval(self.metrics_variables[i]))
            try:
                val = int(strval)
            except:
                val = float(strval)
            metrics.append(val)
        return metrics
    # add for EPOAL

    def EtractConstraintListNotDominatedByX(self, model):
        """
        Returns a Constraint that a  new instance, can't be dominated by the instance represented by model. 
        (it can't be worst in any objective).
        """
        DisjunctionOrLessMetrics  = list()
        for i in range(len(self.metrics_variables)):
            if self.metrics_objective_direction[i] == Common.METRICS_MAXIMIZE:
                DisjunctionOrLessMetrics.append(self.metrics_variables[i] >  model[self.metrics_variables[i]])
            else :
                DisjunctionOrLessMetrics.append(self.metrics_variables[i] <  model[self.metrics_variables[i]])
        return DisjunctionOrLessMetrics
    
    def ConstraintMustDominatesX(self, model):
        """
        Returns a constraint that a new instance has to be better than the instance represented by model in at least one dimension, 
        and better or equal in all the other ones.
        """
        dominationDisjunction= []
        i = 0
        for dominatedByMetric in self.metrics_variables:        
            dominationConjunction = []
            j = 0
            if  self.metrics_objective_direction[i] == Common.METRICS_MAXIMIZE:
                #print(model.eval(dominatedByMetric))
                dominationConjunction.append(dominatedByMetric.convert(self.z3.solver_converter) > model.eval(dominatedByMetric.convert(self.z3.solver_converter)))             
            else:
                dominationConjunction.append(dominatedByMetric.convert(self.z3.solver_converter) < model.eval(dominatedByMetric.convert(self.z3.solver_converter))) 
            for AtLeastEqualInOtherMetric in self.metrics_variables:
                if j != i:
                    if self.metrics_objective_direction[j] == Common.METRICS_MAXIMIZE:
                        dominationConjunction.append(AtLeastEqualInOtherMetric.convert(self.z3.solver_converter) >= model.eval(AtLeastEqualInOtherMetric.convert(self.z3.solver_converter)))#[AtLeastEqualInOtherMetric])
                    else:
                        dominationConjunction.append(AtLeastEqualInOtherMetric.convert(self.z3.solver_converter) <= model.eval(AtLeastEqualInOtherMetric.convert(self.z3.solver_converter)))               
                j = 1 + j
            i = 1 + i    
            dominationDisjunction.append(And(dominationConjunction))         
        constraintDominateX = Or(dominationDisjunction)
        #print(constraintDominateX)
        #sys.exit()
        return constraintDominateX
