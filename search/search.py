# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # unexplored nodes to visit - stack for DFS
    frontier = util.Stack()
    # visited nodes to avoid loops
    visited = set()

    # empty start state, push to frontier
    start_state = problem.getStartState()
    frontier.push((start_state, []))

    while not frontier.isEmpty():
        # node contains state and path to the state
        state, path = frontier.pop()

        # state already visited, then skip
        if state in visited:
            continue

        visited.add(state)

        # reached goal, then return path to goal state
        if problem.isGoalState(state):
            return path
        
        # add allowed next states and paths - tells us all the legal places PacMan can move to next
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                # new path to the successor
                new_path = path + [action]
                frontier.push((successor, new_path))

    # if no route to goal
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # unexplored nodes to visit - queue for BFS
    frontier = util.Queue()
    # visited nodes to avoid loops
    visited = set()

    # start state with empty path, push to frontier
    start_state = problem.getStartState()
    frontier.push((start_state, []))

    while not frontier.isEmpty():
        # node contains state and path to the state
        state, path = frontier.pop()

        # state already visited, then skip
        if state in visited:
            continue

        visited.add(state)

        # reached goal, then return path to goal state
        if problem.isGoalState(state):
            return path

        # add allowed next states and paths to the queue - tells us all the legal places PacMan can move to next
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                # new path to the successor
                new_path = path + [action]
                frontier.push((successor, new_path))    

    # if no route to goal
    return []



def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # unexplored nodes to visit, lowest total cost first - priority queue
    frontier = util.PriorityQueue()
    # visited nodes to avoid loops
    visited = set()

    # start state with empty path and zero cost, push to frontier
    start_state = problem.getStartState()
    # priority queue takes in (state, path, cost) and the priority value - from util.py: def push(self, item, priority):
    frontier.push((start_state, [], 0), 0) 

    while not frontier.isEmpty():
        # node contains state, path to the state, and total cost
        state, path, cost = frontier.pop()

        # state already visited, then skip
        if state in visited:
            continue

        visited.add(state)

        # reached goal, then return path to goal state
        if problem.isGoalState(state):
            return path

        # add allowed next states and paths to the priority queue - tells us all the legal places PacMan can move to next
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                # new path to the successor
                new_path = path + [action]
                # new cost - add next step cost to the cost so far
                new_cost = cost + step_cost
                # use new cost as the priority
                frontier.push((successor, new_path, new_cost), new_cost)
    # if no route to goal
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # unexplored nodes to visit, lowest total cost + heuristic first
    frontier = util.PriorityQueue()
    # visited nodes to avoid loops
    visited = set()

    # start state with empty path and zero cost, push to frontier
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), 0 + heuristic(start_state, problem)) # (state,path, cost), priority with priority = cost + heuristic

    while not frontier.isEmpty():
        # node contains state, path to the state, and total cost
        state, path, cost = frontier.pop()

        # state already visited, then skip
        if state in visited:
            continue

        visited.add(state)

        # reached goal, then return path to goal state
        if problem.isGoalState(state):
            return path

        # add allowed next states and paths to the priority queue
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                # new path to the successor
                new_path = path + [action]
                # new cost - add next step cost to the cost so far
                new_cost = cost + step_cost
                # use new cost plus estimated remaining cost as priority - f(n) = g(n) + h(n)
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, new_path, new_cost), priority)
    # if no route to goal
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
