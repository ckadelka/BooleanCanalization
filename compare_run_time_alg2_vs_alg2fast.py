#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 4 15:40:49 2022

@author: ckadelka
"""

import numpy as np
import matplotlib.pyplot as plt
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
results_runtime1=[]
results_runtime2=[]

which_options = ['kmin0','NCF']
for option in which_options:
    file1 = open('output/testfiles_table_nmin%i_nmax%i_nstep%i_%s_seed%i_layers_py.txt' % (n_min,n_max,n_step,option,seed),'r')
    lines1 = file1.read().splitlines()[1:]
    file1.close()

    file2 = open('output/testfiles_table_nmin%i_nmax%i_nstep%i_%s_seed%i_layers_py_fast.txt' % (n_min,n_max,n_step,option,seed),'r')
    lines2 = file2.read().splitlines()[1:]
    file2.close()
    
    #load the results, which must have been produced beforehand and stored in the folder output
    
    result_runtime1 = []
    for j,line in enumerate(lines1):
        if j%nsim==0:
            result_runtime1.append([])
        result_runtime1[-1].append(float(line.split('\t')[-1]))
    results_runtime1.append(result_runtime1)

    result_runtime2 = []
    for j,line in enumerate(lines2):
        if j%nsim==0:
            result_runtime2.append([])
        result_runtime2[-1].append(float(line.split('\t')[-1]))
    results_runtime2.append(result_runtime2)

ns = np.arange(n_min,n_max+1e-4,n_step)


#Plot of the average run time for the two algorithms and the two options, NCFs and any Boolean functions
lss = ['o-','x:']
f,ax = plt.subplots(figsize=(4,3))
colors = ['b','g']
labels = ['Algorithm 2','Algorithm 2 (fast)']
option_labels = ['non-canalizing','nested canalizing']
for i in range(len(which_options)):
    mean_values1 = [np.mean(results_runtime1[i][j]) for j in range(len(ns))]
    mean_values2 = [np.mean(results_runtime2[i][j]) for j in range(len(ns))]
    ax.semilogy(ns,mean_values1,lss[i],color=colors[0])
    ax.semilogy(ns,mean_values2,lss[i],color=colors[1])
    # if len(which_options)<=2:
    #     max_values1 = [np.max(results_runtime1[i][j]) for j in range(len(ns))]
    #     min_values1 = [np.min(results_runtime1[i][j]) for j in range(len(ns))]    
    #     max_values2 = [np.max(results_runtime2[i][j]) for j in range(len(ns))]
    #     min_values2 = [np.min(results_runtime2[i][j]) for j in range(len(ns))]    
    #     for j,n in enumerate(ns):
    #         ax.semilogy([n,n],[min_values1[j],max_values1[j]],lss[i],color='r',marker=None)
    #         ax.semilogy([n,n],[min_values2[j],max_values2[j]],lss[i],color='b',marker=None)
ax.set_xlabel('number of variables')
ax.set_ylabel('average run time [seconds]')
ax.set_xticks(ns)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax2 = ax.twinx()
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_yticks([])
[x1,x2] = ax.get_xlim()
for i in range(2):
    ax2.add_patch(Rectangle([x2,0.93-i*0.1],0.1*(x2-x1),0.04,color=colors[i],clip_on=False))
    ax2.text(x2+0.13*(x2-x1),0.93+0.01-i*0.1,labels[i],ha='left',va='center')
y1,y2=ax2.get_ylim()
for i in range(2):
    ax2.plot([(x1+x2)/2,(x1+x2)/2],[100,100],lss[i],color='k',label=option_labels[i])
ax2.set_ylim([y1,y2])
ax2.legend(frameon=False,numpoints=2,loc='upper left', bbox_to_anchor=(0.85,0.3))
#ax.set_ylim([1.1838185699532219e-05,ax.get_ylim()[1]])

plt.savefig('figures/comparison_runtime_alg2_vs_alg2fast_nmin%i_nmax%i_nstep%i_seed%i.pdf' % (n_min,n_max,n_step,seed),bbox_inches = "tight")

    