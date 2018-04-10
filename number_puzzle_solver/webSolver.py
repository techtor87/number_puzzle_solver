from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from time import sleep

from helper_functions import *
from guess_solver import *
from edge_solver import *
from line_solver import *

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
   global driver
   puzzle_max_size= 25
   puzzle_clue_horizontal = []
   puzzle_clue_verticle = []
   puzzle_solve = []

   set_helper_globals(puzzle_solve, puzzle_size)
   set_guess_solver_globals(puzzle_size,puzzle_clue_horizontal,puzzle_clue_verticle)
   set_edge_solver_globals(puzzle_size,puzzle_clue_horizontal,puzzle_clue_verticle)
   set_line_solver_globals(puzzle_size,puzzle_clue_horizontal,puzzle_clue_verticle)
   
   for i in range(puzzle_max_size):
       puzzle_clue_horizontal.append(0)
       puzzle_clue_verticle.append(0) 
   
   for i in range(puzzle_size):
      puzzle_row = []
      for j in range(puzzle_size):
         puzzle_row.append('_')
      puzzle_solve.append(puzzle_row)

   for y in range(1, puzzle_size+1):
      id_str = "X0Y" + str(y)
      puzzle_clue_horizontal[y-1] = map(int, driver.find_element_by_id(id_str).text.split(','))

   for x in range(1, puzzle_size+1):
      id_str = "X" + str(x) + "Y0"
      temp_str =  driver.find_element_by_id(id_str).text
      puzzle_clue_verticle[x-1] = map(int, temp_str.split('\n'))

def puzzle_login(size, diff, user=None, passwd=None):
   if size > 4 or diff > 4 or size < 0 or diff < 0:
      size = 0
      diff = 0

   global puzzle_size
   global puzzle_clue_horizontal
   global puzzle_clue_verticle
   global driver

   puzzle_size = 5*size + 5

   opts = ChromeOptions()
   opts.add_extension("C:/Users/210060583/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/3.27.0_0.crx")
   opts.add_argument("-start-maximized")
   driver = webdriver.Chrome(chrome_options=opts)
   driver.implicitly_wait(0)
   driver.get("http://numbergrids.puzzlebaron.com/init.php")
   #ActionChains(driver).key_down(Keys.CONTROL+ '1').key_up(Keys.CONTROL + '1').perform()
   #ActionChains(driver).send_keys(Keys.CONTROL+ '1').perform()

   # If SSO Page
   if "ssologin" in driver.current_url:
      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
      driver.find_element_by_id("username").send_keys("210060583")
      driver.find_element_by_id("password").send_keys("adel2018phikos")
      driver.find_element_by_id("password").submit()

   #login to site
   if user is not None and passwd is not None:
      driver.find_element_by_name("vb_login_username").send_keys(user)
      driver.find_element_by_name("vb_login_password").send_keys(passwd)
      driver.find_element_by_class_name("loginform-submit").click()

   #Select Puzzle Page
   WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "sg-slider")))
   size_slider = driver.find_element_by_id("sg-slider")
   difficulty_slider = driver.find_element_by_id("sd-slider")

   #Using Action Class
   ActionChains(driver).drag_and_drop_by_offset(size_slider, 50*(size-2), 0).perform()
   ActionChains(driver).drag_and_drop_by_offset(difficulty_slider, 50*(diff-2), 0).perform()
   
   if size == 0:
      expected_size = "5 x 5"
   elif size == 1:
      expected_size = "10 x 10"
   elif size == 2:
      expected_size = "15 x 15"
   elif size == 3:
      expected_size = "20 x 20"
   elif size == 4:
      expected_size = "25 x 25"
   else:
      expected_size = "not found"
   if str(driver.find_element_by_id("sel_grid").text) != expected_size:
      print "Grid size not correctly set"
      return -1
   
   if diff == 0:
      expected_diff = "Very Easy"
   elif diff == 1:
      expected_diff = "Moderate"
   elif diff == 2:
      expected_diff = "Challenging"
   elif diff == 3:
      expected_diff = "Difficult"
   elif diff == 4:
      expected_diff = "Fiendish"
   else:
      expected_diff = "not found"
   if str(driver.find_element_by_id("sel_diff").text) != expected_diff:
      print "Grid difficulty not correctly set"
      return -1

   driver.find_element_by_name("CreatePuzzle").click()

   #Confirm Puzzle Page
   driver.find_element_by_name("submit").click()
   

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

if __name__ == "__main__":

   parser = argparse.ArgumentParser()

   parser.add_argument('-s', '--size', type=int, required=True)
   parser.add_argument('-d', '--difficulty', type=int, required=True)
   parser.add_argument('-u', '--user', required=False)
   parser.add_argument('-p', '--password', required=False)
   args = parser.parse_args() 

   print args.size
   print args.difficulty

   if puzzle_login(args.size, args.difficulty, args.user, args.password) is -1:
       quit() 

   init_clues()
   clues_remaining = 1
   while(clues_remaining > 0):
      print "starting loop"
      read_puzzle()
      init_solve_table()
      solve_table_edges()
      solve_table()
      #print_puzzle(puzzle_size, puzzle_solve)
      submit_puzzle()
      clues_remaining = remaining_clues(puzzle_size, puzzle_solve)
      print clues_remaining
      driver.find_element_by_id("check_button").click()
      sleep(5)