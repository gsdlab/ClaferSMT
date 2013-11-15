#!/usr/bin/env python

'''
From the Z3-Str project, slightly adapted to fit into ClaferZ3 by Ed Zulkoski.
'''

import sys
import getopt
import time
import os
import subprocess

# "solver" should point to the binary built. 
# e.g. "/home/z3-str/str"
solver = "/home/ezulkosk/Downloads/Z3-str/str"


#=================================================================== 

def encodeConstStr(constStr):
    constStr = constStr.replace(' ', '_aScIi_040')
    constStr = constStr.replace('\\\"', '_aScIi_042')
    constStr = constStr.replace('#', '_aScIi_043')
    constStr = constStr.replace('$', '_aScIi_044')
    constStr = constStr.replace('\'', '_aScIi_047')
    constStr = constStr.replace('(', '_aScIi_050')
    constStr = constStr.replace(')', '_aScIi_051')
    constStr = constStr.replace(',', '_aScIi_054')
    constStr = constStr.replace(':', '_aScIi_072')
    constStr = constStr.replace(';', '_aScIi_073')
    constStr = constStr.replace('[', '_aScIi_133')
    constStr = constStr.replace(']', '_aScIi_135')
    constStr = constStr.replace('\\\\', '_aScIi_134')
    constStr = constStr.replace('{', '_aScIi_173')
    constStr = constStr.replace('}', '_aScIi_175')
    constStr = constStr.replace('|', '_aScIi_174')
    
    constStr = constStr.replace('`', '_aScIi_140')
    
    
    return constStr


def convert(org_file):  
    absPath = os.path.dirname(os.path.abspath(org_file));
    convertDir = absPath + "/convert";
    if not os.path.exists(convertDir):
        os.makedirs(convertDir)
  
    fileName = os.path.basename(org_file);    
    new_file = os.path.join(convertDir, fileName)    
    
    f_o = open(org_file, 'r')  
    f_n = open(new_file, 'w')
    
    declared_string_var = []
    declared_string_const = []
    converted_cstr = ""
  
    linesInFile = f_o.readlines()
  
    for line in linesInFile:    
        line = line.strip();
        if line == "":
            continue
        if line.startswith(';'):
            continue
        if line.startswith('%'):
            continue
        if line.find("get-model") != -1:
            continue
        if line.find("set-option") != -1:
            continue
        if line.find("declare-variable") != -1:
            #if line.count("(") > 1:
            #print('Format error: Only one declare per line is allowed. Exit...\n')
            #return "eRrOr"
            declared_string_var.append(line.replace('declare-variable', 'declare-const'))      
            continue 

        # -----------------------------
        # start: processing const string
        p1 = -1
        while True:
            p1 = line.find('\"', p1 + 1);
            if p1 == -1:
                break;
            
            # exclude the case "str\"str\"str"
            p2 = line.find('\"', p1 + 1)
            while (not (p2 == -1)) and (not line[p2 - 2] == '\\') and line[p2 - 1] == '\\' and line[p2] == '\"':
                p2 = line.find('\"', p2 + 1)
            
            if p2 == -1:
                print('input format error!\n')
                return "eRrOr"
              
            old_s = line[p1: p2 + 1]
            #print "old_s = " + old_s
            #print "old_s[1 : len(old_s)-1] = " + old_s[1 : len(old_s) - 1] + "\n"
            encoded_s = encodeConstStr( old_s[1 : len(old_s) - 1] )
            line = line.replace(old_s, '__cOnStStR_' + encoded_s)
            
            if encoded_s not in declared_string_const:
                declared_string_const.append(encoded_s)        
            p1 = p2
            # -----------------------------
            # end: processing const string
        converted_cstr = converted_cstr + line + '\n'
    
    output_str = ""
    for strv in declared_string_var:
        output_str = output_str + strv + "\n"
  
    output_str = output_str + '\n'
  
    for str_const in declared_string_const:
        output_str = output_str + '(declare-const __cOnStStR_' + str_const + ' String)\n'
      
    output_str = output_str + '\n'
    output_str = output_str + converted_cstr
      
    f_n.write(output_str)      
  
    f_n.close()
    f_o.close()
    return new_file

  

def processOutput(output):
    output =  str( output, encoding='utf8' )
    lines = output.split("\n")
    result = ""
    for line in lines:
        line = line.strip();
        #skip intermediated variable solutions
        if line.startswith('_t_'):
            continue
        if line == "":
            continue
        result = result + line + "\n"     
    return result
      

def clafer_to_z3str(inputFile):
    if not inputFile:
        inputFile = sys.argv[1]
    
    ctmax = 1   
      
    if not os.path.exists(inputFile):
        print("Input file does not exist: \"" + inputFile + "\"")
        print("Exit...\n")
        exit(0)
    
    deleteConverFile = 0
    if len(sys.argv) > 3:
        deleteConverFile = 1 
  
    convertedFile = convert(inputFile)
    if convertedFile == "eRrOr":
        exit(0)
    ct = 0
  
    try:  
        start = time.time()  
        while ct < ctmax:
            err = subprocess.check_output([solver, "-f", convertedFile]);
            ct = ct + 1    
        eclapse = (time.time() - start)
        outStr = processOutput(err)
        print(outStr)    
        print ("Runs: %s" % ctmax)
        print ("Time(avg) = %s(s)\n" % (eclapse/ctmax))
    except KeyboardInterrupt:
        print ("Interrupted by keyborad")
  
    if deleteConverFile != 0:
        os.remove(convertedFile)   

def main(inputFile=[]):
    if not inputFile:
        inputFile = sys.argv[1]
    
    ctmax = 1
    if len(sys.argv) > 2:
        ctmax = int(sys.argv[2])   
      
    if not os.path.exists(inputFile):
        print("Input file does not exist: \"" + inputFile + "\"")
        print("Exit...\n")
        exit(0)
    
    deleteConverFile = 0
    if len(sys.argv) > 3:
        deleteConverFile = 1 
  
    convertedFile = convert(inputFile)
    if convertedFile == "eRrOr":
        exit(0)
    ct = 0
  
    try:  
        start = time.time()  
        while ct < ctmax:
            err = subprocess.check_output([solver, "-f", convertedFile]);
            ct = ct + 1    
        eclapse = (time.time() - start)
        outStr = processOutput(err)
        print(outStr)    
        print ("Runs: %s" % ctmax)
        print ("Time(avg) = %s(s)\n" % (eclapse/ctmax))
    except KeyboardInterrupt:
        print ("Interrupted by keyborad")
  
    if deleteConverFile != 0:
        os.remove(convertedFile)   
    
if __name__ == '__main__':
    main()
    