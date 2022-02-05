#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 4 15:10:11 2022

@author: ckadelka
"""

import time
import find_layers
import sys

inputfile = sys.argv[1]    
outputfile = sys.argv[2]

if len(sys.argv)>3:
    USE_FAST_METHOD = bool(int(sys.argv[3]))
else:
    USE_FAST_METHOD = True

def get_layer_format(inputfile,outputfile,USE_FAST_METHOD=True):
    if USE_FAST_METHOD:
        method = find_layers.find_layers_fast
    else:
        method = find_layers.find_layers
    
    file = open(inputfile,'r')
    lines = file.read().splitlines()
    file.close()
    
    outputs = []
    
    for line in lines:
        linesplit = line.split('\t')
        ID = linesplit[0]
        f = list(map(int,linesplit[2].split(','))) 
        current=time.time() #record how long the specific method takes to compute the layer format
        dummy = method(f) 
        time_passed = time.time()-current
        
        (canalizing_depth,number_of_layers,canalizing_inputs,canalized_outputs,core_polynomial,canalizing_order) = dummy
        layers = []
        for i in range(canalizing_depth): #a new layer begins wherever there is a change in the canalized_output vector
            if i==0 or canalized_outputs[i]!=canalized_outputs[i-1]:
                layers.append([])
            layers[-1].append('x%i => %i' % (canalizing_order[i]+1,canalizing_inputs[i]))
        layers_str = ', '.join(['({%s},%i)' % (', '.join(layer),canalized_outputs[0] if ii%2==0 else 1-canalized_outputs[0]) for ii,layer in enumerate(layers)])
        #core_polynomial_str = '[%s]' % ''.join(list(map(str,core_polynomial)))
        core_polynomial_str = ''.join(list(map(str,core_polynomial)))
        layer_format = '({%s},%s)' % (layers_str,core_polynomial_str)
        outputs.append('%s\t%i\t%i\t%s\t%f' % (ID,number_of_layers,canalizing_depth,layer_format,time_passed))
    file = open(outputfile,'w')
    file.write('\t'.join(['ID','NumLayers','Depth','CanalizationStructure','CpuTime'])+'\n')
    file.write('\n'.join(outputs))
    file.close()

get_layer_format(inputfile,outputfile,USE_FAST_METHOD=USE_FAST_METHOD)