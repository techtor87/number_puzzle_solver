import sys
from ctypes import *
import time

class _point_t(Structure):
   _fields_ = [
               ('x', c_long),
               ('y', c_long),
               ]

class mouse_control(object):
   def l_click_mouse(self, x, y):
      windll.user32.SetCursorPos(int(x),int(y))
      windll.user32.mouse_event(2,0,0,0,0)
      windll.user32.mouse_event(4,0,0,0,0)

   def r_click_mouse(self, x, y):
      windll.user32.SetCursorPos(int(x),int(y))
      windll.user32.mouse_event(8,0,0,0,0)
      windll.user32.mouse_event(16,0,0,0,0)

   def get_cursor_position(self):
      temp_point = _point_t()
      windll.user32.GetCursorPos(pointer(temp_point))
      print temp_point.x, temp_point.y
      return temp_point






