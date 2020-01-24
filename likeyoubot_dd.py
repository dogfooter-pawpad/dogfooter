import ctypes as c
import sys
from screeninfo import get_monitors


class DDClass:
    dll = None

    @classmethod
    def get_dll(self, refresh=False):
        if DDClass.dll is not None and refresh is not True:
            return DDClass.dll

        dl_file = "DD64.dll"
        if sys.maxsize <= 2 ** 32:
            # 32 비트
            dl_file = "DD32.dll"

        try:
            DDClass.dll = c.WinDLL(dl_file)
        except:
            print(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            raise ValueError

        return DDClass.dll


class DDMouse:
    def __init__(self, dll):
        self.dll = dll
        self.dd_func_move = self.dll['DD_mov']
        self.dd_func_move.argtypes = (c.c_int, c.c_int)
        self.dd_func_move.restype = c.c_int
        self.dd_func_btn = self.dll['DD_btn']
        self.dd_func_btn.argtypes = [c.c_int]
        self.dd_func_btn.restype = c.c_int

        self.main_monitor_height = 0
        self.main_monitor_width = 0
        self.monitor_height = 0
        self.monitor_width = 0
        for m in get_monitors():
            if self.main_monitor_height == 0 and self.main_monitor_width == 0:
                self.main_monitor_height = m.height
                self.main_monitor_width = m.width

            if self.monitor_width < m.x + m.width:
                self.monitor_width = m.x + m.width
            if self.monitor_height < m.y + m.height:
                self.monitor_height = m.y + m.height

        self.monitor_x_ratio = self.main_monitor_width / self.monitor_width
        self.monitor_y_ratio = self.main_monitor_height / self.monitor_height

    def down(self):
        self.dd_func_btn(1)

    def up(self):
        self.dd_func_btn(2)

    def move(self, x, y):
        loc_x = x
        loc_x = int(loc_x * self.monitor_x_ratio)
        loc_y = y
        loc_y = int(loc_y * self.monitor_y_ratio)
        self.dd_func_move(loc_x, loc_y)
