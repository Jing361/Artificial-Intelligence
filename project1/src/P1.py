#!/usr/bin/python3
# P1.py
# Author: Paul Talaga
# 
# This file implements an aStarRobot robot capable of cleaning a fully-observable
# deterministic, static, discrete world.

from roomba_sim import *
from roomba_concurrent import *

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
    self.actionlist = []
    x, y = self.getRobotPosition()
    state = ((int(x), int(y)), self.getDirty())
    node = ([], state)
    actionList, state = self.Astar(node)
    actionList.reverse()
    self.actionlist = actionList

  def runRobot(self):
    self.action = self.actionlist.pop()

  def h(self, node):# Heuristic
    actionList, state = node
    position, dirtList = state
    numDirt = len(dirtList) + len(actionList)*0.1
    return numDirt

  def generateSuccessors(self, fNode):
    children = []
    hVal, node = fNode
    actionList, state = node
    position, dirtList = state
    wallList = self.getWalls()
    x, y = position
    north = (int(x), int(y + 1))
    south = (int(x), int(y - 1))
    east =  (int(x + 1), int(y))
    west =  (int(x - 1), int(y))
    if position in dirtList:
      newCleaned = dirtList.copy()
      newCleaned.remove(position)
      stateSu = (position, newCleaned)
      nodeSu = (actionList + ['Suck'], stateSu)
      return [nodeSu]
    if north not in wallList:
      stateN = (north, dirtList)
      nodeN = (actionList + ['North'], stateN)
      children.append(nodeN)
    if south not in wallList:
      stateS = (south, dirtList)
      nodeS = (actionList + ['South'], stateS)
      children.append(nodeS)
    if east not in wallList:
      stateE = (east, dirtList)
      nodeE = (actionList + ['East'], stateE)
      children.append(nodeE)
    if west not in wallList:
      stateW = (west, dirtList)
      nodeW = (actionList + ['West'], stateW)
      children.append(nodeW)
    return children

  def getHash(self, node):
    aList, state = node
    position, dirtList = state
    h = hash(frozenset(dirtList))
    return(str(position) + str(h))

  def Astar(self, node):
    frontier = [(self.h(node), node)]
    explored = []
    maxexplored = 0
    expansions = 0
    while (not len(frontier) == 0):
      expansions += 1
      thisnode = frontier.pop()
      if thisnode == None:
        print("Broke, bad node")
        return None
      hVal, nNode = thisnode
      aList, state = nNode
      explored.append(self.getHash(nNode))
      position, dirt = state
      if len(dirt) == 0:
        return nNode
      for child in self.generateSuccessors(thisnode):
        if self.getHash(child) in explored:
          continue
        frontier.insert(1, (self.h(child), child))
        if maxexplored < len(explored):
          maxexplored = len(explored)
  
  def dfs(self, node, maxdepth = 999999):
    frontier = [node]
    explored = {}
    maxexplored = 0
    expansions = 0
    while (1):
      if len(frontier) == 0:
        return None
      thisnode = frontier.pop()
      explored[self.getHash(thisnode)] = 1
      expansions += 1
      for newnode in self.generateSuccessors(thisnode):
        if len(newnode[1]) > maxdepth:
          continue;
        if self.getHash(newnode) in explored:
          continue;
        if self.isGoal(newnode):
          return (newnode, maxexplored, expansions)
        frontier.append(newnode)
        if maxexplored < len(explored):
          maxexplored = len(explored)

  def bfs(self, node):
    frontier = [node]
    explored = []
    maxexplored = 0
    expansions = 0
    while (not len(frontier) == 0):
      if len(frontier) == 0:
        print("Broken, frontier is zero")
        return None
      thisnode = frontier.pop()
      if thisnode == None:
        print("Broken, new node is invalid")
        return None
      explored.append(self.getHash(thisnode))
      expansions += 1
      for newnode in self.generateSuccessors(thisnode):
        if self.getHash(newnode) in explored:
          continue;
        if self.isGoal(newnode):
          return (newnode, maxexplored, expansions)
        frontier.insert(1, newnode)
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

boopRoom = RectangularRoom(2, 2, .5)

#############################################    
def aStar():
  print(runSimulation(num_trials = 2,
                    room = allRooms[0],
                    robot_type = aStarRobot,
                    ui_enable = True,
                    ui_delay = 0.01))
                    
def test():
    print(runSimulation(num_trials = 1,
                        room = boopRoom,
                        robot_type = aStarRobot,
                        ui_enable = True))

if __name__ == "__main__":
  # This code will be run if this file is called on its own
  test()
  #aStar()
  
  # Concurrent test execution.
  #concurrent_test(aStarRobot, [allRooms[0], allRooms[1], allRooms[2]], 10)
  #testAllMaps(aStarRobot, [allRooms[0], allRooms[1], allRooms[2]], 2)

