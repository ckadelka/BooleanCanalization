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

def bool_to_poly(f,x=[]):
    len_f = len(f)
    n=int(np.log2(len_f))
    if x==[]: #to reduce run time, this should be calculated once and then passed as argument
        x = list(itertools.product([0, 1], repeat = n))
    num_values = 2**n   
    text = []
    for i in range(num_values):
        if f[i]==True:
            monomial = '*'.join([('x%i' % (j+1)) if entry==1 else ('(1-x%i)' % (j+1)) for j,entry in enumerate(x[i])])
            text.append(monomial)
    if text!=[]:
        return ' + '.join(text)
    else:
        return '0'

def is_degenerated(F):
    len_F = len(F)
    n=int(np.log2(len_F))
    for i in range(n):
        dummy_add=(2**(n-1-i))
        dummy=np.arange(2**n)%(2**(n-i))//dummy_add
        depends_on_i=False
        for j in range(2**n):
            if dummy[j]==1:
                continue
            else:
                if F[j]!=F[j+dummy_add]:
                    depends_on_i=True
                    break
        if depends_on_i==False:
            return True
    return False

def is_canalizing(F,n):
    if type(F) == list:
        F = np.array(F)
    desired_value = 2**(n-1)
    T = np.array(list(itertools.product([0, 1], repeat=n))).T
    A = np.r_[T,1-T]
    AtimesF = np.dot(A,F)
    if np.any(AtimesF==desired_value):
        return True
    elif np.any(AtimesF==0):
        return True
    else:
        return False

def random_non_degenerated_function(n):
    while True: #works because most functions are non-degenerated
        F = np.random.randint(2, size = 2**n) 
        if not is_degenerated(F):
            return F

def random_degenerated_function(n):
    while True: #works because most functions are non-degenerated
        F = np.random.randint(2, size = 2**n) 
        if is_degenerated(F):
            return F

def random_non_canalizing_function(n):
    assert n>1
    while True: #works because most functions are non-canalizing
        F = np.random.randint(2, size = 2**n) 
        if not is_canalizing(F,n):
            return F

def random_non_canalizing_non_degenerated_function(n):
    assert n>1
    while True: #works because most functions are non-canalizing and non-degenerated
        F = np.random.randint(2, size = 2**n) 
        if not is_canalizing(F,n) and not is_degenerated(F):
            return F

def random_k_canalizing(n, k, EXACT_DEPTH_K=False, x=[]):
    try:
        assert (n-k!=1 or EXACT_DEPTH_K==False)
    except AssertionError:
        print('There are no functions of exact canalizing depth n-1.\nEither set EXACT_DEPTH_K=False or ensure k!=n-1')
        return
    try:
        assert 0<=k and k<=n
    except AssertionError:
        print('Error:\nEnsure 0 <= k <= n.')
        return
    if x==[]: #to reduce run time, this should be calculated once and then passed as argument
        x = list(itertools.product([0, 1], repeat = n))
    num_values = 2**n
    aas = np.random.randint(2, size = k)  # inputs
    bbs = np.random.randint(2, size = k)  # outputs
    can_vars = np.random.choice(n, k, replace = False)
    F = np.zeros(num_values, dtype = int)
    
    if k<n:
        if EXACT_DEPTH_K:
            core_polynomial = random_non_canalizing_non_degenerated_function(n-k)
        else:
            core_polynomial = random_non_degenerated_function(n-k)    
    else:
        core_polynomial = [1-bbs[-1]]
        
    counter_non_canalized_positions = 0
    
    for i in range(num_values):
        for j in range(k):
            if x[i][can_vars[j]] == aas[j]:
                F[i] = bbs[j]
                break
        else:
            F[i] = core_polynomial[counter_non_canalized_positions]
            counter_non_canalized_positions += 1
    return F


#main parameters
n_min = 2
n_max = 20
n_step = 2
nsim = 5
option = 'NCF'
#option = 'kmin0'

#further parameters
seed = 0
EXACT_DEPTH_K = False

if seed==None:
    seed = np.random.randint(1,2**32 - 1)
random.seed(seed)
np.random.seed(seed)

file1 = open('testfiles_table_nmin%i_nmax%i_nstep%i_%s_seed%i_v3.txt' % (n_min,n_max,n_step,option,seed),'w')
file2 = open('testfiles_poly_nmin%i_nmax%i_nstep%i_%s_seed%i_v3.txt' % (n_min,n_max,n_step,option,seed),'w')

counter = 0
for n in range(n_min,n_max+1,n_step):
    bool_list_dummy = list(itertools.product([0, 1], repeat = n))
    for _ in range(nsim):
        #generate a random Boolean function with n inputs and canalizing depth >= k or == k if EXACT_DEPTH==True
        f = random_k_canalizing(n, int(option[-1]) if option.startswith('kmin') else (n if option=='NCF' else 0), EXACT_DEPTH_K=False, x=bool_list_dummy)
        f_poly = bool_to_poly(f)
        file1.write(str(counter)+'\t'+str(n)+'\t'+','.join(list(map(str,f)))+'\n')
        file2.write(str(counter)+'\t'+str(n)+'\t'+f_poly+'\n')
        counter+=1       
file1.close()
file2.close()
