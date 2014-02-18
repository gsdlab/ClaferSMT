'''
Created on Jan 16, 2014

@author: ezulkosk
'''
import argparse
import sys


def generate_names(options):
    return ["a_" + str(i) for i in range(options.num_clafers)]

def setCommandLineOptions():
    parser = argparse.ArgumentParser(description='Generate a Clafer model.')
    parser.add_argument('--clafers', '-c', dest='num_clafers', type=int, default='1', help='desired number of clafers')
    parser.add_argument('--constraints', '-b', dest='num_constraints', type=int, default='0', help='desired number of bracketed constraints')
    parser.add_argument('--depth', '-d', dest='max_depth', type=int, default='1', help='maximum depth allowed in tree structure')
    parser.add_argument('--maxcard', '-m', dest='max_card', type=int, default='1', help='maximum cardinality on any clafer')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    options = setCommandLineOptions()
    names = generate_names(options)
    print(names)
