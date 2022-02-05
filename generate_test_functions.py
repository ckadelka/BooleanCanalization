#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 15:57:39 2021

@author: ckadelka


The Macaulay2 implementation of find_layers takes as input a Boolean function in polynomial format.

The Python implementation of find_layers takes as input a Boolean function in vector format (right-hand side of a truth table).

This program generates a set of test files to ensure that both algorithms yield the same output
and to compare the run time between the algorithms and as the number of variables increases.
"""

import numpy as np
import itertools
import random
import sys

if len(sys.argv)>1:
    n_min = int(sys.argv[1])
else:
    n_min = 2

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
    
if len(sys.argv)>7:
    option = str(sys.argv[7])
else:
    option = 'NCF'
    
if len(sys.argv)>8:
    ONLY_CREATE_TABLES = str(sys.argv[8])
else:
    ONLY_CREATE_TABLES = False

def is_degenerated(F): 
    ''''Checks if a Boolean function contains non-essential variables (i.e., variables that have no influence on the output, ever)
    Inputs: 
        1. F = a binary vector of length 2**n (the right-hand side of a Boolean truth table),
    Output:
        True if the function is degenrated (i.e., contains non-essential variables), False otherwise.'''
    len_F = len(F)
    n=int(np.log2(len_F)) #compute number of variables
    for i in range(n):
        dummy_add=(2**(n-1-i))
        dummy=np.arange(2**n)%(2**(n-i))//dummy_add
        depends_on_i=False
        for j in range(2**n):
            if dummy[j]==1:
                continue
            else:
                if F[j]!=F[j+dummy_add]: #check if F differs when all variables but variable i are kept constant
                    depends_on_i=True #if this is the case, F depends on variable i and i is an essential variable
                    break
        if depends_on_i==False: #if we find one non-essential variable, we can stop 
            return True
    return False

def is_canalizing(F,n=-1): #checks if a Boolean function is canalizing (i.e., has at least one canalizing variable)
    ''''Checks if a Boolean function is canalizing (i.e., has at least one canalizing variable)
    Inputs: 
        1. F = a binary vector of length 2**n (the right-hand side of a Boolean truth table),
        2. n (optional) = the number of variables of the function, i.e. np.log2(len(F))
    Output:
        True if the function is canalizing, False otherwise.'''
    if n==-1:
        n = np.log2(len(F)) #compute number of variables
    if type(F) == list:
        F = np.array(F)
    desired_value = 2**(n-1)
    T = np.array(list(itertools.product([0, 1], repeat=n))).T #left-hand side of a truth table
    A = np.r_[T,1-T] #truth table and the negated truth table
    AtimesF = np.dot(A,F) #If there exists a column a in A such that F==1 or F==0 for all entries where a==1, then F is canalizing 
    if np.any(AtimesF==desired_value): #check if there is any canalizing variable with canalized output 1
        return True
    elif np.any(AtimesF==0): #check if there is any canalizing variable with canalized output 0
        return True
    else: #there is no canalizing variables
        return False

def random_non_degenerated_function(n):
    ''''Generates uniformly at random a Boolean function on n variables, which are all essential
    Input: 
        n = number of variables
    Output:
        Boolean function as a numpy.array of length 2**n'''    
    while True: #works because most functions for higher n are non-degenerated
        F = np.random.randint(2, size = 2**n) 
        if not is_degenerated(F):
            return F

def random_degenerated_function(n):
    ''''Generates uniformly at random a Boolean function on n variables, where at least one variable is not essential
    Input: 
        n = number of variables
    Output:
        Boolean function as a numpy.array of length 2**n''' 
    while True: #works because most functions are non-degenerated
        F = np.random.randint(2, size = 2**n) 
        if is_degenerated(F):
            return F

def random_non_canalizing_function(n):
    ''''Generates uniformly at random a Boolean function on n variables, which are all not canalizing
    Input: 
        n = number of variables
    Output:
        Boolean function as a numpy.array of length 2**n''' 
    assert n>1
    while True: #works because most functions are non-canalizing
        F = np.random.randint(2, size = 2**n) 
        if not is_canalizing(F,n):
            return F

def random_non_canalizing_non_degenerated_function(n):
    ''''Generates uniformly at random a Boolean function on n variables, which are all essential but not canalizing
    Input: 
        n = number of variables
    Output:
        Boolean function as a numpy.array of length 2**n''' 
    assert n>1
    while True: #works because most functions are non-canalizing and non-degenerated
        F = np.random.randint(2, size = 2**n) 
        if not is_canalizing(F,n) and not is_degenerated(F):
            return F

def random_k_canalizing(n, k, EXACT_DEPTH_K=False, x=[]):
    ''''Generates uniformly at random a Boolean function on n essential variables, of which (at least) k are canalizing 
    Input: 
        n = number of variables
        k = number of canalizing variables ( 0<= k <= n )
        EXACT_DEPTH_K (optional):
            if True, k == exact number of canalizing variables,
            if False, k == minimal number of canalizing variables (default)
        2. x (optional to improve run time) = a matrix of size 2**n x n, the left-hand side of a Boolean truth table        
    Output:
        Boolean function as a numpy.array of length 2**n''' 
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
        x = list(itertools.product([0, 1], repeat = n)) #left-hand side of a Boolean truth table, size 2**n x n
    num_values = 2**n
    canalizing_inputs = np.random.randint(2, size = k)  # randomly determine the k canalizing input values
    canalized_outputs = np.random.randint(2, size = k)  # randomly determine the k canalized output values
    canalizing_variables = np.random.choice(n, k, replace = False)  # randomly determine the first k canalizing variables (and their order)
    F = np.zeros(num_values, dtype = int)
    
    if k<n: #if not all variables are canalizing, randomly determine the core polynomial, 
            #i.e. the subfunction to be evaluated if all canalizing variables receive their non-canalizing input 
        if EXACT_DEPTH_K: #k == exact number of canalizing variables -> core polynomial may not be canalizing
            core_polynomial = random_non_canalizing_non_degenerated_function(n-k)
        else: #k == minimal number of canalizing variables -> core polynomial is allowed to be canalizing
            core_polynomial = random_non_degenerated_function(n-k)    
    else: #if all variables are canalizing (i.e., F is an NCF), then the core polynomial is simply 1 - last canalized output value (to ensure the last canalizing variable is actually essential)
        core_polynomial = [1-canalized_outputs[-1]]
        
    #build the canalizing Boolean function F based on the generated vectors
    counter_non_canalized_positions = 0
    for i in range(num_values):
        for j in range(k):
            if x[i][canalizing_variables[j]] == canalizing_inputs[j]: #if a canalizing variables receives its canalizing input, set the function value to the corresponding canalizing output value
                F[i] = canalized_outputs[j]
                break
        else: #if none of the canalizing variables receives their canalizing input values, set the function value to the ``next" value in the core polynomial
            F[i] = core_polynomial[counter_non_canalized_positions]
            counter_non_canalized_positions += 1
    return F

def bool_to_poly(f,x=[]):
    ''''Transforms a Boolean function from vector form to polynomial format
    Inputs: 
        1. F = a binary vector of length 2**n (the right-hand side of a Boolean truth table),
        2. x (optional to improve run time) = a matrix of size 2**n x n, the left-hand side of a Boolean truth table
    Output:
        A string describing the Boolean function as a polynomial in the variables x1, ..., xn. 
        Note: This polynomial is not reduced/simplified in any way.'''
    len_f = len(f)
    n=int(np.log2(len_f)) #compute number of variables
    if x==[]: #to reduce run time, this should be calculated once and then passed as argument
        x = list(itertools.product([0, 1], repeat = n)) #left-hand side of a Boolean truth table, size 2**n x n
    num_values = 2**n
    text = []
    for i in range(num_values): #iterate through each line of the truth table 
        if f[i]==True: #for those lines where f==1, transform the left-hand side into a polynomial and add to the list text
            monomial = '*'.join([('x%i' % (j+1)) if entry==1 else ('(1-x%i)' % (j+1)) for j,entry in enumerate(x[i])])
            text.append(monomial)
    if text!=[]:
        return ' + '.join(text) #return a polynomial in disjunctive normal form as a string (note: this polynomial is not reduced)
    else:
        return '0'

def generate_testfiles(n_min=2,n_max=16,n_step=2,nsim=5,option='kmin0',EXACT_DEPTH_K=False,seed=0,ONLY_CREATE_TABLES=False):
    ''''Generates two files that contain a list of randomly generated Boolean functions in (a) vector form and in (b) polynomial format
    Inputs: 
        1. n_min = minimal number of variables considered
        2. n_max = maximal number of variables considered
        3. n_step = step size between consecutive numbers of variables considered
        4. nsim = number of random functions generated per considered number of variables (n)
        5. option restricts the space of considered Boolean functions, allowed options:
            'kmin[%i]' = onsider only functions with at least %i canalizing variables, 
            'NCF' = consider only nested canalizing functions (NCFs with k==n)
        6. EXACT_DEPTH_K == True -> k == exact number of canalizing variables;
           EXACT_DEPTH_K == False -> k == minimal number of canalizing variables
        7. seed = seed for both the random and numpy.random random number generator
    Output:
        A string describing the Boolean function as a polynomial in the variables x1, ..., xn. 
        Note: This polynomial is not reduced/simplified in any way.'''    

    #initialize the random number generators
    if seed==None:
        seed = np.random.randint(1,2**32 - 1)
    random.seed(seed)
    np.random.seed(seed)
    
    #open two files, one for the functions stores as vectors (input to Python Algorithm 2), and one for the functions stored as polynomial (input to Algorithm 1 - Macaulay2)
    file1 = open('input/testfiles_table_nmin%i_nmax%i_nstep%i_%s_seed%i.txt' % (n_min,n_max,n_step,option,seed),'w')
    if not ONLY_CREATE_TABLES:
        file2 = open('input/testfiles_poly_nmin%i_nmax%i_nstep%i_%s_seed%i.txt' % (n_min,n_max,n_step,option,seed),'w')
    
    counter = 0
    for n in range(n_min,n_max+1,n_step):
        bool_list_dummy = list(itertools.product([0, 1], repeat = n))
        for _ in range(nsim):
            #generate a random Boolean function with n inputs and canalizing depth >= k or == k if EXACT_DEPTH==True
            f = random_k_canalizing(n, int(option[4:]) if option.startswith('kmin') else (n if option=='NCF' else 0), EXACT_DEPTH_K=False, x=bool_list_dummy)
            
            #transform the Boolean function to polynomial format
            f_poly = bool_to_poly(f) 
            
            #write to file
            file1.write(str(counter)+'\t'+str(n)+'\t'+','.join(list(map(str,f)))+'\n')
            if not ONLY_CREATE_TABLES:
                file2.write(str(counter)+'\t'+str(n)+'\t'+f_poly+'\n')
            counter+=1       
    file1.close()
    if not ONLY_CREATE_TABLES:
        file2.close()
    
if __name__ == '__main__':
    #generate testfiles
    generate_testfiles(n_min=n_min,n_max=n_max,n_step=n_step,nsim=nsim,option=option,EXACT_DEPTH_K=EXACT_DEPTH_K,seed=seed,ONLY_CREATE_TABLES=ONLY_CREATE_TABLES)
