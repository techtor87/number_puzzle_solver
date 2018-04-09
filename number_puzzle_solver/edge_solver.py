from helper_functions import *

def set_edge_solver_globals(size, clue_h, clue_v):
   global puzzle_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   puzzle_size = size
   puzzle_clue_horizontal = clue_h
   puzzle_clue_verticle = clue_v

def solve_table_edges():
   global puzzle_size
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_edge('r', puzzle_size, line, row_index)
      row_index += 1

   for line in puzzle_clue_verticle:
      solve_edge('c', puzzle_size, line, col_index)
      col_index += 1

def solve_edge(dir, size, clue, line_num):
   if line_num >= size:
      return

   if (dir != 'r') and (dir != 'c'):
      return

   first_indx = 0
   last_indx = size - 1
   #if first column known, first clue is known
   if is_mark(dir, line_num, first_indx):
      index = 0
      for i in range(clue[first_indx]):
         mark_known(dir, line_num,index)
         index += 1
      blank_known(dir, line_num, index)
   
   #if last column known, last clue is known
   if is_mark(dir, line_num, last_indx):
      index = last_indx
      for i in range(clue[len(clue)-1]):
         mark_known(dir, line_num,index)
         index -= 1
      blank_known(dir, line_num, index)

   #if first known mark is closer to edge than clue size
   start_mark = False
   for indx in range(clue[0]):
      if is_mark(dir, line_num, indx):
         start_mark = True
      if start_mark:
         mark_known(dir, line_num,indx)

   #if last known mark is closer to edge than clue size
   start_mark = False
   for indx in range(size-1,size - 1 - clue[len(clue)-1],-1):
      if is_mark(dir, line_num, indx):
         start_mark = True
      if start_mark:
         mark_known(dir, line_num,indx)

   #if impossible to have mark in first Column
   if is_mark(dir, line_num, clue[0]):
      blank_known(dir, line_num, 0)
   #if impossible to have mark in last Column
   if is_mark(dir, line_num, size - clue[-1] - 1):
      blank_known(dir, line_num, size - 1)

   #if first clue is pinned to edge
   if is_blank(dir, line_num, clue[0]) and is_mark(dir, line_num, clue[0]-1):
      mark_known(dir, line_num, 0)
   #if last clue is pinned to edge
   if is_blank(dir, line_num, size - clue[-1] - 1) and is_mark(dir, line_num, size - clue[-1]):
      mark_known(dir, line_num, size - 1)


   