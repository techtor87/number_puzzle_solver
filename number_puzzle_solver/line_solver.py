from helper_functions import *

def set_line_solver_globals(size, clue_h, clue_v):
   global puzzle_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   puzzle_size = size
   puzzle_clue_horizontal = clue_h
   puzzle_clue_verticle = clue_v

def solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_line('r', puzzle_size, line, row_index)
      row_index += 1

   for line in puzzle_clue_verticle:
      solve_line('c', puzzle_size, line, col_index)
      col_index += 1   

def solve_line(dir, size, clue, line_num):
   if line_num >= size:
      return

   if (dir != 'r') and (dir != 'c'):
      return

   clue_indx = 0
   indx = 0
   #check forward
   while indx < size:
      if is_mark(dir, line_num, indx):
         for clue_size in range(clue[clue_indx]):
            mark_known(dir, line_num,indx)
            indx += 1
         blank_known(dir, line_num,indx)
         clue_indx +=1
      elif is_blank(dir, line_num, indx):
         indx += 1
      else:
         if clue_indx == len(clue):
            blank_known(dir, line_num, indx)
            indx += 1
         else:
            break

   #check backward
   indx = size - 1
   clue_indx = len(clue) - 1
   while indx >= 0:
      if is_mark(dir, line_num, indx):
         for clue_size in range(clue[clue_indx]):
            mark_known(dir, line_num,indx)
            indx -= 1
         blank_known(dir, line_num,indx)
         clue_indx -=1
      elif is_blank(dir, line_num, indx):
         indx -= 1
      else:
         if clue_indx == -1:
            blank_known(dir, line_num, indx)
            indx -= 1
         else:
            break

   cur_mark_cnt = 0
   longest_clue = max(clue)
   for indx in range(size):
      if is_mark(dir, line_num, indx):
         cur_mark_cnt += 1
      else:
         if cur_mark_cnt == longest_clue:
            blank_known(dir, line_num,indx)
            blank_known(dir, line_num,indx - cur_mark_cnt -1)
         #if cur_mark_cnt > longest_mark:
         #   longest_mark = cur_mark_cnt
         #   longest_mark_end = indx - 1
         #   longest_mark_start = longest_mark_end - longest_mark
         cur_mark_cnt = 0

   #check if all Marks done
   mark_count = 0
   for indx in range(size):
      if is_mark(dir, line_num, indx):
         mark_count += 1

   if mark_count == sum(clue):
      for indx in range(size):
         if is_unknown(dir, line_num, indx):
            blank_known(dir, line_num,indx)