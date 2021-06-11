#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:57:39 2021

@author: ckadelka
"""

import numpy as np
import matplotlib.pyplot as plt
#import canalizing_function_toolbox_v1_9 as can
import itertools
import random
import time

n_max = 16

def find_layers(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
    n = int(np.log2(len(F)))
    w = sum(F)
    if w == 0 or w == 2**n: #constant F
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)
    if type(variables)==np.ndarray:
        variables = list(variables)
    if variables == []:
        variables = list(range(n))
    if type(F) == list:
        F = np.array(F)
    desired_value = 2**(n-1)
    T = np.array(list(itertools.product([0, 1], repeat=n))).T
    A = np.r_[T,1-T]
        
    indices1 = np.where(np.dot(A,F)==desired_value)[0]
    indices0 = np.where(np.dot(A,1-F)==desired_value)[0]
    if len(indices1)>0:
        inputs = 1-indices1//n
        outputs = np.ones(len(indices1),dtype=int)
        new_canalizing_variables = []
        for index in np.sort(indices1%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices1,inputs)])))]
        return find_layers(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    elif len(indices0):        
        inputs = 1-indices0//n
        outputs = np.zeros(len(indices0),dtype=int)
        new_canalizing_variables = []
        for index in np.sort(indices0%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
        return find_layers(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    else:
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)

tables = []
for i in range(n_max+1):
    T = np.array(list(itertools.product([0, 1], repeat=i))).T
    A = np.r_[T,1-T]
    tables.append(A)
    
def find_layers_with_precomputed_tables(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
    n = int(np.log2(len(F)))
    w = sum(F)
    if w == 0 or w == 2**n: #constant F
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)
    if type(variables)==np.ndarray:
        variables = list(variables)
    if variables == []:
        variables = list(range(n))
    if type(F) == list:
        F = np.array(F)
    desired_value = 2**(n-1)
    
    A=tables[n]
    
    indices1 = np.where(np.dot(A,F)==desired_value)[0]
    indices0 = np.where(np.dot(A,1-F)==desired_value)[0]
    if len(indices1)>0:
        inputs = 1-indices1//n
        outputs = np.ones(len(indices1),dtype=int)
        new_canalizing_variables = []
        for index in np.sort(indices1%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices1,inputs)])))]
        return find_layers_with_precomputed_tables(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    elif len(indices0):        
        inputs = 1-indices0//n
        outputs = np.zeros(len(indices0),dtype=int)
        new_canalizing_variables = []
        for index in np.sort(indices0%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
        return find_layers_with_precomputed_tables(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    else:
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)



    
    