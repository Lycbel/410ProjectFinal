import sys
import pickle
import numpy as np
import scipy.sparse as sparseMatrix
from copy import deepcopy
import json
import timeit

######################################################
####################helper class######################
######################################################
def loadFiles():
    path = "searchAlgorithm/"
    with open(path+"word_dict.dict", "rb") as f:
        wordDict = pickle.load(f)
        #get dimension
        dimension = 0
        for i in wordDict.items():
            if i[1] > dimension:
                dimension = i[1]
        f.close()

    print("word dict loaded.")

    with open(path+"word_dict_inv.dict", "rb") as f:
        wordDictInv = pickle.load(f)
        f.close()

    print("word dict inverse loaded.")

    with open(path+"Go_term.dict", "rb") as f:
        gotermDict = pickle.load(f)
        f.close()

    print("GO term dict loaded.")

    with open(path+"word_matrix.dict", "rb") as f:
        matrix = pickle.load(f)
        f.close()
    print("doc dict loaded.")
    print("matrix shape: " + str(matrix.shape))
    print("=======Initialization completed========")
    return matrix, wordDict, wordDictInv, gotermDict, dimension

def findSample():
    drugidx = 0
    adridx = 0
    docidx = 0
    docDict = {}
    durgDict = {}
    adrDict = {}
    drugList = []
    adrList = []

    with open("doc_word.dict0", "rb") as f:
        docDict = pickle.load(f)
        f.close()

    with open("drug_adr.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    for i in subDict.keys():
        durgDict[i.strip().lower()] = drugidx
        drugidx += 1

    with open("adr_drug.dict", "rb") as f:
        subDict = pickle.load(f)
        f.close()
    for i in subDict.keys():
        adrDict[i.strip().lower()] = adridx
        adridx += 1

    print("files loaded")
    print(durgDict.keys())
    for i in docDict.items():
        wordList = i[1]
        for adr in adrDict.keys():
            if adr in wordList:
                adrList.append(adr)
                print(len(adrList))
        if len(adrList) >= 20:
            break

    return adrList

######################################################
##################father classes######################
######################################################
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

class Node(object):
    nodeCount = 0

    def __init__(self, state, parent=None):
        self.state = state
        Node.nodeCount += 1
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        return [self.makeChild(problem, action) for action in problem.getActions(self.state)]

    def makeChild(self, problem, action):
        childState = problem.applyAction(self.state, action)
        return Node(childState)

    def getState(self):
        return self.state
######################################################
#####################node class#######################
######################################################

# global variables:
#matrix, wordDict, dimension = loadFiles()

class keyWordNode(Node):

    nodeCount = 0

    def __init__(self, state, parent=None, weight=0, ):
        self.state = state #cur index
        self.nodeCount = 0
        self.depth = 0
        self.parent = parent
        self.weight = weight
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        lst = [ self.makeChild( problem, action) for action in problem.getActions( self.state ) ]
        return lst

    def makeChild(self, problem, action):
        Node.nodeCount += 1
        childState, weight = problem.applyAction(self.state, action)
        return keyWordNode(childState, self, weight)

    def getState(self):
        return self.state

    def setParent(self, node):
        self.parent = node

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

######################################################
###################problem class######################
######################################################
class FindDrugToAdr (AIproblem):
    def __init__(self, initialState, goalState, matrix, wordDict, wordDictInv, dimension, evalFn=None):
        self.matrix = matrix
        self.wordDict = wordDict
        self.dimension = dimension
        self.wordDictInv = wordDictInv

        self.initial = self.wordDict[initialState] #the drug index
        self.goal = self.wordDict[goalState] #the adr index
        self.evalFn = evalFn
        self.actions = []

    #for test use
    def printStats(self):
        print(self.dimension)
        print(self.initial)
        print(self.goal)


    #get the whole list of actions
    def getActions( self, state) :
        # produce a list of actions to be applied to the current state
        # Pruning could happen here (i.e. only generate legal actions that result in legal states)
        return list(self.matrix[state].nonzero()[1])

    #apply one action to a state and return the new state
    #islegal() is used to check if one action is legal to a spcific state --> see helper.py
    #if islegal() returns false, then the funtion will return an empty list
    def applyAction ( self, state, action ) :
        # Does nothing but copy the current state. This will be problem specific.
        # Apply the action to the current state to produce a new state
        # If you did not check for illegal states in getActions, then check for illegal states here
        # Can evaluate node based on path cost, heuristic function, or fitness function
        if not action:
            print(action)
            return self.initial, 0
        else :
            return action, self.matrix[state, action]

    #if current state is equal to the goal state
    def isGoal ( self, state ):
        if state == self.goal:
            return True
        return False
######################################################
#######################IDDFS##########################
######################################################
#iterative deepening search
def recursiveDLS(node, problem, limit):
    # basically identical to DFS, but it will quit when limit == 0.
    if problem.isGoal( node.getState() ):
        return node
    elif limit == 0 :
        return None
    else:
        for child in node.expand(problem):
            #print(child.getState())
            rs = None
            rs = recursiveDLS(child, problem, limit-1)
            if not rs == None:
                return rs
        return None

#limited version of dfs
def DepthLimitedSearch(problem, limit):
    node = keyWordNode( problem.initial )
    return recursiveDLS(node, problem, limit)

# increase the depth of DepthLimitedSearch by 1 during each iteration, this algorithm will not end until a solution is found.
def IDDFS(problem, limit):
    depth = 1
    rsList = []
    while depth <= limit:
        rs = DepthLimitedSearch(problem, depth)
        if not rs == None:
            rsList.append(rs)
        depth += 1
        print("cur depth:" + str(depth))
    return rsList

def showResult(probelm, node):
    idxList = []
    while node:
        idxList.append((node.state, np.uint8(np.int8(node.weight))))
        node = node.parent
    idxList.reverse()
    for i in idxList:
        print(probelm.wordDictInv[i[0]] + " ==== " +str(i[1]))

def filterNode(node):
    node_ = deepcopy(node)
    idxList = []
    while node_:
        idxList.append((node_.state, node_.weight))
        node_ = node_.parent
    idxList.reverse()
    for i in idxList:
        idx = idxList.index(i)
        if idx >= 2:
            if i[0] == idxList[idx - 2][0]:
                return False
    return True


def ResultToJson(problem, nodeList, gotermDict, path=""):
    nodeList_ = deepcopy(nodeList)
    drug = problem.wordDictInv[problem.initial]
    adr = problem.wordDictInv[problem.goal]
    keyWordList = []
    output = {}
    nodeDict = {}

    #write drug and adr
    output["nodes"] = []
    output["nodes"].append({
        'id': "0",
        'root': True,
        'type': 'philosopher',
        'title': drug
    })
    output["nodes"].append({
        'id': "1",
        'root': True,
        'type': 'philosopher',
        'title': adr
    })
    nodeDict[drug] = 0
    nodeDict[adr] = 1
    #write nodes
    id = 2
    for n in nodeList_:
        while n:
            keyWordList.append(problem.wordDictInv[n.state])
            n = n.parent
    keyWordList = list(set(keyWordList))
    keyWordList.remove(drug)
    keyWordList.remove(adr)
    for kw in keyWordList:
        if kw.startswith('go:'):
            print("======FOUND GO TERM=======")
            go_id = "GO:" + kw[3:]
            go_term = gotermDict[go_id]
            kw = kw + " : " + go_term
        output["nodes"].append({
            'id': str(id),
            'cluster': '1',
            'title': kw,
            'relatedness': 0.0
        })
        nodeDict[kw] = id
        id += 1

    #write edges
    edgeList = []
    for n in nodeList:
        while n:
            if n.parent:
                edgeList.append((problem.wordDictInv[n.state], problem.wordDictInv[n.parent.state], n.weight))
            n = n.parent

    edgeList = list(set(edgeList))
    output["edges"] = []
    for edge in edgeList:
        output["edges"].append({
            'source': str(nodeDict[edge[1]]),
            'target': str(nodeDict[edge[0]]),
            'relatedness': str(np.uint8(np.int8(edge[2]))),
        })

    if len(path) == 0:
        path = 'output.txt'
    with open(path, 'w+') as outfile:
        json.dump(output, outfile)
    return keyWordList

def webAppSearch(drug, adr, path):
    limitedDepth = 7
    matrix, wordDict, wordDictInv, gotermDict, dimension = loadFiles()
    searchProblem = FindDrugToAdr(drug, adr, matrix, wordDict, wordDictInv, dimension)
    nodeList = IDDFS(searchProblem, limitedDepth)
    filteredList = []
    for n in nodeList:
        if filterNode(n):
            filteredList.append(n)
    if len(filteredList) > 0:
        ResultToJson(searchProblem, filteredList, gotermDict, path)
        return 1
    else:
        return -1


if __name__ == '__main__':
    #test search
    webapp = False
    if webapp:
        start_ = timeit.default_timer()
        drug = "fluoroquinolones".lower().strip()
        adr = "pain".lower().strip()
        limitedDepth = 7

        matrix, wordDict, wordDictInv, gotermDict, dimension = loadFiles()
        searchProblem = FindDrugToAdr(drug, adr, matrix, wordDict, wordDictInv, dimension)
        nodeList = IDDFS(searchProblem, limitedDepth)
        filteredList = []
        for n in nodeList:
            if filterNode(n):
                filteredList.append(n)
        print(len(filteredList))
        print(len(nodeList))
        if len(filteredList) > 0:
            ResultToJson(searchProblem, filteredList, gotermDict)
        else:
            print("No results found.")

        for n in filteredList:
            print("====================")
            showResult(searchProblem, n)
        end_ = timeit.default_timer()
        print("Runtime: " + str(end_ - start_))
    else:
        start_ = timeit.default_timer()
        matrix, wordDict, wordDictInv, gotermDict, dimension = loadFiles()
        limitedDepth = 7
        end_ = timeit.default_timer()
        print("Runtime: " + str(end_ - start_))
        while True:
            start_ = timeit.default_timer()
            drug = input("Please enter drug: ").lower().strip()
            adr = input("Please enter drug: ").lower().strip()

            searchProblem = FindDrugToAdr(drug, adr, matrix, wordDict, wordDictInv, dimension)
            nodeList = IDDFS(searchProblem, limitedDepth)
            filteredList = []
            for n in nodeList:
                if filterNode(n):
                    filteredList.append(n)
            print(len(filteredList))
            print(len(nodeList))
            if len(filteredList) > 0:
                ResultToJson(searchProblem, filteredList, gotermDict)
            else:
                print("No results found.")

            for n in filteredList:
                print("====================")
                showResult(searchProblem, n)
            end_ = timeit.default_timer()
            print("Runtime: " + str(end_ - start_))








'''
test samples:
drugs: ['cell', 'prostate', 'lipase', 'letter', 'enzymes', 'lysine', 'liver', 'fluoroquinolones', 'pazufloxacin', 'garenoxacin', 'ciprofloxacin', 'moxifloxacin', 'sitafloxacin', 'levofloxacin', 'heart', 'radiation', 'polypharmacy', 'stem cells', 'nitric oxide', 'oxygen', 'proteins']
adrs: ['pain', 'renal replacement therapy', 'palliative care', 'hypertrophy', 'inflammation', 'metaplasia', 'pain', 'back pain', 'adenocarcinoma', 'atrial fibrillation', 'pneumonia', 'death', 'osteoarthritis', 'obesity', 'overweight', 'body mass index', 'pelvic pain', 'pain', 'infertility', 'endometriosis']

'''