from localSearch import *
import time

# todo:
def testRandomStarts(alg, reps, sizeList):
    """Run this on hillClimb, stochHillClimb, and simAnnealing only.
    Takes in a function name for one of the local search functions.
    It also has optional inputs for a number of repetitions and list
    of sizes to test. It runs reps tests for each size, and prints the results."""
    allResult = {}
    for size in sizeList:
        print("testing size", size)
        allResult[size] = []
        for rep in range(reps):
            print(".")
            startState = NQueens(size)
            startTime = time.time()
            result = alg(startState)
            endTime = time.time()
            result = list(result)
            result.append(endTime - startTime)
            allResult[size].append(result)
    print("=======================================")
    print("Running Tests on", alg)
    for size in sizeList:
        print("------------------")
        print("Size=", size)
        runs = allResult[size]
        for i in range(len(runs)):
            [lastVal, maxVal, count, deltaTime] = runs[i] 
            print("Run", i+1, ": quality = ", lastVal, "out of", maxVal, "count =", count,
                  "time = {: .5f}".format(deltaTime))
    print("===========================================")



# todo:
def testVaryingPops(alg, popSize, reps, sizeList):
    """Run this on beam search and GA only. Takes in a function name for one
    of the local search functions, and a population size. It
    also has an optional input a number of repetitions. This runs the given
    algorithm with the specified population size. Does
    run reps tests and prints the results."""
    allResult = {}
    for size in sizeList:
        print("testing size", size)
        allResult[size] = []
        for rep in range(reps):
            print(".")
            # startState = NQueens(size)
            startTime = time.time()
            result = alg(size, popSize)
            endTime = time.time()
            result = list(result)
            result.append(endTime - startTime)
            allResult[size].append(result)
    print("=======================================")
    print("Running Tests on", alg)
    for size in sizeList:
        print("------------------")
        print("Size=", size)
        runs = allResult[size]
        for i in range(len(runs)):
            [lastVal, maxVal, count, deltaTime] = runs[i] 
            print("Run", i+1, ": quality = ", lastVal, "out of", maxVal, "count =", count,
                  "time = {: .5f}".format(deltaTime))