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
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.expectimax(gameState,0,0)[1]
        
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
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    DEPTH_PLUS_ONE = 4
    global previousCapsules, previousScared, previousPosition, previousClosestFood

    def getClosestFood(cur_pos, allFood):
        food_distances = []
        for food in allFood:
            food_distances.append(util.manhattanDistance(food, cur_pos))
        return min(food_distances) if len(food_distances) > 0 else 0

    def getClosestGhost(cur_pos, ghosts):
        ghost_distance = []
        for ghost in ghosts:
            ghost_distance.append(util.manhattanDistance(ghost.getPosition(), cur_pos))
        return min(ghost_distance) if len(ghost_distance) > 0 else 1

    def getTotalFoodDistance(cur_pos, food_positions):
        food_distances = []
        for food in food_positions:
            food_distances.append(util.manhattanDistance(food, cur_pos))
        return -sum(food_distances)
    
    def getTotalScaredDistance(cur_pos, scared):
        scaredDistance = []
        for ghost in scared:
            scaredDistance.append(util.manhattanDistance(ghost.getPosition(), cur_pos))
        return -sum(scaredDistance)

    def getClosestCapsule(cur_pos, capsules):
        capsule_distances = []
        for capsule in capsules:
            capsule_distances.append(util.manhattanDistance(capsule, cur_pos))
        return min(capsule_distances) if len(capsule_distances) > 0 else 1

    position = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    food = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghosts = currentGameState.getGhostStates()
    scared = list(filter(lambda x: x.scaredTimer > 0, ghosts))

    closestFood = getClosestFood(position, food)
    closestGhost = getClosestGhost(position, ghosts)
    closestCapsule = getClosestCapsule(position, capsules)
    totalFoodDistance = getTotalFoodDistance(position, food)
    totalScaredDistance = getTotalScaredDistance(position, scared)
    totalFoodCount = len(food)

    if len(scared) > 0:
        score += (len(scared) - len(previousScared)) * 200
        score += totalScaredDistance * 10
        score += closestCapsule * 10
   
    if len(capsules) == len(previousCapsules) - 1:
        score += 300

    if totalFoodCount == 0:
        score *= 2

    if position == previousPosition:
        score -= 100

    if previousClosestFood == 1 and closestFood > 5:
        score += 200

    score += (100 - closestFood * 10) 
    score += (200 - closestCapsule * 20)
    score -= totalFoodCount * 30

    score += 0.50 * totalFoodDistance

    # if totalFoodCount == 1 and len(capsules):
    #     score -= 1000

    # score -= totalFoodDistance / totalFoodCount * 25

    # if totalFoodCount < 10:
    #     score += 250 - closestFood * 5
    #     score += (10 - totalFoodCount) * 50
    #     if closestFood == 0:
    #         score += 100

    # if (closestFood < closestGhost + 3): 
    #     score *= 2

    # TODO prev leri queue yapip pop push yapilacak
    # bir onceki eval function cagirildigindaki degil de
    # bir onceki hamleninkiler alinsin diye
    previousCapsules = capsules
    previousScared = scared
    previousPosition = previousPosition
    previousClosestFood = closestFood
    # print(f'food: {totalFoodCount}, score: {score}, closestFood: {closestFood}')

    return score



    

# Abbreviation
better = betterEvaluationFunction
