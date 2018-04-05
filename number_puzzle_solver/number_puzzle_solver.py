import mouse_control as mc

import sys
import time

from PIL import Image, ImageOps, ImageGrab, ImageFilter
import pytesseract
import argparse
import os

pytesseract.pytesseract.tesseract_cmd = 'C:/tesseract/tesseract.exe'

def submit_puzzle(size, puzzle):
   mouse = mc.mouse_control()
   corner_point_1 = mc._point_t()
   corner_point_2 = mc._point_t()
   print "click UL corner"
   time.sleep(5)
   corner_point_1 = mouse.get_cursor_position()
   print "click BR corner"
   time.sleep(2.5)
   corner_point_2 = mouse.get_cursor_position()
   print "done"   

   print corner_point_1.x, corner_point_1.y, corner_point_2.x, corner_point_2.y

   box_size =  (corner_point_2.x - corner_point_1.x)/size
   print box_size
   #f = open("x_y_coord.csv",'w')
   for row in range(size):
      for cell in range(size):
         if is_mark('r', row, cell):
            mouse.l_click_mouse(corner_point_1.x + box_size / 3 + box_size * cell , 
                          corner_point_1.y + box_size / 3 + box_size * row )
         elif is_blank('r', row, cell):
            mouse.r_click_mouse(corner_point_1.x + box_size / 3 + box_size * cell , 
                          corner_point_1.y + box_size / 3 + box_size * row )
   f.close()
   #corner_point_1

def get_clues_from_image():
   global puzzle_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   #img = Image.open('number_puzzle_1.png')
   img = ImageGrab.grabclipboard()
   imgW, imgH = img.size
   inv_img = ImageOps.grayscale(img)
   print inv_img.getbbox()
   #img.crop((0, 0, 100, imgH)).save('num_puz_crop_1.png')
   inv_img.show()

   text = pytesseract.image_to_string(img)
   print text
   
def init_clues ():
   global puzzle_size
   for i in range(puzzle_max_size):
       puzzle_clue_horizontal.append(0)
       puzzle_clue_verticle.append(0)

   get_clues_from_image()

   with open("puzzle_vals.txt",'r') as f:
      puzzle_size = int(f.readline())
      f.readline()
     
      for i in range(puzzle_size):
         puzzle_clue_horizontal[i] = map(int, f.readline().split(','))

      f.readline()

      for i in range(puzzle_size):
         puzzle_clue_verticle[i] = map(int, f.readline().split(','))

   for i in range(puzzle_size):
      puzzle_row = []
      for j in range(puzzle_size):
         puzzle_row.append('_')
      puzzle_solve.append(puzzle_row)

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

   for indx in range(size):
      clear_unknown(dir, line_num,indx)

def solve_edge(dir, size, clue, line_num):
   if line_num >= size:
      return

   if (dir != 'r') and (dir != 'c'):
      return

   first_indx = 0
   last_indx = size - 1
   #check first column 
   if is_mark(dir, line_num, first_indx):
      index = 0
      for i in range(clue[first_indx]):
         mark_known(dir, line_num,index)
         index += 1
      blank_known(dir, line_num, index)
   
   
   #check last column 
   if is_mark(dir, line_num, last_indx):
      index = last_indx
      for i in range(clue[len(clue)-1]):
         mark_known(dir, line_num,index)
         index -= 1
      blank_known(dir, line_num, index)

   start_mark = False
   for indx in range(clue[0]):
      if is_mark(dir, line_num, indx):
         start_mark = True
      if start_mark:
         mark_known(dir, line_num,indx)

   if is_blank(dir, line_num, clue[0]) and is_mark(dir, line_num, clue[0]-1):
      mark_known(dir, line_num, 0)
      
   if is_blank(dir, line_num, size - clue[-1] - 1) and is_mark(dir, line_num, size - clue[-1]):
      mark_known(dir, line_num, size - 1)

   if is_mark(dir, line_num, clue[0]):
      blank_known(dir, line_num, 0)
      
   if is_mark(dir, line_num, size - clue[-1] - 1):
      blank_known(dir, line_num, size - 1)

   start_mark = False
   for indx in range(size-1,size - 1 - clue[len(clue)-1],-1):
      if is_mark(dir, line_num, indx):
         start_mark = True
      if start_mark:
         mark_known(dir, line_num,indx)

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

def init_solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_guessing('r', puzzle_size, line, row_index)
      row_index += 1

   #print_puzzle(puzzle_size, puzzle_solve)

   for line in puzzle_clue_verticle:
      solve_guessing('c', puzzle_size, line, col_index)
      col_index += 1
def solve_table_edges():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_edge('r', puzzle_size, line, row_index)
      row_index += 1

   #print_puzzle(puzzle_size, puzzle_solve)

   for line in puzzle_clue_verticle:
      solve_edge('c', puzzle_size, line, col_index)
      col_index += 1
def solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_line('r', puzzle_size, line, row_index)
      row_index += 1

   #print_puzzle(puzzle_size, puzzle_solve)

   for line in puzzle_clue_verticle:
      solve_line('c', puzzle_size, line, col_index)
      col_index += 1

def promote_to_known(dir, i, j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if (dir == 'r'):
         if puzzle_solve[i][j] == 'm':
            puzzle_solve[i][j] = 'M'
         elif puzzle_solve[i][j] == 'b':
            puzzle_solve[i][j] = '0'
      elif dir == 'c':
         if puzzle_solve[j][i] == 'm':
            puzzle_solve[j][i] = 'M'
         elif puzzle_solve[j][i] == 'b':
            puzzle_solve[j][i] = '0'
def clear_unknown(dir, i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         if puzzle_solve[i][j] != 'M' and puzzle_solve[i][j] != '0':
            puzzle_solve[i][j] = '_'
      if dir == 'c':
         if puzzle_solve[j][i] != 'M' and puzzle_solve[j][i] != '0':
            puzzle_solve[j][i] = '_'
def guess_mark(dir, i,j,mark=''):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         if puzzle_solve[i][j] != 'M' and puzzle_solve[i][j] != '0':
            puzzle_solve[i][j] = 'm' + str(mark)
      elif dir == 'c':
         if puzzle_solve[j][i] != 'M' and puzzle_solve[j][i] != '0':
            puzzle_solve[j][i] = 'm' + str(mark)
def guess_blank(dir, i,j,blank=''):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         if puzzle_solve[i][j] != 'M' and puzzle_solve[i][j] != '0':
            puzzle_solve[i][j] = 'b' + str(blank)
      elif dir == 'c':
         if puzzle_solve[j][i] != 'M' and puzzle_solve[j][i] != '0':
            puzzle_solve[j][i] = 'b' + str(blank)
def mark_known(dir, i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         puzzle_solve[i][j] = 'M'
      elif dir == 'c':
         puzzle_solve[j][i] = 'M'
def blank_known(dir, i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         puzzle_solve[i][j] = '0'
      elif dir == 'c':
         puzzle_solve[j][i] = '0'
def compare_mark(dir, i,j,mark=''):  
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      mark_test = 'm' + str(mark)
      if puzzle_solve[i][j] == mark_test:
         if dir == 'r':
            puzzle_solve[i][j] = 'M'
         elif dir == 'c':
            puzzle_solve[j][i] = 'M'
         
def is_mark(dir, i,j):
   global puzzle_solve
   is_mark = False
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         if puzzle_solve[i][j] == 'M':
            is_mark = True
      if dir == 'c':
         if puzzle_solve[j][i] == 'M':
            is_mark = True

   return is_mark
def is_blank(dir, i,j):
   global puzzle_solve
   is_blank = False
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         if puzzle_solve[i][j] == '0':
            is_blank = True
      if dir == 'c':
         if puzzle_solve[j][i] == '0':
            is_blank = True

   return is_blank
def is_unknown(dir, i,j):
   global puzzle_solve
   is_unknown = False
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if dir == 'r':
         if puzzle_solve[i][j] == '_':
            is_unknown = True
      if dir == 'c':
         if puzzle_solve[j][i] == '_':
            is_unknown = True

   return is_unknown

def print_puzzle(size, puzzle):
   lead_str  = "    "
   for i in range(size):
      lead_str += str(i).rjust(2) + "   "   
   print lead_str

   for row in range(size):
      row_done = True
      for col in range(size):
         if puzzle[row][col] == "_":
            row_done = False
            break 

      if row_done:
         print str(row).rjust(2) + " " + str(puzzle[row])
      else:
         print str(row).rjust(2) + " " + str(puzzle[row]) + " " + str(puzzle_clue_horizontal[row])

   print "\n"
def print_remaining_clues(size, puzzle):
   clues_remaining = 0 
   for col in range(size):
      for row in range(size):
         if is_unknown('r', row, col):
            print "c " + str(col).rjust(2) + " " + str(puzzle_clue_verticle[col])
            clues_remaining += 1
            break

   return clues_remaining

puzzle_size = 25
puzzle_max_size = 25
puzzle_clue_horizontal = []
puzzle_clue_verticle = []
puzzle_solve = []
orig_stdout = sys.stdout

init_clues()

#for i in range(3):
clues_remaining = 1
while(clues_remaining > 0):
   #sys.stdout = open('solve_step_{}.txt'.format(i),'w')
   init_solve_table()
   solve_table_edges()
   solve_table()
   print_puzzle(puzzle_size, puzzle_solve)
   clues_remaining = print_remaining_clues(puzzle_size, puzzle_solve)
   try:
      m, x, y = raw_input("solve x y:").split(' ')
   except ValueError:
      m = None
   
   if m == 'm' or m == 'M':
      if is_unknown('r',int(x),int(y)):
         mark_known('r', int(x),int(y))
   elif m == 'b' or m == '0':
      if is_unknown('r',int(x),int(y)):
         blank_known('r', int(x),int(y))
   elif m == 's' or m == 'S':
      submit_puzzle(puzzle_size, puzzle_solve)
   else:
      print '{} is not a valid command'.format(m)
   #sys.stdout.close()

#sys.stdout = orig_stdout
print_puzzle(puzzle_size, puzzle_solve)
print_remaining_clues(puzzle_size, puzzle_solve)