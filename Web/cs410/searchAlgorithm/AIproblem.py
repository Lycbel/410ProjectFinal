# This is a parent class from which you can inherit to make a problem class specific to a puzzle/problem.
# For example, you can define a sudoku problem class with "class Sudoku(AIproblem)
# The new class can inherit all attributes and methods from the parent class or you can override each method.
# You can initialize the attributes of the parent by calling AIproblem.__init__(self, ...)

# The intent is to create a problem class that could be used for either a classical search or
# a local search technique, such as Simulated Annealing or Genetic Algorithms

# WARNING: This class has not been used in any substantial way. Please let us know immediately when
# you have an issue so that we can fix it. In the meantime, we will test it more.
from copy import deepcopy

class AIproblem(object):
	def __init__(self, initialState, size, evalFn=None, goal=None  ):

		self.initial = initialState
		self.size = size
		self.goal = goal
		self.evalFn = evalFn

	# Potential additional method of getNeighbors, but essentially this is the same as expanding a node
	# so really not necessary.
	# return [ applyAction( state, a) for a in getActions( state ) ]

	def getRandomAction( self, state ):
		# randomly produce a single action applicable for this state
		return None

	def getActions( self, state ) :
		# produce a list of actions to be applied to the current state
		# Pruning could happen here (i.e. only generate legal actions that result in legal states)
		return []

	def applyAction ( self, state, action ) :
		# Does nothing but copy the current state. This will be problem specific.
		# Apply the action to the current state to produce a new state
		# If you did not check for illegal states in getActions, then check for illegal states here
		# Can evaluate node based on path cost, heuristic function, or fitness function
		if not action :
			return []
		else :
			newState = deepcopy(state)
			return newState

	def evaluation( self, state ):
		if not self.evalFn :
			return 0
		else :
			state.evaluate( state.evalFn )

	def isGoal ( self, state ):
		# Determine if current state is goal
		return False

# ProblemState is a generic state class from which to derive a state specific to a puzzle/problem
# Depending on the application, it might be useful to store a path cost, heuristic value, fitness function, etc.
# For classical search, state is stored within a node. For local search, it is a stand-alone state, and can
# represent a "neighbor" or "successor"
class ProblemState(object):
	def __init__( self, state, size, value=0 ):
		self.state = state
		self.value = value
		self.size = size

	def evaluate( self, evalFn ):
		self.value = evalFn( self.state )

	def isGoal( self ) :
                # Some problems have rules that determine the goal state (e.g. Sudoku), while other problems
                # have a known goal state (e.g. Sliding Puzzle).
                # It might be appropriate to leave goal checking to this State class, or it might be better to
                # have it checked in the Problem State.
                return False

	def __str__( self ) :
                # Converts the state representation to a string (nice for printing)
                return str( self.state )