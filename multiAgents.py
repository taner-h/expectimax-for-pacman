# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

previousCapsules = 'prevCapsules'
previousScared = 'prevScared'
previousPosition = 'prevPosition'
previousClosestFood = 'prevClosestFood'

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):

        def getClosestFood(pacmanPosition, allFood):
            food_distances = [util.manhattanDistance(food, pacmanPosition) for food in allFood]
            return min(food_distances) if len(food_distances) > 0 else 0

        global previousPosition, previousCapsules, previousScared, previousClosestFood
        
        action = self.expectimax(gameState,0,0)[1]

        previousPosition = gameState.getPacmanPosition()
        previousCapsules = gameState.getCapsules()
        ghosts = gameState.getGhostStates()
        previousScared = list(filter(lambda x: x.scaredTimer > 0, ghosts))
        food = gameState.getFood().asList()
        previousClosestFood = getClosestFood(previousPosition, food)

        return action
        
    def expectimax(self,gameState,depth,agent):

        # sira tekrar pacman'de ise depth'i artır ve agent indeksini 0 yap
        if agent == gameState.getNumAgents():
            agent = 0
            depth = depth + 1
        
         # terminal state'te ise evaluation degerini dondur
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [self.evaluationFunction(gameState)]
        
        if agent == 0: # pacman
            bestValue = [-999999] 
            for action in gameState.getLegalActions(agent):
                childState = gameState.generateSuccessor(agent, action)
                childValue = self.expectimax(childState, depth, agent + 1)[0]
                
                if (childValue >= bestValue[0]):
                    bestValue = [childValue, action]

            return bestValue

        else: # ghost'lar
            totalValue = 0
            legalActions = gameState.getLegalActions(agent)

            if len(legalActions) == 0:
                return [self.evaluationFunction(gameState)]
                    
            for action in legalActions:
                childState = gameState.generateSuccessor(agent, action)
                childValue = self.expectimax(childState, depth, agent + 1)[0]
                totalValue += childValue
            
            averageValue = totalValue / len(gameState.getLegalActions(agent))
            return [averageValue]
  

def betterEvaluationFunction(currentGameState):

    global previousCapsules, previousScared, previousPosition, previousClosestFood

    def getClosestFood(pacmanPosition, allFood):
        food_distances = [util.manhattanDistance(food, pacmanPosition) for food in allFood]
        return min(food_distances) if len(food_distances) > 0 else 0

    def getClosestGhost(pacmanPosition, ghosts):
        ghost_distance = [util.manhattanDistance(ghost.getPosition(), pacmanPosition) for ghost in ghosts]
        return min(ghost_distance) if len(ghost_distance) > 0 else 1

    def getTotalFoodDistance(pacmanPosition, food_positions):
        food_distances = [util.manhattanDistance(food, pacmanPosition) for food in food_positions]
        return -sum(food_distances)
    
    def getTotalScaredDistance(pacmanPosition, scared):
        scaredDistance = [util.manhattanDistance(ghost.getPosition(), pacmanPosition) for ghost in scared]
        return -sum(scaredDistance)

    def getClosestCapsule(pacmanPosition, capsules):
        capsule_distances = [util.manhattanDistance(capsule, pacmanPosition) for capsule in capsules]
        return min(capsule_distances) if len(capsule_distances) > 0 else 1

    position = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    food = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghosts = currentGameState.getGhostStates()
    haveLost = currentGameState.isLose()
    scared = list(filter(lambda x: x.scaredTimer > 0, ghosts))

    closestFood = getClosestFood(position, food)
    closestGhost = getClosestGhost(position, ghosts)
    closestCapsule = getClosestCapsule(position, capsules)
    totalFoodDistance = getTotalFoodDistance(position, food)
    totalScaredDistance = getTotalScaredDistance(position, scared)
    totalFoodCount = len(food)

    if len(scared) > 0 or len(previousScared) > 0 :
        score += (len(scared) - len(previousScared)) * 200
        score += totalScaredDistance * 10
        score += closestCapsule * 10
   
    if len(capsules) == len(previousCapsules) - 1:
        score += 300
        if len(previousScared) > 0:
            score -= 400

    if totalFoodCount == 0:
        if len(scared) > 0:
            score -= 500
        else:
            score += 1000
        
    if position == previousPosition:
        score -= 200

    if previousClosestFood == 1 and closestFood > 4:
        score += 100

    score += (100 - closestFood * 5) 

    score += (200 - closestCapsule * 20)

    score -= totalFoodCount * 30

    score += 0.50 * totalFoodDistance

    return score

# Abbreviation
better = betterEvaluationFunction
