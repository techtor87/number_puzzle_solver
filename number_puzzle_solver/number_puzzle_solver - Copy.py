import sys

def init_clues ():
   global puzzle_size
   for i in range(puzzle_max_size):
       puzzle_clue_horizontal.append(0)
       puzzle_clue_verticle.append(0)

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


def init_solve_row(size, clue_row, line_num):
   more_than_one_clue = False
   index = 0
   if line_num >= size:
      return

   for clue_indx in range(len(clue_row)):
      if more_than_one_clue :
         guess_blank(line_num,index)
         index += 1
      else:
         more_than_one_clue = True

      for i in range(clue_row[clue_indx]):
         guess_mark(line_num,index,clue_indx)
         index += 1
      
   index = size -1
   more_than_one_clue = False
   for clue_indx in range(len(clue_row)-1,-1,-1):
      
      if more_than_one_clue :
         #guess_blank(line_num,index)
         index -= 1
      else:
         more_than_one_clue = True

      for i in range(clue_row[clue_indx]):
         compare_mark(line_num,index,clue_indx)
         index -= 1

   for indx in range(size):
      clear_unknown(line_num,indx)

def init_solve_col(size, clue_col, line_num):
   more_than_one_clue = False
   index = 0
   if line_num >= size:
      return

   for clue_indx in range(len(clue_col)):
      if more_than_one_clue :
         guess_blank(index, line_num)
         index += 1
      else:
         more_than_one_clue = True

      for i in range(clue_col[clue_indx]):
         guess_mark(index, line_num,clue_indx)
         index += 1
      
   index = size -1
   more_than_one_clue = False
   for clue_indx in range(len(clue_col)-1,-1,-1):
      
      if more_than_one_clue :
         #guess_blank(line_num,index)
         index -= 1
      else:
         more_than_one_clue = True

      for i in range(clue_col[clue_indx]):
         compare_mark(index,line_num,clue_indx)
         index -= 1

   for indx in range(size):
      clear_unknown(indx,line_num)

def solve_row_edge(size, clue_row, line_num):
   if(line_num >= size):
      return -1

   first_indx = 0
   last_indx = size - 1
   #check first column 
   if is_mark(line_num, first_indx):
      index = 0
      for i in range(clue_row[first_indx]):
         mark_known(line_num,index)
         index += 1
      blank_known(line_num, index)
   
   
   #check last column 
   if is_mark(line_num, last_indx):
      index = last_indx
      for i in range(clue_row[len(clue_row)-1]):
         mark_known(line_num,index)
         index -= 1
      blank_known(line_num, index)

   start_mark = False
   for indx in range(clue_row[0]):
      if is_mark(line_num, indx):
         start_mark = True
      if start_mark:
         mark_known(line_num,indx)

   if clue_row[0] == 1 and is_mark(line_num,1):
      blank_known(line_num, 0)
      blank_known(line_num, 2)

   if clue_row[-1] == 1 and is_mark(line_num, size - 2):
      blank_known(line_num, size - 1)
      blank_known(line_num, size - 3)

   start_mark = False
   for indx in range(size-1,size - 1 - clue_row[len(clue_row)-1],-1):
      if is_mark(line_num, indx):
         start_mark = True
      if start_mark:
         mark_known(line_num,indx)

def solve_col_edge(size, clue_col, line_num):
   if(line_num >= size):
      return -1

   first_indx = 0
   last_indx = size - 1
   #check first row 
   if puzzle_solve[first_indx][line_num] == 'M':
      index = 0
      for i in range(clue_col[first_indx]):
         mark_known(index,line_num)
         index += 1
      blank_known(index, line_num)
   
   
   #check last row 
   if puzzle_solve[last_indx][line_num] == 'M':
      index = last_indx
      for i in range(clue_col[len(clue_col)-1]):
         mark_known(index, line_num)
         index -= 1
      blank_known(index, line_num)

   start_mark = False
   for indx in range(clue_col[0]):
      if puzzle_solve[indx][line_num] == 'M':
         start_mark = True
      if start_mark:
         mark_known(indx, line_num)
 
   if clue_col[0] == 1 and puzzle_solve[1][line_num] == 'M':
      blank_known(0, line_num)
      blank_known(2, line_num)

   if clue_col[-1] == 1 and puzzle_solve[-2][line_num] == 'M':
      blank_known(size - 1,line_num)
      blank_known(size - 3,line_num)

   start_mark = False
   for indx in range(size-1, size - 1 - clue_col[len(clue_col)-1],-1):
      if puzzle_solve[indx][line_num] == 'M':
         start_mark = True
      if start_mark:
         mark_known(indx, line_num)

def solve_row(size, clue_row, line_num):
   if(line_num >= size):
      return -1

   clue_indx = 0
   indx = 0
   #check forward
   while indx < size:
      if puzzle_solve[line_num][indx] == 'M':
         for clue_size in range(clue_row[clue_indx]):
            mark_known(line_num,indx)
            indx += 1
         blank_known(line_num,indx)
         clue_indx +=1
      elif puzzle_solve[line_num][indx] == '0':
         indx += 1
      else:
         if clue_indx == len(clue_row):
            blank_known(line_num, indx)
            indx += 1
         else:
            break

   #check backward
   indx = size - 1
   clue_indx = len(clue_row) - 1
   while indx >= 0:
      if puzzle_solve[line_num][indx] == 'M':
         for clue_size in range(clue_row[clue_indx]):
            mark_known(line_num,indx)
            indx -= 1
         blank_known(line_num,indx)
         clue_indx -=1
      elif puzzle_solve[line_num][indx] == '0':
         indx -= 1
      else:
         if clue_indx == -1:
            blank_known(line_num, indx)
            indx -= 1
         else:
            break

   cur_mark_cnt = 0
   longest_clue = max(clue_row)
   for indx in range(size):
      if puzzle_solve[line_num][indx] == 'M':
         cur_mark_cnt += 1
      else:
         if cur_mark_cnt == longest_clue:
            blank_known(line_num,indx)
            blank_known(line_num,indx - cur_mark_cnt -1)
         #if cur_mark_cnt > longest_mark:
         #   longest_mark = cur_mark_cnt
         #   longest_mark_end = indx - 1
         #   longest_mark_start = longest_mark_end - longest_mark
         cur_mark_cnt = 0

   #check if all Marks done
   mark_count = 0
   for indx in range(size):
      if puzzle_solve[line_num][indx] == 'M':
         mark_count += 1

   if mark_count == sum(clue_row):
      for indx in range(size):
         if puzzle_solve[line_num][indx] == '_':
            blank_known(line_num,indx)

def solve_col(size, clue_col, line_num):
   if(line_num >= size):
      return -1

   clue_indx = 0
   indx = 0
   #check forward
   while indx < size:
      if puzzle_solve[indx][line_num] == 'M':
         for clue_size in range(clue_col[clue_indx]):
            mark_known(indx,line_num)
            indx += 1
         blank_known(indx,line_num)
         clue_indx +=1
      elif puzzle_solve[indx][line_num] == '0':
         indx += 1
      else:
         if clue_indx == len(clue_col):
            blank_known(indx,line_num)
            indx += 1
         else:
            break

   indx = size - 1
   clue_indx = len(clue_col) - 1
   while indx >= 0:
      if puzzle_solve[indx][line_num] == 'M':
         for clue_size in range(clue_col[clue_indx]):
            mark_known(indx,line_num)
            indx -= 1
         blank_known(indx,line_num)
         clue_indx -=1
      elif puzzle_solve[indx][line_num] == '0':
         indx -= 1
      else:
         if clue_indx == -1:
            blank_known(indx,line_num)
            indx -= 1
         else:
            break

   cur_mark_cnt = 0
   longest_clue = max(clue_col)
   for indx in range(size):
      if puzzle_solve[indx][line_num] == 'M':
         cur_mark_cnt += 1
      else:
         if cur_mark_cnt == longest_clue:
            blank_known(indx,line_num)
            blank_known(indx - cur_mark_cnt -1,line_num)
         #if cur_mark_cnt > longest_mark:
         #   longest_mark = cur_mark_cnt
         #   longest_mark_end = indx - 1
         #   longest_mark_start = longest_mark_end - longest_mark
         cur_mark_cnt = 0

   mark_count = 0
   for indx in range(size):
      if puzzle_solve[indx][line_num] == 'M':
         mark_count += 1

   if mark_count == sum(clue_col):
      for indx in range(size):
         if puzzle_solve[indx][line_num] == '_':
            blank_known(indx,line_num)

def init_solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      init_solve_row(puzzle_size, line, row_index)
      row_index += 1

   #print_puzzle(puzzle_size, puzzle_solve)

   for line in puzzle_clue_verticle:
      init_solve_col(puzzle_size, line, col_index)
      col_index += 1

def solve_table_edges():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_row_edge(puzzle_size, line, row_index)
      row_index += 1

   #print_puzzle(puzzle_size, puzzle_solve)

   for line in puzzle_clue_verticle:
      solve_col_edge(puzzle_size, line, col_index)
      col_index += 1

def solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_row(puzzle_size, line, row_index)
      row_index += 1

   #print_puzzle(puzzle_size, puzzle_solve)

   for line in puzzle_clue_verticle:
      solve_col(puzzle_size, line, col_index)
      col_index += 1

def promote_to_known(i, j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] == 'm':
         puzzle_solve[i][j] = 'M'
      elif puzzle_solve[i][j] == 'b':
         puzzle_solve[i][j] = '0'
def clear_unknown(i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] != 'M' and puzzle_solve[i][j] != '0':
         puzzle_solve[i][j] = '_'
def guess_mark(i,j,mark=''):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] != 'M' and puzzle_solve[i][j] != '0':
         puzzle_solve[i][j] = 'm' + str(mark)
def guess_blank(i,j,blank=''):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] != 'M' and puzzle_solve[i][j] != '0':
         puzzle_solve[i][j] = 'b' + str(blank)
def mark_known(i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      puzzle_solve[i][j] = 'M'
def blank_known(i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      puzzle_solve[i][j] = '0'
def compare_mark(i,j,mark=''):  
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      mark_test = 'm' + str(mark)
      if puzzle_solve[i][j] == mark_test:
         puzzle_solve[i][j] = 'M'
def is_mark(i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] == 'M':
         return True
      else:
         return False
def is_blank(i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] == '0':
         return True
      else:
         return False
def is_unknown(i,j):
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle_solve[i][j] == '_':
         return True
      else:
         return False

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
   for col in range(size):
      for row in range(size):
         if is_unknown(row,col):
            print "c " + str(col).rjust(2) + " " + str(puzzle_clue_verticle[col])
            break
     

puzzle_size = 25
puzzle_max_size = 25
puzzle_clue_horizontal = []
puzzle_clue_verticle = []
puzzle_solve = []
orig_stdout = sys.stdout

init_clues()

#for i in range(3):
while(1):
   #sys.stdout = open('solve_step_{}.txt'.format(i),'w')
   init_solve_table()
   solve_table_edges()
   solve_table()
   print_puzzle(puzzle_size, puzzle_solve)
   print_remaining_clues(puzzle_size, puzzle_solve)
   try:
      m, x, y = raw_input("solve x y:").split(' ')
   except ValueError:
      m = None

   if m == 'm' or m == 'M':
      mark_known(int(x),int(y))
   elif m == 'b' or m == '0':
      blank_known(int(x),int(y))
   else:
      print '{} is not a valid command'.format(m)
   #sys.stdout.close()

#sys.stdout = orig_stdout
print_puzzle(puzzle_size, puzzle_solve)
print_remaining_clues(puzzle_size, puzzle_solve)