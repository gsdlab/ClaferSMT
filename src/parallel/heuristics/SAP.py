'''
Created on Mar 15, 2014

@author: ezulkosk
'''
from common import Options
from visitors import Visitor, SimplifyModule
from z3 import And, Or, ArithRef
import random
import sys

class SAP():
    
    def __init__(self, solver, server, service):
        self.solver = solver
        self.server = server
        self.service = service
        self.numServers = self.server.numInstances
        self.numServices = self.service.numInstances
    
    def random_unique_service_random_server(self):
        #so we don't choose the same one twice
        services = [i for i in self.service.instances]
        random.shuffle(services)
        jobs = [True]
        #assume jobs is power(2)
        count = 1
        while len(jobs) != Options.NUM_SPLIT:
            nextService = services.pop()
            #it's ok to choose the same one twice
            nextServer = random.randint(0, self.numServers - 1)
            newjobs = []
            if count * 2 <= Options.NUM_SPLIT:
                
                for i in jobs:
                    newjobs.append(And(i, nextService == nextServer))
                    newjobs.append(And(i, nextService != nextServer))
            else:
                for i in range(Options.NUM_SPLIT - count):
                    newjobs.append(And(jobs[i], nextService == nextServer))
                    newjobs.append(And(jobs[i], nextService != nextServer))
                for i in range(Options.NUM_SPLIT - count, len(jobs)):
                    newjobs.append(jobs[i])
            jobs = newjobs
        return jobs
    
    def random_unique_service_random_server_range(self):
        #so we don't choose the same one twice
        services = [i for i in self.service.instances]
        random.shuffle(services)
        jobs = [True]
        #assume jobs is power(2)
        count = 1
        while len(jobs) != Options.NUM_SPLIT:
            nextService = services.pop()
            #it's ok to choose the same one twice
            nextServer = random.randint(0, self.numServers - 1)
            newjobs = []
            if count * 2 <= Options.NUM_SPLIT:
                [low,high] = sorted([(nextServer - (self.numServers//2)) % self.numServers, nextServer])
                for i in jobs:
                    newjobs.append(And(i, nextService >= low, nextService < high))
                    newjobs.append(And(i, Or(nextService >= high, nextService < low)))
            else:
                for i in range(Options.NUM_SPLIT - count):
                    newjobs.append(And(i, nextService >= low, nextService < high))
                    newjobs.append(And(i, Or(nextService >= high, nextService < low)))
                for i in range(Options.NUM_SPLIT - count, len(jobs)):
                    newjobs.append(jobs[i])
            jobs = newjobs
        return jobs
    
    def turn_off_servers(self, module):
        #Visitor.visit(SimplifyModule.SimplifyModule(), module)
        
        for i in self.server.instances:
            for j in self.solver.assertions():
                for k in j.children():
                    if isinstance(k, ArithRef) and i == k:
                        pass#print(k)
        
        sys.exit()
        #for i in self.solver.assertions():
        #    print(i)
        pass    
    