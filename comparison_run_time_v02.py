#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 15:57:39 2021

@author: ckadelka
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import find_layers
from matplotlib.patches import Rectangle
import sys

if len(sys.argv)>1:
    n_min = int(sys.argv[1])
else:
    n_min = 4

if len(sys.argv)>2:
    n_max = int(sys.argv[2])
else:
    n_max = 16

if len(sys.argv)>3:
    n_step = int(sys.argv[3])
else:
    n_step = 2
    
if len(sys.argv)>4:
    nsim = int(sys.argv[4])
else:
    nsim = 5 
    
if len(sys.argv)>5:
    seed = int(sys.argv[5])
else:
    seed = 0

if len(sys.argv)>6:
    EXACT_DEPTH_K = bool(sys.argv[6])
else:
    EXACT_DEPTH_K = False  
    

#initialize lists for each algorithm that will store the run time for each test function 
results_runtime_m2=[]
results_runtime_py=[]
results_runtime_py_v2=[]
results_runtime_py_v3=[]

which_options = ['real']

#for option in ['kmin0','NCF']:
for option in ['real']:
    file1 = open('input/testfiles_table_nmin%i_nmax%i_nstep%i_%s_seed%i.txt' % (n_min,n_max,n_step,option,seed),'r')
    lines = file1.read().splitlines()
    file1.close()
    
    result_runtime_py = [[] for i in range(n_min,n_max+1,n_step)]
    result_runtime_py_v2 = [[] for i in range(n_min,n_max+1,n_step)]
    result_runtime_py_v3 = [[] for i in range(n_min,n_max+1,n_step)]
    ns=list(range(n_min,n_max+1,n_step)) #array that contains all values for n (number of variables) to be considered
    
    for line in lines:
        linesplit = line.split('\t')
        index = ns.index(int(linesplit[1]))
        f = list(map(int,linesplit[2].split(',')))
        
        current=time.time() #record how long the Python implementation find_layers.find_layers takes
        dummy = find_layers.find_layers(f) 
        time_passed = time.time()-current
        result_runtime_py[index].append(time_passed)    
    
        current=time.time() #record how long the Python implementation find_layers.find_layers_with_precomputed_tables takes
        dummy = find_layers.find_layers_with_precomputed_tables(f)
        time_passed = time.time()-current
        result_runtime_py_v2[index].append(time_passed)

        current=time.time() #record how long the Python implementation find_layers.find_layers_v3 takes
        dummy = find_layers.find_layers_v3(f)
        time_passed = time.time()-current
        result_runtime_py_v3[index].append(time_passed)

    results_runtime_py.append(result_runtime_py)
    results_runtime_py_v2.append(result_runtime_py_v2)
    results_runtime_py_v3.append(result_runtime_py_v3)
    
    nsim_per_n = [len(results_runtime_py[0][j]) for j in range(len(ns))]
    nsim_per_n_cumsum = np.cumsum(nsim_per_n)
    
    #load the Macaulay2 results, which must have been produced beforehand and stored in the folder output
    
    result_runtime_m2 = []
    path = 'output/testfiles_poly_nmin%i_nmax%i_nstep%i_%s_seed%i_layers.txt' % (n_min,n_max,n_step,option,seed)    
    f = open(path,'r')
    textsplit = f.read().splitlines()[1:]
    f.close()
    counter = -1
    for j,line in enumerate(textsplit):
        if j%nsim_per_n_cumsum[counter]==0:
            result_runtime_m2.append([])
            counter+=1
        result_runtime_m2[-1].append(float(line.split('\t')[-1]))

    results_runtime_m2.append(result_runtime_m2)


## CREATE PLOTS

#Plot of the average run time for the two algorithms and the two options, NCFs and any Boolean functions
lss = ['o-','x:']
f,ax = plt.subplots(figsize=(4,3))
colors = ['r','b','g']
labels = ['Algorithm 1','Algorithm 2','Algorithm 2 with\npre-computed values']
option_labels = ['non-canalizing','nested canalizing']
for i in range(len(which_options)):
    mean_values_m2 = [np.mean(results_runtime_m2[0][j]) for j in range(len(ns))]
    mean_values_py = [np.mean(results_runtime_py[0][j]) for j in range(len(ns))]
    ax.semilogy(ns,mean_values_m2,lss[i],color='r',label='Algorithm 1 (Macaulay2)')
    ax.semilogy(ns,mean_values_py,lss[i],color='b',label='Algorithm 2 (Python)')
    if len(which_options)==1:
        max_values_m2 = [np.max(results_runtime_m2[0][j]) for j in range(len(ns))]
        min_values_m2 = [np.min(results_runtime_m2[0][j]) for j in range(len(ns))]    
        max_values_py = [np.max(results_runtime_py[0][j]) for j in range(len(ns))]
        min_values_py = [np.min(results_runtime_py[0][j]) for j in range(len(ns))]    
        for j,n in enumerate(ns):
            ax.semilogy([n,n],[min_values_m2[j],max_values_m2[j]],'_-',color='r')
            ax.semilogy([n,n],[min_values_py[j],max_values_py[j]],'_-',color='b')
            ax.text(n,1,'n='+str(nsim_per_n[j]),va='center',ha='center')
    
    #ax.semilogy(ns[1:-2],np.mean(timer_precomputeds[i],1)[1:-2],lss[i],color='g',label='Algorithm 2 (Python) with\npre-computed values')
ax.set_xlabel('number of variables')
ax.set_ylabel('average run time [seconds]')
ax.set_xticks(ns)
#ax.legend(loc='best',frameon=False)
ax2 = ax.twinx()
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_yticks([])
for i in range(2):
    ax2.add_patch(Rectangle([4,0.93-i*0.1],0.6,0.04,color=colors[i]))
    ax2.text(5,0.93+0.01-i*0.1,labels[i],ha='left',va='center')
y1,y2=ax2.get_ylim()
for i in range(2):
    ax2.plot([10,10],[100,100],lss[i],color='k',label=option_labels[i])
ax2.set_ylim([y1,y2])
ax2.legend(loc='lower right',frameon=False,numpoints=2)
ax.set_ylim([1.1838185699532219e-05,ax.get_ylim()[1]])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig('figures/runtime_all_nmin%i_nmax%i_nstep%i_%s_seed%i.pdf' % (4,16,n_step,option,seed),bbox_inches = "tight")

#Plot of the average run time for the two Python implementations and the two options, NCFs and any Boolean functions
lss = ['o-','x:']
f,ax = plt.subplots(figsize=(4,3))
colors = ['b','g','y']
labels = ['Algorithm 2','Algorithm 2 with\npre-computed values','Algorithm 2 with pre-\ncomputed values (new)']
option_labels = ['non-canalizing','nested canalizing']
for i in range(2):
    #ax.semilogy(ns[1:-2],np.mean(results_runtime_m2[i],1)[1:],lss[i],color='r',label='Algorithm 1 (Macaulay2)')
    ax.semilogy(ns[1:],np.mean(results_runtime_py[i],1)[1:],lss[i],color='b',label='Algorithm 2 (Python)')
    ax.semilogy(ns[1:],np.mean(results_runtime_py_v2[i],1)[1:],lss[i],color='g',label='Algorithm 2 (Python) with\npre-computed values (old)')
    ax.semilogy(ns[1:],np.mean(results_runtime_py_v3[i],1)[1:],lss[i],color='y',label='Algorithm 2 (Python) with\npre-computed values (new)')
ax.set_xlabel('number of variables')
ax.set_ylabel('average run time [seconds]')
ax.set_xticks(ns[1:])
#ax.legend(loc='best',frameon=False)
ax2 = ax.twinx()
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_yticks([])
for i in range(3):
    ax2.add_patch(Rectangle([4,0.93-i*0.13],0.6,0.04,color=colors[i]))
    ax2.text(5,0.93+0.01-i*0.13,labels[i],ha='left',va='center')
y1,y2=ax2.get_ylim()
for i in range(2):
    ax2.plot([10,10],[100,100],lss[i],color='k',label=option_labels[i])
ax2.set_ylim([y1,y2])
ax2.legend(loc='center left',frameon=False,numpoints=2)
ax.set_ylim([1.1838185699532219e-05,14.663561363408045])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig('figures/runtime_all_nmin%i_nmax%i_nstep%i_%s_seed%i_comp.pdf' % (4,16,n_step,option,seed),bbox_inches = "tight")

    