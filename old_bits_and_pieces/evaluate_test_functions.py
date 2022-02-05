#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:57:39 2021

@author: ckadelka
"""

import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
#import canalizing_function_toolbox_v1_9 as can
import itertools
import random
import time

def get_layers_directly_v2(F,can_inputs=np.array([],dtype=int),can_outputs=np.array([],dtype=int),can_order=np.array([],dtype=int),variables=[],depth=0,number_layers=0):
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
        return get_layers_directly_v2(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    elif len(indices0):        
        inputs = 1-indices0//n
        outputs = np.zeros(len(indices0),dtype=int)
        new_canalizing_variables = []
        for index in np.sort(indices0%n)[::-1]:
            new_canalizing_variables.append(variables.pop(index))
        new_canalizing_variables.reverse()
        newF = F[np.sort(list(set.intersection(*[] + [set(np.where(A[index]==0)[0]) for index,INPUT in zip(indices0,inputs)])))]
        return get_layers_directly_v2(newF,np.append(can_inputs,inputs),np.append(can_outputs,outputs),np.append(can_order,new_canalizing_variables),variables,depth+len(new_canalizing_variables),number_layers+1)
    else:
        return (depth,number_layers,can_inputs,can_outputs,F,can_order)






#main parameters\
version='v2'

nsim_per_k_per_n = 10
n_min = 1
n_max = 8

#further parameters
seed = 0
EXACT_DEPTH_K = False

if seed==None:
    seed = np.random.randint(1,2**32 - 1)
random.seed(seed)
np.random.seed(seed)

file1 = open('input/testfiles_table_nmin%i_nmax%i_seed%i_%s.txt' % (n_min,n_max,seed,version),'r')
lines_c = file1.read().splitlines()
file1.close()

fs = []
res = []
times_c = []
corefunctions_c = []
inputs_c = []
outputs_c = []
orders_c = []
rs_c = []
ks_c = []
for line in lines_c:
    linesplit = line.split('\t')
    f = list(map(int,linesplit[2].split(',')))
    fs.append(f)
    current=time.time()
    #res.append(can.get_canalizing_depth_inputs_outputs_corefunction_order(f))
    #times_c.append(time.time()-current)
    #n,k,can_inputs,can_outputs,corefunction,can_order = res[-1]    
    #kis = can.get_layer_structure_given_outputs_corefunction(can_outputs,corefunction,n)
    
    res.append(get_layers_directly_v2(f))
    times_c.append(time.time()-current)
    k,r,can_inputs,can_outputs,corefunction,can_order = res[-1] 
    
    ks_c.append(k)
    rs_c.append(r)

#    if k>=2:
#        if kis[-1]>1:
#            if can_outputs[-1]!=can_outputs[-2]:
#                can_outputs[-1] = 1-can_outputs[-1]
#                can_inputs[-1] = 1-can_inputs[-1]
#
#    counter=0
#    for ki in kis: #sort variables within each layer
#        indices = np.argsort(can_order[counter:counter+ki])
#        can_outputs[counter:counter+ki] = list(np.array(can_outputs[counter:counter+ki])[indices])
#        can_inputs[counter:counter+ki] = list(np.array(can_inputs[counter:counter+ki])[indices])
#        can_order[counter:counter+ki] = list(np.array(can_order[counter:counter+ki])[indices])
#        counter+=ki

#    if n==k and kis[-1]==1:
#        if can_inputs[-1]==1:
#            can_inputs[-1] = 0
#            can_outputs[-1] = 1-can_outputs[-1]
    inputs_c.append(can_inputs)
    outputs_c.append(can_outputs)
    orders_c.append(can_order)
    corefunctions_c.append(np.array(corefunction))
    



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
    
file1 = open('data_brandy_david_elena/polys-layers-d.txt','r')
lines_d = file1.read().splitlines()
file1.close()

rs_d = []
ks_d = []
inputs_d = []
outputs_d = []
orders_d = []
corefunctions_d = [] 
times_d = []
for ii,line in enumerate(lines_d[1:]):
    linesplit = line.split('\t')
    rs_d.append(int(linesplit[1]))
    ks_d.append(int(linesplit[2]))
    times_d.append(float(linesplit[4]))
    text = linesplit[3].replace('{','').replace('}','').replace('(','').replace(')','')
    textsplit = text.split(',')
    inputs_d.append([])
    outputs_d.append([])
    orders_d.append([])
    n_in_current_layer=0
    for el in textsplit[:-1]:
        if el in '01':
            outputs_d[-1].extend([int(el) for _ in range(n_in_current_layer)])
        else:
            var,input_value = el.replace(' ','').split('=>')
            orders_d[-1].append(int(var[1:])-1)
            inputs_d[-1].append(int(input_value))
            n_in_current_layer+=1
    inputs_d[-1] = np.array(inputs_d[-1])
    outputs_d[-1] = np.array(outputs_d[-1])
    orders_d[-1] = np.array(orders_d[-1])
    corefunction = textsplit[-1]
    corefunctions_d.append(poly_to_bool(corefunction) if corefunction not in ['1','0'] else [int(corefunction)])




    
file1 = open('data_brandy_david_elena/polys-layers-e.txt','r')
lines_e = file1.read().splitlines()
file1.close()

rs_e = []
ks_e = []
inputs_e = []
outputs_e = []
orders_e = []
corefunctions_e = [] 
times_e = []
for ii,line in enumerate(lines_e[1:]):
    linesplit = line.split('\t')
    rs_e.append(int(linesplit[1]))
    ks_e.append(int(linesplit[2]))
    times_e.append(float(linesplit[4]))
    text = linesplit[3].replace('{','').replace('}','').replace('(','').replace(')','')
    textsplit = text.split(',')
    inputs_e.append([])
    outputs_e.append([])
    orders_e.append([])
    n_in_current_layer=0
    for el in textsplit[:-1]:
        if el in '01':
            outputs_e[-1].extend([int(el) for _ in range(n_in_current_layer)])
        else:
            var,input_value = el.replace(' ','').split('=>')
            orders_e[-1].append(int(var[1:])-1)
            inputs_e[-1].append(int(input_value))
            n_in_current_layer+=1
    inputs_e[-1] = np.array(inputs_e[-1])
    outputs_e[-1] = np.array(outputs_e[-1])
    orders_e[-1] = np.array(orders_e[-1])
    corefunction = textsplit[-1]
    corefunctions_e.append(poly_to_bool(corefunction) if corefunction not in ['1','0'] else [int(corefunction)])







##comparisons
all_inputs = [inputs_c,inputs_d,inputs_e]
all_outputs = [outputs_c,outputs_d,outputs_e]
all_orders = [orders_c,orders_d,orders_e]
all_rs = [rs_c,rs_d,rs_e]
all_ks = [ks_c,ks_d,ks_e]
all_corefunctions = [corefunctions_c,corefunctions_d,corefunctions_e]
    
try:
    print('checking inputs')
    for i in range(3):
        for j in range(i+1,3):
            for ii,(a,b) in enumerate(zip(all_inputs[i],all_inputs[j])):
                assert np.all(a==b), "error at ID "+str(ii)
    print('all the same')
except AssertionError:
    print('NOT all the same, first error at ID '+str(ii))
  
try:
    print('checking outputs')
    for i in range(3):
        for j in range(i+1,3):
            for ii,(a,b) in enumerate(zip(all_outputs[i],all_outputs[j])):
                assert np.all(a==b), "error at ID "+str(ii)
    print('all the same')
except AssertionError:
    print('NOT all the same, first error at ID '+str(ii))     

try:   
    print('checking orders')       
    for i in range(3):
        for j in range(i+1,3):
            for ii,(a,b) in enumerate(zip(all_orders[i],all_orders[j])):
                assert np.all(a==b), "error at ID "+str(ii)
    print('all the same')
except AssertionError:
    print('NOT all the same, first error at ID '+str(ii))     

try:
    print('checking number of layers')       
    for i in range(3):
        for j in range(i+1,3):
            for ii,(a,b) in enumerate(zip(all_rs[i],all_rs[j])):
                assert np.all(a==b)   , "error at ID "+str(ii)
    print('all the same')
except AssertionError:
    print('NOT all the same, first error at ID '+str(ii))     

try:
    print('checking depth')       
    for i in range(3):
        for j in range(i+1,3):
            for ii,(a,b) in enumerate(zip(all_ks[i],all_ks[j])):
                assert np.all(a==b)   , "error at ID "+str(ii)     
    print('all the same')
except AssertionError:
    print('NOT all the same, first error at ID '+str(ii))     

try:
    print('checking core function')       
    for i in range(3):
        for j in range(i+1,3):
            for ii,(a,b) in enumerate(zip(all_corefunctions[i],all_corefunctions[j])):
                assert np.all(a==b)   , "error at ID "+str(ii)
    print('all the same')
except AssertionError:
    print('NOT all the same, first error at ID '+str(ii))     


all_times = [times_c,times_d,times_e]
names = ['claus.py','david.m2','elena.m2']
names2 = []
distributions = []
for i in range(3):
    for j in range(i+1,3):
        f,ax=plt.subplots()
        ax.scatter(all_times[i],all_times[j])
        ax.set_xlabel(names[i])
        ax.set_ylabel(names[j])
        plt.savefig('running_time_%s_vs_%s_%s.pdf' % (names[i],names[j],version),bbox_inches = "tight")

        distributions.append(np.array(all_times[j])/np.array(all_times[i]))
        names2.append(names[j] + ' vs ' +names[i])
distributions = np.array(distributions)
distributions_log10 = np.log10(distributions)
f,ax=plt.subplots()
for i in range(3):
    ax.violinplot(distributions_log10.T,showextrema=False,showmeans=True)
xs=ax.get_xlim()
ax.plot(xs,[0,0],'k--')
ax.set_xlim(xs)
ax.set_xticks(range(1,4))
ax.set_xticklabels(names2)
ax.set_yticks([-1,0,1,2])
ax.set_yticklabels(list(map(lambda x:10**x,[-1,0,1,2])))
ax.set_ylabel('fold change in run time')
plt.savefig('running_time_altogether_%s.pdf' % (version),bbox_inches = "tight")

        
