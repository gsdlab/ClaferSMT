'''
Created on Mar 15, 2014

@author: ezulkosk
'''

from visitors import Visitor, SimplifyModule
from z3 import And, Or, ArithRef
import random
import sys
    
    
    
def random_unique_service_random_server(server, service, num_split):
    '''
    Choose a service that has not been assigned yet, and assign it to some server randomly.
    '''
    numServers = server.numInstances
    numServices = service.numInstances
    
    services = [i for i in service.instances]
    random.shuffle(services)
    jobs = [True]
    #assume jobs is power(2)
    count = 1
    while len(jobs) != num_split:
        nextService = services.pop()
        #it's ok to choose the same one twice
        nextServer = random.randint(0, numServers - 1)
        newjobs = []
        if count * 2 <= num_split:
            
            for i in jobs:
                newjobs.append(And(i, nextService == nextServer))
                newjobs.append(And(i, nextService != nextServer))
        else:
            for i in range(num_split - count):
                newjobs.append(And(jobs[i], nextService == nextServer))
                newjobs.append(And(jobs[i], nextService != nextServer))
            for i in range(num_split - count, len(jobs)):
                newjobs.append(jobs[i])
        jobs = newjobs
    return jobs

def random_unique_service_random_server_range(server, service, num_split):
    #so we don't choose the same one twice
    numServers = server.numInstances
    numServices = service.numInstances
    services = [i for i in service.instances]
    random.shuffle(services)
    jobs = [True]
    #assume jobs is power(2)
    count = 1
    while len(jobs) != num_split:
        nextService = services.pop()
        #it's ok to choose the same one twice
        nextServer = random.randint(0, numServers - 1)
        newjobs = []
        if count * 2 <= num_split:
            [low,high] = sorted([(nextServer - (numServers//2)) % numServers, nextServer])
            for i in jobs:
                newjobs.append(And(i, nextService >= low, nextService < high))
                newjobs.append(And(i, Or(nextService >= high, nextService < low)))
        else:
            for i in range(num_split - count):
                newjobs.append(And(i, nextService >= low, nextService < high))
                newjobs.append(And(i, Or(nextService >= high, nextService < low)))
            for i in range(num_split - count, len(jobs)):
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
    
    sys.exit("BROKEN")
    #for i in self.solver.assertions():
    #    print(i)
    pass    
