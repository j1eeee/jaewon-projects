from NQueens import *
import random
import math

verbose = True

# ==================================================================
# This section contains an implementation of straightforward
# Hill Climbing. It requires a state class that creates objects
# that implement the following methods: getValue, getMaxValue,
# allNeighbors, randomNeighbors, and that are printable

# todo: hillclimb
def hillClimb(startState, maxRounds=1000):
    """performs hill climbing algorithm, given start state and maximum number of rounds and
    return a best state until solution is found or local maxima is reached."""
    curr = startState
    value = startState.getValue()
    maxValue = startState.getMaxValue()
    count = 0 #알고리즘이 몇번 돌았나.
    if verbose:
        print("==============================START==============================")
    while value < maxValue and count < maxRounds:
        if verbose:
            print("--------------------------Count = ", count, "--------------------------")
            print(curr)
        neighs = curr.allNeighbors()
        bestNeigh = findBestNeighbor(neighs)
        nextValue = bestNeigh.getValue()
        if nextValue >= value:
            if verbose:
                print("Best neighbor:")
                print(bestNeigh)
            curr = bestNeigh
            value = nextValue
        else:
            break
        count += 1
    if verbose:
        print("==========================FINAL STATE===========================")
        print(curr)
        print("          Number of steps =", count)
        if value == maxValue:
            print("          Found perfect solution")
    return value, maxValue, count

# todo: findBestNeighbor
def findBestNeighbor(neighbors):
    """Given a list of neighbors, find and return a neighbor with the best value.
    If there are multiple neighbors with same value, a random one is chosen."""
    startBest = neighbors[0]
    bestValue = startBest.getValue()
    bestNeighs = [startBest] #첫번째께 제일 좋을수도 있으니까 일단 첫번째 넣어줌
    for neigh in neighbors:
        value = neigh.getValue()
        if value > bestValue:
            bestNeighs = [neigh]
            bestValue = value
        elif value == bestValue:
            bestNeighs.append(neigh)
    bestNeighs = random.choice(bestNeighs)
    return bestNeighs


# ==================================================================
# This section contains an implementation of stochastic
# Hill Climbing. Similar to the basic hill-climbing, this function
# generates a fixed number of neighbors, not all, and takes the best
# one

# todo: 실습과제
def stochHillClimb(startState, numNeighs = 10, maxRounds = 1000):
    """Not choosing the optimal solution every time rather choosing better solution than
    the current state value. Neighbors, better value than current state, are generated from
    random numbers stochastically of how much they are better"""
    curr = startState
    value = startState.getValue()
    maxValue = startState.getMaxValue()
    count = 0
    if verbose:
        print("==============================START==============================")
    while value < maxValue and count < maxRounds:
        if verbose:
            print("--------------------------Count = ", count, "--------------------------")
            print(curr)
        neighs = curr.randomNeighbors(numNeighs)
        bestNeigh = stochFindBestNeighbor(neighs,value)
        if bestNeigh != False:
            curr = bestNeigh
            value = bestNeigh.getValue()
            if verbose:
                print("Best Neighor: ")
                print(bestNeigh)
        count += 1
    if verbose:
        print("==========================FINAL STATE===========================")
        print(curr)
        print("          Number of steps =", count)
        if value == maxValue:
            print("          Found perfect solution")

    return value, maxValue, count
             
    


def stochFindBestNeighbor(neighbors, currValue):
    """Use roulette wheel selection, which gives different probability to be chosen,
    to find neighbor with better value than current value. 
    If there are no neighbors with the better values, return False"""
    bestNeighs = []
    for neigh in neighbors:
        value = neigh.getValue()
        if currValue <= value:
            bestNeighs.append(neigh)

    if not bestNeighs:
        return False

    deltaValues = [neigh.getValue() - currValue for neigh in bestNeighs]
    bestPos = rouletteSelect(deltaValues)
    return bestNeighs[bestPos]




# ==================================================================
# This section contains an implementation of simulated annealing.  This
# algorithm randomly generates a move from the current state.  If the randomly
# generated move is better than the current one, then it makes that move.  If
# it is worse, then it decides stochastically whether to take the move or not.
# This involves both the difference in value, and also the current temperature.
# The states involved here need to implement the same set of methods as before,
# Plus a makeRandomMove method, that returns a new state one off from the
# previous one."""

# todo: 실습과제
def simAnnealing(startState, initTemp=5.0):
    """Select a random state and move if it has better value than the current state.
    If not, decide whether to move by threshold caculation. This is to avoid the state falling
    into local maxima. Finish when the solution is found or temperature goes below 0"""
    currTemp = initTemp
    currState = startState
    currState.setPrintMode(full=False)
    currValue = currState.getValue()
    maxValue = currState.getMaxValue()
    count = 0

    if verbose:
        print("==============================START==============================")

    while 0 < currTemp and currValue < maxValue:
        if verbose:
            print("-------------------------------------------")
            print("Current Temperature: ", round(currTemp, 2))
        nextState = currState.makeRandomMove()
        nextValue = nextState.getValue()
        difference = nextValue - currValue

        if difference >= 0:         #nextState has better value then move
            currState = nextState
            currValue = nextValue
            if verbose:
                print("Higher State Value: ", currValue)
            
        else:
            threshold = math.exp(difference/currTemp)
            random_value = random.random()
            if random_value <= threshold:
                currState = nextState
                currValue = nextValue
                if verbose:
                    print("Lower State Value: ", currValue)

        currTemp -= 0.1
        count += 1

    if verbose:
        print("==========================FINAL STATE===========================")
        print("Final state = ", currState)
        print("          Number of steps =", count)
        if currValue == maxValue:
            print("          Found perfect solution")
    return currValue, maxValue, count



# ==================================================================
# This section contains an implementation of beam search.  This algorithm
# randomly generates n starting points.  It then generates all the successors
# of each of the n states, and puts them in one pool.  The top n successors
# are kept at each round.

# todo: 실습과제
def beamSearch(nqueenNum, numStates = 10, stopLimit=500):
    """find the best solution by looking at the pre-set number of neighboring state
    Update the best Node list by value and return a best state when optimal state
    found or count is reached at stop Limit"""
    currStates = []
    for i in range (numStates):
        nextState = NQueens(nqueenNum)
        nextState.setPrintMode(full = False)
        currStates.append(nextState)
    maxValue = currStates[0].getMaxValue()
    sortByValue(currStates)
    count = 0
    foundOptimal = False
    if verbose:
        print("==============================START==============================")


    while (not foundOptimal) and count < stopLimit:
        if verbose:
            print("--------------------------Count = ", count, "--------------------------")
        bestNNeighs = []
        for nextState in (currStates):
            neighs = nextState.allNeighbors()
            (bestNNeighs, foundOptimal) = keepBestNNeighbors(bestNNeighs, neighs,
            numStates, maxValue)
            if foundOptimal:
                break
        currStates = bestNNeighs
        if verbose:
            print("Selected neighbors: ")
            print(currStates[0])
        count += 1
        state = currStates[0]
    
    if verbose:
        print("==========================FINAL STATE===========================")
        print(state)
        print("          Number of steps =", count)
        if state.getValue() == maxValue:
            print("          Found perfect solution")
    
    return state.getValue(), maxValue, count



# todo: 실습과제 - docstring 작성
def sortByValue(stateList):
    """sort the list by state values by descending order"""
    stateList.sort(key=lambda neigh: - neigh.getValue())

# todo: 실습과제 - docstring 작성
def keepBestNNeighbors(bestSoFar, neighs, n, maxVal):
    """Gets bestSoFar, neighs, n, maxVal, and when nextneigh has better
    value than current list in neighs, udate the list by inserting the
    nextNeigh and keep the best list"""
    sortByValue(neighs)
    bestNeigh = neighs[0]
    if bestNeigh.getValue() == maxVal:  # if we have found an optimal solution
        return ([bestNeigh], True)
    else:
        i = 0
        while i < len(neighs):
            nextNeigh = neighs[i]
            if len(bestSoFar) == n:
                worstOfBest = bestSoFar[-1]
                if nextNeigh.getValue() < worstOfBest.getValue():
                    break
            insertState(bestSoFar, nextNeigh, n)
            i = i + 1
        return (bestSoFar, False)

# todo: 실습과제 - docstring 작성
def insertState(sortedList, newState, limit):
    """Insert the new state if it is greater than the existed list.
    However, if the size of the list we set before exceeds because of the new list we delete one"""
    i = 0
    for state in sortedList:
        if newState.getValue() > state.getValue():
            break
        i = i + 1
    sortedList.insert(i, newState)
    if len(sortedList) > limit:
        sortedList.pop(-1)


# ==================================================================
# This section contains an implementation of genetic algorithm search. This
# algorithm randomly generates n starting points.  It then chooses n "parents"
# from the population, based on roulette-wheel selection, which is based on
# the value/fitness of each state.  Another way to put this is that it samples
# with replacement from the probability distribution that corresponds to the
# amount of fitness the individual is responsible for. It crosses over parents
# with each other to create a new generation, and then continues.

# todo: geneticAlg
def geneticAlg(nqueenNum, popSize=10, maxGenerations=500, crossPerc=0.6, mutePerc=0.1):
    if popSize % 2 == 1:
        print("Making population size even:")
        popSize += 1
    currStates = []
    for i in range(popSize):
        nextState = NQueens(nqueenNum)
        currStates.append(nextState)
    maxFit = currStates[0].getMaxValue()

    if verbose:
        print("===================== initial state =====================")
        printNeighbors(currStates, False)
        print("=========================================================")
    count = 0
    foundOptimal = False
    overallBest = currStates[0]

    while (not foundOptimal) and count < maxGenerations:
        count += 1  
        if verbose:
            print("generation: ", count)

        fits = [state.getValue() for state in currStates]
        if maxFit in fits:
            pos = fits.index(maxFit)
            bestOne = currStates[pos]
            foundOptimal = True
        else:
            if verbose:
                print("Average fitness:", sum(fits) / len(fits))
                print("max fitness: ", max(fits))
                print("min fitness: ", min(fits))
            bestLoc = fits.index(max(fits))
            bestOne = currStates[bestLoc]
            parentPool = selectParents(currStates, fits)
            currStates = mateParents(parentPool, crossPerc, mutePerc)
            if verbose:
                printNeighbors(currStates, False)
                print("========================================================")
        if bestOne.getValue() > overallBest.getValue():
            overallBest = bestOne
    if verbose:
        print("=========================== GOAL ===========================")
        print("        Last generation best one: ")
        print(bestOne)
        print("        Overall best discovered: ")
        print(overallBest)
        print("        Number of steps =", count)

    return bestOne.getValue(), maxFit, count


def selectParents(states, fitnesses):
    parents = []
    for i in range(len(states)):
        nextParentPos = rouletteSelect(fitnesses)
        parents.append(states[nextParentPos])
    return parents



def mateParents(parents, crossoverPerc, mutationPerc):
    newPop = []
    for i in range(0, len(parents), 2):
        p1 = parents[i]
        p2 = parents[i+1]
        doCross = random.random()
        if doCross < crossoverPerc:
            n1, n2 = p1.crossover(p2)
            newPop.append(n1)
            newPop.append(n2)
        else:
            newPop.append(p1.copyState())
            newPop.append(p2.copyState())
    
    for i in range(len(newPop)):
        nextOne = newPop[i]
        doMutate = random.random()
        if doMutate <= mutationPerc:
            newPop[i] = nextOne.makeRandomMove()
    return newPop


# ========================================================================
# This next section contains utility functions used by more than one of the algorithms


def rouletteSelect(valueList):
    """takes in a list giving the values for a set of entities. It randomly
    selects one of the positions in the list by treating the values as a kind of
    probability distribution and sampling from that distribution. Each entity gets
    a piece of a roulette wheel whose size is based on comparative value: high-value
    entities have the highest probability of being selected, but low-value entities have
    *some* probability of being selected."""
    totalValues = sum(valueList)
    pick = random.random() * totalValues
    s = 0
    for i in range(len(valueList)):
        s += valueList[i]
        if s >= pick:
            return i
    return len(valueList) - 1


def addNewRandomMove(state, stateList):
    """Generates new random moves (moving one queen within her column) until
    it finds one that is not already in the list of boards. If it finds one,
    then it adds it to the list. If it tries 100 times and doesn't find one,
    then it returns without changing the list"""
    nextNeigh = state.makeRandomMove()
    count = 0
    while alreadyIn(nextNeigh, stateList):
        nextNeigh = state.makeRandomMove()
        count += 1
        if count > 100:
            # if tried 100 times and no valid new neighbor, give up!
            return
    stateList.append(nextNeigh)


def alreadyIn(state, stateList):
    """Takes a state and a list of state, and determines whether the state
    already appears in the list of states"""
    for s in stateList:
        if state == s:
            return True
    return False


def printNeighbors(neighList, full = True):
    """Takes a list of neighbors and values, and prints them all out"""
    print("Neighbors:")
    for neigh in neighList:
        neigh.setPrintMode(full)
        print(neigh)
