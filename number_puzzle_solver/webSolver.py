from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def enum(**named_values):
   return type('Enum', (), named_values)

size = enum(FIVE=0, TEN=1, FIFTEEN=2, TWENTY=3, TWENTYFIVE=4)
difficulty = enum(EASY=0, MODERATE=1, CHALLENGING=2, DIFFICULT=3, FIENDISH=4)

def init_clues ():
   global puzzle_size
   global puzzle_max_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   global puzzle_solve
   puzzle_size = 25
   puzzle_max_size= 25
   puzzle_clue_horizontal = []
   puzzle_clue_verticle = []
   puzzle_solve = []

   for i in range(puzzle_max_size):
       puzzle_clue_horizontal.append(0)
       puzzle_clue_verticle.append(0)

def start_puzzle(size, diff):
   if size > 4 or diff > 4 or size < 0 or diff < 0:
      size = 0
      diff = 0

   init_clues()
   global puzzle_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   global driver

   puzzle_size = 5*size + 5

   for i in range(puzzle_size):
      puzzle_row = []
      for j in range(puzzle_size):
         puzzle_row.append('_')
      puzzle_solve.append(puzzle_row)

   opts = ChromeOptions()
   opts.add_extension("C:/Users/210060583/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/3.27.0_0.crx")
   opts.add_argument("-start-maximized")
   driver = webdriver.Chrome(chrome_options=opts)
   driver.implicitly_wait(0)
   driver.get("http://numbergrids.puzzlebaron.com/init.php")
   #ActionChains(driver).key_down(Keys.CONTROL+ '1').key_up(Keys.CONTROL + '1').perform()
   #ActionChains(driver).send_keys(Keys.CONTROL+ '1').perform()

   if "ssologin" in driver.current_url:
      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
      driver.find_element_by_id("username").send_keys("210060583")
      driver.find_element_by_id("password").send_keys("adel2018phikos")
      driver.find_element_by_id("password").submit()

   WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "sg-slider")))
   size_slider = driver.find_element_by_id("sg-slider")
   difficulty_slider = driver.find_element_by_id("sd-slider")

   #Using Action Class
   ActionChains(driver).drag_and_drop_by_offset(size_slider, 50*(size-2), 0).perform()
   ActionChains(driver).drag_and_drop_by_offset(difficulty_slider, 50*(diff-2), 0).perform()
  
   driver.find_element_by_name("CreatePuzzle").click()
   driver.find_element_by_name("submit").click()
   
   for y in range(1, puzzle_size+1):
      id_str = "X0Y" + str(y)
      puzzle_clue_horizontal[y-1] = map(int, driver.find_element_by_id(id_str).text.split(','))

   for x in range(1, puzzle_size+1):
      id_str = "X" + str(x) + "Y0"
      temp_str =  driver.find_element_by_id(id_str).text
      puzzle_clue_verticle[x-1] = map(int, temp_str.split('\n'))

def init_solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_guessing('r', puzzle_size, line, row_index)
      row_index += 1

   for line in puzzle_clue_verticle:
      solve_guessing('c', puzzle_size, line, col_index)
      col_index += 1
def solve_table_edges():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_edge('r', puzzle_size, line, row_index)
      row_index += 1

   for line in puzzle_clue_verticle:
      solve_edge('c', puzzle_size, line, col_index)
      col_index += 1
def solve_table():
   row_index = 0
   col_index = 0
   for line in puzzle_clue_horizontal:
      solve_line('r', puzzle_size, line, row_index)
      row_index += 1

   for line in puzzle_clue_verticle:
      solve_line('c', puzzle_size, line, col_index)
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
            guess_mark(dir, line_num,index,clue_indx)
            index -= 1
         clue_indx -= 1
      #else:
      #   compare_blank(dir, line_num,index) 

   #for indx in range(size):
   #   compare_mark(dir,line_num, index)

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
def remaining_clues(size, puzzle, do_print=False):
   clues_remaining = 0 
   for col in range(size):
      for row in range(size):
         if is_unknown('r', row, col):
            if do_print:
               print "c " + str(col).rjust(2) + " " + str(puzzle_clue_verticle[col])
            clues_remaining += 1
            break

   return clues_remaining
def submit_puzzle():
   global driver
   for y in range (1, puzzle_size+1):
      for x in range(1, puzzle_size+1):
         id_str = "X" + str(x) + "Y" + str(y)
         if is_mark('r',y-1,x-1):
            element = driver.find_element_by_id(id_str)
            
            if "marked1" not in element.get_attribute('class'):
               element.click()
         elif is_blank('r', y-1, x-1):
            element = driver.find_element_by_id(id_str)
            if "marked2" not in element.get_attribute('class'):
               ActionChains(driver).context_click(element).perform()
def read_puzzle():
   global driver
   for y in range (1, puzzle_size+1):
      for x in range(1, puzzle_size+1):
         if is_unknown('r', y-1, x-1):
            id_str = "X" + str(x) + "Y" + str(y)
            element = driver.find_element_by_id(id_str)
            if "marked1" in element.get_attribute('class'):
               mark_known('r', y-1, x-1)
            elif "marked2" in element.get_attribute('class'):
               blank_known('r', y-1, x-1)


start_puzzle(size.FIFTEEN,difficulty.DIFFICULT)
clues_remaining = 1
while(clues_remaining > 0):
   #sys.stdout = open('solve_step_{}.txt'.format(i),'w')
   print "starting loop"
   read_puzzle()
   init_solve_table()
   solve_table_edges()
   solve_table()
   #print_puzzle(puzzle_size, puzzle_solve)
   submit_puzzle()
   clues_remaining = remaining_clues(puzzle_size, puzzle_solve)
   print clues_remaining
   sleep(2.5)
   #try:
   #   m, x, y = raw_input("solve x y:").split(' ')
   #except ValueError:
   #   m = None
   
   #if m == 'm' or m == 'M':
   #   if is_unknown('r',int(x),int(y)):
   #      mark_known('r', int(x),int(y))
   #elif m == 'b' or m == '0':
   #   if is_unknown('r',int(x),int(y)):
   #      blank_known('r', int(x),int(y))
   #elif m == 's' or m == 'S':
   #   submit_puzzle(puzzle_size, puzzle_solve)
   #elif m == 'e' or m == 'E':
   #   break
   #else:
   #   print '{} is not a valid command'.format(m)
   #sys.stdout.close()