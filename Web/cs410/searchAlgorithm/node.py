import AIproblem

class Node(object):

	nodeCount = 0

	def __init__( self, state, parent=None, action=None ) :
		self.state = state
		Node.nodeCount += 1
		if parent:
			self.depth = parent.depth + 1

	def expand( self, problem ) :
		return [ self.makeChild( problem, action) for action in problem.getActions( self.state ) ]

	def makeChild( self, problem, action ) :
		childState = problem.applyAction( self.state, action )
		return Node( childState )

	def getState( self ) :
		return self.state