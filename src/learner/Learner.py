'''
Created on Apr 4, 2014

@author: ezulkosk
'''
from common import Options, Common
from front import Z3Run
from learner import Classifiers



class Learner():
    
    def __init__(self, options):
        self.options = options
        self.classifier = None
        
   
   
   
  
    def run(self):
        '''
        call Z3run a bunch
        change options.mode
        change heuristic and heuristic variants as necessary
        '''
        Options.MODE = Common.MODELSTATS
        Z3Run.run(self.options)
        print()
        Options.MODE=Common.EXPERIMENT
        Classifiers.test()
        for i in range(self.options.learning_iterations):
            for h in Options.HEURISTICS:
                Options.SPLIT = h
                for s in Options.EXPERIMENT_NUM_SPLIT:
                    Options.NUM_SPLIT = s
                    print("===============================")
                    print("| Iteration: " + str(i))
                    print("| Heuristic: " + str(h))
                    print("| num_split: " + str(s))
                    print("===============================")
                    Z3Run.run(self.options)
        print()


def createClassifier(options):
    return Classifiers.SVM(options)
   
   
if __name__ == '__main__':
    options = Options.setCommandLineOptions() 
    classifier = createClassifier(options)
     
    learner = Learner(options)
    learner.run()
    

    
        
        