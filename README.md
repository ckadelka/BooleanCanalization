# BooleanCanalization
This repository contains a set of algorithms to compute the canalizing structure of Boolean functions. All algorithms compute the canalizing layer structure for any Boolean function. 

Algorithm 1 is implemented in Macaulay2 (find_layers.m2) and takes as input a Boolean function in polynomial form. 

Algorithm 2 is implemented in Python (find_layers.py) and takes as input a Boolean function as a list of length 2^n. There also exists a fast implementation of Algorithm 2, which makes use of precomputed tables. This fast version is used by default and should be preferred when the canalizing structure of many Boolean functions is computed. Note that the tables are only precomputed for functions with up to 20 variables. If functions with more than 20 variables are to be analyzed, n_max in find_layers.py needs to be adapted. The NP-hard algorithm will be slow (run time increases exponentially fast in the number of variables).

## Testing

To test and compare the run time of the algorithms, we provide two bash scripts:

run_test_alg1_vs_alg2 compares Algorithm 1 with Algorithm 2 (slow implementation without precomputed tables), run_test_alg2_vs_alg2fast compares Algorithm 2 with the fast implementation of Algorithm 2 (with precomputed tables).

Both bash scripts take the following **optional** inputs:

1. n_min=${1:-2}               #n_min = minimal number of variables considered
2. n_max=${2:-16}              #n_max = maximal number of variables considered
3. n_step=${3:-2}              #n_step = step size between consecutive numbers of variables considered
4. nsim=${4:-5}                #nsim = number of random functions generated per considered number of variables
5. seed=${5:-0}                #seed = seed for both the random and numpy.random random number generator
6. EXACT_DEPTH=${6:-0}         #EXACT_DEPTH == True (or 1)  -> k == exact number of canalizing variables;
                            #EXACT_DEPTH == False (or 0) -> k == minimal number of canalizing variables
7. COMPARE_OUTPUT=${7:-0}      #COMPARE_OUTPUT == True -->  each line of output between the two algorithms will be compared
8. CREATE_RUNTIME_PLOT=${8:-1} #CREATE_RUNTIME_PLOT == True -->  a plot comparing the run time will be created

Both bash scripts do the following:

1. Generate test files of $nsim randomly chosen non-canalizing functions and $nsim nested canalizing (e.g., most canalizing) functions, for each number of variables in {n_min,n_min+n_step,...,n_max}
2. Run the algorithms on the test files
3. If COMPARE_OUTPUT is 1 (default == 0), an automatic test is conducted that compares the output of the two algorithms
4. If CREATE_RUNTIME_PLOT is 1 (default), a plot is created that compares the run time between the algorithms and the different number of variables and types of test functions

## Do the following

On the command line, run for example the following two commands to convince yourself that everything works correctly (note: you should not see any error messages)

    bash run_test_alg1_vs_alg2 2 6 1 5 0 0 1 1
    bash run_test_alg2_vs_alg2fast 2 6 1 5 0 0 1 1

Each command compares the output of two algorithm implementations and ensures they are the same. In addition, plots comparing the run time are generated. Note that you can change the seed for the random number generators (fifth optional argument). 
The interesting plots, reported in our paper, can be generated like this (note that the first command takes a couple minutes as Algorithm 1 is slow):

    bash run_test_alg1_vs_alg2 4 16 2 5 0 0 0 1
    bash run_test_alg2_vs_alg2fast 4 20 2 5 0 0 0 1
    
Here, we are no longer checking if both algorithms return the same output as it is a very time consuming process (we did not spend time implementing this efficiently). If you do want to check it, change the seventh optional argument to 1.
