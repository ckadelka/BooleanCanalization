# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:57:39 2021

@author: ckadelka
"""

import numpy as np
import itertools

n_max = 20

def find_layers(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
    ''''computes the layer format of any Boolean function in truth table form (array of length 2**n)
    output:
        (depth,number_of_layers,canilizing_inputs,canalized_outputs,core_polynomial,canalizing_order)'''
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
        sorted_order = sorted(range(len(indices1)),key=lambda x: (indices1%n)[x])
        inputs = (1-indices1//n)[np.array(sorted_order)]
        outputs = np.ones(len(indices1),dtype=int)
        new_canalizing_variables = []
        for index in np.sort(indices1%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices1,inputs)])))]
        return find_layers(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    elif len(indices0): 
        sorted_order = sorted(range(len(indices0)),key=lambda x: (indices0%n)[x])
        inputs = (1-indices0//n)[np.array(sorted_order)]
        outputs = np.zeros(len(indices0),dtype=int)
        new_canalizing_variables = []#variables[indices0%n]
        for index in np.sort(indices0%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
        return find_layers(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    else:
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)

# tables = []
# for i in range(n_max+1):
#     T = np.array(list(itertools.product([0, 1], repeat=i))).T
#     A = np.r_[T,1-T]
#     tables.append(A)
    
# def find_layers_with_precomputed_tables(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
#     n = int(np.log2(len(F)))
#     w = sum(F)
#     if w == 0 or w == 2**n: #constant F
#         return (depth,number_layers,can_inputs,can_outputs,F,can_order)
#     if type(variables)==np.ndarray:
#         variables = list(variables)
#     if variables == []:
#         variables = list(range(n))
#     if type(F) == list:
#         F = np.array(F)
#     desired_value = 2**(n-1)
    
#     A=tables[n]
    
#     indices1 = np.where(np.dot(A,F)==desired_value)[0]
#     indices0 = np.where(np.dot(A,1-F)==desired_value)[0]
#     if len(indices1)>0:
#         sorted_order = sorted(range(len(indices1)),key=lambda x: (indices1%n)[x])
#         inputs = (1-indices1//n)[np.array(sorted_order)]
#         outputs = np.ones(len(indices1),dtype=int)
#         new_canalizing_variables = []
#         for index in np.sort(indices1%n)[::-1]:
#             new_canalizing_variables.append(variables.pop(index))
#         new_canalizing_variables.reverse()
#         newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices1,inputs)])))]
#         return find_layers_with_precomputed_tables(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
#     elif len(indices0):        
#         sorted_order = sorted(range(len(indices0)),key=lambda x: (indices0%n)[x])
#         inputs = (1-indices0//n)[np.array(sorted_order)]
#         outputs = np.zeros(len(indices0),dtype=int)
#         new_canalizing_variables = []
#         for index in np.sort(indices0%n)[::-1]:
#             new_canalizing_variables.append(variables.pop(index))
#         new_canalizing_variables.reverse()
#         newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
#         return find_layers_with_precomputed_tables(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
#     else:
#         return (depth,number_layers,can_inputs,can_outputs,F,can_order)
    
indices_tables = [[]]
tables = [[]]
for nn in range(1,n_max+1):
    T = np.array(list(itertools.product([0, 1], repeat=nn))).T
    table = np.array(np.r_[T,1-T],dtype=bool) #attach the negated version of the truth table 
    tables.append(table)
    indices_table = np.zeros((2*nn,2**(nn-1)),dtype=np.int32)
    for i in range(2*nn):
        indices_table[i] = np.where(table[i])[0]
    indices_tables.append(indices_table)
    
def find_layers_fast(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
    n = int(np.log2(len(F))) #n = number of variables
    assert n<=n_max,"Tables have only been precomputed for the analysis of functions with up to n="+str(n_max)+" variables.\nIf you want to proceeed, please manually change n_max to your number of variables at the top of the file find_layers.py"
    w = np.sum(F) #w= Hamming weight = number of 1s in truth table
    if w == 0 or w == 2**n: #constant F
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)
    if type(variables)==np.ndarray:
        variables = list(variables)
    if variables == []: #default variables: 0, 1, ..., n-1
        variables = list(range(n))
    if type(F) == list:
        F = np.array(F)
        
    table = tables[n]
    indices_table = indices_tables[n]

    indices1 = []
    for i in range(2*n):
        for index in indices_table[i]:
            if F[index]==0:
                break
        else:
            indices1.append(i)
    
    if len(indices1)>0: #if any x_i canalizes f to 1
        indices1 = np.array(indices1)
        sorted_order = sorted(range(len(indices1)),key=lambda x: (indices1%n)[x])
        inputs = (1-indices1//n)[np.array(sorted_order)] #if index \in indices1 < n, then the canalizing input value is 1, otherwise 0
        outputs = np.ones(len(indices1),dtype=int) #canalizing outputs are all b=1
        new_canalizing_variables = []
        for index in np.sort(indices1%n)[::-1]: #deletes canalizing variables from variables in reverse order to avoid an index error
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.all(np.array([table[(index+n)%(2*n)] for index in indices1]),0)]
        return find_layers_fast(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    else: #if any x_i canalizes f to 0, only possible if no x_i canalizes f to 1 because all canalizing variables that are part of the same layer have the same output
        indices0 = []
        for i in range(2*n):
            for index in indices_table[i]:
                if F[index]==1:
                    break
            else:
                indices0.append(i)
        if len(indices0):        
            indices0 = np.array(indices0)
            sorted_order = sorted(range(len(indices0)),key=lambda x: (indices0%n)[x])
            inputs = (1-indices0//n)[np.array(sorted_order)] #if index \in indices0 < n, then the canalizing input value is 1, otherwise 0
            outputs = np.zeros(len(indices0),dtype=int)
            new_canalizing_variables = []
            for index in np.sort(indices0%n)[::-1]:  #deletes canalizing variables from variables in reverse order to avoid an index error
                new_canalizing_variables.append(variables.pop(index))
            new_canalizing_variables.reverse()
            newF = F[np.all(np.array([table[(index+n)%(2*n)] for index in indices0]),0)]
            return find_layers_fast(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    # if there is no x_i that canalizes f to 0 or 1, stop the recursion and return the results
    return (depth,number_layers,can_inputs,can_outputs,F,can_order)

    