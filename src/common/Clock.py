'''
Created on Oct 10, 2013

@author: ezulkosk
'''
from common import Options, Common
from common.Options import experiment_print
import sys
import time

class Clock():
    ''' 
    :var isBroken: If true, profiling is off, and therefore we should not output data.
    :var event_map: Maps the beginning and end of events.
    '''
    isBroken = False
    event_map = {}
    
    
    def __init__(self):
        """
        The profiler. Tick...tock...tick...tock...
        """
        if not Options.PROFILING:
            self.isBroken = True
        self.map = {}
        self.completed_event_map = {}
    
    def tick(self, event):
        """
        :param event: ID of the event that will be mapped. Used to match the start and end of the event.
        :type event: string
        """
        if self.isBroken:
            return
        startTime = time.clock()
        self.event_map[event] = startTime
        
    def tock(self, event):
        """
        :param event: ID of the event that was already mapped. If it does not exist, error.
        :type event: string
        """
        endTime = time.clock()
        if self.isBroken:
            return
        if not event in self.event_map.keys():
            print("Tock with no matching tick: " + event)
            sys.exit(1)
        startTime = self.event_map[event]
        self.event_map.pop(event)
        self.completed_event_map[event] = endTime - startTime        
            
    
    def tack(self, event):
        """
        :param event: ID of the event that may occur many times. Output will be the sum of these times.
        :type event: string
        """
        endTime = time.clock()
        if self.isBroken:
            return
        if not event in self.event_map.keys():
            print("Tack with no matching tick: " + event)
            sys.exit(1)
        startTime = self.event_map[event]
        self.event_map.pop(event)
        self.completed_event_map[event] = self.completed_event_map.get(event, 0) + endTime - startTime      
    
    def printEvent(self, event):
        """
        :param event: ID of the event that we want to print. If it does not exist, error.
        :type event: string
        """
        if self.isBroken:
            return
        if not event in self.completed_event_map.keys():
            print("Event doesn't exist or did not complete: " + event)
        eventTime = self.completed_event_map[event]
        print("Time for " + event + ": " + str(eventTime))
        
    def combineClocks(self, other):
        assert isinstance(other, Clock)
        clock = Clock()
        for i in self.completed_event_map.keys():
            if other.completed_event_map.get(i):
                clock.completed_event_map[i] = self.completed_event_map[i] + other.completed_event_map[i] 
            else:
                clock.completed_event_map[i] = self.completed_event_map[i] 
        for i in other.completed_event_map.keys():
            if not self.completed_event_map.get(i):
                clock.completed_event_map[i] = other.completed_event_map[i]      
             
        return clock
    
    def printEvents(self):
        """
        Prints out all completed events.
        """
        if self.isBroken:
            return
        if Options.MODE == Common.EXPERIMENT:
            sys.exit("Shouldn't get here")
        for i in self.completed_event_map.keys():
            self.printEvent(i)
            
    def getParallelStats(self, cfr):
        """
        Prints out all completed events.
        """
        if self.isBroken:
            return
        if Options.MODE == Common.EXPERIMENT:
            longestConsumer = -1
            longestTask = -1
            merge = -1
            longestConsumerPlusMerge = -1
            
            for key in self.completed_event_map.keys():
                val = self.completed_event_map.get(key)
                if "Consumer" in key and val > longestConsumer:
                    longestConsumer = val
                if "Task" in key and val > longestTask:
                    longestTask = val
                if "Merge" in key:
                    merge = val
                longestConsumerPlusMerge = longestConsumer + merge
            if Options.VERBOSE_PRINT:
                experiment_print("Longest Consumer: " + str(longestConsumer))  
                experiment_print("Longest Task: " + str(longestTask))  
                experiment_print("Merge: " + str(merge))  
                experiment_print("Longest Consumer Plus Merge: " + str(longestConsumerPlusMerge))  
                experiment_print("")  
            cfr.metric = longestConsumerPlusMerge
            #experiment_print(self)  
            return
     
    def hackUnsat(self, starttime):
        #print("B")
        self.completed_event_map["unsattime"] = time.clock() - starttime   
    
    def __str__(self):
        retstr = []
        for i in self.completed_event_map.keys():
            eventTime = self.completed_event_map[i]
            retstr.append(i + ": " + str(eventTime))
        return "\n".join(retstr)+"\n"
            