#!/usr/bin/python3
# P1.py
# Author: Paul Talaga
# 
# This file implements an aStarRobot robot capable of cleaning a fully-observable
# deterministic, static, discrete world.

from roomba_sim import *
from roomba_concurrent import *
try:
  import Queue
except ImportError:
  import queue as Queue

import time

class aStarRobot(DiscreteRobot):
  # A state is represented as a location, and the positions of dirty tiles
  # [(location), [(list of dirt),..]]
  # [(xr, yr), [(x1, y1), (x2, y2), ...]]
  # A node is the state with the path taken there
  # [[(xr, yr), [(x1, y1), (x2, y2), ...]], 'uplr']
  # The goal state is any location, and an empty list of dirty tiles
  # [(xr, yr), []]

  def initialize(self, chromosome):
    # Setup action, state, and node formats
    # Action format is a list
    self.actionlist = []
    # A state is a 2-tuple of position and a list of dirty tiles
    x, y = self.getRobotPosition()
    state = ((int(x), int(y)), self.getDirty())
    # A node is a 2-tuple of the action list and the state
    node = ([], state)
    # Search returns a node
    actionList, state = self.Astar(node)
    actionList.reverse()
    self.actionlist = actionList

  def runRobot(self):
    self.action = self.actionlist.pop()

  def h(self, node):# Heuristic
    actionList, state = node
    position, dirtList = state
    # The more dirt remaining, the less we want to go this way
    # The 
    numDirt = len(dirtList) + len(actionList) * 0.1
    return numDirt

  def generateSuccessors(self, heurNode):
    # Generate all possible successors to the current position
    # If it can move down, create a 'down' node to explore
    # 'children' is the list of successors that will be returned
    # Clean current space, if dirty
    # For each cleaned space, update list of dirt
    # Branch in all available directions
    # For each branch update direction and add action to list
    
    # Rip up heurNode for useful parts
    children = []
    heurVal, node = heurNode
    actionList, state = node
    position, dirtList = state
    wallList = self.getWalls()
    x, y = position
    # Generate new positions after movement
    north = (int(x), int(y + 1))
    south = (int(x), int(y - 1))
    east =  (int(x + 1), int(y))
    west =  (int(x - 1), int(y))
    # Check if cleaning needs to be done
    if position in dirtList:
      newCleaned = dirtList.copy()
      newCleaned.remove(position)
      stateSu = (position, newCleaned)
      nodeSu = (actionList + ['Suck'], stateSu)
      return [nodeSu]
    # Check if each direction is valid(not a wall)
    if north not in wallList:
      stateN = (north, dirtList)
      newList = actionList.copy()
      newList.append('North')
      nodeN = (newList, stateN)
      children.append(nodeN)
    if south not in wallList:
      stateS = (south, dirtList)
      newList = actionList.copy()
      newList.append('South')
      nodeS = (newList, stateS)
      children.append(nodeS)
    if east not in wallList:
      stateE = (east, dirtList)
      newList = actionList.copy()
      newList.append('East')
      nodeE = (newList, stateE)
      children.append(nodeE)
    if west not in wallList:
      stateW = (west, dirtList)
      newList = actionList.copy()
      newList.append('West')
      nodeW = (newList, stateW)
      children.append(nodeW)
    return children

  def getHash(self, node):
    # Create a unique identifier for the state in node
    #  Be sure to ignore actionlist
    
    # Rip up the node
    actions, state = node
    position, dirtList = state
    h = hash(frozenset(dirtList))
    return(str(position) + str(h))

  def Astar(self, node):
    # Generate action list to clean given space
    # A priority queue using the heuristic
    #  as the priority index will implement A*
    frontier = Queue.PriorityQueue()
    frontier.put((self.h(node), node))
    explored = []
    maxexplored = 0
    expansions = 0
    while not frontier.empty():
      expansions += 1
      thisnode = frontier.get()
      if thisnode == None:
        print("Broke, bad node")
        return None
      heurVal, nNode = thisnode
      aList, state = nNode
      explored.append(self.getHash(nNode))
      position, dirt = state
      # Check goal
      if len(dirt) == 0:
        return nNode
      for child in self.generateSuccessors(thisnode):
        if self.getHash(child) in explored:
          continue
        frontier.put((self.h(child), child))
        if maxexplored < len(explored):
          maxexplored = len(explored)
  
  def dfs(self, node, maxdepth = 999999):
    frontier = Queue.Queue()
    frontier.put(node)
    explored = []
    maxexplored = 0
    expansions = 0
    while not frontier.empty():
      expansions += 1
      thisnode = frontier.get()
      if thisnode == None:
        print("Broke, bad node")
        return None
      heurVal, nNode = thisnode
      aList, state = nNode
      explored.append(self.getHash(nNode))
      position, dirt = state
      if len(dirt) == 0:
        return nNode
      for child in self.generateSuccessors(thisnode):
        if self.getHash(child) in explored:
          continue
        frontier.put((self.h(child), child))
        if maxexplored < len(explored):
          maxexplored = len(explored)

  def bfs(self, node):
    frontier = []
    frontier.append(node)
    explored = []
    maxexplored = 0
    expansions = 0
    while not len(frontier) == 0:
      expansions += 1
      thisnode = frontier.pop()
      if thisnode == None:
        print("Broke, bad node")
        return None
      heurVal, nNode = thisnode
      aList, state = nNode
      explored.append(self.getHash(nNode))
      position, dirt = state
      if len(dirt) == 0:
        return nNode
      for child in self.generateSuccessors(thisnode):
        if self.getHash(child) in explored:
          continue
        frontier.append((self.h(child), child))
        if maxexplored < len(explored):
          maxexplored = len(explored)
    
############################################
## A few room configurations

allRooms = []

smallEmptyRoom = RectangularRoom(8,8)
allRooms.append(smallEmptyRoom)  # [0]

smallEmptyRoom2 = RectangularRoom(8,8)
smallEmptyRoom2.setWall( (4,1), (4,5) )
allRooms.append(smallEmptyRoom2) # [1]

smallEmptyRoom3 = RectangularRoom(8,8, 0.5)
smallEmptyRoom3.setWall( (4,1), (4,5) )
allRooms.append(smallEmptyRoom3) # [2]

mediumWalls1Room = RectangularRoom(20,20)
mediumWalls1Room.setWall((5,5), (15,15))
allRooms.append(mediumWalls1Room) # [3]

mediumWalls2Room = RectangularRoom(20,20)
mediumWalls2Room.setWall((5,15), (15,15))
mediumWalls2Room.setWall((5,5), (15,5))
allRooms.append(mediumWalls2Room) # [4]

mediumWalls3Room = RectangularRoom(15,15, 0.75)
mediumWalls3Room.setWall((3,3), (10,10))
mediumWalls3Room.setWall((3,10), (10,10))
mediumWalls3Room.setWall((10,3), (10,10))
allRooms.append(mediumWalls3Room) # [5]

mediumWalls4Room = RectangularRoom(30,30, 0.25)
mediumWalls4Room.setWall((7,5), (26,5))
mediumWalls4Room.setWall((26,5), (26,25))
mediumWalls4Room.setWall((26,25), (7,25))
allRooms.append(mediumWalls4Room) # [6]

mediumWalls5Room = RectangularRoom(30,30, 0.25)
mediumWalls5Room.setWall((7,5), (26,5))
mediumWalls5Room.setWall((26,5), (26,25))
mediumWalls5Room.setWall((26,25), (7,25))
mediumWalls5Room.setWall((7,5), (7,22))
allRooms.append(mediumWalls5Room) # [7]

#############################################    
def aStar():
  print(runSimulation(num_trials = 1,
                    room = allRooms[7],
                    robot_type = aStarRobot,
                    ui_enable = True,
                    ui_delay = 0.01))

if __name__ == "__main__":
  # This code will be run if this file is called on its own
  aStar()
  
  # Concurrent test execution.
  #concurrent_test(aStarRobot, [allRooms[0], allRooms[1], allRooms[2]], 10)
  #testAllMaps(aStarRobot, [allRooms[0], allRooms[1], allRooms[2]], 2)
