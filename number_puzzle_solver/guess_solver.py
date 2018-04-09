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
   if line_num >= size:
      return

   if (dir != 'r') and (dir != 'c'):
      return

   #Guess Forward
   index = 0
   clue_indx = 0
   while clue_indx < len(clue):
      space_for_clue = True
      for check_index in range(clue[clue_indx]):
         if is_blank(dir, line_num, index + check_index):
            space_for_clue = False
            break

      if space_for_clue:
         for i in range(clue[clue_indx]):
            guess_mark(dir, line_num, index, clue_indx)
            index += 1
         clue_indx += 1

      index += 1 #for blank after clue

   #Guess Reverse
   index = size - 1
   clue_indx = len(clue) - 1
   while clue_indx >= 0:
      space_for_clue = True
      for check_index in range(clue[clue_indx]):
         if is_blank(dir, line_num, index - check_index):
            space_for_clue = False
            break

      if space_for_clue:
         for i in range(clue[clue_indx]):
            compare_mark(dir, line_num, index, clue_indx)
            index -= 1
         clue_indx -= 1

      index -= 1 #for blank after clue

   #Clear table of Unknown Values
   for index in range(size):
      clear_unknown(dir, line_num, index)