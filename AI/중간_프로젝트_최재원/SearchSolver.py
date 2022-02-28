"""  =================================================================
File: SearchSolver.py

This file contains generic definitions for a state space SearchState class,
and a general SearchSolver class.  These classes should be subclassed to make
solvers for a specific problem.
 ==================================================================="""


from Queue import Queue, PriorityQueue
from Stack import Stack

# Change this to true to see information about the search as it goes.
verbose = False


class SearchState(object):
    """
    This is, essentially an abstract class for a search state.  It contains only a path, the sequence of moves in
    the state space from the starting point to this state, and the cost of the state.  The meaning of the cost and
    its value are meant to be computed external to this state.  This is just a container for qData.
    Note that this asks the subclasses to implement the comparison operators. This is important, as the search
    algorithms use == and possibly <, <=, etc. to compare the qData when searching for an item in a stack, queue, or
    priority queue. These should compare the qData associated with a state, and not the cost/priority!
    Also, the state must implement the __hash__ method, so that states can be stored in sets or dictionaries, in such
    a way that states that are == always produce the same hash value.
    """

    def __init__(self, path=None, cost=None):
        """Initialize the two basic instance variables to some value"""
        if path is None:
            self.pathToMe = []
        else:
            self.pathToMe = path
        self.myCost = cost

    def getPath(self):
        """Access the value of the pathToMe instance variable"""
        return self.pathToMe

    def getCost(self):
        """Access the value of the myCost instance variable"""
        return self.myCost

    # The comparison operators are defined by these methods. Note that if not specified, __neq__ returns the opposite
    # of what __eq__ returns

    def __eq__(self, state):
        """Determine whether the input state is equal to this one.
        Subclass should override this!"""
        print("Need to implement equals")
        return False

    def __lt__(self, state):
        """Determine whether this state comes before the other state.
        Subclass should override this!"""
        print("SearchState: Need to implement less-than!")
        return False

    def __le__(self, state):
        """Determine whether this state is less than or equal to the input state.
        Subclass should override this!"""
        print("SearchState: Need to implement less-than or equal to!")
        return False

    def __gt__(self, state):
        """Determine whether this state comes before the other state.
        Subclass should override this!"""
        print("SearchState: Need to implement greater-than!")
        return False

    def __ge__(self, state):
        """Determine whether this state is less than or equal to the input state.
        Subclass should override this!"""
        print("SearchState: Need to implement greater-than or equal to!")
        return False

    def __hash__(self):
        """Makes states hashable, so that they can be stored in sets or dictionary"""
        print("SearchState: Need to implement __hash__!")
        return hash(False)

    def __str__(self):
        """Make a string representation of this state, for printing"""
        return str(self.pathToMe) + '  ' + str(self.myCost)



class AbstractTaskAdvisor(object):
    """This object will hold the information about the actual task the state space searchers need, including
    knowing information about start state and goal state, knowing how to check if a state is a goal, generating
    the neighbors of a given state, and their associated costs. """

    def __init__(self):
        """Would set up start and goal and other information..."""
        # print("AbstractTaskAdvisor: Subclass must implement __init__!")
        self.startState = None


    def isGoal(self, state):
        """Given a state, determines if the state is the goal state or not."""
        print("AbstractTaskAdvisor: Subclass must implement isGoal")
        return False

    def getStartState(self):
        """Returns the start state, in the proper form to be used by the search."""
        return self.startState

    def generateNeighbors(self, state):
        """Takes in a state and builds a list of states, the viable neighbors of the current state. It
        returns the list. Does not check for which neighbors have been visited in the state space search, just
        which are possible states."""
        print("AbstractTaskAdvisor: Subclass should implement generateNeighbors")
        return []





class AbstractSearchSolver(object):
    """This is an abstract class that implements a search-based solver. It can be used to implement both uninformed search
    methods like BFS and DFS, or heuristic-based search methods like UCS and A*. These algorithms share a common structure:
    1. A section that initializes the search, checks if the search is unnecessary, and sets up fringe and visited sets.
    2. A loop that continues until the fringe set becomes empty or the goal is found
    3. Inside the loop, code that processes a single selected state from the fringe set, updating the fringe with neighbors.
    This class separates those three parts of the algorithm into three separate methods: initSearch, searchLoop, and searchStep.
    These allow us to do a step-by-step look at the loop part of the algorithm, rather than running from start to finish
    with one call.

    This class contains stubs for the helper methods that those algorithms need.  The initSearch and searchStep methods
    should be overridden by subclasses for specific kinds of search, and the isGoal and generateNeighbors methods
    should be overridden by subclasses that know the details of the problem we are searching about.
    These algorithms assume that the qData stored in the states implement the equality operators properly!"""

    def __init__(self, taskAdvisor):
        """This takes in a "task advisor" and sets up the qData needed for the search, the fringe and visited sets, and the counts of
        how many nodes were created and visited.
        The only generic qData are instance variables that count the number of nodes created and the number of
        nodes visited (that corresponds more or less to the number of nodes added to the queue and the number of nodes
        removed from the queue (and not found to be redundant)).  In addition, there are instance variables for the
        search queues for both BFS and PQSearch, so that we can step through the algorithms rather than just running
        them all at once"""
        self.taskAdvisor = taskAdvisor
        self._initializeCounts()
        self.fringe = None
        self.visited = None

    def _initializeCounts(self):
        """A private helper to initialize the counts, since they need to be initialized anew each time the
        search algorithms are called"""
        self.nodesCreated = 0
        self.nodesVisited = 0

    def getNodesCreated(self):
        """Returns the value of self.nodesCreated"""
        return self.nodesCreated

    def getNodesVisited(self):
        """Returns the value of self.nodesVisited"""
        return self.nodesVisited


    def initSearch(self):
        """This method sets up a priority-queue-based search process, initializing the fringe queue, the set of
        visited states, and adding the start state to the fringe queue."""
        self._initializeCounts()
        startState = self.taskAdvisor.getStartState()
        if self.taskAdvisor.isGoal(startState):
            return startState.getPath()
        self.visited = set()
        self._setupFringe(startState)
        self.nodesCreated += 1


    def _setupFringe(self, startState):
        """This method sets up the proper kind of fringe set for this particular search.
        This method should be overridden by the subclass!"""
        print("AbstractSearchSolver: Subclass should implement _setupFringe")
        self.fringe = [startState]


    def searchLoop(self):
        """This method runs the search, repeatedly calling for the next step until either
        the search fails and False is returned, or the search completes"""
        while True:
            (nextState, neighbors, isDone) = self.searchStep()
            if nextState == "Fail":
                return False
            elif isDone == "Done":
                # is search is done then nextState actually holds the result
                return nextState
            # Otherwise just do another step of the search


    def searchStep(self):
        """This method performs one step of a state-space search.
        This must be overridden by the subclass! It should
        return a tuple consisting of: the current state, the neighbors of the current state, and a status
        message.  The message is either "Done", "Fail", or "Step" for a normal step."""
        print("AbstractSearchSolver: Subclass should implement searchStep")
        return (False, False, "Fail")


    def _hasBeenVisited(self, state):
        """Given a state, it looks through the visited set and seeks a node
        that is "equal" to the input state. It is up to the subclass to
        define what it means for them to be equal. It returns the matching
        state, if any, or False if none"""
        for s in self.visited:
            if s == state:
                return s
        return False

    def _hasBeenFringed(self, state):
        """Given a state, it looks through the fringe set and seeks a node that is "equal" to the
        input state.  It is up to the objects to define what it means for them to be equal.  It
        returns the matching state, if any, or False if none"""
        foundInfo = self.fringe.contains(state)
        if foundInfo:
            return foundInfo
        else:
            return False




class BestFirstSearchSolver(AbstractSearchSolver):
    """This class contains a priority-queue based search algorithm. The Priority-Queue Search can act like
    any best-first search, including UCS and A*, depending on how the "cost" is calculated.  This class contains
    stubs for the helper methods that those algorithms need.  Only the isGoal and generateNeighbors methods
    should be overridden by the subclass.
    These algorithms assume that the qData stored in the states implement the equality operators properly!"""
    
    def __init__(self, taskAdvisor):
        """Creates a Best-First search solver, with the given task advisor."""
        AbstractSearchSolver.__init__(self, taskAdvisor)


    def _setupFringe(self, startState):
        """This method sets up the proper kind of fringe set for this particular search.
        In this case, it creates a priority queue and adds the start state to it."""
        self.fringe = PriorityQueue()
        self.fringe.insert(startState, startState.getCost())


    def searchStep(self):
        """This method performs one step of a priority-queue search. It finds the next node in
        the priority queue, generates its children, and adds the appropriate ones to the priority queue
        It returns three values: the current state, the neighbors of the current state, and a status 
        message.  The message is either "Done", "Fail", or "Step" for a normal step."""
        # TODO: your code here
        newNeighbors = []
        if self.fringe.isEmpty():
            return (False, False, "Fail")
        nextState, cost = self.fringe.delete()
        if self.taskAdvisor.isGoal(nextState):
            return (nextState, [], "Done")  # when hit goal, neighbors are irrelevant

        # Otherwise, go one
        if verbose:
            print("----------------------")
            print("Current state:", nextState)
        neighbors = self.taskAdvisor.generateNeighbors(nextState)
        self.visited.add(nextState)
        self.nodesVisited += 1

        for n in neighbors:
            visitedMatch = self._hasBeenVisited(n)
            fringeMatch = self._hasBeenFringed(n)

            if (not visitedMatch) and (not fringeMatch):
                if verbose:
                    print("    Neighbor never seen before", n)
                # this node has not been generated before, add it to the fringe
                self.fringe.insert(n, n.getCost())
                newNeighbors.append(n)
                self.nodesCreated += 1
            elif visitedMatch:
                if verbose:
                    print("    Neighbor was already in explored, skipping", n)
            elif fringeMatch.getCost() > n.getCost():
                if verbose:
                    print("    Replace frontier node with child")
                self.fringe.removeValue(fringeMatch)
                self.fringe.insert(n, n.getCost())
                self.nodesCreated += 1
                

        # end for
        return nextState, newNeighbors, "Not Done"




class NoCostSearchSolver(AbstractSearchSolver):
    """This class contains a stack or queue search algorithm, so that it can do either BFS or DFS depending on whether
    it is instructed to use a stack or queue. This class contains stubs for the helper methods that those algorithms
    need.  Only the isGoal and generateNeighbors methods should be overridden by the subclass.  BFS is not
    guaranteed to give the best solution on a weighted graph, though it will always give the solution with the least
    edges.  DFS is not guaranteed to give the best solution, ever, but it is more memory-efficient.
    These algorithms assume that the states implement the comparison operators correctly!"""


    def __init__(self, taskAdvisor, mode = 'BFS'):
        """Takes in the task advisor, and an optional mode, which selects DFS or BFS.
        Sets up the qData needed for the search, the fringe and visited sets, and the counts of
        how many nodes were created and visited. The only generic qData are instance variables that count
        the number of nodes created and the number of nodes visited (that corresponds more or less to the
        number of nodes added to the queue and the number of nodes removed from the queue (and not found to be
        redundant))."""
        AbstractSearchSolver.__init__(self, taskAdvisor)
        self.mode = mode


    def _setupFringe(self, startState):
        """This method sets up the proper kind of fringe set for this particular search.
        In this case, it creates either a Queue or a Stack, depending on whether we are doing
        BFS or DFS, and it inserts the start state into it."""
        if self.mode == "BFS":
            self.fringe = Queue()
        else:
            self.fringe = Stack()
        self.fringe.insert(startState)


    def searchStep(self):
        """This method performs one step of a stack or queue search. It finds the next node in
        the stack/queue, generates its children, and adds the appropriate ones to the stack/queue.
        It returns three values: the current state, the neighbors of the current state, and a status
        message.  The message is either "Done", "Fail", or "Step" for a normal step."""
        newNeighbors = []
        if self.fringe.isEmpty():
            return (False, False, "Fail")
        nextState = self.fringe.delete()
        if self.taskAdvisor.isGoal(nextState):
            return (nextState, [], "Done")  # when hit goal, neighbors are irrelevant

        # Otherwise, go one
        if verbose:
            print("----------------------")
            print("Current state:", nextState)
        neighbors = self.taskAdvisor.generateNeighbors(nextState)
        self.visited.add(nextState)
        self.nodesVisited += 1

        for n in neighbors:
            visitedMatch = self._hasBeenVisited(n)
            fringeMatch = self._hasBeenFringed(n)

            if (not visitedMatch) and (not fringeMatch):
                if verbose:
                    print("    Neighbor never seen before", n)
                # this node has not been generated before, add it to the fringe
                self.fringe.insert(n)
                newNeighbors.append(n)
                self.nodesCreated += 1
            elif visitedMatch:  
                if verbose:
                    print("    Neighbor was already in explored, skipping", n)
            elif fringeMatch:
                if verbose:
                    print("    Neighbor was already in fringe, skipping", n)

        # end for
        return nextState, newNeighbors, "Not Done"



