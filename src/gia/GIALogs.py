'''
Created on Apr 25, 2013

@author: rafaelolaechea
'''

from cgi import escape
from gia import consts
from time import time


class GIALogEntry(object):
    '''
    classdocs
    '''
    def __init__(self, options, constraints=[], start_time=None,):
        self.options = options
        self.start_time = start_time
        self.statistics = {}
    
    def FillInformationOnCallerFinish(self,  end_time=None, satisfiable=None, model=None, statistics=None):
        self.end_time = end_time
        self.satisfiable = satisfiable
        self.model = model

        for k, v in statistics:
            self.statistics[k] = v

        
    def MarkAsParetoPoint(self):            
        self.is_pareto_point = True
            

class GIALogging(object):
    def __init__(self, options, objective_variables, feature_variables):
        self.options = options
        self.objective_variables = objective_variables
        self.feature_variables = feature_variables
        self.logEntryList = list()
    
    def getLog(self):
        return self.logEntryList
    
    def logStartCall(self, constraints=[]):
        if self.options.useCallLogs == True:
            if self.options.verbosity > consts.VERBOSE_NONE:
                print("LogStartCall")
            if self.options.incrementallyWriteLog == True:
                if len(self.logEntryList) > 0:
                    self.options.logfile.write(",\n {")
                else:
                    self.options.logfile.write("{")  
            self.options.logfile.write("\"constraints\" : \"%s\",\n" % str(constraints).replace("\n",""))             
            logEntry = GIALogEntry(self.options, constraints, start_time=time())
            self.logEntryList.append(logEntry)

    
    def _toLowerCaseIfBoolean(self, value):
        if str(value) == "True" or str(value) == "False":
            return str(value).lower()
        else:
            return value
        
    def logEndCall(self, satisfiable, model=None, statistics=None):
        if self.options.useCallLogs == True:        
            if self.options.verbosity > consts.VERBOSE_NONE:
                print("LogEndCall")
            logEntry = self.logEntryList[-1]
            logEntry.FillInformationOnCallerFinish(end_time=time(), satisfiable=satisfiable, model=model, statistics=statistics)
            
            if self.options.incrementallyWriteLog == True:
                statisticsSerializedDict = ",\n".join(\
                    ["\"%s\"  : %s " % (k,logEntry.statistics[k])  for k in \
                      logEntry.statistics.keys()])
                self.options.logfile.write("\"statistics\": {\n %s },\n" % statisticsSerializedDict)
                self.options.logfile.write("\"timeTaken\":  %s ,\n" %  (logEntry.end_time - logEntry.start_time))            
                if logEntry.satisfiable==True:                
                    objectivesSerializedDict = ",\n".join(\
                        ["\"%s\"  : %s " % (k ,self._toLowerCaseIfBoolean(logEntry.model[k]))  for k in \
                          self.objective_variables])                
                    self.options.logfile.write("\"objective_variables\" : {\n %s },\n" %  objectivesSerializedDict)    
                    decisionsSerializedDict = ",\n".join(\
                        ["\"%s\"  : %s " % (k ,self._toLowerCaseIfBoolean(logEntry.model[k]))  for k in \
                          self.feature_variables])                            
                    self.options.logfile.write("\"feature_variables\": {\n %s },\n" %  decisionsSerializedDict)                
                self.options.logfile.write("\"satisfiable\":  %s \n" %  str(logEntry.satisfiable).lower())
                self.options.logfile.write("}")
                self.options.logfile.flush()
    