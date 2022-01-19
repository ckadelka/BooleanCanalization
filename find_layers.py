# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:57:39 2021

@author: ckadelka
"""

import numpy as np
import itertools

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
    
def find_layers_v3(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
    n = int(np.log2(len(F))) #n = number of variables
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
        inputs = 1-indices1//n #if index \in indices1 < n, then the canalizing input value is 1, otherwise 0
        outputs = np.ones(len(indices1),dtype=int) #canalizing outputs are all b=1
        new_canalizing_variables = []
        for index in np.sort(indices1%n)[::-1]: #deletes canalizing variables from variables in reverse order to avoid an index error
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.all(np.array([table[(index+n)%(2*n)] for index in indices1]),0)]
        return find_layers_v3(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
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
            inputs = 1-indices0//n #if index \in indices0 < n, then the canalizing input value is 1, otherwise 0
            outputs = np.zeros(len(indices0),dtype=int)
            new_canalizing_variables = []
            for index in np.sort(indices0%n)[::-1]:  #deletes canalizing variables from variables in reverse order to avoid an index error
                new_canalizing_variables.append(variables.pop(index))
            new_canalizing_variables.reverse()
            newF = F[np.all(np.array([table[(index+n)%(2*n)] for index in indices0]),0)]
            return find_layers_v3(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    # if there is no x_i that canalizes f to 0 or 1, stop the recursion and return the results
    return (depth,number_layers,can_inputs,can_outputs,F,can_order)



# import time
    
# def get_layers_directly_v3(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
#     start = time.time()
#     n = int(np.log2(len(F))) #n = number of variables
#     timer = [(time.time() - start)]
#     w = np.sum(F) #w= Hamming weight = number of 1s in truth table
#     timer.append(time.time() - start)
#     if w == 0 or w == 2**n: #constant F
#         return (depth,number_layers,can_inputs,can_outputs,F,can_order)
#     if type(variables)==np.ndarray:
#         variables = list(variables)
#     if variables == []: #default variables: 0, 1, ..., n-1
#         variables = list(range(n))
#     if type(F) == list:
#         F = np.array(F)
#     #desired_value = 2**(n-1) #variable x_i is canalizing if f is constant when x_i receives canalizing input a, that is, the dot product of t_i==a and f==b is 2^{n-1}
#     #T = np.array(list(itertools.product([0, 1], repeat=n))).T #creates the right hand side of the truth table
#     timer.append(time.time() - start)
        
#     AA = AAs[n]
#     indicesA = indicesAs[n]
#     #indicesA=np.zeros((2*n,desired_value),dtype=np.int32)
#     #for i in range(n):
#     #    indicesA[i] = np.where(T[i])[0]
#     #    indicesA[i+n] = np.where(T[i]==0)[0]
#     timer.append(time.time() - start)

    
#     #indices1 = np.where(np.all(F[indicesA],1))[0] #check if any x_i canalizes f to 1
#     indices1 = np.array([],dtype=np.int32)
#     for i in range(2*n):
#         for index in indicesA[i]:
#             if F[index]==0:
#                 break
#         else:
#             indices1 = np.append(indices1,i)
#     timer.append(time.time() - start)
    
#     if len(indices1)>0: #if any x_i canalizes f to 1
#         inputs = 1-indices1//n #if index \in indices1 < n, then the canalizing input value a=1, otherwise a=0
#         outputs = np.ones(len(indices1),dtype=int) #canalizing outputs are all b=1
#         new_canalizing_variables = []
#         for index in np.sort(indices1%n)[::-1]:
#             new_canalizing_variables.append(variables.pop(index))
#         new_canalizing_variables.reverse()
#         #newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices1,inputs)])))]
#         newF = F[np.all(np.array([AA[(index+n)%(2*n)] for index in indices1]),0)]
#         print(n,'\n'.join(map(str,timer)),'\n')
#         return get_layers_directly_v3(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
#     else:
#         #indices0 = np.where(np.all(1-F[indicesA],1))[0] #check if any x_i canalizes f to 0, i.e. 1-f to 1        
#         indices0 = np.array([],dtype=np.int32)
#         for i in range(2*n):
#             for index in indicesA[i]:
#                 if F[index]==1:
#                     break
#             else:
#                 indices0 = np.append(indices0,i)
#         timer.append(time.time() - start)
#         if len(indices0):        
#             inputs = 1-indices0//n
#             outputs = np.zeros(len(indices0),dtype=int)
#             new_canalizing_variables = []
#             for index in np.sort(indices0%n)[::-1]:
#                 new_canalizing_variables.append(variables.pop(index))
#             new_canalizing_variables.reverse()
#             #newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
#             newF = F[np.all(np.array([AA[(index+n)%(2*n)] for index in indices0]),0)]
#             print(n,'\n'.join(map(str,timer)),'\n')
#             return get_layers_directly_v3(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
#     print(n,'\n'.join(map(str,timer)),'\n')
#     return (depth,number_layers,can_inputs,can_outputs,F,can_order)


# def find_layers_with_precomputed_tables(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
#     start = time.time()
#     n = int(np.log2(len(F)))
#     timer = [(time.time() - start)]
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
#     timer.append(time.time() - start)
#     if len(indices1)>0:
#         inputs = 1-indices1//n
#         outputs = np.ones(len(indices1),dtype=int)
#         new_canalizing_variables = []
#         for index in np.sort(indices1%n)[::-1]:
#             new_canalizing_variables.append(variables.pop(index))
#         new_canalizing_variables.reverse()
#         newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices1,inputs)])))]
#         return find_layers_with_precomputed_tables(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
#     elif len(indices0):        
#         inputs = 1-indices0//n
#         outputs = np.zeros(len(indices0),dtype=int)
#         new_canalizing_variables = []
#         for index in np.sort(indices0%n)[::-1]:
#             new_canalizing_variables.append(variables.pop(index))
#         new_canalizing_variables.reverse()
#         newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
#         return find_layers_with_precomputed_tables(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
#     else:
#         print(n,'\n'.join(map(str,timer)),'\n')
#         return (depth,number_layers,can_inputs,can_outputs,F,can_order)
    
    
    