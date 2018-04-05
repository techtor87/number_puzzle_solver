
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
            if puzzle_solve[i][j] == '_':
               puzzle_solve[i][j] = 'm' + str(mark)
            #else:
            #   puzzle_solve[i][j] += ' m' + str(mark)
      elif dir == 'c':
         if puzzle_solve[j][i] != 'M' and puzzle_solve[j][i] != '0':
            if puzzle_solve[j][i] == '_':
               puzzle_solve[j][i] = 'm' + str(mark)
            #else:
            #   puzzle_solve[j][i] += ' m' + str(mark)

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
      #if dir == 'r':
      #   str_list = puzzle_solve[i][j].split(' ')
      #   if len(str_list) > 1:
      #      if str_list[0] == str_list[1]:
      #         puzzle_solve[i][j] = 'M'
      #if dir == 'c':
      #   str_list = puzzle_solve[j][i].split(' ')
      #   if len(str_list) > 1:
      #      if str_list[0] == str_list[1]:
      #         puzzle_solve[j][i] = 'M'

      mark_test = 'm' + str(mark)
      if dir == 'r':
         if puzzle_solve[i][j] == mark_test:
            puzzle_solve[i][j] = 'M'
      elif dir == 'c':
         if puzzle_solve[j][i] == mark_test:
            puzzle_solve[j][i] = 'M'

def compare_blank(dir, i,j,mark=''):  
   global puzzle_solve
   if i < puzzle_size and j < puzzle_size and i >= 0 and j >= 0:
      mark_test = 'b' + str(mark)
      if puzzle_solve[i][j] == mark_test:
         if dir == 'r':
            puzzle_solve[i][j] = '0'
         elif dir == 'c':
            puzzle_solve[j][i] = '0'
         
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