"""  =================================================================
File: MazeStateAdvisors.py

This file contains a subclasses of the SearchSolver class, specific to 
solving mazes.  It has four classes: a State and a Solver class for 
Uniform-Cost Search, and a State and a Solver class for A-star search
 ==================================================================="""



from SearchSolver import SearchState, AbstractTaskAdvisor

# ==========================================================================================

class MazeState(SearchState):
    """This represents the state of a search in a maze.  It does not
    represent the maze, just the current location in the maze, and the
    series of cells that have been traversed to get to this location.  That
    is represented in the pathToMe instance variable inherited from the parent
    class.  The cost is determined externally, """

    def __init__(self, row, col, path=None, cost=None):
        """Given the row and column location of the current state, and optional path
        and cost, initializes the state for the search"""
        SearchState.__init__(self, path, cost)
        self.row = row
        self.col = col

    def getLocation(self):
        """Return the row and column location of this state"""
        return (self.row, self.col)

    def __eq__(self, state):
        """Check if the input is the same type, and if it has the same row and column
        Overloads the == operator."""
        if type(state) is type(self):
            return (state.row == self.row) and (state.col == self.col)
        else:
            return False

    def __hash__(self):
        """Makes the state hashable by hashing a tuple of its row and column, so that it can be stored in
        a set or dictionary. Note that states that are == will produce the same hash value."""
        return hash( (self.row, self.col) )

    def __str__(self):
        """To print this object, print the row and column in brackets, followed by the
        path and cost"""
        strng = "[" + str(self.row) + ", " + str(self.col) + "]"
        strng += "  " + str(self.pathToMe) + " " + str(self.myCost)
        return strng


# ==========================================================================================


class MazeTaskAdvisor(AbstractTaskAdvisor):
    """This is the task advisor for the Maze task in general. it knows how to determine what a goal
    is, and how to work with the MazeState, and how to generate neighbors in general. There will be
    subclasses of this class for each kind of search, because the details of costs for neighbors vary from
    one algorithm to the next."""

    def __init__(self, mazeMap, startRow, startCol, goalRow, goalCol):
        """Given a map of a maze, the starting and goal locations, this initializes the variables
        that hold details of the problem"""
        AbstractTaskAdvisor.__init__(self)
        self.maze = mazeMap
        self.goalRow = goalRow
        self.goalCol = goalCol
        self.startState = self._setupInitialState(startRow, startCol)


    def _setupInitialState(self, startRow, startCol):
        """This creates and returns a proper start state for this particular
        class."""
        return MazeState(startRow, startCol, [])

    def isGoal(self, state):
        """Given a state, check if it is a goal state.  It must have the same row and column
        as the goal"""
        row, col = state.getLocation()
        if row == self.goalRow and col == self.goalCol:
            return True
        else:
            return False

    def generateNeighbors(self, state):
        """Given a state, determine all legal neighbor states.  This assumes that movements are
        restricted to north, south, east, and west.  It asks the maze map to determine which moves
        are legal for this given map, and it generates the resulting state for each legal move.
        It returns a list of neighbors."""
        (row, col) = state.getLocation()
        neighs = []
        # Move north, if it can
        if self.maze.isAccessible(row - 1, col):
            neighs.append(self._buildNeighbor(state, 'N', row - 1, col))
        # Move east, if it can
        if self.maze.isAccessible(row, col + 1):
            neighs.append(self._buildNeighbor(state, 'E', row, col + 1))
        # Move south, if it can
        if self.maze.isAccessible(row + 1, col):
            neighs.append(self._buildNeighbor(state, 'S', row + 1, col))
        # Move west, if it can
        if self.maze.isAccessible(row, col - 1):
            neighs.append(self._buildNeighbor(state, 'W', row, col - 1))
        return neighs


    def _buildNeighbor(self, currState, direction, neighRow, neighCol):
        """Given the current state and the location of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        This will be overridden by most subclasses!"""
        newPath = currState.getPath()[:]
        newPath.append(direction)
        return MazeState(neighRow, neighCol, newPath)



# ==========================================================================================

    
class UCSMazeAdvisor(MazeTaskAdvisor):
    """This class is a subclass of the MazeTaskAdvisor. It implements the cost calculations
    used for UCS search, and is intended to be paired with a BestFirstSearchSolver."""


    def _setupInitialState(self, startRow, startCol):
        """This creates and returns a proper start state for this particular
        class. In this case cost is the distance travelled so far, and that
        starts at whatever the starting position has in it."""
        return MazeState(startRow, startCol, [], self.maze.getWeight(startRow, startCol))


    def _buildNeighbor(self, currState, direction, neighRow, neighCol):
        """Given the current state and the location of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        In this case, the cost is the cost in currState plus the cost in the neighbor."""
        newPath = currState.getPath()[:]
        newPath.append(direction)
        oldCost = currState.getCost()
        newCost = self.maze.getWeight(neighRow, neighCol)
        return MazeState(neighRow, neighCol, newPath, oldCost + newCost)




#==========================================================================================


    
class GreedyMazeAdvisor(MazeTaskAdvisor):
    """This class is a subclass of the MazeTaskAdvisor. It implements the cost calculations
    used for Greedy Best-First Search, and is intended to be paired with a BestFirstSearchSolver."""

    def _setupInitialState(self, startRow, startCol):
        """This creates and returns a proper start state for this particular
        class. In this case, it computes the distance to the goal and uses
        that as the cost."""
        distToGoal = self._calcDistToGoal(startRow, startCol)
        return MazeState(startRow, startCol, [], distToGoal)


    def _buildNeighbor(self, currState, direction, neighRow, neighCol):
        """Given the current state and the location of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        In this case, the cost is the distance to the goal."""
        newPath = currState.getPath()[:]
        newPath.append(direction)
        distToGoal = self._calcDistToGoal(neighRow, neighCol)
        return MazeState(neighRow, neighCol, newPath, distToGoal)


    def _calcDistToGoal(self, row, col):
        """Compute the distance to the goal using the city block metric.  Compute 
        the difference in row values and in column values, and add them up"""
        yDist = abs(row - self.goalRow)
        xDist = abs(col - self.goalCol)
        return xDist + yDist


# ==========================================================================================

class AStarMazeState(MazeState):
    """This represents the state of a search in a maze.  It does not
represent the maze, just the current location in the maze, and the
series of cells that have been traversed to get to this location.  That
is represented in the pathToMe instance variable inherited from the parent
class.  The cost is determined externally."""

    def __init__(self, row, col, path = None, costToHere = None, costToGoal = None):
        """Given the row and column, the current path, and the two costs (cost so far and heuristic 
        cost to come, this creates a state/node for the search"""

        MazeState.__init__(self, row, col, path, costToHere + costToGoal)
        self.costToHere = costToHere
        self.costToGoal = costToGoal
        self.myCost = self.costToHere + self.costToGoal

    def getCostToHere(self):
        """Return the cost so far"""
        return self.costToHere

    def getCostToGoal(self):
        """Return the heuristic estimate cost to the goal"""
        return self.costToGoal

    def __str__(self):
        """Create a string for printing that contains the row, col plus path and costs"""
        strng = "[" + str(self.row) + ", " + str(self.col) + "]"
        strng += "  " + str(self.pathToMe) + " (" + str(self.costToHere)
        strng += " + " + str(self.costToGoal) + ") = " + str(self.myCost)
        return strng


    
class AStarMazeAdvisor(MazeTaskAdvisor):
    """This class is a subclass of the MazeTaskAdvisor. It implements the cost calculations
    used for A* search, using the AStarState, which maintains both g and h costs. It is intended to
    be paired with a BestFirstSearchSolver."""

    def _setupInitialState(self, startRow, startCol):
        """This creates and returns AStarMazeState class for A* algorithm.
        In this case, it computes all the two values, g, and h:
        g = the cost of the starting cell (maze.getWeight)
        h = the heuristic distance to goal (_calcDistToGoal)
        The f cost is automatically computed by the AStarMazeState (f = g + h)
        path is initialized with an empty list.
        """
        # TODO: your code here
        distToGoal = self._calcDistToGoal(startRow, startCol)
        return AStarMazeState(startRow, startCol, [], self.maze.getWeight(startRow, startCol), distToGoal)

    def _buildNeighbor(self, currState, direction, neighRow, neighCol):
        """Given the current state and the location of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        In this case, we need to update both g and h costs for the new state:
        new g = old g + new cell's weight,
        new h = distance to goal of new cell"""
        # TODO: your code here
        newPath = currState.getPath()[:]
        newPath.append(direction)
        costToHere = currState.getCostToHere() + self.maze.getWeight(neighRow, neighCol)
        distToGoal = self._calcDistToGoal(neighRow, neighCol)
        return AStarMazeState(neighRow, neighCol, newPath, costToHere, distToGoal)


    def _calcDistToGoal(self, row, col):
        """Compute the distance to the goal using the city block metric.  Compute 
        the difference in row values and in column values, and add them up"""
        # TODO: your code here
        yDist = abs(row - self.goalRow)
        xDist = abs(col - self.goalCol)
        return xDist + yDist