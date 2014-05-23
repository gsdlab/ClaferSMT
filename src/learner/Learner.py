'''
Created on Apr 4, 2014

@author: ezulkosk
'''
from common import Options, Common
from common.Options import experiment_print
from front import ClaferModel, ModelStats
from learner import Classifiers
from parallel.heuristics import GeneralHeuristics
from parallel.heuristics.GeneralHeuristics import HeuristicFailureException
import itertools
import numpy as np
import operator
import os
import random
import shutil
import subprocess
import sys



class Learner():

    def __init__(self, options):
        self.options = options
        self.heuristics = self.loadHeuristicsFile()
        self.heuristic_list = self.numberHeuristics(self.heuristics, Options.EXPERIMENT_NUM_SPLIT)
        if not Options.FILE:
            (self.parameters, self.parameter_constraints, self.attribute_constraints, self.non_modelstats) = self.loadParametersFile()
            (self.constrained_parameters, self.constrained_parameters_and_ranges) = self.getConstrainedParameterRanges()
            self.classifier = self.createClassifier(self.options)
    
    def getModelStats(self, file):
        currMode = Options.MODE
        module = Common.load(file)
        z3 = ClaferModel.ClaferModel(module)
        parameters = ModelStats.run(z3, self.parameters, self.non_modelstats)
        Common.MODE = currMode
        return parameters
  
    def run(self):
        '''
        call Z3run a bunch
        change heuristic and heuristic variants as necessary
        '''
        Common.MODE=Common.EXPERIMENT  
        if Options.FILE:
            self.getBestHeuristicForNewInstance(0, [], single_instance_mode=True)
            return
        
        self.print_separator("Generating Test Set")
        self.mode = "test"
        (test_set_parameters, test_set_labels) = self.createInstances(int(self.options.test_set))
        
        
        self.print_separator("Training")
        self.mode = "training"
        (training_set_parameters, training_set_labels) =  self.createInstances(int(self.options.learning_iterations))
        
    
        self.print_separator("Learning")
        print()
        print("Label map:")
        for i in range(len(self.heuristic_list)):
            print("    " + str(i) + " -- " + str(self.heuristic_list[i]))
        print()
        print("Test parameters: " + str(test_set_parameters))
        print("Test labels: " + str(test_set_labels))
        print()
        print("Training parameters: " + str(training_set_parameters))
        print("Training labels: " + str(training_set_labels))
        self.classifier.learn(training_set_parameters, training_set_labels)
        coefficients = self.classifier.getCoefficients()
        print("Coefficients: " + str(coefficients))
        
        self.print_separator("Testing")
        print()
        correct_ratio = self.test(test_set_parameters, test_set_labels)
        print("Ratio of correct labels: " + str(correct_ratio))
    
    
    def test(self, test_set_parameters, test_set_labels):
        num_correct = 0
        for params,best_label in zip(test_set_parameters, test_set_labels):
            predicted_label = self.classifier.predict(params)
            if predicted_label == best_label:
                experiment_print("Correctly Labeled Instance: " + str(params) + " " + str(self.heuristic_list[best_label]))
                num_correct = num_correct + 1
            else:
                experiment_print("Incorrectly Labeled Instance: " + str(params) 
                      + ", Predicted: " + str(self.heuristic_list[predicted_label])
                      + ", Best: " + str(self.heuristic_list[best_label]))
        return num_correct / len(test_set_labels)
            
        
    

    ''' 
    #######################################################################
    # GENERATE NEW INSTANCE  
    #######################################################################
    '''

    def generateNewInstance(self, instance_number=0, list_of_parameters=[]):
        instance_parameters = self.generateInstanceParameters()
        print("\nGenerating " + self.mode + " instance "+ str(instance_number) + " with parameters: " +str(instance_parameters))
        cfr_file = self.plugIntoGenerator(instance_parameters)
        generated_clafer_file = self.generateClaferPy(cfr_file)
        instance = self.generateInstance(generated_clafer_file, instance_number)
        self.checkIfInstanceIsUnsat(instance, instance_number)
        formatted_instance = self.formatFile(instance, instance_number)
        attributed_instance = self.plugInAttributes(formatted_instance, instance_parameters, instance_number)
        py_instance = self.generateClaferPy(attributed_instance)
        module = Common.load(py_instance)
        parameters = self.getModelStats(py_instance)
        if parameters in list_of_parameters:
            experiment_print("Duplicate input generated: " + str(parameters) + ", trying again.")
            return self.generateNewInstance(instance_number, list_of_parameters)
        else:
            return (module, parameters)

    def createInstances(self, iterations):
        list_of_parameters = []
        list_of_labels = []
        #try:
        for i in range(iterations):
            (parameters, best_heuristic_index) = self.getBestHeuristicForNewInstance(i, list_of_parameters)
            experiment_print("Instantiated parameters: " + str(parameters))
            experiment_print("Best heuristic: " + str(self.heuristic_list[best_heuristic_index]))
            list_of_parameters.append(parameters)
            list_of_labels.append(best_heuristic_index)
        #except:
        #    sys.exit("Do not handle explicit test sets yet")
        return (list_of_parameters, list_of_labels)
    
    def getBestHeuristicForNewInstance(self, instance_number, list_of_parameters, single_instance_mode=False):
        if single_instance_mode:
            parameters = []
            module = Common.load(Options.FILE)
        else:
            (module, parameters)  = self.query(instance_number, list_of_parameters)
        best_metric = Common.BOUND
        best_heuristic = ""
        num_models_list = []
        heuristics = []
        all_metrics = []
        unsorted_chart_headers = []
        unsorted_chart = []
        Options.MODE = Common.EXPERIMENT
        for h in self.heuristics:
            Options.SPLIT = h
            unsorted_chart_headers.append(h)
            chart_col = []
            for s in Options.EXPERIMENT_NUM_SPLIT:
                Options.NUM_SPLIT = s
                try:
                    z3 = ClaferModel.ClaferModel(module)
                    z3.run()
                    metric = z3.metric
                    num_models_list.append(z3.num_models)
                except (HeuristicFailureException, RuntimeError) as e:
                    experiment_print(e.value)
                    metric = Common.BOUND
                
                if Options.VERBOSE_PRINT:
                    experiment_print("===============================")
                    experiment_print("| Iteration: " + str(instance_number))
                    experiment_print("| Heuristic: " + str(h))
                    experiment_print("| num_split: " + str(s))
                    experiment_print("===============================")
                    experiment_print(str(parameters) + "," + str(metric))
                heuristics.append(self.heuristic_split_to_str(h, s))
                all_metrics.append(metric)
                chart_col.append("%.2f" % metric)
                if metric < best_metric: 
                    best_metric = metric
                    best_heuristic = self.heuristic_split_to_str(h, s)
            unsorted_chart.append(chart_col)
        experiment_print("Number of instances List: "  + str(num_models_list))
        experiment_print("All metrics: "  + str(all_metrics))
        if len(set(num_models_list)) > 1 and Options.NUM_INSTANCES >= 0:
            experiment_print("WARNING: NUMBER OF INSTANCES DIFFERS BETWEEN TWO HEURISTICS.")
        if single_instance_mode:
            experiment_print()
            results = list(zip(heuristics, all_metrics))
            
            sorted_file = open("sorted", "w")
            unsorted_file = open("unsorted", "w")
            chart_file = open("chart", "w")
            
            self.print_separator("Unsorted")
            for (i,j) in results:
                experiment_print(i + " : " + str(j)) 
                unsorted_file.write(i + " " + str(j) + "\n")
            experiment_print()
            results.sort(key=operator.itemgetter(1))
            self.print_separator("Sorted")
            for (i,j) in results:
                experiment_print(i + " : " + str(j)) 
                sorted_file.write(i + " " + str(j) + "\n")
            
            #chart
            print("Iteration " + " ".join(unsorted_chart_headers))
            count = 1
            for tup in zip(*unsorted_chart):
                print(str(count) + " " + " ".join([str(i) for i in list(tup)]))
                count = count + 1
            
            
            
            if self.options.generate_graphs:
                pass
        
        return (parameters, self.heuristic_list.index(best_heuristic))

    def query(self, instance_number, list_of_parameters):
        #self.classifier.learn(self.parameters, self.labels)
        instance_file = self.generateNewInstance(instance_number, list_of_parameters)
        return instance_file

    def checkIfInstanceIsUnsat(self, instance, instance_number):
        opened_instance = open(instance, 'r')
        for i in opened_instance.readlines():
            if i.startswith("UNSAT"):
                opened_instance.close()
                experiment_print("Produced an UNSAT instance, trying again.")
                self.generateNewInstance(instance_number)


    def getConstrainedParameterRanges(self):
        constrained_parameters = []
        final_ranges = []
        print("Beginning Constrained Parameter Ranges")
        for (involved_parameters, lam) in self.parameter_constraints:
            involved_range_parameters = []
            constrained_parameters = constrained_parameters + involved_parameters
            for (p, low, high) in self.parameters:
                if p in involved_parameters:
                    involved_range_parameters.append((p,low,high))
            ranges = [range(low, high+1) for (_, low, high) in involved_range_parameters]
            new_range = list(filter(lambda x : self.applyLambda(lam, x), itertools.product(*ranges)))
            
            final_ranges.append((involved_parameters, new_range))
        print("Finished Constrained Parameter Ranges")
        return (constrained_parameters, final_ranges)

    def generateInstanceParameters(self):
        instance_parameters = []
        for (f, low,high) in self.parameters:
            if f in self.constrained_parameters:
                continue
            instance_parameters.append((f, random.randint(low, high)))
        
        for (parameters, valid_tuples) in self.constrained_parameters_and_ranges:
            tup = random.choice(valid_tuples)
            for param,val in zip(parameters, tup):
                instance_parameters.append((param, val))
        
        #stupid sort
        sorted_instance_parameters = []
        for (i,_,_) in self.parameters:
            for (j, val) in instance_parameters:
                if i == j:
                    sorted_instance_parameters.append((j,val))
                    break
        
        return sorted_instance_parameters

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
        file_name = self.options.output_directory + self.mode + str(instance_number) + "_noattributes.cfr"
        opened_temp_file = open(file_name, "w")
        subprocess.call(['python3', self.options.formatter, file], stdout=opened_temp_file)
        return file_name
    
    def plugInAttributes(self, file, instance_parameters, instance_number):
        file_name = self.options.output_directory + self.mode + str(instance_number) + ".cfr"
        opened_temp_file = open(file_name, "w")
        
        with open(file) as f:
            content = f.readlines()
        
        attributes = [ "@" + i for (i, _, _, _) in self.attribute_constraints]
        
        for i in content:
            for a in attributes:
                if a in i:
                    for (attr, l, h, lam) in self.attribute_constraints:
                        if a == "@" + attr:
                            low = [val for (param, val) in instance_parameters if param == l][0]
                            high = [val for (param, val) in instance_parameters if param == h][0]
                    i = i.replace(a, str(lam(low,high)))
            opened_temp_file.write(i)
        
        return file_name
    
    def generateClaferPy(self, file):
        fnull = open(os.devnull, "w")
        subprocess.call(['clafer', '-m', 'python', file], stdout=fnull)
        return file.split(".")[0] + ".py"
    
    def generateInstance(self, claferpyfile, instance_number=0):
        file_name = self.options.output_directory + self.mode  + str(instance_number) + "_unformatted" + ".cfr"
        instance = open(file_name, "w")
        subprocess.call(['ClaferZ3', '--delimeter=\"\"', claferpyfile], stdout=instance)
        return file_name

    ''' 
    #######################################################################
    # END GENERATE NEW INSTANCE  
    #######################################################################
    '''
    
    def writeLabeledInstanceToFile(self, string, file):
        pass
        
    def loadFile(self):
        self.data = np.loadtxt(self.options.data_file, delimiter=',', ndmin=2)
        self.parameters, self.labels = self.data[:, :-1], self.data[:, -1].astype(np.int)

    def createClassifier(self, options):
        return Classifiers.LDAC(options)
   
    def numberHeuristics(self, heuristics, splits):
        heuristic_list = []
        for h in heuristics:
            for s in splits:
                heuristic_list.append(self.heuristic_split_to_str(h, s))
        return heuristic_list
                
    def heuristic_split_to_str(self, heuristic, split):
        return str(heuristic) + "#" + str(split)
   
    def loadParametersFile(self):
        file = self.options.parameters_file
        parameters = []
        parameter_constraints = []
        attribute_constraints = []
        non_modelstats = []
        f = open(file)
        for i in f:
            if "//" in i:
                i = i.split("//", 1)[0]
            i = i.strip()
            if i == "":
                continue
            if i.startswith("@Constraint"):
                parameter_constraints.append(self.produce_lambda(i.split("@Constraint",1)[1], parameters))
            elif i.startswith("@Attribute"):
                line = i.split()
                attribute_constraints.append((line[1], line[2], line[3], self.produce_attribute_lambda()))
            elif i.startswith("@NonModelStats"):
                line = i.split()
                non_modelstats.append(line[1])
                parameters.append((line[1], int(line[2]), int(line[3])))
            else:
                line = i.split()
                parameters.append((line[0], int(line[1]), int(line[2])))
        return (parameters, parameter_constraints, attribute_constraints, non_modelstats)
    
    def loadHeuristicsFile(self):
        file = self.options.heuristics_file
        if Options.SPLIT != "no_split":
            return [Options.SPLIT]
        if file == "all":
            return GeneralHeuristics.heuristics_list
        
        heuristics = []
        f = open(file)
        for i in f:
            if "//" in i:
                i = i.split("//", 1)[0]
            if i.strip() == "":
                continue
            line = i.split()
            heuristics.append(line[0])
        return heuristics
    
    def print_separator(self, string):
        experiment_print()
        experiment_print("===============================")
        experiment_print("| " + string)
        experiment_print("===============================")
    
    ''' 
    #######################################################################
    # LAMBDA PARAMETER CONSTRAINT 
    #######################################################################
    '''    
        
    def produce_lambda(self, constraint, parameters):
        involved_parameters = []
        for (param, _, _) in parameters:
            if param in constraint:
                involved_parameters.append(param)
        lam_str = "lambda " + ", ".join(involved_parameters) + ":" + constraint
        lam = eval(lam_str)
        return (involved_parameters, lam)
    
    def produce_attribute_lambda(self):
        lam_str = "lambda lowerBound, upperBound: random.randint(lowerBound, upperBound)"
        #print(lam_str)
        lam = eval(lam_str)
        return lam
        
    
    def applyLambda(self, lam, tuple):
        return lam(*tuple)
    ''' 
    #######################################################################
    # END LAMBDA PARAMETER CONSTRAINT 
    #######################################################################
    '''
    
if __name__ == '__main__':
    options = Options.setCommandLineOptions(learner=True) 
    learner = Learner(options)
    learner.run()
        