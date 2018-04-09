from helper_functions import *

def set_guess_solver_globals(size, clue_h, clue_v):
   global puzzle_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   puzzle_size = size
   puzzle_clue_horizontal = clue_h
   puzzle_clue_verticle = clue_v

def init_solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_guessing('r', puzzle_size, line, row_index)
      row_index += 1

   for line in puzzle_clue_verticle:
      solve_guessing('c', puzzle_size, line, col_index)
      col_index += 1

def solve_guessing(dir, size, clue, line_num):
   more_than_one_clue = False
   index = 0
   if line_num >= size:
      return

   if (dir != 'r') and (dir != 'c'):
      return
   
   while((is_blank(dir,line_num, index)) and index <= size):
      index += 1

   clue_indx = 0
   while clue_indx < len(clue):
      if more_than_one_clue : # guess blank
         index += 1
      else:
         more_than_one_clue = True

      space_for_clue = True
      for check_i in range(clue[clue_indx]):
         if is_blank(dir,line_num, index + check_i):
            space_for_clue = False

      if space_for_clue:
         for i in range(clue[clue_indx]):
            guess_mark(dir, line_num,index,clue_indx)
            index += 1
         clue_indx += 1
      #else:
      #   guess_blank(dir, line_num, index)
      #   index += 1   
 

   index = size - 1
   clue_indx = len(clue) -1

   while((is_blank(dir,line_num, index)) and index <= size):
      index -= 1

   more_than_one_clue = False
   while clue_indx >= 0:
      if more_than_one_clue :
         index -= 1
      else:
         more_than_one_clue = True

      space_for_clue = True
      for check_i in range(clue[clue_indx]):
         if is_blank(dir,line_num, index - check_i):
            space_for_clue = False

      if space_for_clue:
         for i in range(clue[clue_indx]):
            compare_mark(dir, line_num,index,clue_indx)
            index -= 1
         clue_indx -= 1
      #else:
      #   compare_blank(dir, line_num,index) 

   #for indx in range(size):
   #   compare_mark(dir,line_num, index)

   for indx in range(size):
      clear_unknown(dir, line_num,indx)