
from common import Common, SMTLib
from common.Common import preventSameModel
from time import time
from solvers import BaseSolver



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
    def __init__(self, cfr_inst, s,  metrics_variables, metrics_objective_direction, decision_variables=[], options=GuidedImprovementAlgorithmOptions()):
        self.cfr = cfr_inst
        self.s = s
        self.metrics_variables = metrics_variables
        self.metrics_objective_direction = metrics_objective_direction
        self.decision_variables = decision_variables
        self.options = options
        self.verbosity = self.options.verbosity


    '''
    CAUTION: REMOVED FUNCTIONALITY FOR OUTPUT E.G RECORDPOINT STUFF BELOW
    '''
    def genEquivalentSolutions(self, point, count):
        self.s.push()
        equivalentSolutions = []
        equalConstraint = self.ConstraintEqualToX(point)
        self.s.add(equalConstraint)
        preventSameModel(self.cfr, self.s, point)
        while(self.s.check() == Common.SAT and not(len(equivalentSolutions) + count == self.options.num_models)):                          
            solution = self.s.model()
            preventSameModel(self.cfr, self.s, solution)
            equivalentSolutions.append(solution)
            
        self.s.pop()
        return equivalentSolutions    

    def addParetoPoints(self, ParetoFront, point):
        ParetoFront.append(point)
        return ParetoFront


    def replicateSolver(self, solver, num_consumers):
        solvers = []
        for _ in range(num_consumers):
            newSolver = BaseSolver.getSolver()
            for j in solver.assertions():
                newSolver.add(j)
            solvers.append(newSolver)
        return solvers   

    def ExecuteGuidedImprovementAlgorithm(self, outfilename):
        """ 
        Ran the Guided Improvement Algorithm.
        """
        count_paretoPoints = 0
        ParetoFront = []
        initial_start_time = time()
        start_time = time()
        count_sat_calls = 0
        count_unsat_calls = 0
        if self.options.magnifying_glass:
            self.s.push()
        if self.s.check() == Common.SAT:
            count_sat_calls += 1
            prev_solution = self.s.model()          
            self.s.push()
            FirstParetoPoint, local_count_sat_calls, local_count_unsat_calls = self.ranToParetoFront(prev_solution)
            end_time = time()
            count_sat_calls += local_count_sat_calls
            count_unsat_calls += local_count_unsat_calls
            count_paretoPoints += 1
            
            ParetoFront = self.addParetoPoints(ParetoFront, FirstParetoPoint)
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

            self.s.pop()

            tmpNotDominatedByFirstParetoPoint = self.ConstraintNotDominatedByX(FirstParetoPoint)
            self.s.add(tmpNotDominatedByFirstParetoPoint)
            start_time = time()
            
            while(self.s.check() == Common.SAT and not(len(ParetoFront) == self.options.num_models)):
                count_sat_calls += 1                             
                prev_solution = self.s.model()
                self.s.push()
                NextParetoPoint, local_count_sat_calls, local_count_unsat_calls = self.ranToParetoFront(prev_solution)
                end_time = time()
                count_sat_calls += local_count_sat_calls
                count_unsat_calls += local_count_unsat_calls
                count_paretoPoints += 1
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
                self.s.pop()
                tmpNotDominatedByNextParetoPoint = self.ConstraintNotDominatedByX(NextParetoPoint)
                self.s.add(tmpNotDominatedByNextParetoPoint)
                start_time = time()              
        count_unsat_calls += 1

        end_time = time()
        
        if self.options.magnifying_glass:
            self.s.pop()
            for i in ParetoFront:
                equivalentSolutions = self.genEquivalentSolutions(i, len(ParetoFront))
                ParetoFront = ParetoFront + equivalentSolutions
        
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
        while (self.s.check() == Common.SAT):
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
                DisjunctionOrLessMetrics.append(SMTLib.SMT_GT(self.metrics_variables[i], SMTLib.SMT_IntConst(Common.evalForNum(model, self.metrics_variables[i].convert(self.cfr.solver.converter)))))#model[self.metrics_variables[i]])
            else :
                DisjunctionOrLessMetrics.append(SMTLib.SMT_LT(self.metrics_variables[i], SMTLib.SMT_IntConst(Common.evalForNum(model, self.metrics_variables[i].convert(self.cfr.solver.converter)))))#model[self.metrics_variables[i]])
        return SMTLib.SMT_Or(*DisjunctionOrLessMetrics)


    def ConstraintEqualToX(self, model):
        """
        Returns a Constraint that a  new instance, can't be dominated by the instance represented by model. 
        (it can't be worst in any objective).
        """
        EqualMetrics  = list()
        for i in range(len(self.metrics_variables)):
            EqualMetrics.append(SMTLib.SMT_EQ(self.metrics_variables[i], Common.evalForNum(model, self.metrics_variables[i])))
        return SMTLib.SMT_And(EqualMetrics)

    def get_metric_values(self, model):
        metrics  = list()
        for i in range(len(self.metrics_variables)):
            strval = str(model.eval(self.metrics_variables[i].convert(self.cfr.solver.converter)))
            try:
                val = int(strval)
            except:
                val = float(strval)
            metrics.append(val)
        return metrics
    
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
                dominationConjunction.append(SMTLib.SMT_GT(dominatedByMetric,
                                                           SMTLib.SMT_IntConst(Common.evalForNum(model, dominatedByMetric.convert(self.cfr.solver.converter))))) 
            else:
                dominationConjunction.append(SMTLib.SMT_LT(dominatedByMetric, 
                                                           SMTLib.SMT_IntConst(Common.evalForNum(model, dominatedByMetric.convert(self.cfr.solver.converter)))))
            for AtLeastEqualInOtherMetric in self.metrics_variables:
                if j != i:
                    if self.metrics_objective_direction[j] == Common.METRICS_MAXIMIZE:
                        dominationConjunction.append(SMTLib.SMT_GE(AtLeastEqualInOtherMetric,
                                                                   SMTLib.SMT_IntConst(Common.evalForNum(model, AtLeastEqualInOtherMetric.convert(self.cfr.solver.converter)))))
                    else:
                        dominationConjunction.append(SMTLib.SMT_LE(AtLeastEqualInOtherMetric,
                                                                   SMTLib.SMT_IntConst(Common.evalForNum(model, AtLeastEqualInOtherMetric.convert(self.cfr.solver.converter)))))              
                j = 1 + j
            i = 1 + i    
            dominationDisjunction.append(SMTLib.SMT_And(*dominationConjunction))         
        constraintDominateX = SMTLib.SMT_Or(*dominationDisjunction)
        return constraintDominateX
