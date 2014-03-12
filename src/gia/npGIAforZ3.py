
from common.Common import preventSameModel
from gia import consts
from gia.GIALogs import GIALogging
from time import time
from z3 import *
import inspect
import multiprocessing
import random
import string
import sys


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
    def __init__(self, s,  metrics_variables, metrics_objective_direction, decision_variables=[], options=GuidedImprovementAlgorithmOptions()):
        self.s = s
        self.metrics_variables = metrics_variables
        self.metrics_objective_direction = metrics_objective_direction
        self.decision_variables = decision_variables
        self.options = options
        self.verbosity = self.options.verbosity
        self.GIALogger = GIALogging(self.options, self.metrics_variables, self.decision_variables)

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
    def genEquivalentSolutions(self, ParetoFront, point):
        self.s.push()
        equalConstraint = self.ConstraintEqualToX(point)
        self.s.add(equalConstraint)
        #print(self.s.check()==sat)
        while(self.s.check() == sat and not(len(ParetoFront) == self.options.num_models)):
            #print("in")
            #count_sat_calls += 1
#                 self.GIALogger.logEndCall(True, model = self.s.model(), statistics = self.s.statistics())                              
            solution = self.s.model()
            preventSameModel(self.s, solution)
            ParetoFront.append(solution)
            
        self.s.pop()
        return ParetoFront
#           
          

    def addParetoPoints(self, ParetoFront, point):
        if self.options.magnifying_glass:
            self.s.pop()
            self.genEquivalentSolutions(ParetoFront, point)
            self.s.push()
        else:
            ParetoFront.append(point)
        return ParetoFront

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
        if OUTPUT_PARETO_FRONT:
            #         print count_paretoPoints, count_sat_calls, count_sat_calls, end_time - start_time
            outputFile2 = open("ERS_ParetoFront.csv", 'a')
            ParetoPointsList2 = []
            try:
                for paretopoint in ParetoFront:
                    strParetoPoint = list((d.name(), str(paretopoint[d])) for d in paretopoint.decls())
                    dict = {}
                    for item in strParetoPoint:
                        if( item[0] == 'total_batteryusage' or item[0] == 'total_cost' or item[0] == 'total_deploymenttime' or
                            item[0] == 'total_developmenttime' or item[0] == 'total_rampuptime' or item[0] == 'total_reliability' or
                            item[0] == 'total_responsetime' ):
                            # print item
                            outputFile2.writelines(str(item) + ';')
                            dict[str(item[0])] = str(item[1])
                    ParetoPointsList2.append(dict)
                    outputFile2.writelines('\n')
            finally:
                outputFile2.close()
            
            totalpoints = count_paretoPoints
            for i in range(len(ParetoPointsList2)):
                isDominated = False
                for j in range(i+1, len(ParetoPointsList2)):
                        strlist1 = ParetoPointsList2[i]['total_reliability'].split("/")
                        #print strlist1
                        strlist2 = ParetoPointsList2[j]['total_reliability'].split("/")
                        #print strlist2
                        if (int(ParetoPointsList2[i]['total_cost']) >= int(ParetoPointsList2[j]['total_cost']) and 
                            int(ParetoPointsList2[i]['total_responsetime']) >= int(ParetoPointsList2[j]['total_responsetime']) and
                            int(ParetoPointsList2[i]['total_batteryusage']) >= int(ParetoPointsList2[j]['total_batteryusage']) and 
                            int(ParetoPointsList2[i]['total_deploymenttime']) >= int(ParetoPointsList2[j]['total_deploymenttime']) and 
                            int(ParetoPointsList2[i]['total_developmenttime']) >= int(ParetoPointsList2[j]['total_developmenttime']) and
                            int(ParetoPointsList2[i]['total_rampuptime']) >= int(ParetoPointsList2[j]['total_rampuptime']) and
                            # precision of reliability is 1/1000 
                            round(float(strlist1[0])/float(strlist1[1]),12) >= round(float(strlist2[0])/float(strlist2[1]), 12)):
                            isDominated = True
        #                     print str(i) + " dominated by " + str(j)
        #                     print str(int(ParetoPointsList2[i]['total_cost'])) + " cost >=" + str(int(ParetoPointsList2[j]['total_cost']))
        #                     print str(int(ParetoPointsList2[i]['total_responsetime'])) + "response >=" + str(int(ParetoPointsList2[j]['total_responsetime']))
        #                     print str(int(ParetoPointsList2[i]['total_batteryusage'])) + "battery >=" + str(int(ParetoPointsList2[j]['total_batteryusage']))
        #                     print str(int(ParetoPointsList2[i]['total_deploymenttime'])) + "deploy >=" + str(int(ParetoPointsList2[j]['total_deploymenttime']))
        #                     print str(int(ParetoPointsList2[i]['total_developmenttime'])) + "develp >=" + str(int(ParetoPointsList2[j]['total_developmenttime']))
        #                     print str(int(ParetoPointsList2[i]['total_rampuptime'])) + "rampup >=" + str(int(ParetoPointsList2[j]['total_rampuptime']))
        #                     print str(strlist1[0]) + "/" + str(strlist1[1])  + "reliability >=" + str(strlist2[0]) + "/" + str(strlist2[1])
        #                     print str(round(float(strlist1[0])/float(strlist1[1]),3)) +"reliability >=" + str(round(float(strlist2[0])/float(strlist2[1]), 3))
                            break;
                if isDominated == True: 
                    totalpoints -= 1   
            print(totalpoints)
        
        
        
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
        
#         TotalUniqueParetoFront = len(ParetoFront)
#         print TotalUniqueParetoFront
#         ParetoPointsList = []
#         for i in xrange(len(ParetoFront)):
#             point = ParetoFront[i]
#             strPoint = list((d.name(), str(point[d])) for d in point.decls())
#             dict = {}
#             for item in strPoint:
#                 dict[str(item[0])] = str(item[1])
#             ParetoPointsList.append(dict)
#             
#         for i in xrange(len(ParetoPointsList)):
#             isDominated = False
#             for j in xrange(i+1, len(ParetoPointsList)):
#                     strlist1 = ParetoPointsList[i]['total_reliability'].split("/")
#                     #print strlist1
#                     strlist2 = ParetoPointsList[j]['total_reliability'].split("/")
#                     #print strlist2
#                     if (int(ParetoPointsList[i]['total_cost']) < int(ParetoPointsList[j]['total_cost']) and 
#                         int(ParetoPointsList[i]['total_responsetime']) < int(ParetoPointsList[j]['total_responsetime']) and
#                         int(ParetoPointsList[i]['total_batteryusage']) < int(ParetoPointsList[j]['total_batteryusage']) and 
#                         int(ParetoPointsList[i]['total_deploymenttime']) < int(ParetoPointsList[j]['total_deploymenttime']) and 
#                         int(ParetoPointsList[i]['total_developmenttime']) < int(ParetoPointsList[j]['total_developmenttime']) and
#                         int(ParetoPointsList[i]['total_rampuptime']) < int(ParetoPointsList[j]['total_rampuptime']) and 
#                         float(int(strlist1[0])/int(strlist1[1])) < float(int(strlist2[0])/int(strlist2[1]))):
#                         isDominated = True
#             if isDominated == True: 
#                 TotalUniqueParetoFront = TotalUniqueParetoFront - 1
#         print TotalUniqueParetoFront

             
#         if self.verbosity > consts.VERBOSE_NONE:
#             print "ParetoFront has size of %s " % len(ParetoFront)
#             print "Time taken is %s " % (end_time - start_time)
#         
#             for ParetoPoint in ParetoFront:
#                 self.print_solution(ParetoPoint)
#        
#         if  self.options.useSummaryStatsFile == True:        
#             self.print_stats_info(end_time, start_time, ParetoFront)
# 
#         self.options.timefilelog =  open(self.options.writeTotalTimeFilename, "a")            
#         self.options.timefilelog.write("%s, %s\n" %  ( self.options.writeLogFilename , (end_time - start_time)))
#         self.options.timefilelog.close()
        
        #for entry in self.GIALogger.getLog():
        #    print entry.statistics

        
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
        It iterates getting close and closer to the pareto front.
        """
#         if self.verbosity > consts.VERBOSE_NONE:
#             self.print_solution(prev_solution)

        local_count_sat_calls = 0
        local_count_unsat_calls = 0
        tmpConstraintMustDominateX= self.ConstraintMustDominatesX(prev_solution)
#         self.GIALogger.logStartCall(tmpConstraintMustDominateX)
        self.s.add(tmpConstraintMustDominateX)
        while (self.s.check() == sat):
            local_count_sat_calls += 1
#             self.GIALogger.logEndCall(True, model = self.s.model(), statistics = self.s.statistics())              
#             if self.verbosity > consts.VERBOSE_NONE:
#                 self.print_solution(prev_solution)
            prev_solution = self.s.model()     
            tmpConstraintMustDominateX = self.ConstraintMustDominatesX(prev_solution)
            self.s.add(tmpConstraintMustDominateX)
            self.GIALogger.logStartCall(tmpConstraintMustDominateX)
        local_count_unsat_calls += 1
#         self.GIALogger.logEndCall(False, statistics = self.s.statistics())  
#         if self.verbosity > consts.VERBOSE_NONE:
#             self.print_solution(prev_solution)
        return prev_solution, local_count_sat_calls, local_count_unsat_calls

    def ConstraintNotDominatedByX(self, model):
        """
        Returns a Constraint that a  new instance, can't be dominated by the instance represented by model. 
        (it can't be worst in any objective).
        """
        DisjunctionOrLessMetrics  = list()
        for i in range(len(self.metrics_variables)):
            if self.metrics_objective_direction[i] == consts.METRICS_MAXIMIZE:
                DisjunctionOrLessMetrics.append(self.metrics_variables[i] >  model.eval(self.metrics_variables[i]))#model[self.metrics_variables[i]])
            else :
                DisjunctionOrLessMetrics.append(self.metrics_variables[i] <  model.eval(self.metrics_variables[i]))#model[self.metrics_variables[i]])
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


    # add for EPOAL

    def EtractConstraintListNotDominatedByX(self, model):
        """
        Returns a Constraint that a  new instance, can't be dominated by the instance represented by model. 
        (it can't be worst in any objective).
        """
        DisjunctionOrLessMetrics  = list()
        for i in range(len(self.metrics_variables)):
            if self.metrics_objective_direction[i] == consts.METRICS_MAXIMIZE:
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
            if  self.metrics_objective_direction[i] == consts.METRICS_MAXIMIZE :
                #print(model.eval(dominatedByMetric))
                dominationConjunction.append(dominatedByMetric > model.eval(dominatedByMetric))#[dominatedByMetric])             
            else:
                dominationConjunction.append(dominatedByMetric < model.eval(dominatedByMetric))#model[dominatedByMetric]) 
            for AtLeastEqualInOtherMetric in self.metrics_variables:
                if j != i:
                    if self.metrics_objective_direction[j] == consts.METRICS_MAXIMIZE:
                        dominationConjunction.append(AtLeastEqualInOtherMetric >= model.eval(AtLeastEqualInOtherMetric))#[AtLeastEqualInOtherMetric])
                    else:
                        dominationConjunction.append(AtLeastEqualInOtherMetric <= model.eval(AtLeastEqualInOtherMetric))               
                j = 1 + j
            i = 1 + i    
            dominationDisjunction.append(And(dominationConjunction))         
        constraintDominateX = Or(dominationDisjunction)
        #print(constraintDominateX)
        #sys.exit()
        return constraintDominateX
