
def puzzle(dir, i, j, val=None):
   global puzzle_solve
   if dir == 'r':
      if val != None:
         puzzle_solve[i][j] = val
      else:
         return puzzle_solve[i][j]
   elif dir == 'c':
      if val != None:
         puzzle_solve[j][i] = val
      else:
         return puzzle_solve[j][i]

def set_helper_globals(puzzle, size):
   global puzzle_size
   global puzzle_solve
   puzzle_solve = puzzle
   puzzle_size = size

def promote_to_known(dir, i, j):
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) == 'm':
         puzzle(dir,i,j, 'M')
      elif puzzle(dir,i,j) == 'b':
         puzzle(dir,i,j, '0')

def clear_unknown(dir, i,j):
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) != 'M' and puzzle(dir,i,j) != '0':
         puzzle(dir,i,j,'_')


def guess_mark(dir, i,j,mark=''):
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) != 'M' and puzzle(dir,i,j) != '0':
         if puzzle(dir,i,j) == '_':
            puzzle(dir,i,j, 'm' + str(mark))
         #else:
         #   puzzle(dir,i,j) += ' m' + str(mark)

def guess_blank(dir, i,j,blank=''):
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) != 'M' and puzzle(dir,i,j) != '0':
         puzzle(dir,i,j, 'b' + str(blank))

def mark_known(dir, i,j):
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      puzzle(dir, i, j, 'M')
     
def blank_known(dir, i,j):
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      puzzle(dir,i,j,'0')

def compare_mark(dir, i,j,mark=''):  
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      #if dir == 'r':
      #   str_list = puzzle(dir,i,j).split(' ')
      #   if len(str_list) > 1:
      #      if str_list[0] == str_list[1]:
      #         puzzle(dir,i,j) = 'M'
      #if dir == 'c':
      #   str_list = puzzle(dir,i,j).split(' ')
      #   if len(str_list) > 1:
      #      if str_list[0] == str_list[1]:
      #         puzzle(dir,i,j) = 'M'

      mark_test = 'm' + str(mark)
      if puzzle(dir, i, j) == mark_test:
         puzzle(dir, i, j, 'M')


def compare_blank(dir, i,j,mark=''):  
   global puzzle_size
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      mark_test = 'b' + str(mark)
      if puzzle(dir,i,j) == mark_test:
         puzzle(dir, i, j, '0')
         
         
def is_mark(dir, i,j):
   global puzzle_size
   is_mark = False
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) == 'M':
         is_mark = True
      
   return is_mark

def is_blank(dir, i,j):
   global puzzle_size
   is_blank = False
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) == '0':
         is_blank = True 

   return is_blank

def is_unknown(dir, i,j):
   global puzzle_size
   is_unknown = False
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      if puzzle(dir,i,j) == '_':
         is_unknown = True

   return is_unknown