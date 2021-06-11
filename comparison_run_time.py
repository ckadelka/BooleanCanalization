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

#main parameters
n_min = 2
n_max = 20
n_step = 2
nsim = 5


#further parameters
seed = 0
timers=[]
timer_precomputeds=[]
timer_macaulay2s=[]

for option in ['kmin0','NCF']:
    file1 = open('testfiles_table_nmin%i_nmax%i_nstep%i_%s_seed%i_v3.txt' % (n_min,n_max,n_step,option,seed),'r')
    lines = file1.read().splitlines()
    file1.close()
    
    res = [[] for i in range(n_min,n_max+1,n_step)]
    timer = [[] for i in range(n_min,n_max+1,n_step)]
    timer_precomputed = [[] for i in range(n_min,n_max+1,n_step)]
    ns=list(range(n_min,n_max+1,n_step))
    for line in lines:
        linesplit = line.split('\t')
        index = ns.index(int(linesplit[1]))
        f = list(map(int,linesplit[2].split(',')))
        current=time.time()
        dummy = find_layers.find_layers(f)
        time_passed = time.time()-current
        timer[index].append(time_passed)    
        res[index].append(dummy)
    
        current=time.time()
        dummy = find_layers.find_layers_with_precomputed_tables(f)
        time_passed = time.time()-current
        timer_precomputed[index].append(time_passed)
    
    folder = 'Macaulay2_results/'
    if option == 'kmin0':
        files = ['polys-layers-kmin0-%i_%i.txt' % (10*i+1,10*(i+1)) for i in range(4)]
    if option == 'NCF':
        files = ['polys-layers-NCF-%i_%i.txt' % (10*i+1,10*(i+1)) for i in range(4)]
    
    timer_macaulay2 = []
    
    for i,fname in enumerate(files):
        f = open(folder+fname,'r')
        textsplit = f.read().splitlines()[1:]
        f.close()
            
        for j,line in enumerate(textsplit):
            if j%nsim==0:
                timer_macaulay2.append([])
            timer_macaulay2[-1].append(float(line.split('\t')[-1]))
    
    timers.append(timer)
    timer_precomputeds.append(timer_precomputed)
    timer_macaulay2s.append(timer_macaulay2)


lss = ['o-','x:']
f,ax = plt.subplots(figsize=(4,3))
colors = ['r','b','g']
labels = ['Algorithm 1','Algorithm 2','Algorithm 2 with\npre-computed values']
option_labels = ['non-canalizing','nested canalizing']
for i in range(2):
    ax.semilogy(ns[1:-2],np.mean(timer_macaulay2s[i],1)[1:],lss[i],color='r',label='Algorithm 1 (Macaulay2)')
    ax.semilogy(ns[1:-2],np.mean(timers[i],1)[1:-2],lss[i],color='b',label='Algorithm 2 (Python)')
    #ax.semilogy(ns[1:-2],np.mean(timer_precomputeds[i],1)[1:-2],lss[i],color='g',label='Algorithm 2 (Python) with\npre-computed values')
ax.set_xlabel('number of variables')
ax.set_ylabel('average run time [seconds]')
ax.set_xticks(ns[1:-2])
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
plt.savefig('runtime_all_nmin%i_nmax%i_nstep%i_%s_seed%i_v3.pdf' % (4,16,n_step,option,seed),bbox_inches = "tight")

lss = ['o-','x:']
f,ax = plt.subplots(figsize=(4,3))
colors = ['b','g']
labels = ['Algorithm 2','Algorithm 2 with\npre-computed values']
option_labels = ['non-canalizing','nested canalizing']
for i in range(2):
    #ax.semilogy(ns[1:-2],np.mean(timer_macaulay2s[i],1)[1:],lss[i],color='r',label='Algorithm 1 (Macaulay2)')
    ax.semilogy(ns[1:-2],np.mean(timers[i],1)[1:-2],lss[i],color='b',label='Algorithm 2 (Python)')
    ax.semilogy(ns[1:-2],np.mean(timer_precomputeds[i],1)[1:-2],lss[i],color='g',label='Algorithm 2 (Python) with\npre-computed values')
ax.set_xlabel('number of variables')
ax.set_ylabel('average run time [seconds]')
ax.set_xticks(ns[1:-2])
#ax.legend(loc='best',frameon=False)
ax2 = ax.twinx()
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_yticks([])
for i in range(2):
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
plt.savefig('runtime_all_nmin%i_nmax%i_nstep%i_%s_seed%i_v3_comp.pdf' % (4,16,n_step,option,seed),bbox_inches = "tight")

    