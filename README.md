# BooleanCanalization
This repository contains a set of algorithms to compute the canalizing structure of Boolean functions.

Algorithm 1 is implemented in Macaulay2 (find_layers.m2) and takes as input a Boolean function in polynomial form. Algorithm 2 is implemented in Python (find_layers.py) and takes as input a Boolean function as a list of length 2^n. Both algorithms compute the canalizing layer structure for any Boolean function. 

To test the run time of each algorithm, execute in the following order:

1. python generate_test_functions_for_evaluation_of_run_time.py - test functions will be generated in the folder testfiles
2. m2 evaluate_test_functions.m2
3. python comparison_run_time.py

This will create a set of plots that compare the run time of each algorithm for various numbers of inputs (default n=2,4,6,...,16) and various types of functions (any Boolean function and NCFs).
