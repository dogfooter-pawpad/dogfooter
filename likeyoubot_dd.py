import ctypes as c
from ctypes import CDLL
import sys
from screeninfo import get_monitors
import traceback


class DDClass:
    dll = None
    dd_func_move = None
    dd_func_btn = None
    op_count = 0

    @classmethod
    def get_dll(cls, refresh=False):
        if DDClass.dll is not None and refresh is not True:
            return [DDClass.dll, DDClass.dd_func_move, DDClass.dd_func_btn, DDClass.op_count]

        dl_file = "DD64.dll"
        if sys.maxsize <= 2 ** 32:
            # 32 비트
            dl_file = "DD32.dll"

        try:
            DDClass.dll = c.WinDLL(dl_file)
        except:
            print(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return None, None, None, 0

        DDClass.dd_func_move = DDClass.dll['DD_mov']
        DDClass.dd_func_move.argtypes = (c.c_int, c.c_int)
        DDClass.dd_func_move.restype = c.c_int
        DDClass.dd_func_btn = DDClass.dll['DD_btn']
        DDClass.dd_func_btn.argtypes = [c.c_int]
        DDClass.dd_func_btn.restype = c.c_int

        DDClass.op_count = 0

        print("DEBUG----> Loaded", DDClass.op_count)
        return [DDClass.dll, DDClass.dd_func_move, DDClass.dd_func_btn, DDClass.op_count]

    @classmethod
    def free(cls, dll):
        print("free CDLL")
        CDLL("DD64.dll")

class DDMouse:
    def __init__(self, dll, mov, btn):
        self.dll = dll
        self.mov = mov
        self.btn = btn

        self.main_monitor_height = 0
        self.main_monitor_width = 0
        self.monitor_height = 0
        self.monitor_width = 0
        self.monitor_x_ratio = 1.0
        self.monitor_y_ratio = 1.0
        for m in get_monitors():
            if self.main_monitor_height == 0 and self.main_monitor_width == 0:
                self.main_monitor_height = m.height
                self.main_monitor_width = m.width

            if self.monitor_width < m.x + m.width:
                self.monitor_width = m.x + m.width
            if self.monitor_height < m.y + m.height:
                self.monitor_height = m.y + m.height

        if self.monitor_width > 0 and self.main_monitor_width > 0 and self.monitor_height > 0 and self.main_monitor_height > 0:
            self.monitor_x_ratio = self.main_monitor_width / self.monitor_width
            self.monitor_y_ratio = self.main_monitor_height / self.monitor_height

    def down(self):
        try:
            self.btn(1)
        except:
            print(traceback.format_exc())

    def up(self):
        try:
            self.btn(2)
        except:
            print(traceback.format_exc())

    def move(self, x, y):
        loc_x = x
        loc_x = int(loc_x * self.monitor_x_ratio)
        loc_y = y
        loc_y = int(loc_y * self.monitor_y_ratio)
        try:
            self.mov(loc_x, loc_y)
        except:
            print(traceback.format_exc())
