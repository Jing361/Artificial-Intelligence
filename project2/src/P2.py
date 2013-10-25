#!/usr/bin/python3
# P2.py
# Author: Chris Samuelson
# 
# This file implements a sudoku solver
# deterministic, static, discrete world.
import sys
try:
  import Queue
except ImportError:
  import queue as Queue

def same_row(i, j):
  #print("row check")
  return (i/9 == j/9)

def same_col(i, j):
  #print("column check")
  return ((i % 9) == (j % 9))
 
def same_block(i, j):
  #print("block check")
  return ((i/27 == j/27) and (i%9/3 == j%9/3))

def generateSuccessors(a):
  #print("generatin' dem successors")
  i = a.find('.')
  if i == -1:
    return
  ret = []
  excluded = []

  for j in range(81):
    if same_row(i,j) or same_col(i,j) or same_block(i,j):
      excluded.append(a[j])

  for n in '123456789':
    for j in range(81):
      if same_row(i, j) and n == a[j]:
        excluded.append(n)
      if same_col(i, j) and n == a[j]:
        excluded.append(n)
      if same_block(i, j) and n == a[j]:
        excluded.append(n)
    if n not in excluded:
      res = a.replace('.', n, 1)
      ret.append(res)
  return ret

def bfs(node):
  frontier = []
  frontier.append(node)
  explored = []
  while not len(frontier) == 0:
    thisnode = frontier.pop()
    if thisnode == None:
      return None
    explored.append(thisnode)
    if thisnode.count('.') == 0:
      return thisnode
    for child in generateSuccessors(thisnode):
      if child in explored:
        continue
      frontier.append(child)

def dfs(node):
  frontier = Queue.Queue()
  frontier.put(node)
  explored = []
  while not frontier.empty():
    thisnode = frontier.get()
    if thisnode == None:
      return None
    explored.append(thisnode)
    if thisnode.count('.') == 0:
      return thisnode
    for child in generateSuccessors(thisnode):
      if child in explored:
        continue
      frontier.put(child)

def h(node):
  return node.count(".")

def greedy(node):
  frontier = Queue.PriorityQueue()
  frontier.put((h(node), node))
  explored = []
  while not frontier.empty():
    heur, thisnode = frontier.get()
    if thisnode == None:
      return None
    explored.append(thisnode)
    if thisnode.count('.') == 0:
      return thisnode
    for child in generateSuccessors(thisnode):
      if child in explored:
        continue
      frontier.put((h(node), child))

def r(a):
  i = a.find('.')
  if i == -1:
    return a

  excluded_numbers = set()
  for j in range(81):
    if same_row(i,j) or same_col(i,j) or same_block(i,j):
      excluded_numbers.add(a[j])
  for m in '123456789':
    if m not in excluded_numbers:
      r(a[:i]+m+a[i+1])

def backtracking-search(csp):
  return recursiveBacktracking({}, csp)

def recursiveBacktracking(assignment, csp)
  if complete:
    return assignment
  var = selectUnassignedVariable(variables{csp], assignment, csp)
  for value in orderDomainValues(var, assignment, csp):
    if value valid:
      assignment[var] = value
      result = recursiveBacktraceking(assignment, csp)
      if result not fail:
        return result
      del assignment[var]
  return 'fail'

############################################
## A few grid configurations
state0 = '.........456789123789123456234567891567891234891234567345678912678912345912345678'
state1 = '759.4....68.5...4..3.2.95..56.1..9....3...1....1..6.37..53.7.9..7...8.53....6.721'


#############################################
def main(gridFile):
  f = open(gridFile, 'r')
  grid = f.read().replace('\n', '')
  print("starting")
  print("========")
  print(grid)
  print("result")
  print("======")
  print(astar(grid))

if __name__ == "__main__":
  # This code will be run if this file is called on its own
  sudoku = sys.argv[1]
  main(sudoku)

