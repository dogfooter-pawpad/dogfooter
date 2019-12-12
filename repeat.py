import pyautogui
import pickle
import time
import os
import win32api
import win32gui
import sys
import likeyoubot_resource as lybresource
import likeyoubot_win as lybwin
import likeyoubot_configure as lybconfigure
from PIL import ImageGrab


class LYBCheck():
    def __init__(self):
        self.filename = None
        self.window_title = None
        self.resource_manager = None
        self.anchor_x = -1
        self.anchor_y = -1
        self.bx = -1
        self.by = -1
        self.current_grab_window = None
        self.epb = None

    def execute(self):
        self.window_title = ".*" + ".*"

        window = lybwin.LYBWin('.*check.py.*')
        window.find_window_wildcard(self.window_title)
        if len(window.handle_list) < 1:
            print('Not found window:', self.window_title)
            sys.exit()

        # print(window.my_handle)

        # window.set_invisible(window.my_handle)
        # window.set_foreground_console(window.handle_list[0])
        window.set_foreground_console(window.handle_list[0])
        adj_x, adj_y = window.get_player_adjust(window.handle_list[0])
        self.anchor_x, self.anchor_y, self.bx, self.by = win32gui.GetWindowRect(window.handle_list[0])
        self.anchor_x += adj_x
        self.anchor_y += adj_y

        # x, y = pyautogui.position()
        # if pyautogui.pixel(self.anchor_x + 400, self.anchor_y + 240) == (0, 0, 0):
            # sys.exit(99)

        while True:
            x, y = pyautogui.position()
            position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + \
                           ' ' + str(pyautogui.pixel(x, y)).rjust(16) + \
                           '      ' + 'R-X: ' + str(x - self.anchor_x).rjust(4) + ' R-Y: ' + str(
                y - self.anchor_y).rjust(4)
            print(position_str, end='')
            print('\b' * len(position_str), end='', flush=True)

            time.sleep(0.5)


LYBCheck().execute()
