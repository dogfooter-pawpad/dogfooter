import time
import sys
import win32gui
import win32api
import win32con
import re
import pyautogui
import win32ui
from ctypes import windll
from PIL import Image
from likeyoubot_configure import LYBConstant as lybconstant
import random


class LYBWin:
    WIDTH = 960
    HEIGHT = 540
    NOX_EXTRA_WIDTH = 2
    NOX_EXTRA_HEIGHT = 30
    NOX_EXTRA_UHD_HEIGHT = 46

    def __init__(self, my_name, configure=None):
        # self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.handle_list = []
        self.multi_window_handle_dic = {}
        self.side_window_handle_list = []
        self.parent_handle_dic = {}
        self.side_window_dic = {}
        self.inner_handle_list = []
        self.current_window_list = []
        self.my_handle = None
        self.my_name = my_name
        self.configure = configure

    def find_window(self, class_name, window_name=None):
        handle = win32gui.FindWindow(class_name, window_name)
        if not handle in self.handle_list:
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = win32gui.GetWindowRect(handle)
            if abs(bottom_right_x - top_left_x - LYBWin.WIDTH) < 50 and abs(
                                    bottom_right_y - top_left_y - LYBWin.HEIGHT) < 100:
                self.handle_list.append(handle)

        handle = win32gui.FindWindow(class_name, 'Nox')
        if not hwnd in self.side_window_handle_list:
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = win32gui.GetWindowRect(hwnd)
            if abs(bottom_right_x - top_left_x) - 36 < 40 and abs(bottom_right_y - top_left_y - LYBWin.HEIGHT) < 40:
                self.side_window_handle_list.append(hwnd)

    def callback_child_process(self, hwnd, lParam):

        s = win32gui.GetWindowText(hwnd)
        if len(s) > 0:
            if not hwnd in self.current_window_list:
                # print(win32gui.GetWindowText(lParam), '  :  ', win32gui.GetWindowText(hwnd))
                self.current_window_list.append(hwnd)

        return 1

    def callback_momo_child_process(self, hwnd, lParam):
        s = win32gui.GetWindowText(hwnd)
        if len(s) > 3:
            # (s_x, s_y, e_x, e_y) = win32gui.GetWindowRect(hwnd)
            # w_width = e_x - s_x
            # w_height = e_y - s_y
            # print("MOMO Render: " + str(win32gui.GetWindowText(hwnd)) + '[' + str ( (s_x, s_y) ) + '] [' + str( (w_width, w_height) ) + ']')
            if not hwnd in self.handle_list:
                self.handle_list.append(hwnd)
                # print(lParam)
                self.parent_handle_dic[hwnd] = lParam
        return 1

    def callback_memu_child_process(self, hwnd, lParam):
        s = win32gui.GetWindowText(hwnd)
        (s_x, s_y, e_x, e_y) = win32gui.GetWindowRect(hwnd)
        w_width = e_x - s_x
        w_height = e_y - s_y
        # print("MEMU Render: " + str(win32gui.GetWindowText(hwnd)) + '[' + str(hwnd) + '] [' + str((s_x, s_y)) + '] [' + str((w_width, w_height)) + ']')
        if 'RenderWindowWindow' in s:
            if not hwnd in self.handle_list:
                self.handle_list.append(hwnd)
                # print(lParam)
                self.parent_handle_dic[hwnd] = lParam

        return 1

    def callback_nox_child_process(self, hwnd, lParam):

        s = win32gui.GetWindowText(hwnd)
        # print('-----------', s)
        # print("nox, child_hwnd: %d   txt: %s rect: %s" % (hwnd, s, str(win32gui.GetWindowRect(hwnd))))
        if not hwnd in self.handle_list and 'ScreenBoardClassWindow' in s:
            self.handle_list.append(hwnd)
            # print(lParam)
            self.parent_handle_dic[hwnd] = lParam
        return 1

    def set_window_pos(self, hwnd, x, y):
        (s_x, s_y, e_x, e_y) = win32gui.GetWindowRect(hwnd)
        width = e_x - s_x
        height = e_y - s_y

        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, win32con.SWP_SHOWWINDOW)

    def getInnerWindow(self, hwnd):
        (s_x, s_y, e_x, e_y) = win32gui.GetWindowRect(hwnd)
        self.inner_handle_list = []
        win32gui.EnumWindows(self.inner_window_enum_callback, (s_x, s_y, e_x, e_y))

        return self.inner_handle_list

    def inner_window_enum_callback(self, hwnd, parent_rect):
        (s_x, s_y, e_x, e_y) = parent_rect
        if win32gui.IsWindowVisible(hwnd) != 0:
            (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = win32gui.GetWindowRect(hwnd)

            if (s_x < top_left_x and s_x < bottom_right_x and
                        e_x > top_left_x and e_x > bottom_right_x and
                        s_y < top_left_y and s_y < bottom_right_y and
                        e_y > top_left_y and e_y > bottom_right_y):
                (x, y, x2, y2) = win32gui.GetWindowRect(hwnd)
                w_width = x2 - x
                w_height = y2 - y
                if w_height > 0 and w_width > 0:
                    self.inner_handle_list.append(hwnd)

    def _window_enum_callback(self, hwnd, wildcard):

        if win32gui.IsWindowVisible(hwnd) != 0:
            (s_x, s_y, e_x, e_y) = win32gui.GetWindowRect(hwnd)
            w_width = e_x - s_x
            w_height = e_y - s_y
            # print(str(win32gui.GetWindowText(hwnd)) + '[' + str ( (s_x, s_y) ) + '] [' + str( (w_width, w_height) ) + ']')

        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None and win32gui.IsWindowVisible(hwnd) != 0:
            # print('--------------------> !!! found window DEBUG2 new : ', wildcard, str(win32gui.GetWindowText(hwnd)), ':', self.handle_list, ':')
            if not hwnd in self.handle_list:
                (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = win32gui.GetWindowRect(hwnd)
                # print('--------------------> !!! found window DEBUG3 new : ', (top_left_x, top_left_y, bottom_right_x, bottom_right_y))
                # print(win32gui.GetWindowText(hwnd), abs(bottom_right_y - top_left_y))

                if (abs(bottom_right_x - top_left_x - LYBWin.WIDTH) < 100 and
                            abs(bottom_right_y - top_left_y - LYBWin.HEIGHT) < 100
                    ):

                    diff_width = abs(top_left_x - bottom_right_x)
                    diff_height = abs(bottom_right_y - top_left_y)

                    print(win32gui.GetWindowText(hwnd), diff_width, diff_height)

                    if diff_height == LYBWin.HEIGHT + 34 and diff_width == LYBWin.WIDTH + 4:
                        # 녹스 FHD
                        self.handle_list.append(hwnd)
                    elif diff_height == LYBWin.HEIGHT + 50 and diff_width == LYBWin.WIDTH + 4:
                        # 녹스 UHD
                        self.handle_list.append(hwnd)
                    elif diff_height == LYBWin.HEIGHT + 38 and diff_width == LYBWin.WIDTH + 38:
                        # LDPlayer FHD
                        win32gui.EnumChildWindows(hwnd, self.callback_momo_child_process, hwnd)
                    elif diff_height == LYBWin.HEIGHT + 56 and diff_width == LYBWin.WIDTH + 56:
                        # LDPlayer UHD
                        win32gui.EnumChildWindows(hwnd, self.callback_momo_child_process, hwnd)
                    elif diff_height == LYBWin.HEIGHT + 30 and diff_width == LYBWin.WIDTH + 38:
                        # MEmu FHD Portrait
                        win32gui.EnumChildWindows(hwnd, self.callback_memu_child_process, hwnd)
                    elif diff_height == LYBWin.HEIGHT + 34 and diff_width == LYBWin.WIDTH + 40:
                        # MEmu FHD Landscape
                        win32gui.EnumChildWindows(hwnd, self.callback_memu_child_process, hwnd)
                    elif abs(bottom_right_y - top_left_y) == LYBWin.HEIGHT + 38:
                        # LDPlayer FHD
                        win32gui.EnumChildWindows(hwnd, self.callback_momo_child_process, hwnd)
                    elif abs(bottom_right_y - top_left_y) == LYBWin.HEIGHT + 56:
                        # LDPlayer UHD
                        win32gui.EnumChildWindows(hwnd, self.callback_momo_child_process, hwnd)
                    elif abs(bottom_right_y - top_left_y) == LYBWin.HEIGHT + 34:
                        # Nox FHD
                        self.handle_list.append(hwnd)
                    elif abs(bottom_right_y - top_left_y) == LYBWin.HEIGHT + 37:
                        # Nox UHD
                        self.handle_list.append(hwnd)
                        # win32gui.EnumChildWindows(hwnd, self.callback_nox_child_process, hwnd)
                    elif abs(bottom_right_y - top_left_y) == LYBWin.HEIGHT + 50:
                        # Nox UHD
                        self.handle_list.append(hwnd)
                        # win32gui.EnumChildWindows(hwnd, self.callback_nox_child_process, hwnd)
                    elif abs(bottom_right_x - top_left_x) == LYBWin.WIDTH + 40:
                        # Memu
                        win32gui.EnumChildWindows(hwnd, self.callback_memu_child_process, hwnd)

                        # if re.match('Nox', str(win32gui.GetWindowText(hwnd))):
                        #     print('Nox 사이드 바: ', str(win32gui.GetWindowText(hwnd)), win32gui.IsWindowVisible(hwnd))

        if win32gui.IsWindowVisible(hwnd) != 0:
            # 녹스 사이드 바 이름 변경됨 6.0.5.1
            if (re.match('nox', str(win32gui.GetWindowText(hwnd))) is not None or
                    re.match('Nox', str(win32gui.GetWindowText(hwnd))) is not None or
                    re.match('Form', str(win32gui.GetWindowText(hwnd))) is not None):
                print('--------------------> !!! found window DEBUG4 Nox : ', str(win32gui.GetWindowText(hwnd)))
                if hwnd not in self.side_window_handle_list:
                    (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = win32gui.GetWindowRect(hwnd)
                    print('--------------------> !!! found window DEBUG5 Nox : ', (top_left_x, top_left_y, bottom_right_x, bottom_right_y))
                    if abs(bottom_right_x - top_left_x) - 36 < 100 and abs(
                                            bottom_right_y - top_left_y - LYBWin.HEIGHT) < 80:
                        self.side_window_handle_list.append(hwnd)
                        #
                        # 모모 멀티플레이어
                        # if win32gui.IsWindowVisible(hwnd) != 0:
            if lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO in str(win32gui.GetWindowText(hwnd)):
                self.multi_window_handle_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO] = hwnd

            # 미뮤 멀티
            if lybconstant.LYB_MULTI_APP_PLAYER_NAME_MEMU in str(win32gui.GetWindowText(hwnd)):
                self.multi_window_handle_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_MEMU] = hwnd

            # 녹스 멀티앱플레이어
            if lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX in str(win32gui.GetWindowText(hwnd)):
                # print(str(lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX) + ':[' + str(win32gui.GetWindowText(hwnd)) + '][' + str ( (s_x, s_y) ) + '] [' + str( (w_width, w_height) ) + ']') 
                self.multi_window_handle_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX] = hwnd

        if re.match(self.my_name, str(win32gui.GetWindowText(hwnd))) != None and win32gui.IsWindowVisible(hwnd) != 0:
            self.my_handle = hwnd

    def find_window_wildcard(self, wildcard):
        self.handle_list = []
        self.my_handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

        for each_side in self.side_window_handle_list:
            (s_x, s_y, s_bx, s_by) = win32gui.GetWindowRect(each_side)
            # self.logger.debug('side:' + str((s_x, s_y, s_bx, s_by)) ) 
            for each_window in self.handle_list:
                (w_x, w_y, w_bx, w_by) = win32gui.GetWindowRect(each_window)
                # self.logger.debug('main:' + str((w_x, w_y, w_bx, w_by)) )
                if (abs(abs(s_x - w_x) - (LYBWin.WIDTH + 4)) < 40 and
                            abs(abs(s_y - w_y) - 30) < 40 and
                            abs(abs(s_bx - w_bx) - 36) < 40 and
                            abs(s_by - w_by) < 40):
                    self.side_window_dic[each_window] = each_side
                    # 녹스 사이드바

    def set_invisible(self, hwnd):
        try:
            # win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
            #                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW);

            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                   win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW);
            win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, 2)
            # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        except:
            print('fail: ' + str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')

    def set_visible(self, hwnd):
        try:
            # win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_APPWINDOW);
            # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
            #                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_TOOLWINDOW);
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                   win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_LAYERED & ~win32con.WS_EX_TOOLWINDOW );
            # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            self.set_foreground(hwnd)
        except:
            print('fail: ' + str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')

    def getCurrentWindowList(self):
        self.current_window_list = []
        win32gui.EnumWindows(self.callbackGetCurrentWindow, "")

        return self.current_window_list

    def callbackGetCurrentWindow(self, hwnd, wildcard):
        if win32gui.IsWindowVisible(hwnd) != 0:
            self.current_window_list.append(hwnd)
            try:
                # print('oooooooo---->', win32gui.GetWindowText(hwnd))
                win32gui.EnumChildWindows(hwnd, self.callback_child_process, hwnd)
            except:
                # print('xxxxxxxx---->', 'No child')
                pass

    def set_foreground_console(self, handle):
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)

    def get_title(self, handle):
        return win32gui.GetWindowText(handle)

    def set_foreground(self, handle):

        try:
            win32gui.SetForegroundWindow(handle)
        except:
            # self.logger.warn('SetForegroundWindow fail')
            pass

    def get_window_location(self, hwnd):
        # (anchor_x, anchor_y, end_x, end_y) = win32gui.GetWindowRect(hwnd)

        # print('DEBUG::::::::', abs(anchor_x - end_x),  abs(anchor_y - end_y), (anchor_x, anchor_y, end_x, end_y))
        (anchor_x, anchor_y, end_x, end_y) = self.get_player_anchor_rect(hwnd)

        return (anchor_x, anchor_y, end_x, end_y)

    def mouse_click(self, hwnd, x, y, delay=0, release=True):

        rand_x = 0
        rand_y = 0
        if self.configure is not None and self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK] is True:
            random_error = int(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK + 'pixel'])
            rand_x += int(random_error * random.random())
            rand_y += int(random_error * random.random())

        rand_delay = 0.05
        if self.configure is not None and self.configure.common_config[lybconstant.LYB_DO_STRING_RANDOM_CLICK_DELAY] is not None:
            rand_delay = float(self.configure.common_config[lybconstant.LYB_DO_STRING_RANDOM_CLICK_DELAY])
            if rand_delay == 0:
                rand_delay = 0.05

        # print('>>>> RANDOM:', (rand_x, rand_y))
        # print('>>> RANDOM DELAY:', rand_delay)
        # (anchor_x, anchor_y, end_x, end_y) = win32gui.GetWindowRect(hwnd)

        lParam = win32api.MAKELONG(int(x + rand_x), int(y + rand_y))

        # lParam = win32api.MAKELONG(int(x), int(y))

        # win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        if delay == 0:
            delay = rand_delay

        if delay > 0:
            time.sleep(delay)

        if release is True:
            # win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

            # win32api.SetCursorPos((int(x), int(y)))
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)

    def mouse_drag(self, hwnd, from_x, from_y, to_x, to_y, delay=0.5, stop_delay=0, move_away=True):

        if from_x == to_x and from_y == to_y:
            return

        if from_x == to_x:
            x_step = 1
        else:
            x_step = abs(from_x - to_x)

        if x_step < 15:
            x_step = 1

        if from_y == to_y:
            y_step = 1
        else:
            y_step = abs(from_y - to_y)

        if y_step < 15:
            y_step = 1

        step_delay = delay / (abs(x_step) * abs(y_step))

        if from_x > to_x:
            x_factor = -1
        else:
            x_factor = 1

        if from_y > to_y:
            y_factor = -1
        else:
            y_factor = 1

        (anchor_x, anchor_y, end_x, end_y) = self.get_player_anchor_rect(hwnd)
        adj_x, adj_y = self.get_player_adjust(hwnd)
        lParam = win32api.MAKELONG(from_x + adj_x, from_y + adj_y)

        anchor_x, anchor_y, bottom_right_x, bottom_right_y = self.get_window_location(hwnd)

        # 사용자 마우스 커서가 윈도우 화면안에 들어와 있으면 비활성 마우스 이동이 되지 않기때문에
        # 마우스 커서를 잠깐 밖으로 이동시킨다.

        if move_away == True:
            if self.is_cursor_in_window(hwnd):
                pyautogui.moveTo(anchor_x - 2, anchor_y - 2)

        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)

        if x_step == 1 or y_step == 1:
            for i in range(int(x_step)):
                for j in range(int(y_step)):
                    lParam = win32api.MAKELONG(from_x + adj_x + i * x_factor, from_y + adj_y + j * y_factor)
                    # lParam = win32api.MAKELONG(from_x + i*x_factor, from_y + j*y_factor)
                    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, lParam)
                    time.sleep(step_delay)
        else:
            inclination = y_step / x_step
            for i in range(int(x_step)):
                lParam = win32api.MAKELONG(from_x + adj_x + i * x_factor,
                                           from_y + adj_y + int(i * y_factor * inclination))
                # lParam = win32api.MAKELONG(from_x + i*x_factor, from_y + j*y_factor)
                win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, lParam)
                time.sleep(step_delay)

        if stop_delay > 0:
            time.sleep(stop_delay)

        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

    def is_cursor_in_window(self, hwnd):
        cursor_x, cursor_y = win32gui.GetCursorPos()
        anchor_x, anchor_y, bottom_right_x, bottom_right_y = self.get_window_location(hwnd)

        if cursor_x >= anchor_x and cursor_x <= bottom_right_x:
            if cursor_y >= anchor_y and cursor_y <= bottom_right_y:
                return True

        return False

    def get_player(self, hwnd):

        (s_x, s_y, e_x, e_y) = win32gui.GetWindowRect(hwnd)
        process_name = win32gui.GetWindowText(hwnd)

        w_width = e_x - s_x
        w_height = e_y - s_y

        # print('[APP PLAYER]', win32gui.GetWindowText(hwnd), '[', s_x, s_y, ']', '[', w_width, 'x', w_height, ']')
        extra_width = LYBWin.NOX_EXTRA_WIDTH * 2
        extra_height = LYBWin.NOX_EXTRA_HEIGHT + extra_width
        extra_uhd_height = LYBWin.NOX_EXTRA_UHD_HEIGHT + extra_width
        resolution = self.get_player_resolution(hwnd)
        if w_width == (LYBWin.WIDTH + extra_width) and w_height == (LYBWin.HEIGHT + extra_height):
            return 'nox', resolution
        elif w_width == (LYBWin.WIDTH + extra_width) and w_height == (LYBWin.HEIGHT + extra_uhd_height):
            return 'nox', resolution
        elif w_width == LYBWin.WIDTH and w_height == LYBWin.HEIGHT and process_name == 'TheRender':
            return 'momo', resolution
        elif w_width == LYBWin.WIDTH and w_height == LYBWin.HEIGHT and process_name == 'RenderWindowWindow':
            return 'momo', resolution

        return '', resolution

    def get_player_screen_rect(self, hwnd):
        player_name, resolution = self.get_player(hwnd)

        if player_name == 'nox' and resolution == 'uhd':
            return LYBWin.NOX_EXTRA_WIDTH, LYBWin.NOX_EXTRA_UHD_HEIGHT + LYBWin.NOX_EXTRA_WIDTH, LYBWin.NOX_EXTRA_WIDTH + LYBWin.WIDTH, LYBWin.NOX_EXTRA_UHD_HEIGHT + LYBWin.NOX_EXTRA_WIDTH + LYBWin.HEIGHT
        elif player_name == 'nox':
            return LYBWin.NOX_EXTRA_WIDTH, LYBWin.NOX_EXTRA_HEIGHT + LYBWin.NOX_EXTRA_WIDTH, LYBWin.NOX_EXTRA_WIDTH + LYBWin.WIDTH, LYBWin.NOX_EXTRA_HEIGHT + LYBWin.NOX_EXTRA_WIDTH + LYBWin.HEIGHT
        else:
            return 0, 0, LYBWin.WIDTH, LYBWin.HEIGHT

    def get_player_anchor_rect(self, hwnd):
        (anchor_x, anchor_y, end_x, end_y) = win32gui.GetWindowRect(hwnd)

        player_name, resolution = self.get_player(hwnd)

        if player_name == 'nox':
            return anchor_x, anchor_y, end_x, end_y
        else:
            if resolution == 'uhd':
                # LDPlayer
                return anchor_x - int(LYBWin.NOX_EXTRA_WIDTH * 0.5), anchor_y - 54, end_x, end_y
            else:
                # LDPlayer
                return anchor_x - int(LYBWin.NOX_EXTRA_WIDTH * 0.5), anchor_y - 36, end_x, end_y

    def get_player_size(self, hwnd):
        (anchor_x, anchor_y, end_x, end_y) = win32gui.GetWindowRect(hwnd)

        player_name, resolution = self.get_player(hwnd)

        w = end_x - anchor_x
        h = end_y - anchor_y

        extra_width = LYBWin.NOX_EXTRA_WIDTH * 2
        extra_height = LYBWin.NOX_EXTRA_HEIGHT + extra_width
        extra_uhd_height = LYBWin.NOX_EXTRA_UHD_HEIGHT + extra_width
        if player_name == 'nox' and resolution == 'uhd':
            w = end_x - anchor_x - extra_width
            h = end_y - anchor_y - extra_uhd_height
        elif player_name == 'nox':
            w = end_x - anchor_x - extra_width
            h = end_y - anchor_y - extra_height
        else:
            w = end_x - anchor_x
            h = end_y - anchor_y

        return (w, h)

    def get_player_resolution(self, hwnd):
        (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = win32gui.GetWindowRect(hwnd)

        diff_width = abs(top_left_x - bottom_right_x)
        diff_height = abs(bottom_right_y - top_left_y)

        if diff_height == LYBWin.HEIGHT + 34 and diff_width == LYBWin.WIDTH + 4:
            # 녹스 FHD
            return 'fhd'
        elif diff_height == LYBWin.HEIGHT + 50 and diff_width == LYBWin.WIDTH + 4:
            # 녹스 UHD
            return 'uhd'
        elif diff_height == LYBWin.HEIGHT + 38 and diff_width == LYBWin.WIDTH + 38:
            # LDPlayer FHD
            return 'fhd'
        elif diff_height == LYBWin.HEIGHT + 56 and diff_width == LYBWin.WIDTH + 56:
            # LDPlayer UHD
            return 'uhd'
        else:
            return 'fhd'

    def get_player_adjust(self, hwnd):

        player_name, resolution = self.get_player(hwnd)
        if player_name == 'nox' and resolution == 'uhd':
            return 0, LYBWin.NOX_EXTRA_UHD_HEIGHT - LYBWin.NOX_EXTRA_HEIGHT
        elif player_name == 'nox':
            return 0, 0
        else:
            return -LYBWin.NOX_EXTRA_WIDTH, -(LYBWin.NOX_EXTRA_WIDTH + LYBWin.NOX_EXTRA_HEIGHT)

    def get_player_adjust_capture(self, hwnd):

        player_name, resolution = self.get_player(hwnd)
        if player_name == 'nox':
            return 0, 0
        else:
            if resolution == 'uhd':
                return -1, -54
            else:
                return -1, -36

    def get_window_screenshot(self, hwnd, flag):
        # hwnd = win32gui.FindWindow(None, '계산기')

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        # left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), flag)
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        return im
