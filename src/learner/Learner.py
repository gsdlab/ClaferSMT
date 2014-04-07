'''
Created on Apr 4, 2014

@author: ezulkosk
'''
from common import Options, Common
from common.Common import experiment_print
from front import Z3Instance, ModelStats
from learner import Classifiers
import numpy as np
import os
import random
import shutil
import subprocess
import sys



class Learner():
    
    def __init__(self, options):
        self.options = options
        self.features = self.loadFeatureFile()
        self.classifier = self.createClassifier(self.options)
        self.numberHeuristics(Options.HEURISTICS, Options.EXPERIMENT_NUM_SPLIT)
   
    def runZ3(self, module):
        z3 = Z3Instance.Z3Instance(module)
        z3.run()
        return z3
  
    
    def getModelStats(self, file):
        currMode = Common.MODE
        Common.MODE = Common.PRELOAD
        module = Common.load(file)
        z3 = self.runZ3(module)
        parameters = ModelStats.run(z3, module, self.features)
        Common.MODE = currMode
        return parameters
  
    def run(self):
        '''
        call Z3run a bunch
        change options.mode
        change heuristic and heuristic variants as necessary
        '''
        
        
        
        Common.MODE=Common.EXPERIMENT
        for i in range(self.options.learning_iterations):
            instance_file = self.query(i)
            module = Common.load(instance_file)
            parameters = self.getModelStats(instance_file)
            #print(parameters)
            best_metric = 99999999999999999
            best_heuristic = ""
            for h in Options.HEURISTICS:
                Options.SPLIT = h
                for s in Options.EXPERIMENT_NUM_SPLIT:
                    Options.NUM_SPLIT = s
                    z3 = self.runZ3(module)
                    if Options.VERBOSE_PRINT:
                        experiment_print("===============================")
                        experiment_print("| Iteration: " + str(i))
                        experiment_print("| Heuristic: " + str(h))
                        experiment_print("| num_split: " + str(s))
                        experiment_print("===============================")
                        experiment_print(str(parameters) + "," + str(z3.metric))
                    if z3.metric < best_metric: 
                        best_metric = z3.metric
                        best_heuristic = self.heuristic_split_to_str(h, s)
            print(best_heuristic)
            #print(self.heuristic_list.index(best_heuristic))
            self.writeLabeledInstanceToFile(str(parameters) + "," + str(z3.metric), self.options.data_file)
        print()

    def query(self, instance_number):
        #self.classifier.learn(self.parameters, self.labels)
        instance_file = self.generateNewInstance(instance_number)
        return instance_file

    ''' ----------- GENERATE NEW INSTANCE ------------ '''

    def generateNewInstance(self, instance_number=0):
        instance_parameters = self.generateInstanceParameters()
        print("Generating instance "+ str(instance_number) + " with parameters: " +str(instance_parameters))
        
        cfr_file = self.plugIntoGenerator(instance_parameters)
        generated_clafer_file = self.generateClaferPy(cfr_file)
        instance = self.generateInstance(generated_clafer_file, instance_number)
        self.checkIfInstanceIsUnsat(instance, instance_number)
        formatted_instance = self.formatFile(instance, instance_number)
        py_instance = self.generateClaferPy(formatted_instance)
        return py_instance

    def checkIfInstanceIsUnsat(self, instance, instance_number):
        opened_instance = open(instance, 'r')
        for i in opened_instance.readlines():
            if i.startswith("UNSAT"):
                opened_instance.close()
                print("Produced an UNSAT instance, trying again.")
                self.generateNewInstance(instance_number)

    def generateInstanceParameters(self):
        instance_parameters = []
        for (f, low,high) in self.features:
            instance_parameters.append((f, random.randint(low, high)))
        return instance_parameters

    def plugIntoGenerator(self, instanceParameters):
        new_file = self.options.output_directory + "temp.cfr"
        out_file = self.options.output_directory + "temp"
        shutil.copyfile(self.options.generator_file, new_file)
        for (feature, num) in instanceParameters:
            opened_out_file = open(out_file, "w")
            matchstr = 's/@' + feature + '/' + str(num) + '/g'
            subprocess.call(['sed', matchstr, new_file], stdout=opened_out_file )
            shutil.copyfile(out_file, new_file)
        os.remove(out_file)
        return new_file
    
    def formatFile(self, file, instance_number):
        file_name = self.options.output_directory + "inst" + str(instance_number) + ".cfr"
        opened_temp_file = open(file_name, "w")
        subprocess.call(['python3', self.options.formatter, file], stdout=opened_temp_file)
        return file_name

    def generateClaferPy(self, file):
        fnull = open(os.devnull, "w")
        subprocess.call(['clafer', '-m', 'python', file], stdout=fnull)
        return file.split(".")[0] + ".py"
    
    def generateInstance(self, claferpyfile, instance_number=0):
        file_name = self.options.output_directory + "temp" + str(instance_number) + ".cfr"
        instance = open(file_name, "w")
        subprocess.call(['ClaferZ3', '--delimeter=\"\"', claferpyfile], stdout=instance)
        return file_name

    '''---------- END GENERATE NEW INSTANCE --------- '''

    def writeLabeledInstanceToFile(self, string, file):
        pass
        
    def loadFile(self):
        self.data = np.loadtxt(self.options.data_file, delimiter=',', ndmin=2)
        self.parameters, self.labels = self.data[:, :-1], self.data[:, -1].astype(np.int)

    def createClassifier(self, options):
        return Classifiers.LDAC(options)
   
    def numberHeuristics(self, heuristics, splits):
        self.heuristic_list = []
        for h in heuristics:
            for s in splits:
                self.heuristic_list.append(self.heuristic_split_to_str(h, s))
                
    def heuristic_split_to_str(self, heuristic, split):
        return str(heuristic) + "#" + str(split)
   
    def loadFeatureFile(self):
        file = self.options.features_file
        features = []
        f = open(file)
        for i in f:
            line = i.split()
            features.append((line[0], int(line[1]), int(line[2])))
        return features
   
if __name__ == '__main__':
    options = Options.setCommandLineOptions() 
    learner = Learner(options)
    learner.run()
    

    
        
        