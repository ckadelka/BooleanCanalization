#!/bin/bash

n_min=${1:-2}       #n_min = minimal number of variables considered (default 2)
n_max=${2:-16}      #n_max = maximal number of variables considered (default 16)
n_step=${3:-2}      #n_step = step size between consecutive numbers of variables considered (default 2)
nsim=${4:-5}        #nsim = number of random functions generated per considered number of variables (default 5)
seed=${5:-0}        #seed = seed for both the random and numpy.random random number generator (default 0)
EXACT_DEPTH=${6:-0} #EXACT_DEPTH == True (or 1)  -> k == exact number of canalizing variables;
                    #EXACT_DEPTH == False (or 0) -> k == minimal number of canalizing variables (default)

mkdir -p input
python generate_test_functions_for_evaluation_of_run_time_v2.py $n_min $n_max $n_step $nsim $seed $EXACT_DEPTH NCF
python generate_test_functions_for_evaluation_of_run_time_v2.py $n_min $n_max $n_step $nsim $seed $EXACT_DEPTH kmin0
echo "step 1 completed: test files generated in /input"

mkdir -p output
M2 filename.m2 input/testfiles_poly_nmin2_nmax16_nstep2_NCF_seed0.txt output/layers_nmin2_nmax16_nstep2_NCF_seed0.txt
M2 filename.m2 input/testfiles_poly_nmin2_nmax16_nstep2_kmin0_seed0.txt output/layers_nmin2_nmax16_nstep2_kmin0_seed0.txt
echo "step 2 completed: Algorithm 1 (Macaulay2) output written to /output"

mkdir -p figures
python comparison_run_time.py $n_min $n_max $n_step $nsim $seed $EXACT_DEPTH
echo "step 3 completed: figures comparing the run time generated in /figures"

