# -*- coding: utf-8 -*-
import random

class Board:
  def __init__(self, n, board_map):
    for i, q in enumerate(board_map):
      if(q >= n):
        print('error: queen is out of boundry on column {}: (val:{})'.format(i,q))
        board_map[i] = random.randrange(n)
        print('replaced randomly with {}'.format(board_map[i]))
    self.__n = n
    self.__board_map = board_map # initializing board columns
    self.h = heuristic_value(self.__board_map)
  
  @property
  def board_map(self):
    return self.__board_map
  
  @property
  def n(self):
    return self.__n
    
  def move(self, column, val):
    if(column >= self.n or val >= self.n):
      return
    self.__board_map[column] = val
    
  def print_board(self):
    board = ''
    for i in range(self.__n):
      for j in range(self.__n):
        if(self.__board_map[j] == self.__n - i - 1):
          board+='Q '
        else:
          board+='- '
      board+='\n'
      h = 'h={} Queens Conflicting'.format(self.h)
    print(board + h)
    
  def steepest_climb(self): # choose randomly between the steepest moves.
    min_h = self.h
    moves = []
    temp_map = list(self.__board_map)
    for i, val in enumerate(temp_map):
      for j in range(self.__n):
        temp_map[i] = j
        heuristic = heuristic_value(temp_map)
        if heuristic <= min_h:
          min_h = heuristic
          if(j != self.__board_map[i]):
            moves += [{'col':i, 'val':j, 'h':heuristic}]
      temp_map = list(self.__board_map)
    best_moves = [move for move in moves if move['h'] == min_h]
    if(self.h <= min_h or len(best_moves)==0):
      return False
    self.h = min_h
    x = random.choice(best_moves)
    self.__board_map[x['col']] = x['val']
    return True
  
  def stochastic_climb(self): # choose randomly between the ascending moves.
    min_h = self.h
    moves = []
    temp_map = list(self.__board_map)
    for i, val in enumerate(temp_map):
      for j in range(self.__n):
        temp_map[i] = j
        heuristic = heuristic_value(temp_map)
        if heuristic < min_h:
          if(j != self.__board_map[i]):
            moves += [{'col':i, 'val':j, 'h':heuristic}]
      temp_map = list(self.__board_map)
    if(len(moves)==0):
      return False
    x = random.choice(moves)
    self.h = x['h']
    self.__board_map[x['col']] = x['val']
    return True
  
  def random_restart_climb(self, show = False): # use steepest_climb function until solution found, if not restart from random state
    restart, count = 0, 0
    while(self.h != 0):
      while(self.steepest_climb()==True):
        count +=1
      if(show == True):
        self.print_board()
      if(self.h == 0):
        break
      restart += 1
      self.__board_map = random_board(self.__n)
      self.h = heuristic_value(self.__board_map)
      if(show == True):
        print('randomized board')
        self.print_board()
    return (restart,count)
    
      
def heuristic_value(board_map): # helper function to calculate heuristic value(total conflicting queens)
    h = 0
    for i, val1 in enumerate(board_map):
      for j, val2 in enumerate(board_map[i+1:]):
        if(conflict(i,j+i+1,val1,val2)):
          h += 1
    return h
  
def conflict(column1, column2, val1, val2):  # helper function to determine if two queen conflicting
    if column2 < column1: # swap columns so column1 has lesser value
      (column1, column2)  = (column2, column1)
    if(val1 == val2): # check queens horizontal
      return True
    coldif = column2 - column1
    if(abs(val1 - val2) == coldif): # check queens  diagonal
      return True
    return False
  
def random_board(n): # creating random board
  board = []
  for i in range(n):
    board.append(random.randrange(n))
  return board


print('This program solve N-Queens problem by hill-climbing methods')
print('program provides Steepest hill climb, random-restart hill climb and stochastic hill climb')

choice = input('Randomly Generated Problems (Y/N):').upper()
repeats = 1
if(choice[0] != 'Y'):
  initial = input('Enter board(spaces between):').split(' ')
  initial = list(map(int,initial)) # convert chars to int
if(choice[0] == 'Y'):
  n = input('Enter board size N: ')
  while(int(n) < 4):
    n = input('Enter board size N (minimum 4): ')
  repeats = input('Enter how many tests you want:')
  while(int(repeats) < 1):
    repeats = input('Tests can not be less than 1:')
  n = int(n)
repeats = int(repeats)
print('RR:Random Restart, S:Steepest, ST:Stochastic')
method = input('Enter method(s) (spaces between): ').upper().split(' ')
stepbystep = input('Step by Step solution(Y/N)): ').upper()
for x in range(repeats):
  if(choice[0] == 'Y'):
    initial = random_board(n)
  board_initial = Board(len(initial), initial)
  print('\nInitial board')
  board_initial.print_board()
  for m in method:
    board = Board(int(board_initial.n), list(board_initial.board_map))
    restart = -1
    moves = 0
    
    if(m == 'RR'):
      print('\nRandom Restart Hill Climb')
      (restart,moves) = board.random_restart_climb(stepbystep[0] == 'Y')
    elif(m == 'ST'):
      print('\nStochastic Hill Climb')
      while(board.stochastic_climb()==True):
        moves = 1 + moves
        if(stepbystep[0] == 'Y'):
          board.print_board()
    
    elif(m == 'S'):
      print('\nSteepest Hill Climb')
      while(board.steepest_climb()==True):
        moves = 1 + moves
        if(stepbystep[0] == 'Y'):
          board.print_board()  
    
    else:
      continue
    print('Final State:')
    board.print_board()
    statistics = '{} moves'.format(moves)
    if(restart!= -1):
      statistics = '{} restarts, '.format(restart) + statistics
    print(statistics)
    