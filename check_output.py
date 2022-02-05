#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 4 15:23:21 2022

@author: ckadelka
"""

import itertools
import sys

def poly_to_bool(poly):
    var = list(set(poly.replace('*',',').replace('+',',').split(','))-set(['1','']))
    var_ids = list(map(lambda x: int(x[1:]), var))
    var_ids.sort() 
    var = list(map(lambda i: 'x'+str(i), var_ids))
    n = len(var)
    bool_list_dummy = list(itertools.product([0, 1], repeat = n))
    for i in range(n-1,-1,-1):
        poly = poly.replace(var[i],'x[%i]' % i)
    f = []
    for x in bool_list_dummy:
        f.append(eval(poly)%2)
    return f
    

outputfile1 = sys.argv[1]    
outputfile2 = sys.argv[2]

file1 = open(outputfile1,'r')
lines1 = file1.read().splitlines()
file1.close()

file2 = open(outputfile2,'r')
lines2 = file2.read().splitlines()
file2.close()

for line1,line2 in zip(lines1[1:],lines2[1:]):
    linesplit1 = line1.split('\t')
    linesplit2 = line2.split('\t')
    layer_structure1 = linesplit1[3]
    layer_structure2 = linesplit2[3]
    layers1 = layer_structure1[1:layer_structure1.rfind(',')]
    layers2 = layer_structure2[1:layer_structure2.rfind(',')]
    corefunction1 = layer_structure1[layer_structure1.rfind(',')+1:-1]
    corefunction2 = layer_structure2[layer_structure2.rfind(',')+1:-1]
    assert layers1==layers2,"layers not the same at ID "+str(linesplit1[0])
    
    #check for each core function if it is a polynomial (from M2 code) or a table (from Python code) and turn it into a string of a table
    corefunction1_astable_string = corefunction1 if set(corefunction1)<=set(['0','1']) else str(poly_to_bool(corefunction1))[1:-1].replace(', ','')
    corefunction2_astable_string = corefunction2 if set(corefunction2)<=set(['0','1']) else str(poly_to_bool(corefunction2))[1:-1].replace(', ','')        
    assert corefunction1_astable_string==corefunction2_astable_string,"core functions not the same at ID "+str(linesplit1[0])
    

        
