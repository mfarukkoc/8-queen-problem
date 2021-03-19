# 8-queen-problem

The eight queens puzzle is the problem of placing eight chess queens on an 8×8 chessboard so that no two queens threaten each other; thus, a solution requires that no two queens share the same row, column, or diagonal.

This repository is an implementation of hill climbing algorithms for 8 queen problem using python.  
Steepest hill climb, random-restart hill climb and stochastic hill climb variations are implemented.

## Hill Climbing

Hill climbing search algorithm is a local search algorithm, that starts with a initial state and attempts to find a better state in terms of heuristics value of the problem. If it founds a better state then, better state becomes the initial state and so on until there is no better state. The main problem is it can stuck in local maxima and can not find the solution of problem since algorithm can not make decreasing step. There are several variations of algorithm to increase the probability of finding solution.
