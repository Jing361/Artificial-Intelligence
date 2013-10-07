#!/usr/bin/python3
# P1.py
# Author: Paul Talaga
# 
# This file implements an aStarRobot robot capable of cleaning a fully-observable
# deterministic, static, discrete world.

from roomba_sim import *
from roomba_concurrent import *


class aStarRobot(DiscreteRobot):
  # A state is represented as a location, and the positions of dirty tiles
  # [(location), [(list of dirt),..]]
  # [(xr, yr), [(x1, y1), (x2, y2), ...]]
  # A node is the state with the path taken there
  # [[(xr, yr), [(x1, y1), (x2, y2), ...]], 'uplr']
  # The goal state is any location, and an empty list of dirty tiles
  # [(xr, yr), []]

  goal = 0

  def initialize(self, chromosome):
    self.state = None
    loc = self.getRobotPosition()
    dirt = []
    for spot in self.getDirty():
        dirt.append(spot)
    path = ''
    node = [loc, dirt, path]
    print("print(loc)")
    print(loc)
    print("print(dirt)")
    print(dirt)
    print("print(path)")
    print(path)
    print("print(node)")
    print(node)
    print("print(bfs(node))")
    print(self.bfs(node))

  def isGoal(self, node):
    loc, dirt, path = node
    return self.goal == len(dirt)

  def actNew(self, state, d):
    copy = state[:]
    loc, dirt = copy
    newLoc = ()
    newDirt = dirt[:]
    # Up
    if d == 1:
      newLoc = loc[0], loc[1] - 1
    # Down
    elif d == 2:
      newLoc = loc[0], loc[1] + 1
    # Left
    elif d == 3:
      newLoc = loc[0] - 1, loc[1]
    # Right
    elif d == 4:
      newLoc = loc[0] + 1, loc[1]

    flatLoc = (math.floor(newLoc[0]), math.floor(newLoc[1]))
    if flatLoc in newDirt:
      newDirt.remove(flatLoc)

    copy = [newLoc, newDirt]
    return copy

  def h(self):# Heuristic
    return len(self.getDirty())

  def generateSuccessors(self, node):
    loc, dirt, path = node
    state = [loc, dirt]
    ret = []
    # Up
    if loc[1] > 1:
      newloc = 1
      app = self.actNew(state, newloc)
      app.append(path + 'u')
      ret.append(app)
    # Down
    if loc[1] < self.getRoomHeight():
      newloc = 2
      app = self.actNew(state, newloc)
      app.append(path + 'd')
      ret.append(app)
    # Left
    if loc[0] > 1:
      newloc = 3
      app = self.actNew(state, newloc)
      app.append(path + 'l')
      ret.append(app)
    # Right
    if loc[0] > self.getRoomWidth():
      newloc = 4
      app = self.actNew(state, newloc)
      app.append(path + 'r')
      ret.append(app)
    return ret

  def getHash(self, node):
    loc, dirt, path = node
    state = [loc, dirt]
    return str(state)

  def Astar(self, node):
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
        if self.getHash(newnode) in explored:
          continue;
        if self.isGoal(newnode):
          return (newnode, maxexplored, expansions)
        frontier.insert(0, newnode)
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
        if self.getHash(newnode) in explored:
          continue;
        if self.isGoal(newnode):
          return (newnode, maxexplored, expansions)
        frontier.insert(0, newnode)
        if maxexplored < len(explored):
          maxexplored = len(explored)

  def runRobot(self):
    #if self.state == None:
    #  self.state = 
    (bstate, dirt) = self.percepts
    # Do lots of robot stuff here!
    if dirt:
      self.action = 'Suck'
    else:
        self.action = random.choice(['North','South','East','West','Suck'])
    
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

boopRoom = RectangularRoom(5,5, .5)

#############################################    
def aStar():
  print(runSimulation(num_trials = 2,
                    room = allRooms[0],
                    robot_type = aStarRobot,
                    ui_enable = False,
                    ui_delay = 0.01))
                    
def test():
    print(runSimulation(num_trials = 1,
                        room = boopRoom,
                        robot_type = aStarRobot,
                        ui_enable = False))


if __name__ == "__main__":
  # This code will be run if this file is called on its own
  test()
  #aStar()
  
  # Concurrent test execution.
  #concurrent_test(aStarRobot, [allRooms[0], allRooms[1], allRooms[2]], 10)
  #testAllMaps(aStarRobot, [allRooms[0], allRooms[1], allRooms[2]], 2)

