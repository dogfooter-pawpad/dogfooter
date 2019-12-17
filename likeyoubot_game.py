import likeyoubot_configure as lybconfigure
import likeyoubot_win
import likeyoubot_message
import likeyoubot_resource as lybrsc
import likeyoubot_scene as lybscene
import pickle
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pyautogui
import operator
import random
import tkinter
from tkinter import ttk
from tkinter import font
import copy
import time
import sys
import unicodedata
import math
import threading
import datetime
from belfrywidgets import ToolTip
import os

from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_rest
import likeyoubot_license
import likeyoubot_logger
import traceback


class LYBGame():
    def __init__(self, game_name, game_data_name, window):
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.game_name = game_name
        self.game_data_name = game_data_name
        self.game_tab = None
        self.resource_manager = None
        self.window = window
        self.global_status = ''
        self.scene_dic = {}
        self.logging_queue = None
        self.hwnd = None
        self.side_hwnd = None
        self.parent_hwnd = None
        self.multi_hwnd_dic = {}
        self.last_time = 0
        self.configure = None
        self.common_config = None
        self.window_config = None
        self.event_limit = {}
        self.weight_threshold = 1.0
        self.weight_tolerance = 1.0
        self.last_scene = {}
        self.last_event = {}
        self.last_click = {}
        self.current_matched_scene = {}
        self.current_matched_event = {}
        self.request_terminate = False
        self.request_restart_app_player = False
        self.terminate_status = 0
        self.start_time = None
        self.interval = None
        self.player_type = ''
        self.window_title = ''
        self.current_schedule_work = ''
        self.window_image = None
        self.window_pixels = None
        self.last_window_pixels = None
        self.depth_config = None
        self.last_logging = 0
        self.cursor_loc = (0, 0)
        self.wait_for_start_reserved_work = False

        self.current_matched_scene['name'] = ''
        self.current_matched_scene['rate'] = 0
        self.current_matched_event['name'] = ''
        self.current_matched_event['rate'] = 0

        self.main_scene = None
        self.rest = None
        self.options = {}
        self.statistics = {}
        self.statistics[lybconstant.LYB_STATISTIC_0] = 0
        self.statistics[lybconstant.LYB_STATISTIC_1] = time.time()
        self.statistics_iterator = 0
        self.count_for_freeze = time.time()
        self.start_status = 0

        try:
            with open(lybconfigure.LYBConfigure.resource_path(self.game_data_name + '.lyb'), 'rb') as dat_file:
                self.resource_manager = pickle.load(dat_file)
        except:
            self.logger.error(self.logger.error(traceback.format_exc()) + ' ' + str(self.game_data_name) + '.lyb')

        self.sorted_resource_dic = self.resource_manager.resource_dic.sortedResourceListByCount()

    def get_work_list(self):
        return self.work_list

    def process(self, window_image):
        # self.process_restart_app_player()
        if self.start_time is None:
            self.start_time = time.time()
            if self.start_status != 0:
                self.get_scene('main_scene').status = self.start_status

        self.statistics[lybconstant.LYB_STATISTIC_1] = str(datetime.timedelta(seconds=int(time.time() - self.start_time)))

        if self.weight_threshold < 0.9:
            self.weight_threshold = 1.0

        if self.weight_tolerance < 0.9:
            self.weight_tolerance = 1.0

        self.window_image = window_image

        window_pixels = window_image.load()
        if self.request_terminate is True:
            self.process_terminate_applications()
            return 0

        restart_app = self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER]
        if restart_app is True:
            if self.get_option('restart_app_player_checkpoint') is None:
                self.set_option('restart_app_player_checkpoint', time.time())

            period_restart = int(
                self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'period'])
            # delay_restart = int(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay'])
            # retry_restart = int(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'retry'])

            # self.logger.warn(str(period_restart) + ':' + str(delay_restart) + ':' + str(retry_restart))
            # self.logger.warn(str(int(time.time() - self.get_option('restart_app_player_checkpoint'))))
            self.loggingElapsedTime('앱 플레이어 강제 종료', int(time.time() - self.get_option('restart_app_player_checkpoint')),
                                    period_restart, period=60)
            if time.time() - self.get_option('restart_app_player_checkpoint') > period_restart:
                self.set_option('restart_app_player_checkpoint', time.time())
                self.request_restart_app_player = True

        # self.logger.warn(self.request_restart_app_player)

        if self.request_restart_app_player == True:
            # self.process_restart_app_player()
            self.request_restart_app_player = False
            return 7000051

        if self.last_window_pixels != None and self.window_pixels != None:
            if self.is_freezing() == True:
                self.request_terminate = True
                return 0

        self.last_window_pixels = self.window_pixels
        self.window_pixels = window_pixels

        custom_name = self.custom_check(window_image, window_pixels)
        if len(custom_name) > 0:
            return 1111111

        self.check_reserved()

        event_name = ''
        scene_name = ''
        is_new_search = False

        if ('name' in self.current_matched_scene and
                    'rate' in self.current_matched_scene and
                    len(self.current_matched_scene['name']) > 0 and
                    self.current_matched_scene['rate'] >= float(
                    self.get_window_config('threshold_entry')) * self.weight_threshold
            ):           

            match_rate = self.rateMatchedResource(window_pixels, self.current_matched_scene['name'],
                                                  weight_tolerance=self.weight_tolerance)


            # self.logger.info(match_rate)
            # self.logger.info(self.current_matched_scene['name'])
            # self.logger.info(self.current_matched_scene['rate'])
            

            if match_rate > 0.9 and abs(int(match_rate * 100) - self.current_matched_scene['rate']) < 10:
                scene_name = self.current_matched_scene['name']
            else:
                self.current_matched_scene['name'] = ''

        if scene_name == '':
            # print('CP 1', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            if ('name' in self.current_matched_event and
                        'rate' in self.current_matched_event and
                        len(self.current_matched_event['name']) > 0 and
                        self.current_matched_event['rate'] >= float(
                        self.get_window_config('threshold_entry')) * self.weight_threshold
                ):

                # 이벤트는 더 빡시게 검사
                match_rate = self.rateMatchedResource(window_pixels, self.current_matched_event['name'],
                                                      weight_tolerance=self.weight_tolerance * 0.5)
                if match_rate > 0.9 and abs(int(match_rate * 100) - self.current_matched_scene['rate']) < 10:
                    event_name = self.current_matched_event['name']
                else:
                    self.current_matched_event['name'] = ''

            if event_name == '':
                resource_type_dic = self.get_screen(window_pixels, resource_type='event',
                                                    weight_threshold=self.weight_threshold * 1.3,
                                                    weight_tolerance=self.weight_tolerance * 0.5)
                event_name = resource_type_dic['event']
                is_new_search = True

            # print('CP 2', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

            if len(event_name) > 0:
                if self.process_event(window_pixels, event_name):
                    self.logger.info("[인식 화면] 이벤트 %s %s%%" \
                                     % (self.get_adjusted_name(self.current_matched_event['name']),
                                        # str(resource_type),
                                        self.current_matched_event['rate']))
                    return 222222

            resource_type_dic = self.get_screen(window_pixels, resource_type='scene',
                                                weight_threshold=self.weight_threshold,
                                                weight_tolerance=self.weight_tolerance)
            scene_name = resource_type_dic['scene']
            is_new_search = True
        # print('CP 3', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        if len(scene_name) < 1:
            # 적당한 씬을 찾지 못했다면, 일일히 검색해보자
            scene_name = self.get_screen_by_location(window_image)

            if len(scene_name) < 1:
                if self.last_time == 0:
                    self.last_time = time.time()

                if time.time() - self.last_time > 180:
                    self.telegram_send('창 이름 [' + str(self.window_title) + ']에서 인식 불가 화면이 3분간 감지되어 게임을 강제 종료합니다.')
                    png_name = self.save_image('freeze')
                    self.telegram_send('인식 불가', image=png_name)
                    return -1
                else:
                    # self.weight_threshold = self.weight_threshold - int(self.get_window_config('adjust_entry'))*0.001
                    # self.weight_tolerance = self.weight_tolerance + int(self.get_window_config('adjust_entry'))*0.001
                    self.weight_threshold = self.weight_threshold - 0.01
                    self.weight_tolerance = self.weight_tolerance + 0.01
                    self.logger.debug('허용 가중치: ' + str(int(self.weight_threshold * 100)) + '%, RGB 가중치: ' + str(
                        int(self.weight_tolerance * 100)) + '%')

                    return 0

        if is_new_search:
            self.logger.info("[화면 전환] %s %s%% 상태 코드: %s" \
                             % (self.get_adjusted_name(self.current_matched_scene['name']),
                                # str(resource_type),
                                self.current_matched_scene['rate'],
                                # self.current_matched_scene['threshold'],
                                self.get_scene(self.current_matched_scene['name']).status))
            self.logger.debug('[Scene Changed] ' +
                              str(self.current_matched_scene['name']) + ' ' +
                              str(self.current_matched_scene['rate']) + ' ' +
                              str(self.get_scene(self.current_matched_scene['name']).status) + ' scene_name: ' + str(
                scene_name))

        self.last_time = time.time()

        # print('CP 4', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        rc = self.get_scene(scene_name).process(window_image, window_pixels)
        if rc < 0:
            return rc
        elif rc == 1000000:
            self.clear_scene()
            return rc
        # self.loggingToGUI("%-52s [%-5s] 상태값:    %11s" \
        # 	% (self.get_adjusted_name(self.current_matched_scene['name']), 'scene', str(rc)))


        # print('[DEBUG]: rc=', rc, scene_name, self.last_scene)
        is_same = False
        if 'name' in self.last_scene:
            if self.last_scene['name'] == scene_name:
                if self.last_scene['status'] == rc:
                    if time.time() - self.last_scene['time'] > 120:
                        # 같은 화면, 같은 상태가 10초 이상 반복된다면.. 감지하는 제한값을 풀어주자.
                        # 화면 중앙을 클릭해보자..

                        self.weight_threshold *= 0.99
                        self.weight_tolerance *= 1.11
                    # self.loggingToGUI('같은 상태가 반복되어 화면 중앙을 클릭합니다. [' \
                    # +str(scene_name)+']['+str(rc)+'['+str(self.weight_threshold)+','+str(self.weight_tolerance)+']')
                    # self.window.mouse_click(self.hwnd, 320, 180)
                    else:
                        is_same = True
                else:
                    self.logger.debug(
                        '[Scene] ' + str(scene_name) + ', status: ' + str(self.last_scene['status']) + '-->' + str(rc))

        if is_same == False:
            # 못찾을 경우에는 점점 낮아지고, 찾았다면 원위치.
            self.weight_threshold = 1.0
            self.weight_tolerance = 1.0
            self.last_scene['name'] = scene_name
            self.last_scene['status'] = rc
            self.last_scene['time'] = time.time()
            self.last_scene['rate'] = self.current_matched_scene['rate']

        return rc

    def custom_check(self, window_image, window_pixels):
        return ''

    def custom_event(self, event_name):
        return False

    def compare_reserved(self, reserved_hour, reserved_minute, reserved_second):

        now = datetime.datetime.now()
        now_time = now.strftime('%H:%M:%S')
        now_hour = int(now_time.split(':')[0])
        now_minute = int(now_time.split(':')[1])
        now_second = int(now_time.split(':')[2])

        # print('[DEBUG] ReservedTime Check:', reserved_hour, reserved_minute, reserved_second, ':', now_hour, now_minute, now_second)

        if reserved_hour != now_hour:
            return False

        if reserved_minute != now_minute:
            return False

        if abs(reserved_second - now_second) > 5:
            return False

        self.logger.debug(
            'ReservedTime: ' + str(reserved_hour) + str(reserved_minute) + str(reserved_second) + ':' + str(
                now_hour) + str(now_minute) + str(now_second))
        return True

    def check_reserved(self):

        if self.main_scene is None:
            return

        if self.wait_for_start_reserved_work is False:
            work_index_to_move = self.recursive_check_reserved(self.get_game_config(self.game_name, '', flag=1), [], [])
            if work_index_to_move is not None:
                self.logger.debug('reserved work index=' + str(work_index_to_move))
                schedule_list = self.get_game_config(self.game_name, 'schedule_list')
                self.main_scene.move_status[self.current_schedule_work] = work_index_to_move
                self.wait_for_start_reserved_work = True

            # print('[DEBUG] return_callstack:', self.main_scene.callstack,
            # 	'work to move:', work_to_move, self.wait_for_start_reserved_work)

        return

    def recursive_check_reserved(self, config, arg_callstack, arg_callstack_status):
        if self.main_scene == None:
            return

        schedule_list = config['schedule_list']

        if '[작업 예약]' in schedule_list:
            r_work_done_dic = self.main_scene.get_option('r_work_done_dic')
            if r_work_done_dic is None:
                r_work_done_dic = {}

            # print('[DEBUG] ReservedQueue:', r_work_done_dic)

            reserved_hour = int(config[lybconstant.LYB_DO_STRING_RESERVED_HOUR])
            reserved_minute = int(config[lybconstant.LYB_DO_STRING_RESERVED_MINUTE])
            reserved_second = int(config[lybconstant.LYB_DO_STRING_RESERVED_SECOND])

            queue_elem = reserved_hour * 60 * 60 + reserved_minute * 60 + reserved_second

            if queue_elem in r_work_done_dic:
                last_done_time = r_work_done_dic[queue_elem]

                if time.time() - last_done_time > 3600:
                    # 작업 예약된 애들을 보관해놓고 1시간 이상되면 꺼내서 버린다.
                    # 작업 예약 한번만 실행되게 하려고.
                    r_work_done_dic.pop(queue_elem)
                else:
                    return None

            is_there = self.compare_reserved(reserved_hour, reserved_minute, reserved_second)
            if is_there == True:
                r_work_done_dic[queue_elem] = time.time()
                self.main_scene.set_option('r_work_done_dic', r_work_done_dic)
                call_index = 0
                if len(self.main_scene.callstack) > 0:
                    for each_call in self.main_scene.callstack:
                        iterator_key = self.build_iterator_key(call_index, each_call)
                        self.main_scene.set_option(iterator_key, None)
                        call_index += 1
                    self.main_scene.callstack.clear()
                # self.main_scene.callstack.clear()
                self.main_scene.callstack = arg_callstack

                self.main_scene.callstack_status.clear()
                self.main_scene.callstack_status = arg_callstack_status

                # self.logger.debug('current_schedule_work:' + str(self.current_schedule_work))
                if self.current_schedule_work != None and len(self.current_schedule_work) > 0:
                    self.main_scene.set_option(self.current_schedule_work + '_end_flag', True)

                if len(arg_callstack) > 0:
                    # 1depth 이상
                    iterator_key = self.build_iterator_key(len(arg_callstack) - 1, arg_callstack[-1])
                    custom_config_dic = self.configure.window_config['custom_config_dic']

                    self.main_scene.set_option(iterator_key,
                                               custom_config_dic[arg_callstack[-1]]['schedule_list'].index('[작업 예약]'))

                    return custom_config_dic[arg_callstack[-1]]['schedule_list'].index('[작업 예약]')
                else:
                    return schedule_list.index('[작업 예약]') + 1

        custom_config_dic = self.configure.window_config['custom_config_dic']
        i = 1
        for each_work in schedule_list:
            if each_work in custom_config_dic:
                arg_callstack.append(each_work)
                arg_callstack_status.append(i)
                work_index_to_move = self.recursive_check_reserved(custom_config_dic[each_work], arg_callstack,
                                                                   arg_callstack_status)
                if work_index_to_move != None:
                    return work_index_to_move
                else:
                    arg_callstack.pop()
                    arg_callstack_status.pop()
            i += 1

        return None

    def addStatistic(self, name):
        if not name in self.statistics:
            self.statistics[name] = 0

        self.statistics[name] += 1

    def getStatistic(self, index):
        if len(self.statistics) <= index:
            return ''

        s_key = list(self.statistics)[index]
        s_value = self.statistics[s_key]

        return '%-38s' % (s_key + '    ' + str(s_value))

    def getCurrentStatistic(self):
        return self.getStatistic(self.statistics_iterator)

    def telegram_send(self, message, image=None):
        if self.rest is None:
            self.rest = self.login()
            self.rest.login()
        chat_id = self.rest.get_chat_id()

        if image == None:
            self.rest.send_telegram_message(chat_id, message)
        else:
            self.rest.send_telegram_image(chat_id, image)

    def login(self):
        user_id = self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id']
        user_password = likeyoubot_license.LYBLicense().get_decrypt(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'])

        rest = likeyoubot_rest.LYBRest(self.configure.root_url, user_id, user_password)

        return rest

    def save_image(self, png_name):

        # window_image_org = cv2.cvtColor(np.array(self.window_image), cv2.COLOR_RGB2BGR)
        # img = Image.fromarray(window_image_org, 'RGB')

        try:
            directory = lybconfigure.LYBConfigure.resource_path('screenshot')
            if not os.path.exists(directory):
                os.makedirs(directory)

            now = datetime.datetime.now()
            now_time = now.strftime('%y%m%d_%H%M%S')
            app_player_type, resolution = self.window.get_player(self.hwnd)
            png_name = directory + '\\' + png_name + '_' + str(now_time) + '_' + str(app_player_type) + '.png'

            crop_area = self.window.get_player_screen_rect(self.hwnd)

            self.window_image.crop(crop_area).save(png_name)

            return png_name
        except:
            self.logger.error('스크린샷 저장 중 에러 발생')
            self.logger.error(traceback.format_exc())

            return None

    def build_iterator_key(self, index, work_name):
        return str(index) + work_name + '_config_iterator'

    def process_restart_app_player(self):
        if self.player_type == 'nox':
            if lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX in self.multi_hwnd_dic:
                mHwnd = self.multi_hwnd_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX]
                app_player_index = int(
                    self.window_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number']) - 1
                self.logger.debug('app_player_index: ' + str(app_player_index))
                self.logger.debug('mHwnd: ' + str(mHwnd))

                while True:
                    self.window.mouse_click(mHwnd, 523, 116 + (57 * app_player_index))
                    time.sleep(1)

                    confirm_window_hwnd_list = self.window.getInnerWindow(mHwnd)
                    self.logger.debug(confirm_window_hwnd_list)
                    if len(confirm_window_hwnd_list) > 0:
                        for each_hwnd in confirm_window_hwnd_list:
                            self.logger.debug(each_hwnd)
                            time.sleep(1)
                            self.window.mouse_click(each_hwnd, 120, 180)
                        break
                    else:
                        time.sleep(1)

                return
        elif self.player_type == 'momo':
            if lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO in self.multi_hwnd_dic:
                mHwnd = self.multi_hwnd_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO]
                app_player_index = int(
                    self.window_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number']) - 1
                self.logger.debug('app_player_index: ' + str(app_player_index))

                while True:
                    self.window.mouse_click(mHwnd, 387, 116 + (50 * app_player_index))
                    time.sleep(1)

                    confirm_window_hwnd_list = self.window.getInnerWindow(mHwnd)
                    self.logger.debug(confirm_window_hwnd_list)
                    if len(confirm_window_hwnd_list) > 0:
                        for each_hwnd in confirm_window_hwnd_list:
                            self.logger.debug(each_hwnd)
                            time.sleep(1)
                            self.window.mouse_click(each_hwnd, 310, 210)
                        break
                    else:
                        time.sleep(1)

                return

        self.set_option('restart_app_player_checkpoint', time.time())
        self.logger.warn('앱플레이어 재시작 기능 사용 가능')

    def is_freezing(self):
        freezing_limit = int(self.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT + 'freezing_limit'])
        if freezing_limit == 0:
            return False

        (x, y, x2, y2) = self.window.get_player_anchor_rect(self.hwnd)
        w = x2 - x
        h = y2 - y

        check_position_list = [
            (int(w * 0.5), int(h * 0.5)),
            (int(w * 0.25), int(h * 0.25)),
            (int(w * 0.75), int(h * 0.25)),
            (int(w * 0.25), int(h * 0.75)),
            (int(w * 0.75), int(h * 0.75))
        ]

        for each_pos in check_position_list:
            loc_x = each_pos[0]
            loc_y = each_pos[1]
            if self.last_window_pixels[loc_x, loc_y] != self.window_pixels[loc_x, loc_y]:
                self.count_for_freeze = time.time()
                return False

            # self.logger.debug(str((loc_x, loc_y)) + ' ' + str(self.last_window_pixels[loc_x, loc_y]) + ' ' + str(self.window_pixels[loc_x, loc_y]))

        elapsed_time = time.time() - self.count_for_freeze
        if elapsed_time >= freezing_limit:
            self.count_for_freeze = time.time()
            self.telegram_send('창 이름 [' + str(self.window_title) + ']에서 화면 프리징이 감지되어 게임을 강제 종료합니다.')
            png_name = self.save_image('freeze')
            self.telegram_send('', image=png_name)
            return True
        else:
            if elapsed_time > 120:
                self.logger.warn('화면 프리징 감지됨...(' + str(int(elapsed_time)) + '/' + str(freezing_limit) + '초)')

        return False

    def click_back(self):
        if self.player_type == 'nox':
            if self.terminate_status == 0:
                if self.side_hwnd == None:
                    self.logger.warn('녹스 사이드바 검색 실패로 종료 기능 사용 불가')
                    self.request_terminate = False
                    return
                self.window.mouse_click(self.side_hwnd, 16, likeyoubot_win.LYBWin.HEIGHT - 115)
        elif self.player_type == 'momo':
            if self.terminate_status == 0:
                self.window.mouse_click(self.parent_hwnd,
                                        likeyoubot_win.LYBWin.WIDTH + 20,
                                        likeyoubot_win.LYBWin.HEIGHT - 80)

    def process_terminate_applications(self):

        max_app_close_count = self.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_COUNT]
        self.logger.debug('CloseMaxCount: ' + str(max_app_close_count))
        if self.player_type == 'nox':
            if self.terminate_status == 0:
                # self.mouse_click_with_cursor(660, 350)
                if self.side_hwnd is None:
                    self.logger.warn('녹스 사이드바 검색 실패로 종료 기능 사용 불가')
                    self.request_terminate = False
                    return
                self.window.mouse_click(self.side_hwnd, 16, likeyoubot_win.LYBWin.HEIGHT - 40)
                self.terminate_status += 1
            elif 0 < self.terminate_status < max_app_close_count:
                self.logger.info('녹스 앱 종료 중..')
                if self.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_NOX_NEW] is True:
                    self.window.mouse_drag(self.hwnd,
                                           int(likeyoubot_win.LYBWin.WIDTH * 0.5),
                                           likeyoubot_win.LYBWin.HEIGHT - 90, 0,
                                           likeyoubot_win.LYBWin.HEIGHT - 90,
                                           delay=0,
                                           move_away=self.common_config[lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away'])
                else:
                    # self.window.mouse_drag(self.hwnd, 630, 220, 630, 80, 0.5)
                    self.window.mouse_click(self.hwnd,
                                            likeyoubot_win.LYBWin.WIDTH - 10,
                                            likeyoubot_win.LYBWin.HEIGHT - 230,
                                            delay=2)
                    time.sleep(2)
                    self.window.mouse_click(self.hwnd,
                                            likeyoubot_win.LYBWin.WIDTH - 90,
                                            likeyoubot_win.LYBWin.HEIGHT - 335,
                                            )
                self.terminate_status += 1
            else:
                self.terminate_status = 0
                self.request_terminate = False
        elif self.player_type == 'momo':
            if self.terminate_status == 0:
                resolution = self.window.get_player_resolution(self.hwnd)
                if resolution == 'fhd':
                    self.window.mouse_click(self.parent_hwnd,
                                            likeyoubot_win.LYBWin.WIDTH + 20,
                                            likeyoubot_win.LYBWin.HEIGHT - 5)
                else:
                    self.window.mouse_click(self.parent_hwnd,
                                            likeyoubot_win.LYBWin.WIDTH + 20,
                                            likeyoubot_win.LYBWin.HEIGHT - 5)
                # self.move_mouse_location(660, 355)
                self.terminate_status += 1
            elif self.terminate_status > 0 and self.terminate_status < max_app_close_count:
                self.logger.info('모모 앱 종료 중...')
                self.window.mouse_drag(self.hwnd,
                                       int(likeyoubot_win.LYBWin.WIDTH * 0.5),
                                       likeyoubot_win.LYBWin.HEIGHT - 90, 0,
                                       likeyoubot_win.LYBWin.HEIGHT - 90,
                                       0.5,
                                       move_away=self.common_config[lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away'])
                self.terminate_status += 1
            else:
                self.terminate_status = 0
                self.request_terminate = False

    def process_event(self, window_pixels, event_name):

        if not event_name in self.event_limit:
            self.event_limit[event_name] = time.time()
            self.event_limit[event_name + '_count'] = 0
        else:
            # 동일한 이벤트 10초마다 발생
            if time.time() - self.event_limit[event_name] < 10:
                if self.event_limit[event_name + '_count'] > 10:
                    return False
            else:
                self.event_limit[event_name + '_count'] = 0

        if self.custom_event(event_name) == True:
            return True

        # 이벤트 인식 오류가 있을 수 있기 때문에 10초 안에 2번 이상 반복 인식될 경우 클릭하는 걸로 하자/
        # if self.event_limit[event_name + '_count'] % 2 == 0:
        # match_rate = self.rateMatchedPixelBox(window_pixels, event_name + '_button')

        # # self.loggingToGUI("%-47s  %-2s  클릭위치매칭률:    %10s%%" \
        # # 	% (self.get_adjusted_name(self.current_matched_scene['name']), '', \
        # # 		str(int(match_rate*self.weight_threshold*100))))

        # if match_rate > 0.1 * self.weight_threshold:
        # 	self.logger.debug('click success event: ' + str(event_name) + '_button ' + str(match_rate))
        # 	self.mouse_click(event_name + '_button')
        # else:
        # 	self.logger.warn('click fail event: ' + str(event_name) + '_button ' + str(match_rate))

        self.mouse_click(event_name + '_button')

        self.event_limit[event_name] = time.time()
        self.event_limit[event_name + '_count'] += 1
        self.last_event['name'] = event_name
        self.last_event['rate'] = self.current_matched_event['rate']

        return True

    def get_screen_by_location(self, window_image):

        return ''

    def get_scene(self, scene_name):
        if not scene_name in self.scene_dic:
            self.add_scene(scene_name)
        return self.scene_dic[scene_name]

    def clear_scene(self):
        pass

    def setAppPlayer(self, player_type):
        self.player_type = player_type

    def add_scene(self, scene_name):
        self.scene_dic[scene_name] = lybscene.LYBScene(scene_name)
        self.scene_dic[scene_name].setLoggingQueue(self.logging_queue)
        self.scene_dic[scene_name].setGameObject(self)

    def setGameTab(self, game_tab_object):
        self.game_tab = game_tab_object

    def setLoggingQueue(self, logging_queue):
        self.logging_queue = logging_queue

    def setWindowHandle(self, hwnd, side_hwnd, parent_hwnd, multi_hwnd_dic):
        self.hwnd = hwnd

        if parent_hwnd == 0 or parent_hwnd == None:
            self.window_title = self.window.get_title(self.hwnd)
        else:
            self.window_title = self.window.get_title(parent_hwnd)

        if parent_hwnd != None and parent_hwnd != 0:
            self.parent_hwnd = parent_hwnd
        else:
            self.side_hwnd = side_hwnd
            if self.side_hwnd == None:
                self.logger.warn('녹스 사이드바가 검색 실패. 자동 재시작 기능 사용 불가')
            else:
                self.logger.critical('녹스 사이드바가 검색 성공. 자동 재시작 기능 사용 가능)')

        self.multi_hwnd_dic = multi_hwnd_dic

    def setStartFlag(self, flag):
        self.start_status = flag

    def setCommonConfig(self, config):
        self.configure = config
        self.common_config = self.configure.common_config

    def setWindowConfig(self, config):
        self.window_config = config

    def get_adjusted_name(self, object_name):
        return object_name.replace('lin2rev', '', 1).replace('clans', '', 1).replace('tera', '', 1).replace('scene', '',
                                                                                                            1).replace(
            'event', '', 1).replace('_', '', 10).upper()

    def loggingElapsedTime(self, title, elapsed_time, limit_time, period=10):
        if time.time() - self.last_logging < period:
            return
        self.last_logging = time.time()

        if limit_time == 0:
            self.logger.info("%s:%9s" % (
                self.preformat_cjk(title, 1),
                str(time.strftime('%H:%M:%S', time.gmtime(int(elapsed_time))))))
        else:
            self.logger.info("%s:%9s / %s" % (
                self.preformat_cjk(title, 1),
                str(time.strftime('%H:%M:%S', time.gmtime(int(elapsed_time)))),
                str(time.strftime('%H:%M:%S', time.gmtime(int(limit_time))))))

    def get_work_status(self, work_name):
        return -1

    def get_option(self, option_name):
        if not option_name in self.options:
            self.options[option_name] = None

        return self.options[option_name]

    def set_option(self, option_name, value):
        self.options[option_name] = value

    def preformat_cjk(self, string, width, align='<', fill=' '):
        count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                             for c in string))
        return {
            '>': lambda s: fill * count + s,
            '<': lambda s: s + fill * count,
            '^': lambda s: fill * (count / 2)
                           + s
                           + fill * (count / 2 + count % 2)
        }[align](string)

    def loggingToGUI(self, log_message, log_type='log'):

        message = '%s %s' % (self.preformat_cjk(self.window_title, 1), log_message)
        if log_type == 'log':
            self.logger.debug(message)
        else:
            self.logger.info(message)
        # if self.get_window_config('debug_booleanvar') == True or log_type != 'log':
        # 	message = '%s%s'%(self.preformat_cjk(self.window_title, 20), log_message)
        # 	self.logging_queue.put_nowait(likeyoubot_message.LYBMessage(log_type, message))

    def locationOnWindowPart(self, parent, child,
                             custom_threshold=-1,
                             custom_below_level=-1,
                             custom_top_level=-1,
                             source_custom_below_level=-1,
                             source_custom_top_level=-1,
                             custom_flag=-1,
                             custom_rect=(-1, -1, -1, -1)  # x, y, width, height
                             ):

        if custom_flag != -1:
            adj_x, adj_y = self.get_player_adjust()
            custom_rect2 = (
            custom_rect[0] + adj_x, custom_rect[1] + adj_y, custom_rect[2] + adj_x, custom_rect[3] + adj_y)
        else:
            custom_rect2 = (-1, -1, -1, -1)

        return LYBGame.locationOnWindowWithRate2(parent, child,
                                                 custom_threshold=custom_threshold,
                                                 custom_below_level=custom_below_level,
                                                 custom_top_level=custom_top_level,
                                                 source_custom_below_level=source_custom_below_level,
                                                 source_custom_top_level=source_custom_top_level,
                                                 custom_flag=custom_flag,
                                                 custom_rect=custom_rect2
                                                 )

    @classmethod
    def locationOnWindow(self, parent, child, custom_threshold=-1, custom_below_level=-1, custom_top_level=-1):
        (loc_x, loc_y), rate = LYBGame.locationOnWindowWithRate2(parent, child,
                                                                 custom_threshold=custom_threshold,
                                                                 custom_below_level=custom_below_level,
                                                                 custom_top_level=custom_top_level)

        return (loc_x, loc_y)


    def locationResourceOnWindowPart2(self, parent, child_resource,
                                     custom_threshold=-1,
                                     custom_below_level=-1,
                                     custom_top_level=-1,
                                     source_custom_below_level=-1,
                                     source_custom_top_level=-1,
                                     custom_flag=-1,
                                     near=32,
                                     average=False,
                                     debug=False
                                     ):
        if not child_resource in self.resource_manager.resource_dic:
            return ((-1, -1), 0)

        left = likeyoubot_win.LYBWin.WIDTH
        top = likeyoubot_win.LYBWin.HEIGHT
        right = -1
        bottom = -1

        pb_width = 0
        pb_height = 0

        resource = self.resource_manager.resource_dic[child_resource]
        for each_pixel_box_name in resource:
            pixel_box = self.resource_manager.pixel_box_dic[each_pixel_box_name]
            if pb_width < pixel_box.width:
                pb_width = pixel_box.width
            if pb_height < pixel_box.height:
                pb_height = pixel_box.height
                
            (loc_x, loc_y) = self.get_location(each_pixel_box_name)
            if loc_x < left:
                left = loc_x
            if loc_x > right:
                right = loc_x
            if loc_y < top:
                top = loc_y
            if loc_y > bottom:
                bottom = loc_y


        adj_x, adj_y = self.get_player_adjust()


        left = left - pb_width - near + adj_x
        top = top - pb_height - near + adj_y
        right = right + pb_width + near - adj_x
        bottom = bottom + pb_height + near - adj_y

        if left < 0:
            left = 0
        if top < 1:
            top = 1
        if right > likeyoubot_win.LYBWin.WIDTH - adj_x:
            right = likeyoubot_win.LYBWin.WIDTH - adj_x
        if bottom > likeyoubot_win.LYBWin.HEIGHT - adj_y:
            bottom = likeyoubot_win.LYBWin.HEIGHT - adj_y

        near_rect = (left, top, right, bottom) 

        self.logger.warn(near_rect)

        return self.locationResourceOnWindowPart(parent, child_resource,
            custom_threshold=custom_threshold,
            custom_below_level=custom_below_level,
            custom_top_level=custom_top_level,
            source_custom_below_level=source_custom_below_level,
            source_custom_top_level=source_custom_top_level,
            custom_flag=custom_flag,
            custom_rect=near_rect,
            average=average,
            debug=debug)

    def locationResourceOnWindowPart(self, parent, child_resource,
                                     custom_threshold=-1,
                                     custom_below_level=-1,
                                     custom_top_level=-1,
                                     source_custom_below_level=-1,
                                     source_custom_top_level=-1,
                                     custom_flag=-1,
                                     custom_rect=(-1, -1, -1, -1),  # x, y, width, height
                                     average=False,
                                     debug=False
                                     ):

        if not child_resource in self.resource_manager.resource_dic:
            return ((-1, -1), 0)

        resource = self.resource_manager.resource_dic[child_resource]

        sum_match_rate = 0
        # is_matched = True
        s_loc_x = -1
        s_loc_y = -1
        i = 0
        for each_pixel_box_name in resource:
            (loc_x, loc_y), match_rate = self.locationOnWindowPart(
                parent,
                self.resource_manager.pixel_box_dic[each_pixel_box_name],
                custom_below_level=custom_below_level,
                custom_top_level=custom_top_level,
                source_custom_below_level=source_custom_below_level,
                source_custom_top_level=source_custom_top_level,
                custom_threshold=custom_threshold,
                custom_flag=custom_flag,
                custom_rect=custom_rect
            )
            # if '굴' in each_pixel_box_name:
            # 	print('[DEBUG] location:', each_pixel_box_name, match_rate)
            # if loc_x == -1:
            # 	# is_matched = False
            # 	continue
            # else:
            if debug == True:
                self.logger.debug(each_pixel_box_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))

            if loc_x == -1 and average == False:
                return (-1, -1), 0

            if s_loc_x == -1:
                s_loc_x = loc_x
                s_loc_y = loc_y

            # print('[DEBUG] AreaTest:', (loc_x, loc_y), round(match_rate,2))
            sum_match_rate += match_rate
            i += 1

        if i > 0:
            if sum_match_rate / i >= custom_threshold:
                return (s_loc_x, s_loc_y), sum_match_rate / i
            else:
                return (-1, -1), sum_match_rate / i
        else:
            return (-1, -1), 0

    @classmethod
    def locationOnWindowWithRate2(self, parent, child,
                                  custom_threshold=-1,
                                  custom_below_level=-1,
                                  custom_top_level=-1,
                                  source_custom_below_level=-1,
                                  source_custom_top_level=-1,
                                  custom_flag=-1,
                                  custom_rect=(-1, -1, -1, -1)  # x, y, width, height
                                  ):

        if custom_flag == -1:
            window_image_org = cv2.cvtColor(np.array(parent), cv2.COLOR_RGB2BGR)
        else:
            window_image_org = np.array(parent)

        if custom_rect != -1:
            temp_custom_rect = []
            for i in range(4):
                if custom_rect[i] < 0:
                    temp_custom_rect.append(0)
                else:
                    temp_custom_rect.append(custom_rect[i])

            custom_rect = (temp_custom_rect[0], temp_custom_rect[1], temp_custom_rect[2], temp_custom_rect[3])

        # window_image = window_image_org.copy()
        template_image = np.ndarray(shape=(child.height, child.width, 3), dtype='uint8')

        window_image = window_image_org
        # print("!!!!!--:", window_image)
        if custom_flag == -1:
            # print("CP0")
            if custom_below_level != -1 or custom_below_level != -1:
                # printf("CP1")
                window_image = cv2.inRange(window_image, custom_below_level, custom_top_level)
            # print("AAAAAAAAAAA-", window_image)
            # window_image = np.array(window_image)
        else:
            temp_window_image = window_image[custom_rect[1]:custom_rect[3], custom_rect[0]:custom_rect[2]]
            if custom_below_level != -1 or custom_below_level != -1:
                window_image = cv2.inRange(temp_window_image, custom_below_level, custom_top_level)
            else:
                window_image = temp_window_image

            # print("KKKKKKKKKKKKKK--:", type(window_image), window_image)
            # window_image = np.array(window_image)
            # print("5555--:", type(window_image), window_image)

        # if 'jangbiham_scene_holy_rank' in child.pixel_box_name:
        # 	cv2.imwrite(child.pixel_box_name+str(time.time())+'.png', window_image)

        # 	img = Image.fromarray(window_image, 'RGB')
        # 	img.save(child.pixel_box_name+str(time.time())+'.png')

        if custom_threshold != -1:
            threshold = custom_threshold
        else:
            threshold = 0.8

        i = 0
        j = 0
        k = 0

        if source_custom_top_level != -1:
            temp_custom_top_level = source_custom_top_level
            temp_custom_below_level = source_custom_below_level
        else:
            temp_custom_top_level = custom_top_level
            temp_custom_below_level = custom_below_level

        for elem in np.nditer(template_image, op_flags=['readwrite']):
            if temp_custom_below_level != -1:
                if child[i + j][1][k] < temp_custom_below_level[k]:
                    elem[...] = 0
                elif child[i + j][1][k] > temp_custom_top_level[k]:
                    elem[...] = 255
                else:
                    elem[...] = child[i + j][1][k]
            else:
                elem[...] = child[i + j][1][k]

            k += 1
            if k >= 3:

                i += child.height
                k = 0
                if i >= child.height * child.width:
                    j += 1
                    i = 0
                    rgb, w, h = template_image.shape[::-1]

        if custom_flag != -1:
            if temp_custom_top_level != -1:
                template_image = cv2.inRange(np.array(template_image), temp_custom_below_level, temp_custom_top_level)
            # template_image = np.array(template_image)

            # for each_elem in template_image:
            # 	i = 0
            # 	for each_elem2 in each_elem:
            # 		if custom_below_level != -1 or custom_below_level != -1:
            # 			if (	each_elem2[0] >= custom_below_level[0] and
            # 					each_elem2[1] >= custom_below_level[1] and
            # 					each_elem2[2] >= custom_below_level[2] and
            # 					each_elem2[0] <= custom_top_level[0] and
            # 					each_elem2[1] <= custom_top_level[1] and
            # 					each_elem2[2] <= custom_top_level[2]
            # 				):
            # 				each_elem[i] = [255, 255, 255]
            # 			else:
            # 				each_elem[i] = [0, 0, 0]

            # 		i += 1

            # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


            # if 'jangbiham_scene_holy_rank' in child.pixel_box_name:
            # 	cv2.imwrite(child.pixel_box_name+'2_'+str(time.time())+'.png', template_image)

            # img = Image.fromarray(template_image, 'RGB')
            # img.save(child.pixel_box_name+'2_'+str(time.time())+'.png')

        methods = ['cv2.TM_CCOEFF_NORMED']
        result_dic = {}
        max_match_rate = 0

        for meth in methods:
            # img = window_image.copy()
            img = window_image
            method = eval(meth)

            # print("XXXX--:", img, template_image)

            res = cv2.matchTemplate(img, template_image, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # loc = np.where( res > 0.8 )
            # for pt in zip(*loc[::-1]):
            # 	print('DEBUG LOC:', pt, child.pixel_box_name, threshold)
            # 	# print('DEBUG LOC: ', pt)
            # 	pass

            # print(min_val, max_val, min_loc, max_loc, custom_threshold, child.pixel_box_name)

            # print(child.pixel_box_name, int(threshold*100), ':', int(max_val*100), max_loc, max_match_rate)

            if max_match_rate < max_val:
                max_match_rate = max_val

            if max_val < threshold:
                continue

            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            try:
                result_dic[(int(top_left[0] + w / 2), int(top_left[1] + h / 2))] += 1
            except:
                result_dic[(int(top_left[0] + w / 2), int(top_left[1] + h / 2))] = 1



            # if 'boss' in child.pixel_box_name:
            # 	img = Image.fromarray(window_image, 'RGB')
            # 	img.save(child.pixel_box_name+'.png')


            # print(meth, ':', min_val, max_val, min_loc, max_loc)


            # bottom_right = (top_left[0] + w, top_left[1] + h)

            # cv2.rectangle(img,top_left, bottom_right, 255, 2)

            # plt.subplot(121),plt.imshow(res,cmap = 'gray')
            # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            # plt.subplot(122),plt.imshow(img,cmap = 'gray')
            # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            # plt.suptitle(meth)
            # # plt.show()
            # plt.savefig('./'+str(meth)+'.png')

        if len(result_dic) > 0:
            sorted_list = sorted(result_dic.items(), key=operator.itemgetter(1), reverse=True)
            # print(sorted_list)
            if custom_flag == -1:
                return (sorted_list[0][0], max_match_rate)
            else:
                return ((sorted_list[0][0][0] + custom_rect[0], sorted_list[0][0][1] + custom_rect[1]), max_match_rate)
        else:
            return ((-1, -1), max_match_rate)

    @classmethod
    def locationOnWindowWithRate(self, parent, child,
                                 custom_threshold=-1,
                                 custom_below_level=-1,
                                 custom_top_level=-1,
                                 custom_flag=-1,
                                 custom_rect=(-1, -1, -1, -1)  # x, y, width, height
                                 ):

        if custom_flag == -1:
            window_image_org = cv2.cvtColor(np.array(parent), cv2.COLOR_RGB2BGR)
        else:
            window_image_org = np.array(parent)

        window_image = window_image_org.copy()
        template_image = np.ndarray(shape=(child.height, child.width, 3), dtype='uint8')

        if custom_flag == -1:
            if custom_below_level != -1 or custom_below_level != -1:
                for each_elem in window_image:
                    for each_elem2 in each_elem:
                        if (each_elem2[0] < custom_below_level[0] and
                                    each_elem2[1] < custom_below_level[1] and
                                    each_elem2[2] < custom_below_level[2]):
                            each_elem2 = [0, 0, 0]
                        elif (each_elem2[0] > custom_top_level[0] and
                                      each_elem2[1] > custom_top_level[1] and
                                      each_elem2[2] > custom_top_level[2]):
                            each_elem2 = [255, 255, 255]
        else:
            custom_width = custom_rect[2] - custom_rect[0]
            custom_height = custom_rect[3] - custom_rect[1]
            custom_window_image = np.ndarray(shape=(custom_height, custom_width, 3), dtype='uint8')
            # print(window_image)

            for j in range(custom_height):
                for i in range(custom_width):
                    # print(j, i, window_image[custom_rect[1] + j][custom_rect[0] + i])
                    # 모모도 추가해야함
                    if custom_below_level != -1 or custom_below_level != -1:
                        if (window_image[custom_rect[1] + j][custom_rect[0] + i][0] < custom_below_level[0] or
                                    window_image[custom_rect[1] + j][custom_rect[0] + i][1] < custom_below_level[1] or
                                    window_image[custom_rect[1] + j][custom_rect[0] + i][2] < custom_below_level[2] or
                                    window_image[custom_rect[1] + j][custom_rect[0] + i][0] > custom_top_level[0] or
                                    window_image[custom_rect[1] + j][custom_rect[0] + i][1] > custom_top_level[1] or
                                    window_image[custom_rect[1] + j][custom_rect[0] + i][2] > custom_top_level[2]
                            ):
                            custom_window_image[j][i] = [0, 0, 0]
                        else:
                            custom_window_image[j][i] = [255, 255, 255]
                    else:
                        custom_window_image[j][i] = window_image[custom_rect[1] + j][custom_rect[0] + i]

            window_image = custom_window_image

        # if 'quest_scene_elite' in child.pixel_box_name:
        # 	img = Image.fromarray(window_image, 'RGB')
        # 	img.save(child.pixel_box_name+str(time.time())+'.png')

        if custom_threshold != -1:
            threshold = custom_threshold
        else:
            threshold = 0.8

        i = 0
        j = 0
        k = 0

        for elem in np.nditer(template_image, op_flags=['readwrite']):
            if custom_below_level != -1:
                if child[i + j][1][k] < custom_below_level[k]:
                    elem[...] = 0
                elif child[i + j][1][k] > custom_top_level[k]:
                    elem[...] = 255
                else:
                    elem[...] = child[i + j][1][k]
            else:
                elem[...] = child[i + j][1][k]

            k += 1
            if k >= 3:

                i += child.height
                k = 0
                if i >= child.height * child.width:
                    j += 1
                    i = 0
                    rgb, w, h = template_image.shape[::-1]

        if custom_flag != -1:
            for each_elem in template_image:
                i = 0
                for each_elem2 in each_elem:
                    if custom_below_level != -1 or custom_below_level != -1:
                        if (each_elem2[0] >= custom_below_level[0] and
                                    each_elem2[1] >= custom_below_level[1] and
                                    each_elem2[2] >= custom_below_level[2] and
                                    each_elem2[0] <= custom_top_level[0] and
                                    each_elem2[1] <= custom_top_level[1] and
                                    each_elem2[2] <= custom_top_level[2]
                            ):
                            each_elem[i] = [255, 255, 255]
                        else:
                            each_elem[i] = [0, 0, 0]

                    i += 1

        # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
        # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        # if 'quest_scene_elite' in child.pixel_box_name:
        # 	img = Image.fromarray(template_image, 'RGB')
        # 	img.save(child.pixel_box_name+'2_'+str(time.time())+'.png')

        methods = ['cv2.TM_CCOEFF_NORMED']

        result_dic = {}
        max_match_rate = 0

        for meth in methods:
            img = window_image.copy()
            method = eval(meth)

            print("YYYY:", img, template_image)
            res = cv2.matchTemplate(img, template_image, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # loc = np.where( res > 0.8 )
            # for pt in zip(*loc[::-1]):
            # 	print('DEBUG LOC:', pt)
            # 	# print('DEBUG LOC: ', pt)
            # 	pass

            # print(min_val, max_val, min_loc, max_loc, custom_threshold, child.pixel_box_name)

            # print(child.pixel_box_name, int(threshold*100), ':', int(max_val*100), max_loc, max_match_rate)

            if max_match_rate < max_val:
                max_match_rate = max_val

            if max_val < threshold:
                continue

            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            try:
                result_dic[(int(top_left[0] + w / 2), int(top_left[1] + h / 2))] += 1
            except:
                result_dic[(int(top_left[0] + w / 2), int(top_left[1] + h / 2))] = 1



            # if 'boss' in child.pixel_box_name:
            # 	img = Image.fromarray(window_image, 'RGB')
            # 	img.save(child.pixel_box_name+'.png')


            # print(meth, ':', min_val, max_val, min_loc, max_loc)


            # bottom_right = (top_left[0] + w, top_left[1] + h)

            # cv2.rectangle(img,top_left, bottom_right, 255, 2)

            # plt.subplot(121),plt.imshow(res,cmap = 'gray')
            # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            # plt.subplot(122),plt.imshow(img,cmap = 'gray')
            # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            # plt.suptitle(meth)
            # # plt.show()
            # plt.savefig('./'+str(meth)+'.png')

        if len(result_dic) > 0:
            sorted_list = sorted(result_dic.items(), key=operator.itemgetter(1), reverse=True)
            # print(sorted_list)
            if custom_flag == -1:
                return (sorted_list[0][0], max_match_rate)
            else:
                return ((sorted_list[0][0][0] + custom_rect[0], sorted_list[0][0][1] + custom_rect[1]), max_match_rate)
        else:
            return ((-1, -1), max_match_rate)

    def get_location(self, object_name):
        pixel_box = self.get_center_pixel_info(object_name)

        return (pixel_box[0][0], pixel_box[0][1])

    def get_center_pixel_info(self, object_name):
        pixel_box = self.resource_manager.pixel_box_dic[object_name]

        width = int(math.sqrt(len(pixel_box)))
        height = int(math.sqrt(len(pixel_box)))
        half = int(width * 0.5)

        middle_index = width * half + half

        return pixel_box[middle_index]

    def get_pixel_info(
            self,
            window_pixels,
            x, y):

        start_x, start_y, max_x, max_y = self.window.get_window_location(self.hwnd)
        adj_x, adj_y = self.window.get_player_adjust(self.hwnd)

        x = x + adj_x
        y = y + adj_y
        start_x = start_x - adj_x
        start_y = start_y - adj_y

        if x >= (max_x - start_x) or y > (max_y - start_y):
            return (-1, -1, -1)
        if x <= 0 or y <= 0:
            return (-1, -1, -1)

        return window_pixels[x, y]

    def isMatchedCenterPixelBox(
            self,
            window_pixels,
            pixel_box_name,
            custom_x=-1,
            custom_y=-1,
            custom_tolerance=-1
    ):
        try:
            pixel_box = self.resource_manager.pixel_box_dic[pixel_box_name]
        except:
            self.logger.error('Not found pixel box data:' + str(pixel_box_name))
            return False

        start_x, start_y, max_x, max_y = self.window.get_window_location(self.hwnd)
        adj_x, adj_y = self.window.get_player_adjust(self.hwnd)

        center_pixel = self.get_center_pixel_info(pixel_box_name)

        if custom_x != -1 and custom_y != -1:
            locx = custom_x
            locy = custom_y
        else:
            locx = center_pixel[0][0]
            locy = center_pixel[0][1]

        locx = locx + adj_x
        locy = locy + adj_y

        start_x = start_x - adj_x
        start_y = start_y - adj_y

        if locx >= (max_x - start_x) or locy > (max_y - start_y):
            return False
        if locx <= 0 or locy <= 0:
            return False

        (pixelR, pixelG, pixelB) = window_pixels[locx, locy]

        centerR = center_pixel[1][0]
        centerG = center_pixel[1][1]
        centerB = center_pixel[1][2]

        if custom_tolerance == -1:
            tolerance = float(self.get_window_config('pixel_tolerance_entry'))
        else:
            tolerance = custom_tolerance

        # print('DEBUG30: RGB=', (pixelR, pixelG, pixelB), ':', (centerR, centerG, centerB), tolerance)


        if (abs(pixelR - centerR) <= tolerance and
                    abs(pixelG - centerG) <= tolerance and
                    abs(pixelB - centerB) <= tolerance
            ):
            return True

        return False

    def rateMatchedPixelBox(
            self,
            window_pixels,
            pixel_box_name,
            custom_tolerance=-1,
            weight_tolerance=1.0,
            custom_below_level=-1,
            custom_top_level=-1
    ):
        (match_rate, match_location_number, total_num) = \
            self.numMatchedPixelBox(
                window_pixels, pixel_box_name,
                custom_tolerance=custom_tolerance,
                weight_tolerance=weight_tolerance,
                custom_below_level=custom_below_level,
                custom_top_level=custom_top_level)
        return match_rate

    def numMatchedPixelBox(
            self,
            window_pixels,
            pixel_box_name,
            custom_tolerance=-1,
            weight_tolerance=1.0,
            custom_below_level=-1,
            custom_top_level=-1
    ):
        try:
            pixel_box = self.resource_manager.pixel_box_dic[pixel_box_name]
        except:
            self.logger.error('Not found pixel box data: ' + str(pixel_box_name))
            return (0, 0, 0)

        match_location_number = 0
        match_rate = 0

        if custom_below_level != -1:
            below_level = custom_below_level
        else:
            below_level = 0

        if custom_top_level != -1:
            top_level = custom_top_level
        else:
            top_level = 255

        start_x, start_y, max_x, max_y = self.window.get_window_location(self.hwnd)
        adj_x, adj_y = self.window.get_player_adjust(self.hwnd)

        start_x = start_x - adj_x
        start_y = start_y - adj_y

        # self.logger.info(str(adj_x) + ', ' + str(adj_y))

        compare_pixel_len = 0

        # w, h = math.sqrt(len(pixel_box)), math.sqrt(len(pixel_box))
        # i =0
        # j=0
        # if 'tera_main_scene_maul' in pixel_box_name:
        # 	print(w, h)
        # 	data = np.zeros((int(h), int(w), 3), dtype=np.uint8)

        for each_location in pixel_box:
            try:

                ((locx, locy), (pR, pG, pB)) = each_location
                # if pR > top_level:
                # 	pR = 0
                # if pG > top_level:
                # 	pG = 0
                # if pB > top_level:
                # 	pB = 0

                # if pR < below_level:
                # 	pR = 0
                # if pG < below_level:
                # 	pG = 0
                # if pB < below_level:
                # 	pB = 0

                # if 'tera_main_scene_maul' in pixel_box_name:
                # 	data[j][i] = [pR, pG, pB]
                # 	j = j+1
                # 	if j > int(w) - 1:
                # 		i = i+1
                # 		j = 0


                if pR > top_level or pG > top_level or pB > top_level:
                    continue

                if pR < below_level or pG < below_level or pB < below_level:
                    continue

                locx = locx + adj_x
                locy = locy + adj_y
                if locx >= (max_x - start_x) or locy >= (max_y - start_y):
                    continue
                if locx <= 0 or locy <= 0:
                    continue

                (pixelR, pixelG, pixelB) = window_pixels[locx, locy]

                # if pixelR > top_level:
                # 	pixelR = 0
                # if pixelG > top_level:
                # 	pixelG = 0
                # if pixelB > top_level:
                # 	pixelB = 0

                # if pixelR < below_level:
                # 	pixelR = 0
                # if pixelG < below_level:
                # 	pixelG = 0
                # if pixelB < below_level:
                # 	pixelB = 0
                if pixelR > top_level or pixelG > top_level or pixelB > top_level:
                    continue

                if pixelR < below_level or pixelG < below_level or pixelB < below_level:
                    continue

                org_gap_RG = abs(pixelR - pixelG)
                org_gap_RB = abs(pixelR - pixelB)
                org_gap_GB = abs(pixelG - pixelB)

                tgt_gap_RG = abs(pR - pG)
                tgt_gap_RB = abs(pR - pB)
                tgt_gap_GB = abs(pG - pB)

                # TODO: 윈도우마다 설정 가능하게
                tolerance = float(self.get_window_config('pixel_tolerance_entry')) * weight_tolerance
                if custom_tolerance != -1:
                    tolerance = custom_tolerance

                compare_pixel_len += 1
                if ((abs(pixelR - pR) <= tolerance and abs(pixelG - pG) <= tolerance and abs(
                            pixelB - pB) <= tolerance) and
                        (abs(org_gap_RG - tgt_gap_RG) <= tolerance and abs(
                                org_gap_RB - tgt_gap_RB) <= tolerance and abs(org_gap_GB - tgt_gap_GB) <= tolerance)):
                    match_location_number += 1
                else:
                    # if 'tera_main_scene_maul' in pixel_box_name:
                    # 	print('[',pixel_box_name, ']:', (pixelR, pixelG, pixelB), (pR, pG, pB))
                    continue


            except:
                self.logger.warn(str(self.window_title) + str((locx, locy, start_x, start_y, max_x, max_y)))
                self.logger.error(traceback.format_exc())

        # if 'tera_main_scene_maul' in pixel_box_name:
        # 	print('[',pixel_box_name, ']:', match_location_number, '/', compare_pixel_len)
        # 	img = Image.fromarray(data, 'RGB')
        # 	img.save(pixel_box_name+'.png')
        # 	img.show()


        if compare_pixel_len > 0:
            match_rate = match_location_number / compare_pixel_len
        else:
            compare_pixel_len = len(pixel_box)
        # print(pixel_box_name, ':', int(match_rate * 100), '%')

        return (match_rate, match_location_number, compare_pixel_len)

    def mouse_click_location(self, loc_x, loc_y, delay=0, release=True):

        adj_x, adj_y = self.window.get_player_adjust(self.hwnd)

        self.last_click['loc'] = (loc_x + adj_x, loc_y + adj_y)
        # self.logger.warn((loc_x + adj_x, loc_y + adj_y))
        self.window.mouse_click(self.hwnd, loc_x + adj_x, loc_y + adj_y, delay=delay, release=release)

        return (loc_x + adj_x, loc_y + adj_y)

    def mouse_click(self, point_box_name, delay=0, release=True):
        s_x, s_y = self.resource_manager.pixel_box_dic[point_box_name][0][0]
        e_x, e_y = self.resource_manager.pixel_box_dic[point_box_name][-1][0]

        loc_x = int((s_x + e_x) / 2)
        loc_y = int((s_y + e_y) / 2)

        self.last_click['name'] = point_box_name
        self.mouse_click_location(loc_x, loc_y, delay=delay, release=release)

    def move_mouse(self, point_box_name):
        s_x, s_y = self.resource_manager.pixel_box_dic[point_box_name][0][0]
        e_x, e_y = self.resource_manager.pixel_box_dic[point_box_name][-1][0]

        loc_x = int((s_x + e_x) / 2)
        loc_y = int((s_y + e_y) / 2)

        self.move_mouse_location(loc_x, loc_y)

    def mouse_click_with_cursor(self, loc_x, loc_y):
        anchor_x, anchor_y, bx, by = self.window.get_window_location(self.hwnd)
        adj_x, adj_y = self.window.get_player_adjust(self.hwnd)

        loc_x = loc_x + adj_x
        loc_y = loc_y + adj_y
        anchor_x = anchor_x - adj_x
        anchor_y = anchor_y - adj_y

        pyautogui.click(anchor_x + loc_x, anchor_y + loc_y)

    def move_mouse_location(self, loc_x, loc_y):
        anchor_x, anchor_y, bx, by = self.window.get_window_location(self.hwnd)
        adj_x, adj_y = self.window.get_player_adjust(self.hwnd)

        loc_x = loc_x + adj_x
        loc_y = loc_y + adj_y
        anchor_x = anchor_x - adj_x
        anchor_y = anchor_y - adj_y

        pyautogui.moveTo(anchor_x + loc_x, anchor_y + loc_y)

    def drag_mouse(self, from_x, from_y, to_x, to_y, delay, stop_delay=0):
        self.window.mouse_drag(self.hwnd, int(from_x), int(from_y), int(to_x), int(to_y), delay=delay,
                               stop_delay=stop_delay,
                               move_away=self.common_config[lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away'])

    def rateMatchedResource(
            self,
            window_pixels,
            resource_name,
            weight_tolerance=1.0,
            custom_tolerance=-1,
            custom_below_level=-1,
            custom_top_level=-1
    ):
        try:
            resource = self.resource_manager.resource_dic[resource_name]
        except:
            self.logger.error('Not found resource data: ' + str(resource_name))
            return 0

        match_rate_sum = 0
        total_sum = 0

        for each_pixel_name in resource:
            (match_rate, match_rate_num, total_num) = self.numMatchedPixelBox(
                window_pixels,
                each_pixel_name,
                weight_tolerance=weight_tolerance,
                custom_tolerance=custom_tolerance,
                custom_below_level=custom_below_level,
                custom_top_level=custom_top_level
            )

            match_rate_sum += match_rate_num
            total_sum += total_num

        if total_sum > 0:
            return match_rate_sum / total_sum
        else:
            return 0

    def get_screen(self, window_pixels, resource_type=None, weight_threshold=1.0, weight_tolerance=-1):
        top_match_rate = {}
        match_resource_name = {}
        match_rate = {}

        resource_type_list = [
            'event',
            'scene'
        ]

        for each_resource_type in resource_type_list:
            top_match_rate[each_resource_type] = 0
            match_rate[each_resource_type] = 0
            match_resource_name[each_resource_type] = ''

        for each_resource in self.sorted_resource_dic:
            each_resource_name = each_resource.resource_name

            local_w = 1.0
            if resource_type != None:
                if each_resource.resource_type == resource_type:
                    match_rate[each_resource.resource_type] = self.rateMatchedResource(window_pixels,
                                                                                       each_resource_name,
                                                                                       weight_tolerance=weight_tolerance)
                else:
                    continue
            else:
                if each_resource.resource_type == 'event':
                    match_rate[each_resource.resource_type] = self.rateMatchedResource(window_pixels,
                                                                                       each_resource_name,
                                                                                       weight_tolerance=weight_tolerance * 0.5)
                    local_w = 1.3
                elif each_resource.resource_type == 'scene':
                    match_rate[each_resource.resource_type] = self.rateMatchedResource(window_pixels,
                                                                                       each_resource_name,
                                                                                       weight_tolerance=weight_tolerance)
                else:
                    continue


                ########################## DEBUG
                # if 'main_scene' in each_resource_name:
                # 	self.logger.info('main_scene : ' + str(match_rate) +  '%')
                # self.logger.info('threshold: ' + str(match_rate[each_resource.resource_type]) + ' ' + str(float(self.get_window_config('threshold_entry'))*weight_threshold*local_w) + ' ' + str(top_match_rate[each_resource.resource_type]))
            # print('threshold: ', float(self.common_config['threshold_entry']))

            threshold_value = float(self.get_window_config('threshold_entry')) * weight_threshold * local_w
            if threshold_value >= 1.0:
                threshold_value = 1.0

            if (match_rate[each_resource.resource_type] >= threshold_value and
                        match_rate[each_resource.resource_type] > top_match_rate[each_resource.resource_type]
                ):
                top_match_rate[each_resource.resource_type] = match_rate[each_resource.resource_type]
                match_resource_name[each_resource.resource_type] = each_resource_name
            # print(each_resource_name, ':', int(match_rate * 100), '%')

            if top_match_rate[each_resource.resource_type] >= 1.0:
                break

            # 유동적으로 변하는 씬은 제외하자.
            # if match_resource_name == 'lin2rev_google_play_account_select_scene':
            # 	match_resource_name = ''
            # print('+-------------------------------------------------+')
            # print('|                                                 |')
            # print('|    [' + match_resource_name + '][' + resource_type + '] :' + str(int(top_match_rate*100)) + '%')
            # print('|                                                 |')
            # print('+-------------------------------------------------+')

        if resource_type == 'event':
            self.current_matched_event['name'] = match_resource_name['event']
            self.current_matched_event['rate'] = int(top_match_rate['event'] * 100)
        elif resource_type == 'scene':
            self.current_matched_scene['name'] = match_resource_name['scene']
            self.current_matched_scene['rate'] = int(top_match_rate['scene'] * 100)
            self.current_matched_scene['threshold'] = str(
                int(self.get_window_config('threshold_entry') * weight_threshold * 100))
        else:
            self.current_matched_scene['name'] = match_resource_name['scene']
            self.current_matched_scene['rate'] = int(top_match_rate['scene'] * 100)
            self.current_matched_scene['threshold'] = str(
                int(self.get_window_config('threshold_entry') * weight_threshold * 100))
            self.current_matched_event['name'] = match_resource_name['event']
            self.current_matched_event['rate'] = int(top_match_rate['event'] * 100)

        return match_resource_name

    def get_window_config(self, config_name):
        if not config_name in self.window_config:
            return self.common_config[config_name]
        else:
            return self.window_config[config_name]

    def get_game_config(self, game_name, config_name, flag=0):

        if flag != 0:
            if not game_name in self.window_config:
                self.window_config[game_name] = copy.deepcopy(self.common_config[game_name])

            return self.window_config[game_name]

        if not game_name in self.window_config:
            self.window_config[game_name] = copy.deepcopy(self.common_config[game_name])
        elif not config_name in self.window_config[game_name]:
            self.window_config[game_name][config_name] = copy.deepcopy(self.common_config[game_name][config_name])

        config_value = self.window_config[game_name][config_name]
        if config_value == None:
            config_value = 0

        return config_value

    def get_player_adjust(self):
        return self.window.get_player_adjust(self.hwnd)

    def terminate_application(self):
        self.request_terminate = True

    def period_bot(self, weight):
        # 	print(self.get_window_config('wakeup_period_entry'))
        # 	print('[DEBUGXXXX] 1', self.common_config['wakeup_period_entry'])
        # 	print('[DEBUGXXXX] 2', self.window_config['wakeup_period_entry'])

        return float(self.common_config['wakeup_period_entry']) * float(weight)

    def getImagePixelBox(self, pixel_box_name):

        try:
            pixel_box = self.resource_manager.pixel_box_dic[pixel_box_name]
        except:
            self.logger.error('Not found pixel box data:' + str(pixel_box_name))
            return None

        template_image = np.ndarray(shape=(pixel_box.height, pixel_box.width, 3), dtype='uint8')

        i = 0
        j = 0
        k = 0

        for elem in np.nditer(template_image, op_flags=['readwrite']):
            elem[...] = pixel_box[i + j][1][k]

            k += 1
            if k >= 3:

                i += pixel_box.height
                k = 0
                if i >= pixel_box.height * pixel_box.width:
                    j += 1
                    i = 0
                    rgb, w, h = template_image.shape[::-1]

        return Image.fromarray(template_image, 'RGB')

    def getImageLocation(self, parent, custom_rect, custom_below_level=-1, custom_top_level=-1):
        window_image = np.array(parent)

        adj_x, adj_y = self.get_player_adjust()
        custom_rect2 = (custom_rect[0] + adj_x, custom_rect[1] + adj_y, custom_rect[2] + adj_x, custom_rect[3] + adj_y)

        custom_width = custom_rect2[2] - custom_rect2[0]
        custom_height = custom_rect2[3] - custom_rect2[1]
        custom_window_image = np.ndarray(shape=(custom_height, custom_width, 3), dtype='uint8')
        # print(window_image)
        custom_rect = custom_rect2
        for j in range(custom_height):
            for i in range(custom_width):
                # print(j, i, window_image[custom_rect[1] + j][custom_rect[0] + i])
                # 모모도 추가해야함
                if custom_below_level != -1 or custom_below_level != -1:
                    # self.logger.debug(window_image[custom_rect[1] + j][custom_rect[0] + i])
                    if (window_image[custom_rect[1] + j][custom_rect[0] + i][0] < custom_below_level[0] or
                                window_image[custom_rect[1] + j][custom_rect[0] + i][1] < custom_below_level[1] or
                                window_image[custom_rect[1] + j][custom_rect[0] + i][2] < custom_below_level[2] or
                                window_image[custom_rect[1] + j][custom_rect[0] + i][0] > custom_top_level[0] or
                                window_image[custom_rect[1] + j][custom_rect[0] + i][1] > custom_top_level[1] or
                                window_image[custom_rect[1] + j][custom_rect[0] + i][2] > custom_top_level[2]
                        ):
                        custom_window_image[j][i] = [0, 0, 0]
                    else:
                        custom_window_image[j][i] = [255, 255, 255]
                else:
                    custom_window_image[j][i] = window_image[custom_rect[1] + j][custom_rect[0] + i]

        window_image = custom_window_image

        return Image.fromarray(window_image, 'RGB')

    # if 'main_quest_complete' in child.pixel_box_name:
    # 	img = Image.fromarray(window_image, 'RGB')
    # 	img.save(child.pixel_box_name+str(time.time())+'.png')


class LYBGameTab():
    def __init__(self, root_frame, configure, game_options, inner_frames, width, height, game_name=''):
        self.master = root_frame
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.configure = configure
        self.option_dic = game_options
        self.inner_frame_dic = inner_frames
        self.frame_relief = 'flat'
        self.game_name = game_name
        self.width = width
        self.height = height
        self.schedule_lock_index = -1
        self.my_wlist_lock_index = -1

        # ----------------------------------------------------------------------
        #
        # 설정
        #
        # ----------------------------------------------------------------------

        frame_label = ttk.Frame(
            master=self.master
        )
        frame = ttk.Frame(frame_label)
        label = ttk.Label(

            master=frame,
            text='① [일반]탭에서 검색을 누르면 해당 게임을 실행할 창 정보가 보입니다',
            foreground='blue'

        )

        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)

        self.option_dic['window_list_stringvar'] = tkinter.StringVar(frame)
        self.option_dic['window_list_stringvar'].set('')
        self.option_dic['window_list_stringvar'].trace('w', lambda *args: self.select_window_list(args))

        self.option_dic['window_list_option_menu'] = ttk.Combobox(
            master=frame,
            values=[],
            textvariable=self.option_dic['window_list_stringvar'],
            state="readonly",
            height=10,
            width=15,
            font=lybconstant.LYB_FONT
        )
        self.option_dic['window_list_option_menu'].pack(anchor=tkinter.W, side=tkinter.LEFT)
        self.tooltip(self.option_dic['window_list_option_menu'], lybconstant.LYB_TOOLTIP_WINDOW_LIST)
        # self.option_dic['window_list_option_menu'] = ttk.OptionMenu(
        # 	frame,
        # 	self.option_dic['window_list_stringvar'],
        # 	''
        # 	)

        # self.option_dic['window_list_stringvar'].trace('w', lambda *args: self.select_window_list(args))
        # self.option_dic['window_list_option_menu'].configure(width=15)
        # self.option_dic['window_list_option_menu'].pack(side=tkinter.LEFT)

        label = ttk.Label(

            master=frame,
            text='←② 창 선택',
            foreground='blue'

        )

        label.pack(side=tkinter.LEFT, padx=2)

        self.option_dic['config_list_stringvar'] = tkinter.StringVar(frame)
        self.option_dic['config_list_stringvar'].set('')
        self.option_dic['config_list_stringvar'].trace('w', lambda *args: self.callback_select_config_stringvar(args))

        self.option_dic['config_list_option_menu'] = ttk.Combobox(
            master=frame,
            values=[],
            textvariable=self.option_dic['config_list_stringvar'],
            state="readonly",
            height=10,
            width=30,
            font=lybconstant.LYB_FONT
        )
        self.option_dic['config_list_option_menu'].pack(side=tkinter.LEFT)
        self.tooltip(self.option_dic['config_list_option_menu'], lybconstant.LYB_TOOLTIP_CUSTOM_CONFIG)

        # self.option_dic['config_list_option_menu'] = ttk.OptionMenu(
        # 	frame,
        # 	self.option_dic['config_list_stringvar'],
        # 	''
        # 	)
        # self.option_dic['config_list_stringvar'].trace('w', lambda *args: self.callback_select_config_stringvar(args))
        # self.option_dic['config_list_option_menu'].configure(width=18)
        # self.option_dic['config_list_option_menu'].pack(side=tkinter.LEFT)

        label = ttk.Label(

            master=frame,
            text='←③ 설정 선택',
            foreground='blue'

        )

        label.pack(side=tkinter.LEFT, padx=2)

        self.option_dic['config_save_stringvar'] = tkinter.StringVar(frame)
        self.option_dic['config_save_stringvar'].trace('w',
                                                       lambda *args: self.callback_save_config_stringvar(args))

        self.option_dic['config_save_entry'] = ttk.Entry(
            master=frame,
            textvariable=self.option_dic['config_save_stringvar'],
            justify=tkinter.LEFT,
            width=18,
            font=lybconstant.LYB_FONT
        )

        self.option_dic['config_save_entry'].pack(side=tkinter.LEFT)

        self.option_dic['config_save_button'] = ttk.Button(
            master=frame,
            text="저장",
            width=4,
            command=lambda: self.callback_save_button_stringvar(None)
        )
        self.option_dic['config_save_button'].pack(side=tkinter.LEFT, padx=2)

        self.option_dic['config_copy_button'] = ttk.Button(
            master=frame,
            text="복사",
            width=4,
            command=lambda: self.callback_copy_button_stringvar(None)
        )
        self.option_dic['config_copy_button'].pack(side=tkinter.LEFT, padx=2)

        self.option_dic['config_change_button'] = ttk.Button(
            master=frame,
            text="변경",
            width=4,
            command=lambda: self.callback_change_button_stringvar(None)
        )
        self.option_dic['config_change_button'].pack(side=tkinter.LEFT, padx=2)

        self.option_dic['config_delete_button'] = ttk.Button(
            master=frame,
            text="삭제",
            width=4,
            command=lambda: self.callback_delete_button_stringvar(None)
        )
        self.option_dic['config_delete_button'].pack(side=tkinter.LEFT, padx=2)

        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.W, fill=tkinter.BOTH, padx=1)

        # Notebook

        self.option_dic['schedule_note'] = ttk.Notebook(
            master=self.master
        )

        self.option_dic['schedule_note'].bind('<Button-1>', self.clicked_schedule_tab)

        # 일반 설정
        self.inner_frame_dic['normal_schedule_tab'] = ttk.Frame(
            master=self.option_dic['schedule_note']
        )

        self.inner_frame_dic['normal_schedule_tab'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['schedule_note'].add(self.inner_frame_dic['normal_schedule_tab'], text='스케쥴')

        # 고급 설정
        self.inner_frame_dic['advanced_schedule_tab'] = ttk.Frame(
            master=self.option_dic['schedule_note']
        )

        self.inner_frame_dic['advanced_schedule_tab'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['schedule_note'].add(self.inner_frame_dic['advanced_schedule_tab'], text='고급 설정')

        frame = ttk.Frame(self.inner_frame_dic['normal_schedule_tab'])

        s = ttk.Style()
        s.configure('workList.TFrame', background="green")
        s.configure('workListTitle.TFrame', background='green', foreground='black')
        s.configure('workListTitle.TLabel', background='green', foreground='black')

        s.configure('myWorkList.TFrame', background="grey")
        s.configure('myWorkListTitle.TFrame', background='grey', foreground='black')
        s.configure('myWorkListTitle.TLabel', background='grey', foreground='black')

        s.configure('schedule.TFrame', background='black')
        s.configure('schedule_title.TFrame', background='black', foreground='white')
        s.configure('schedule_title.TLabel', background='black', foreground='white')

        frame_l = ttk.Frame(
            master=frame)

        frame_l_l = ttk.Frame(
            master=frame_l,
            style='myWorkList.TFrame')

        frame_l_work = ttk.Frame(frame_l_l)

        frame_l_work_t = ttk.Frame(
            master=frame_l_work,
            style='myWorkListTitle.TFrame')

        # Label of work list
        self.option_dic['my_work_list_label'] = ttk.Label(

            master=frame_l_work_t,
            text=lybconstant.LYB_LABEL_AVAILABLE_WORK_LIST,
            style='myWorkListTitle.TLabel'

        )

        self.option_dic['my_work_list_label'].pack()
        self.tooltip(self.option_dic['my_work_list_label'], lybconstant.LYB_TOOLTIP_MY_WLIST)
        frame_l_work_t.pack(fill=tkinter.X)

        frame_l_work_b = ttk.Frame(frame_l_work)
        # Work list
        self.option_dic['my_work_list_listbox'] = tkinter.Listbox(

            master=frame_l_work_b,
            activestyle='none',
            exportselection=False,
            font=lybconstant.LYB_FONT,
            width=24

        )

        self.option_dic['my_work_list_vsb'] = ttk.Scrollbar(frame_l_work_b)
        self.option_dic['my_work_list_listbox'].configure(yscrollcommand=self.option_dic['my_work_list_vsb'].set)
        self.option_dic['my_work_list_vsb'].configure(command=self.option_dic['my_work_list_listbox'].yview)
        self.option_dic['my_work_list_vsb'].pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.option_dic['my_work_list_listbox'].pack(side=tkinter.LEFT)
        self.option_dic['my_work_list_listbox'].bind(
            '<<ListboxSelect>>',
            lambda event: self.select_my_work_list(event)
        )

        self.option_dic['my_work_list_listbox'].bind(
            '<MouseWheel>',
            lambda event: self.mouse_wheel(event, 'my_work_list_listbox')
        )
        frame_l_work_b.pack(anchor=tkinter.W)
        frame_l_work.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.Y, padx=2, pady=2)
        frame_l_l.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.Y)

        frame_l_r = ttk.Frame(
            master=frame_l,
            style='schedule.TFrame')

        frame_l_schedule = ttk.Frame(
            master=frame_l_r)

        frame_l_schedule_t = ttk.Frame(
            master=frame_l_schedule,
            style='schedule_title.TFrame')

        self.option_dic['schedule_list_label'] = ttk.Label(

            master=frame_l_schedule_t,
            text=lybconstant.LYB_LABEL_SCHEDULE_WORK_LIST,
            style='schedule_title.TLabel'

        )
        self.option_dic['schedule_list_label'].pack()
        self.tooltip(self.option_dic['schedule_list_label'], lybconstant.LYB_TOOLTIP_SCHEDULE)

        frame_l_schedule_t.pack(fill=tkinter.X)

        frame_l_schedule_b = ttk.Frame(frame_l_schedule)

        # scheule list
        self.option_dic['schedule_list_listbox'] = tkinter.Listbox(

            master=frame_l_schedule_b,
            activestyle='none',
            font=lybconstant.LYB_FONT,
            width=24

        )

        self.option_dic['schedule_list_vsb'] = ttk.Scrollbar(frame_l_schedule_b)
        self.option_dic['schedule_list_listbox'].configure(yscrollcommand=self.option_dic['schedule_list_vsb'].set)
        self.option_dic['schedule_list_vsb'].configure(command=self.option_dic['schedule_list_listbox'].yview)
        self.option_dic['schedule_list_vsb'].pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.option_dic['schedule_list_listbox'].pack(anchor=tkinter.W)
        self.option_dic['schedule_list_listbox'].bind(
            '<<ListboxSelect>>',
            lambda event: self.select_schedule_list(event)
        )
        self.option_dic['schedule_list_listbox'].bind(
            '<MouseWheel>',
            lambda event: self.mouse_wheel(event, 'schedule_list_listbox')
        )

        frame_l_schedule_b.pack(anchor=tkinter.W)
        frame_l_schedule.pack(side=tkinter.LEFT, anchor=tkinter.W, padx=2, pady=2)
        frame_l_r.pack(side=tkinter.LEFT, anchor=tkinter.W)

        frame_l_schedule_button = ttk.Frame(
            master=frame_l
        )

        button_padding = 1
        schedule_button = ttk.Button(
            master=frame_l_schedule_button,
            text="D",
            width=2,
            command=lambda: self.callback_schedule_delete_button_stringvar(None)
        )
        schedule_button.pack(side=tkinter.BOTTOM, pady=button_padding)
        self.tooltip(schedule_button, lybconstant.LYB_TOOLTIP_DELETE)

        schedule_button = ttk.Button(
            master=frame_l_schedule_button,
            text="C",
            width=2,
            command=lambda: self.callback_schedule_copy_button_stringvar(None)
        )
        schedule_button.pack(side=tkinter.BOTTOM, pady=button_padding)
        self.tooltip(schedule_button, lybconstant.LYB_TOOLTIP_COPY)

        s = ttk.Style()
        s.configure('toggle_false.TButton', relief='raised', foreground='green')
        s.configure('toggle_true.TButton', relief='sunken', foreground='red')

        self.option_dic['schedule_lock_button'] = ttk.Button(
            master=frame_l_schedule_button,
            text="U",
            width=2,
            style='toggle_false.TButton',
            command=lambda: self.callback_schedule_lock_button_stringvar(None)
        )
        self.option_dic['schedule_lock_button'].pack(side=tkinter.BOTTOM, pady=button_padding)
        self.tooltip(self.option_dic['schedule_lock_button'], lybconstant.LYB_TOOLTIP_SCHEDULE_LOCK_BUTTON)

        schedule_button = ttk.Button(
            master=frame_l_schedule_button,
            text="▼",
            width=2,
            command=lambda: self.callback_schedule_down_button_stringvar(None)
        )
        schedule_button.pack(side=tkinter.BOTTOM, pady=button_padding)

        schedule_button = ttk.Button(
            master=frame_l_schedule_button,
            text="▲",
            width=2,
            command=lambda: self.callback_schedule_up_button_stringvar(None)
        )
        schedule_button.pack(side=tkinter.BOTTOM, pady=button_padding)

        # self.option_dic[lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE] = tkinter.BooleanVar(frame_l_schedule_button)
        # self.option_dic[lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE].trace(
        # 	'w', lambda *args: self.callback_schedule_lock_booleanvar(args)
        # 	)

        # checkbutton = ttk.Checkbutton(

        # 	master				= frame_l_schedule_button,
        # 	text 				= '잠금',
        # 	variable 			= self.option_dic[lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE],
        # 	onvalue 			= True,
        # 	offvalue 			= False

        # 	)
        # checkbutton.pack(side=tkinter.BOTTOM)

        frame_l_schedule_button.pack(anchor=tkinter.W, fill=tkinter.Y, expand=True, pady=2)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=5)

        # 게임 설정

        # self.configure.common_config[self.game_name] = {}
        if not self.game_name in self.configure.common_config:
            self.configure.common_config[self.game_name] = {}

        frame_r = ttk.Frame(frame)
        label = ttk.Label(
            master=frame_r,
            text="※ 자동 재시작을 위해서는 스케쥴에 [게임 시작][로그인] 작업 등록 필수",
            foreground='red'
        )

        label.pack(side=tkinter.LEFT)
        frame_r.pack(anchor=tkinter.W)

        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)

        self.option_dic[lybconstant.LYB_DO_BOOLEAN_RESTART_GAME] = tkinter.BooleanVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_BOOLEAN_RESTART_GAME].trace(
            'w', lambda *args: self.callback_restart_game_booleanvar(args, lybconstant.LYB_DO_BOOLEAN_RESTART_GAME)
        )

        if not lybconstant.LYB_DO_BOOLEAN_RESTART_GAME in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_BOOLEAN_RESTART_GAME] = False

        check_box = ttk.Checkbutton(

            master=frame_r,
            text='등록된 스케쥴이 모두 완료되면 게임을 종료합니다',
            variable=self.option_dic[lybconstant.LYB_DO_BOOLEAN_RESTART_GAME],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(side=tkinter.LEFT, anchor=tkinter.W)

        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)

        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'] = tkinter.BooleanVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'].trace('w',
                                                                                          lambda
                                                                                              *args: self.callback_period_restart_game_schedule_booleanvar(
                                                                                              args,
                                                                                              option_name=lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'))

        if not lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'] = True

        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'].set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'])

        checkbutton = ttk.Checkbutton(
            master=frame_r,
            text="게임 시작시 스케쥴을 초기화 합니다",
            variable=self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME + 'schedule'],
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)
        label = ttk.Label(
            master=frame_r,
            text="등록된 스케쥴이 모두 완료되면 "
        )

        label.pack(side=tkinter.LEFT)

        combo_list = []
        for i in range(0, 601):
            combo_list.append(str(i))

        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_REST] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_REST].trace('w',
                                                                     lambda *args: self.callback_period_rest_stringvar(
                                                                         args,
                                                                         option_name=lybconstant.LYB_DO_STRING_PERIOD_REST))

        if not lybconstant.LYB_DO_STRING_PERIOD_REST in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_PERIOD_REST] = combo_list[0]

        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_REST].set(combo_list[0])
        combobox = ttk.Combobox(
            master=frame_r,
            values=combo_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_REST],
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT,
            justify=tkinter.RIGHT
        )
        combobox.set(combo_list[0])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text=" 초 동안 작업을 쉽니다"
        )
        label.pack(side=tkinter.LEFT)
        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)
        label = ttk.Label(
            master=frame_r,
            text="게임을 "
        )

        label.pack(side=tkinter.LEFT)

        combo_list = []
        for i in range(0, 1441):
            combo_list.append(str(i))

        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME].trace('w',
                                                                             lambda
                                                                                 *args: self.callback_period_restart_game_stringvar(
                                                                                 args,
                                                                                 option_name=lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME))

        if not lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME] = combo_list[
                1439]

        self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME].set(combo_list[1439])

        combobox = ttk.Combobox(
            master=frame_r,
            values=combo_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME],
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT,
            justify=tkinter.RIGHT
        )
        combobox.set(combo_list[1439])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text="분 마다 주기적으로 종료합니다(0:사용안함)"
        )
        label.pack(side=tkinter.LEFT)
        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)
        label = ttk.Label(
            master=frame_r,
            text="[반복 시작][반복 종료] 작업을 "
        )

        label.pack(side=tkinter.LEFT)

        repeat_list = []
        for i in range(1, 1000):
            repeat_list.append(str(i))

        self.option_dic[lybconstant.LYB_DO_STRING_COUNT_LOOP] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_COUNT_LOOP].trace(
            'w',
            lambda *args: self.callback_count_loop_stringvar(args, option_name=lybconstant.LYB_DO_STRING_COUNT_LOOP)
        )

        if not lybconstant.LYB_DO_STRING_COUNT_LOOP in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_COUNT_LOOP] = repeat_list[0]

        self.option_dic[lybconstant.LYB_DO_STRING_COUNT_LOOP].set(repeat_list[0])

        combobox = ttk.Combobox(
            master=frame_r,
            values=repeat_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_COUNT_LOOP],
            state="readonly",
            height=10,
            width=4,
            font=lybconstant.LYB_FONT,
            justify=tkinter.RIGHT
        )
        combobox.set(repeat_list[0])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text="회 수행합니다"
        )

        label.pack(side=tkinter.LEFT)
        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)
        label = ttk.Label(
            master=frame_r,
            text="[작업 예약] 시간:"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_HOUR] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_HOUR].trace('w',
                                                                       lambda
                                                                           *args: self.callback_reserved_hour_stringvar(
                                                                           args,
                                                                           lybconstant.LYB_DO_STRING_RESERVED_HOUR))

        hour_list = []
        for i in range(24):
            hour_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_RESERVED_HOUR in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_RESERVED_HOUR] = hour_list[0]

        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_HOUR].set(hour_list[0])

        combobox = ttk.Combobox(
            master=frame_r,
            values=hour_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_HOUR],
            state="readonly",
            height=10,
            width=3,
            font=lybconstant.LYB_FONT
        )
        combobox.set(hour_list[0])

        # for each_elem in hour_list:
        # 	option_menu['menu'].add_command(
        # 		label 				= each_elem,
        # 		command 			= tkinter._setit(self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_HOUR], each_elem)
        # 		)
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text="시"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_MINUTE] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_MINUTE].trace('w',
                                                                         lambda
                                                                             *args: self.callback_reserved_minute_stringvar(
                                                                             args,
                                                                             lybconstant.LYB_DO_STRING_RESERVED_MINUTE))

        minute_list = []
        for i in range(60):
            minute_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_RESERVED_MINUTE in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_RESERVED_MINUTE] = minute_list[0]

        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_MINUTE].set(minute_list[0])

        combobox = ttk.Combobox(
            master=frame_r,
            values=minute_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_MINUTE],
            state="readonly",
            height=10,
            width=3,
            font=lybconstant.LYB_FONT
        )
        combobox.set(minute_list[0])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text="분"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_SECOND] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_SECOND].trace('w',
                                                                         lambda
                                                                             *args: self.callback_reserved_second_stringvar(
                                                                             args,
                                                                             lybconstant.LYB_DO_STRING_RESERVED_SECOND))

        second_list = []
        for i in range(0, 60, 5):
            second_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_RESERVED_SECOND in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_RESERVED_SECOND] = second_list[0]

        self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_SECOND].set(second_list[0])

        combobox = ttk.Combobox(
            master=frame_r,
            values=second_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_RESERVED_SECOND],
            state="readonly",
            height=10,
            width=3,
            font=lybconstant.LYB_FONT
        )
        combobox.set(second_list[0])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text="초"
        )
        label.pack(side=tkinter.LEFT)
        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)
        label = ttk.Label(
            master=frame_r,
            text="[작업 대기] 시간:"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT] = tkinter.StringVar(frame_r)
        self.option_dic[lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT].trace('w',
                                                                       lambda
                                                                           *args: self.callback_wait_for_next_stringvar(
                                                                           args,
                                                                           lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT))

        hour_list = []
        for i in range(1, 3600):
            hour_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT] = hour_list[59]

        self.option_dic[lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT].set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT])

        combobox = ttk.Combobox(
            master=frame_r,
            values=hour_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT],
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT
        )
        # combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame_r,
            text="초"
        )
        label.pack(side=tkinter.LEFT)
        frame_r.pack(anchor=tkinter.W)

        frame_r = ttk.Frame(frame)

        label = ttk.Label(
            master=frame_r,
            text="[알림]:"
        )
        label.pack(side=tkinter.LEFT)
        self.option_dic[lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE].trace('w',
                                                                        lambda
                                                                            *args: self.callback_notify_message_stringvar(
                                                                            args,
                                                                            lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE))

        if not lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE] = '도그푸터 매크로에서 보내는 메세지입니다.'

        self.option_dic[lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE].set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE])
        entry = ttk.Entry(
            master=frame_r,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE],
            justify=tkinter.LEFT,
            font=lybconstant.LYB_FONT
        )

        entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        frame_r.pack(anchor=tkinter.W, fill=tkinter.X)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(self.inner_frame_dic['advanced_schedule_tab'])

        frame_l = ttk.Frame(
            master=frame)

        frame_l_l = ttk.Frame(
            master=frame_l,
            style='workList.TFrame')

        frame_l_work = ttk.Frame(frame_l_l)

        frame_l_work_t = ttk.Frame(
            master=frame_l_work,
            style='workListTitle.TFrame')

        self.option_dic['work_list_label'] = ttk.Label(

            master=frame_l_work_t,
            text=lybconstant.LYB_LABEL_WORK_LIST,
            style='workListTitle.TLabel'

        )

        self.option_dic['work_list_label'].pack()
        frame_l_work_t.pack(fill=tkinter.X)

        frame_l_work_b = ttk.Frame(frame_l_work)

        # Work list
        self.option_dic['work_list_listbox'] = tkinter.Listbox(

            master=frame_l_work_b,
            activestyle='none',
            exportselection=False,
            font=lybconstant.LYB_FONT,
            width=24

        )

        self.option_dic['work_list_vsb'] = ttk.Scrollbar(frame_l_work_b)
        self.option_dic['work_list_listbox'].configure(yscrollcommand=self.option_dic['work_list_vsb'].set)
        self.option_dic['work_list_vsb'].configure(command=self.option_dic['work_list_listbox'].yview)
        self.option_dic['work_list_vsb'].pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.option_dic['work_list_listbox'].pack(side=tkinter.LEFT)
        self.option_dic['work_list_listbox'].bind(
            '<<ListboxSelect>>',
            lambda event: self.select_work_list(event)
        )

        self.option_dic['work_list_listbox'].bind(
            '<MouseWheel>',
            lambda event: self.mouse_wheel(event, 'work_list_listbox')
        )
        frame_l_work_b.pack(anchor=tkinter.W)
        frame_l_work.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.X, padx=2, pady=2)
        frame_l_l.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.Y)

        frame_l_r = ttk.Frame(
            master=frame_l,
            style='myWorkList.TFrame')

        frame_l_r_frame = ttk.Frame(frame_l_r)

        frame_l_r_frame_t = ttk.Frame(
            master=frame_l_r_frame,
            style='myWorkListTitle.TFrame')

        self.option_dic['advanced_my_work_list'] = ttk.Label(

            master=frame_l_r_frame_t,
            text=lybconstant.LYB_LABEL_AVAILABLE_WORK_LIST,
            style='myWorkListTitle.TLabel'

        )
        self.option_dic['advanced_my_work_list'].pack()
        frame_l_r_frame_t.pack(fill=tkinter.X)

        frame_l_work_b = ttk.Frame(frame_l_r_frame)
        self.option_dic['advanced_my_work_list_listbox'] = tkinter.Listbox(

            master=frame_l_work_b,
            activestyle='none',
            font=lybconstant.LYB_FONT,
            width=24

        )

        self.option_dic['advanced_my_work_list_vsb'] = ttk.Scrollbar(frame_l_r_frame)
        self.option_dic['advanced_my_work_list_listbox'].configure(
            yscrollcommand=self.option_dic['advanced_my_work_list_vsb'].set)
        self.option_dic['advanced_my_work_list_vsb'].configure(
            command=self.option_dic['advanced_my_work_list_listbox'].yview)
        self.option_dic['advanced_my_work_list_vsb'].pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.option_dic['advanced_my_work_list_listbox'].pack(anchor=tkinter.W)
        self.option_dic['advanced_my_work_list_listbox'].bind(
            '<<ListboxSelect>>',
            lambda event: self.select_advanced_my_work_list(event)
        )
        self.option_dic['advanced_my_work_list_listbox'].bind(
            '<MouseWheel>',
            lambda event: self.mouse_wheel(event, 'advanced_my_work_list_listbox')
        )

        frame_l_work_b.pack(anchor=tkinter.W)
        frame_l_r_frame.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.Y, padx=2, pady=2)
        frame_l_r.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.Y)

        frame_l_my_wlist_button = ttk.Frame(
            master=frame_l
        )

        button_padding = 1
        w_button = ttk.Button(
            master=frame_l_my_wlist_button,
            text="D",
            width=2,
            command=lambda: self.callback_my_wlist_delete_button_stringvar(None)
        )
        w_button.pack(side=tkinter.BOTTOM, pady=button_padding)

        w_button = ttk.Button(
            master=frame_l_my_wlist_button,
            text="I",
            width=2,
            command=lambda: self.callback_my_wlist_init_button_stringvar(None)
        )
        w_button.pack(side=tkinter.BOTTOM, pady=button_padding)

        self.option_dic['my_wlist_lock_button'] = ttk.Button(
            master=frame_l_my_wlist_button,
            text="U",
            width=2,
            style='toggle_false.TButton',
            command=lambda: self.callback_my_wlist_lock_button_stringvar(None)
        )
        self.option_dic['my_wlist_lock_button'].pack(side=tkinter.BOTTOM, pady=button_padding)

        w_button = ttk.Button(
            master=frame_l_my_wlist_button,
            text="▼",
            width=2,
            command=lambda: self.callback_my_wlist_down_button_stringvar(None)
        )
        w_button.pack(side=tkinter.BOTTOM, pady=button_padding)

        w_button = ttk.Button(
            master=frame_l_my_wlist_button,
            text="▲",
            width=2,
            command=lambda: self.callback_my_wlist_up_button_stringvar(None)
        )
        w_button.pack(side=tkinter.BOTTOM, pady=button_padding)
        frame_l_my_wlist_button.pack(anchor=tkinter.W, fill=tkinter.Y, expand=True, pady=2)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW, fill=tkinter.Y, padx=5)

        frame.pack(anchor=tkinter.W)

        self.option_dic['schedule_note'].pack(anchor=tkinter.NW, fill=tkinter.BOTH)
        self.inner_frame_dic['frame_top'] = frame

        self.configure.common_config[self.game_name]['work_list'] = []
        self.configure.common_config[self.game_name]['schedule_list'] = []

        if not lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE] = False

        if not lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST] = False

        self.set_work_list()

        temp_schdule_list = copy.deepcopy(self.configure.common_config[self.game_name]['work_list'])
        for each_schedule in temp_schdule_list:
            if len(each_schedule) > 0:
                self.configure.common_config[self.game_name]['schedule_list'].append(each_schedule)

        self.configure.common_config[self.game_name]['schedule_list'].append('')

        for each_work in self.configure.common_config[self.game_name]['schedule_list']:
            self.option_dic['schedule_list_listbox'].insert('end', each_work)

        if not 'my_work_list' in self.configure.common_config[self.game_name]:
            self.initialize_my_wlist()
        # self.configure.common_config[self.game_name]['my_work_list'] = []
        # for each_schedule in temp_schdule_list:
        # 	if len(each_schedule) > 0:
        # 		self.configure.common_config[self.game_name]['my_work_list'].append(each_schedule)

        # self.configure.common_config[self.game_name]['my_work_list'].append('')

        self.set_option()

        self.callback_select_config_stringvar(None)

    def tooltip(self, widget_name, text):
        tooltip = ToolTip(widget_name, text)
        tooltip.wraplength = 640

    def set_work_list(self):
        self.option_dic['work_list_listbox'].delete(0, 'end')

    def set_option(self):
        self.logger.debug('Game set_option')
        pass

    # def set_game_option(self):
    # 	pass

    def callback_delete_button_stringvar(self, event):
        # selected_window_name = self.option_dic['window_list_stringvar'].get()
        user_config_name = self.option_dic['config_save_stringvar'].get()
        last_config_name = self.game_name + '_last'

        # if len(selected_window_name) < 1:
        # 	return

        if len(user_config_name) < 1:
            delete_config_name = self.game_name + '_기본설정'
        else:
            delete_config_name = self.game_name + '_' + user_config_name

        if delete_config_name == self.game_name + '_기본설정':
            return

        self.configure.window_config['custom_config_dic'].pop(delete_config_name, None)
        self.option_dic['config_list_stringvar'].set(self.game_name + '_기본설정')
        self.callback_select_config_stringvar(None)

    def callback_change_button_stringvar(self, event):
        delete_config_name = self.option_dic['config_list_stringvar'].get()

        if delete_config_name == self.game_name + '_기본설정':
            return

        self.logger.debug('DeleteConfigFileName: ' + str(delete_config_name))

        self.callback_copy_button_stringvar(None)
        self.configure.window_config['custom_config_dic'].pop(delete_config_name, None)
        self.callback_select_config_stringvar(None)

    def callback_copy_button_stringvar(self, event):
        selected_window_name = self.option_dic['window_list_stringvar'].get()
        user_config_name = self.option_dic['config_save_stringvar'].get()
        config_name = self.option_dic['config_list_stringvar'].get()

        last_config_name = self.game_name + '_last'

        # if len(selected_window_name) < 1:
        # 	return

        if len(user_config_name) < 1:
            save_config_name = self.game_name + '_기본설정'
        else:
            save_config_name = self.game_name + '_' + user_config_name
        # while True:
        # 	if save_config_name in self.configure.window_config['custom_config_dic']:
        # 		save_config_name = save_config_name + '_복사본'
        # 	else:
        # 		break

        # if len(selected_window_name) > 0:
        # 	self.configure.window_config['custom_config_dic'][save_config_name] = \
        # 		copy.deepcopy(self.configure.window_config[selected_window_name][self.game_name])
        # else:
        self.configure.window_config['custom_config_dic'][save_config_name] = \
            copy.deepcopy(self.configure.window_config['custom_config_dic'][config_name])

        self.option_dic['config_list_stringvar'].set(save_config_name)
        index = 0
        for each_work in self.configure.common_config[self.game_name]['my_work_list']:
            if len(each_work) < 1:
                break
            index += 1
        self.configure.common_config[self.game_name]['my_work_list'].insert(index, save_config_name)
        self.callback_select_config_stringvar(None)

    def callback_save_button_stringvar(self, event):

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_save_config_stringvar(self, *args):
        # print('[SAVE CONFIG]')
        # print('[SAVE CONFIG STRINGVAR]', self.option_dic['config_save_stringvar'].get())
        self.set_game_option()

    def callback_select_config_stringvar(self, *args):

        selected_window_name = self.option_dic['window_list_stringvar'].get()
        # if len(selected_window_name) < 1:
        # 	return
        # print('[SELECT CONFIG]:', selected_window_name)
        # print(self.configure.window_config[selected_window_name][self.game_name])


        # print('DEBUG CONFIG LIST:', self.option_dic['config_list_stringvar'].get())

        last_config_name = self.game_name + '_last'
        default_config_name = self.game_name + '_기본설정'

        if not 'custom_config_dic' in self.configure.window_config:
            self.configure.window_config['custom_config_dic'] = {}
            self.configure.window_config['custom_config_dic'][default_config_name] = \
                copy.deepcopy(self.configure.common_config[self.game_name])
        elif not default_config_name in self.configure.window_config['custom_config_dic']:
            self.configure.window_config['custom_config_dic'][default_config_name] = \
                copy.deepcopy(self.configure.common_config[self.game_name])

        selected_config = self.option_dic['config_list_stringvar'].get()
        # if not selected_config in self.configure.window_config['custom_config_dic']:
        # 	selected_config = ''

        if len(selected_window_name) > 0:
            if len(selected_config) < 1:
                if not last_config_name in self.configure.window_config[selected_window_name]:
                    self.configure.window_config[selected_window_name][last_config_name] = default_config_name
                selected_config = self.configure.window_config[selected_window_name][last_config_name]

            else:
                self.configure.window_config[selected_window_name][last_config_name] = selected_config
        else:
            if len(selected_config) < 1:
                selected_config = default_config_name

        new_config_list = []
        for each_config, each_config_value in self.configure.window_config['custom_config_dic'].items():
            if self.game_name in each_config:
                # print('[SELECT CONFIG EACH]:', each_config)

                if each_config == last_config_name:
                    pass
                elif each_config == self.game_name:
                    pass
                else:
                    new_config_list.append(each_config)
        # print('<<<<<<<<<<<<<<<<<<<<<<< S')

        self.option_dic['config_list_stringvar'].set('')
        self.option_dic['config_list_stringvar'].set(selected_config)

        # last_index = self.option_dic['config_list_option_menu']['menu'].index('end')
        # print('[DEBUG========]', threading.current_thread(), self.option_dic['config_list_option_menu']['menu'], last_index)
        # self.option_dic['config_list_option_menu']['menu'].delete(0, 'end')

        # if last_index != None:
        # 	for i in range(last_index + 1):
        # 		print('==========>', self.option_dic['config_list_option_menu']['menu'].entrycget(i, "label"))


        self.option_dic['config_list_option_menu']['values'] = new_config_list
        # for each_config in new_config_list:
        # 	self.option_dic['config_list_option_menu']['menu'].add_command(
        # 		label 				= each_config,
        # 		command 			= tkinter._setit(self.option_dic['config_list_stringvar'], each_config)
        # )

        # print('>>>>>>>>>>>>>>>>>>>>>>> E')

        try:
            if len(selected_window_name) > 0:
                self.configure.window_config[selected_window_name][self.game_name] = \
                    self.configure.window_config['custom_config_dic'][selected_config]
            # print('=====================', self.adjust_config_name(selected_config))
            self.option_dic['config_save_stringvar'].set(self.adjust_config_name(selected_config))
            # self.option_dic['config_save_entry'].selection_range(0, 'end')
            self.callback_save_config_stringvar(None)
            self.update_schedule_list()
            self.update_my_work_list()
            # s = time.time()
            self.update_work_list()
            self.update_lock_button()
        # e = time.time()
        # print('[DEBUG] ElapsedWorkListLoadingTime:', e - s)
        # self.update_my_work_list()
        except:
            self.logger.error(traceback.format_exc())

    def adjust_config_name(self, config_name):
        return config_name.replace(self.game_name, '', 1).replace('_', '', 1)

    def select_window_list(self, *args):

        selected_window_name = self.option_dic['window_list_stringvar'].get()
        if len(selected_window_name) > 0:
            if not self.game_name in self.configure.window_config[selected_window_name]:
                self.configure.window_config[selected_window_name][self.game_name] = \
                    copy.deepcopy(self.configure.common_config[self.game_name])
            size = self.option_dic['schedule_list_listbox'].size()
            self.option_dic['schedule_list_listbox'].delete(0, size - 1)

            schedule_work_list = self.get_game_schedule_list()

            # window_name = self.option_dic['window_list_stringvar'].get()

            for each_work in schedule_work_list:
                self.option_dic['schedule_list_listbox'].insert('end', each_work)

        self.option_dic['config_list_stringvar'].set('')
        self.callback_select_config_stringvar(None)

    def select_work_list(self, event):
        last_index = self.option_dic['work_list_listbox'].size() - 1
        self.option_dic['work_list_listbox'].selection_clear(last_index)

        my_wlist = self.configure.common_config[self.game_name]['my_work_list']

        if len(self.option_dic['work_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['work_list_listbox'].curselection()[0]
            # 공백이면 리턴
            if item_index == last_index:
                return

            selected_work_name = self.option_dic['work_list_listbox'].get(item_index)

            if len(selected_work_name) < 1:
                self.option_dic['work_list_listbox'].selection_clear(item_index)
                return

            # if selected_work_name in self.configure.window_config['custom_config_dic']:
            # 	if selected_work_name == self.option_dic['config_list_stringvar'].get():
            # 		return

            if len(self.option_dic['advanced_my_work_list_listbox'].curselection()) == 0:
                self.my_wlist_lock_index = -1
            else:
                self.my_wlist_lock_index = self.option_dic['advanced_my_work_list_listbox'].curselection()[0]
                self.option_dic['advanced_my_work_list_listbox'].selection_clear(self.my_wlist_lock_index)

            blank_index = 0
            for i in range(self.option_dic['advanced_my_work_list_listbox'].size()):
                if len(self.option_dic['advanced_my_work_list_listbox'].get(i)) < 1:
                    break
                blank_index += 1

            self.logger.debug('blankIndex=' + str(blank_index))

            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST) == True:
                if self.my_wlist_lock_index == -1 or self.my_wlist_lock_index > blank_index - 1:
                    self.option_dic['advanced_my_work_list_listbox'].selection_clear(blank_index - 1)
                    self.my_wlist_lock_index = blank_index

                my_wlist.insert(self.my_wlist_lock_index + 1, selected_work_name)
                self.option_dic['advanced_my_work_list_listbox'].insert(self.my_wlist_lock_index + 1,
                                                                        selected_work_name)
                self.option_dic['advanced_my_work_list_listbox'].select_set(self.my_wlist_lock_index + 1)
            else:
                self.option_dic['advanced_my_work_list_listbox'].selection_clear(blank_index - 1)
                my_wlist.insert(blank_index, selected_work_name)
                self.option_dic['advanced_my_work_list_listbox'].insert(blank_index, selected_work_name)
                self.option_dic['advanced_my_work_list_listbox'].select_set(blank_index)

            # self.build_schedule_list()
            # self.update_my_work_list()

    def select_advanced_my_work_list(self, event):
        game_name = self.game_name

        blank_index = 0
        for i in range(self.option_dic['advanced_my_work_list_listbox'].size()):
            if len(self.option_dic['advanced_my_work_list_listbox'].get(i)) < 1:
                break
            blank_index += 1

        last_index = blank_index

        self.logger.debug('last index:' + str(last_index))
        self.option_dic['advanced_my_work_list_listbox'].selection_clear(last_index)

        my_wlist = self.configure.common_config[self.game_name]['my_work_list']

        if len(self.option_dic['advanced_my_work_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['advanced_my_work_list_listbox'].curselection()[0]
            self.logger.debug('item_index:' + str(item_index))

            if item_index == last_index:
                return

            selected_work_name = self.option_dic['advanced_my_work_list_listbox'].get(item_index)
            self.logger.debug('selected_work_name:' + str(selected_work_name))

            if len(selected_work_name) < 1:
                self.option_dic['advanced_my_work_list_listbox'].selection_clear(item_index)
                return

            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST) == True:
                self.my_wlist_lock_index = item_index
            else:
                my_wlist.remove(selected_work_name)
                self.option_dic['advanced_my_work_list_listbox'].delete(item_index)
            # print('DEBUG77:', self.option_dic['schedule_list_listbox'].size())
            # self.update_my_work_list()

    # 리스트박스를 클릭하면 선택되는 거 같다. 그래서 마지막에 공백을 넣었다.
    def select_my_work_list(self, event):
        game_name = self.game_name
        last_index = self.option_dic['my_work_list_listbox'].size() - 1
        self.option_dic['my_work_list_listbox'].selection_clear(last_index)

        # selected_window_name = self.option_dic['window_list_stringvar'].get()

        schedule_list = self.get_game_schedule_list()
        # print('DEBUG12:', schedule_list)
        # for i in range(self.option_dic['work_list_listbox'].size()):
        # 	print('DEBUG12-1:', self.option_dic['work_list_listbox'].get(i))

        # print('DEBUG13:', self.option_dic['work_list_listbox'].curselection())
        if len(self.option_dic['my_work_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['my_work_list_listbox'].curselection()[0]
            # 공백이면 리턴
            if item_index == last_index:
                return

            selected_work_name = self.option_dic['my_work_list_listbox'].get(item_index)

            if len(selected_work_name) < 1:
                self.option_dic['my_work_list_listbox'].selection_clear(item_index)
                return

            if selected_work_name in self.configure.window_config['custom_config_dic']:
                if selected_work_name == self.option_dic['config_list_stringvar'].get():
                    return


                # print('DEBUG88:', self.option_dic['schedule_list_listbox'].size())

                # if not selected_work_name in schedule_list:
                # schedule_list.append(selected_work_name)

            # print('DEBUG::', self.schedule_lock_index)


            if len(self.option_dic['schedule_list_listbox'].curselection()) == 0:
                self.schedule_lock_index = -1
            else:
                self.schedule_lock_index = self.option_dic['schedule_list_listbox'].curselection()[0]
                self.option_dic['schedule_list_listbox'].selection_clear(self.schedule_lock_index)

            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == True:
                if self.schedule_lock_index == -1 or self.schedule_lock_index > self.option_dic[
                    'schedule_list_listbox'].size() - 1:
                    self.option_dic['schedule_list_listbox'].selection_clear(
                        self.option_dic['schedule_list_listbox'].size() - 2)
                    self.schedule_lock_index = self.option_dic['schedule_list_listbox'].size() - 2

                schedule_list.insert(self.schedule_lock_index + 1, selected_work_name)
                self.option_dic['schedule_list_listbox'].insert(self.schedule_lock_index + 1, selected_work_name)

                self.schedule_lock_index += 1
                self.option_dic['schedule_list_listbox'].select_set(self.schedule_lock_index)
            else:
                self.option_dic['schedule_list_listbox'].selection_clear(
                    self.option_dic['schedule_list_listbox'].size() - 2)
                schedule_list.insert(len(schedule_list) - 1, selected_work_name)
                self.option_dic['schedule_list_listbox'].insert(self.option_dic['schedule_list_listbox'].size() - 1,
                                                                selected_work_name)
                self.option_dic['schedule_list_listbox'].select_set(self.option_dic['schedule_list_listbox'].size() - 2)

            # self.build_schedule_list()

    def build_schedule_list(self):
        schedule_list = self.get_game_schedule_list()
        selected_window_name = self.option_dic['window_list_stringvar'].get()
        # print('S ----')
        temp_schdule_list = copy.deepcopy(schedule_list)
        for each_schedule in temp_schdule_list:
            if each_schedule in self.configure.window_config['custom_config_dic']:
                # print('**** each_schedule', each_schedule)
                if self.configure.window_config[selected_window_name][self.game_name] == \
                        self.configure.window_config['custom_config_dic'][each_schedule]:
                    continue
                else:
                    for each_sub in self.configure.window_config['custom_config_dic'][each_schedule]['schedule_list']:
                        if each_sub in self.configure.window_config['custom_config_dic']:
                            self.logger.debug(str(each_schedule) + ' 안의 스케쥴 설정 ' + str(each_sub) + '는 무시됩니다')
                        elif each_sub == '':
                            continue
                        else:
                            schedule_list.insert(len(schedule_list) - 1, each_sub)
                    schedule_list.insert(len(schedule_list) - 1, each_schedule)

                # print(schedule_list)
                # print('E ----')

    def update_lock_button(self):
        is_locked = self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE)
        if is_locked == True:
            self.option_dic['schedule_lock_button'].config(style='toggle_true.TButton')
            self.option_dic['schedule_lock_button'].config(text='L')
        else:
            self.option_dic['schedule_lock_button'].config(style='toggle_false.TButton')
            self.option_dic['schedule_lock_button'].config(text='U')

        is_locked = self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST)
        if is_locked == True:
            self.option_dic['my_wlist_lock_button'].config(style='toggle_true.TButton')
            self.option_dic['my_wlist_lock_button'].config(text='L')
        else:
            self.option_dic['my_wlist_lock_button'].config(style='toggle_false.TButton')
            self.option_dic['my_wlist_lock_button'].config(text='U')

    def update_work_list(self):
        # print('S DEBUG: update_work_list - ')
        self.configure.common_config[self.game_name]['work_list'] = []
        self.set_work_list()
        # print('S--------')

        for i in range(self.option_dic['work_list_listbox'].size()):
            if self.option_dic['work_list_listbox'].get(i) == '':
                idx = i
                break

        for each_custom_config in self.configure.window_config['custom_config_dic']:
            if not self.game_name in each_custom_config:
                continue

            is_there = False
            for i in range(self.option_dic['work_list_listbox'].size()):
                if each_custom_config == self.option_dic['work_list_listbox'].get(i):
                    is_there = True
                    break

            if is_there == False:
                self.option_dic['work_list_listbox'].insert(idx, each_custom_config)
                # work_list.insert(idx, each_custom_config)
                idx += 1
            # self.configure.window_config[self.game_name]['work_list'].append(each_work)
            # print('E-------')

            # print('E DEBUG: update_work_list - ')

    def update_schedule_list(self):
        game_name = self.game_name

        self.option_dic['schedule_list_listbox'].delete(0, self.option_dic['schedule_list_listbox'].size() - 1)
        schedule_list = self.get_game_schedule_list()

        for schedule in schedule_list:
            self.option_dic['schedule_list_listbox'].insert(self.option_dic['schedule_list_listbox'].size(), schedule)

    def update_my_work_list(self):
        self.option_dic['my_work_list_listbox'].delete(0, self.option_dic['my_work_list_listbox'].size() - 1)
        self.option_dic['advanced_my_work_list_listbox'].delete(0, self.option_dic[
            'advanced_my_work_list_listbox'].size() - 1)

        my_work_list = self.configure.common_config[self.game_name]['my_work_list']

        # print(my_work_list)
        for work in my_work_list:
            self.option_dic['my_work_list_listbox'].insert(self.option_dic['my_work_list_listbox'].size(), work)
            self.option_dic['advanced_my_work_list_listbox'].insert(
                self.option_dic['advanced_my_work_list_listbox'].size(), work)

    def select_schedule_list(self, event):
        game_name = self.game_name
        last_index = self.option_dic['schedule_list_listbox'].size() - 1
        self.option_dic['schedule_list_listbox'].selection_clear(last_index)

        schedule_list = self.get_game_schedule_list()

        if len(self.option_dic['schedule_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['schedule_list_listbox'].curselection()[0]
            if item_index == last_index:
                return

            self.logger.debug(
                str(item_index) + ', ' + str(last_index) + ', ' + str(schedule_list[item_index]) + ', ' + str(
                    self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE)))
            selected_schedule_work_name = self.option_dic['schedule_list_listbox'].get(item_index)
            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == True:
                self.schedule_lock_index = item_index
            else:
                schedule_list.remove(selected_schedule_work_name)
                self.option_dic['schedule_list_listbox'].delete(item_index)
            # print('DEBUG77:', self.option_dic['schedule_list_listbox'].size())

        window_name = self.option_dic['window_list_stringvar'].get()

    def get_game_schedule_list(self):

        window_name = self.option_dic['window_list_stringvar'].get()
        if len(window_name) > 0:
            return self.get_game_config('schedule_list')
        else:
            custom_config = self.configure.window_config['custom_config_dic']
            selected_config = self.option_dic['config_list_stringvar'].get()

            return custom_config[selected_config]['schedule_list']

    def get_game_config(self, config_name):

        window_name = self.option_dic['window_list_stringvar'].get()
        configuration_name = self.option_dic['config_list_stringvar'].get()

        if len(window_name) > 0:
            if not self.game_name in self.configure.window_config[window_name]:
                self.configure.window_config[window_name][self.game_name] = copy.deepcopy(
                    self.configure.common_config[self.game_name])
            elif not config_name in self.configure.window_config[window_name][self.game_name]:
                self.configure.window_config[window_name][self.game_name][config_name] = copy.deepcopy(
                    self.configure.common_config[self.game_name][config_name])

            config_value = self.configure.window_config[window_name][self.game_name][config_name]
        elif len(configuration_name) > 0:
            if not config_name in self.configure.window_config['custom_config_dic'][configuration_name]:
                self.configure.window_config['custom_config_dic'][configuration_name][config_name] = copy.deepcopy(
                    self.configure.common_config[self.game_name][config_name])

            config_value = self.configure.window_config['custom_config_dic'][configuration_name][config_name]
        else:
            config_value = self.configure.common_config[self.game_name][config_name]

        return config_value

    def set_game_config(self, config_name, config_value):
        window_name = self.option_dic['window_list_stringvar'].get()
        configuration_name = self.option_dic['config_list_stringvar'].get()

        if len(window_name) > 0:
            if not self.game_name in self.configure.window_config[window_name]:
                self.configure.window_config[window_name][self.game_name] = copy.deepcopy(
                    self.configure.common_config[self.game_name])

            self.configure.window_config[window_name][self.game_name][config_name] = config_value
        elif len(configuration_name) > 0:
            self.configure.window_config['custom_config_dic'][configuration_name][config_name] = config_value
        else:
            self.configure.common_config[self.game_name][config_name] = config_value

    def set_game_option(self):
        for key, value in self.option_dic.items():
            if lybconstant.LYB_DO_PREFIX in key:
                self.option_dic[key].set(str(self.get_game_config(key)))

    def preformat_cjk(self, string, width, align='<', fill=' '):
        count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                             for c in string))
        return {
            '>': lambda s: fill * count + s,
            '<': lambda s: s + fill * count,
            '^': lambda s: fill * (count / 2)
                           + s
                           + fill * (count / 2 + count % 2)
        }[align](string)

    def mouse_wheel(self, event, listbox_name):
        if event.delta > 0:
            self.option_dic[listbox_name].yview_scroll(-1, 'units')

    # def callback_schedule_lock_booleanvar(self, args):
    # 	self.set_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE, self.option_dic[lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE].get())
    # 	if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == False:
    # 		if self.schedule_lock_index != -1:
    # 			self.option_dic['schedule_list_listbox'].selection_clear(self.schedule_lock_index)
    # 			self.schedule_lock_index = -1


    def clicked_schedule_tab(self, event):
        tab_index = self.option_dic['schedule_note'].tk.call(self.option_dic['schedule_note']._w, "identify", "tab",
                                                             event.x, event.y)
        self.logger.debug('tab index=' + str(tab_index))
        self.update_my_work_list()

    def callback_schedule_up_button_stringvar(self, event):
        self.logger.debug('UpButton clicked')
        schedule_list = self.get_game_schedule_list()

        if len(self.option_dic['schedule_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['schedule_list_listbox'].curselection()[0]
            if item_index < 1:
                return

            selected_schedule_work_name = self.option_dic['schedule_list_listbox'].get(item_index)
            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == True:
                selected_one, change_one = item_index, item_index - 1
                schedule_list[change_one], schedule_list[selected_one] = schedule_list[selected_one], schedule_list[
                    change_one]
                self.update_schedule_list()
                self.option_dic['schedule_list_listbox'].select_set(item_index - 1)
                self.option_dic['schedule_list_listbox'].see(item_index - 1)

    def callback_schedule_down_button_stringvar(self, event):
        self.logger.debug('DownButton clicked')
        schedule_list = self.get_game_schedule_list()
        last_index = self.option_dic['schedule_list_listbox'].size() - 1

        if len(self.option_dic['schedule_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['schedule_list_listbox'].curselection()[0]
            if item_index >= last_index - 1:
                return

            selected_schedule_work_name = self.option_dic['schedule_list_listbox'].get(item_index)
            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == True:
                selected_one, change_one = item_index, item_index + 1
                schedule_list[change_one], schedule_list[selected_one] = schedule_list[selected_one], schedule_list[
                    change_one]
                self.update_schedule_list()
                self.option_dic['schedule_list_listbox'].select_set(item_index + 1)
                self.option_dic['schedule_list_listbox'].see(item_index + 1)

    def callback_schedule_delete_button_stringvar(self, event):
        self.logger.debug('DeleteButton clicked')
        schedule_list = self.get_game_schedule_list()
        last_index = self.option_dic['schedule_list_listbox'].size() - 1

        if len(self.option_dic['schedule_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['schedule_list_listbox'].curselection()[0]
            if item_index > last_index - 1:
                return

            selected_schedule_work_name = self.option_dic['schedule_list_listbox'].get(item_index)
            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == True:
                schedule_list.pop(item_index)
                self.update_schedule_list()
                if item_index > 0:
                    item_index -= 1

                if len(self.option_dic['schedule_list_listbox'].get(item_index)) > 0:
                    self.option_dic['schedule_list_listbox'].select_set(item_index)
                    self.option_dic['schedule_list_listbox'].see(item_index)

    def callback_schedule_copy_button_stringvar(self, event):
        self.logger.debug('CopyButton clicked')
        schedule_list = self.get_game_schedule_list()
        last_index = self.option_dic['schedule_list_listbox'].size() - 1

        if len(self.option_dic['schedule_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['schedule_list_listbox'].curselection()[0]
            if item_index > last_index - 1:
                return

            selected_schedule_work_name = self.option_dic['schedule_list_listbox'].get(item_index)
            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == True:
                schedule_list.insert(item_index, selected_schedule_work_name)
                self.update_schedule_list()
                self.option_dic['schedule_list_listbox'].select_set(item_index + 1)
                self.option_dic['schedule_list_listbox'].see(item_index + 1)

    def callback_schedule_lock_button_stringvar(self, event):

        self.logger.debug(str(self.option_dic['schedule_lock_button'].config('style')[-1]))

        if 'false' in self.option_dic['schedule_lock_button'].config('style')[-1]:
            self.option_dic['schedule_lock_button'].config(style='toggle_true.TButton')
            self.option_dic['schedule_lock_button'].config(text='L')
            is_locked = True
        else:
            self.option_dic['schedule_lock_button'].config(style='toggle_false.TButton')
            self.option_dic['schedule_lock_button'].config(text='U')
            is_locked = False

        self.set_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE, is_locked)
        if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_SCHEDULE) == False:
            if self.schedule_lock_index != -1:
                self.option_dic['schedule_list_listbox'].selection_clear(self.schedule_lock_index)
                self.schedule_lock_index = -1

    def callback_my_wlist_up_button_stringvar(self, event):
        my_wlist = self.configure.common_config[self.game_name]['my_work_list']

        if len(self.option_dic['advanced_my_work_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['advanced_my_work_list_listbox'].curselection()[0]
            if item_index < 1:
                return

            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST) == True:
                selected_one, change_one = item_index, item_index - 1
                my_wlist[change_one], my_wlist[selected_one] = my_wlist[selected_one], my_wlist[change_one]
                self.update_my_work_list()
                self.option_dic['advanced_my_work_list_listbox'].select_set(item_index - 1)
                self.option_dic['advanced_my_work_list_listbox'].see(item_index - 1)

    def callback_my_wlist_down_button_stringvar(self, event):
        my_wlist = self.configure.common_config[self.game_name]['my_work_list']
        last_index = self.option_dic['advanced_my_work_list_listbox'].size() - 1

        if len(self.option_dic['advanced_my_work_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['advanced_my_work_list_listbox'].curselection()[0]
            if item_index >= last_index - 1:
                return

            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST) == True:
                selected_one, change_one = item_index, item_index + 1
                my_wlist[change_one], my_wlist[selected_one] = my_wlist[selected_one], my_wlist[change_one]
                self.update_my_work_list()
                self.option_dic['advanced_my_work_list_listbox'].select_set(item_index + 1)
                self.option_dic['advanced_my_work_list_listbox'].see(item_index + 1)

    def callback_my_wlist_delete_button_stringvar(self, event):
        my_wlist = self.configure.common_config[self.game_name]['my_work_list']
        last_index = self.option_dic['advanced_my_work_list_listbox'].size() - 1

        if len(self.option_dic['advanced_my_work_list_listbox'].curselection()) > 0:
            item_index = self.option_dic['advanced_my_work_list_listbox'].curselection()[0]
            if item_index > last_index - 1:
                return

            if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST) == True:
                my_wlist.pop(item_index)
                self.update_my_work_list()
                if item_index > 0:
                    item_index -= 1

                if len(self.option_dic['advanced_my_work_list_listbox'].get(item_index)) > 0:
                    self.option_dic['advanced_my_work_list_listbox'].select_set(item_index)
                    self.option_dic['advanced_my_work_list_listbox'].see(item_index)

    def initialize_my_wlist(self):
        self.configure.common_config[self.game_name]['my_work_list'] = \
            copy.deepcopy(self.configure.common_config[self.game_name]['work_list'])

        idx = 0
        for i in range(len(self.configure.common_config[self.game_name]['my_work_list'])):
            if self.configure.common_config[self.game_name]['my_work_list'][i] == '':
                idx = i
                break

        if 'custom_config_dic' in self.configure.window_config:

            for each_custom_config in self.configure.window_config['custom_config_dic']:
                if not self.game_name in each_custom_config:
                    continue

                if each_custom_config in self.configure.common_config[self.game_name]['my_work_list']:
                    continue
                self.configure.common_config[self.game_name]['my_work_list'].insert(idx, each_custom_config)
                idx += 1
        else:
            default_config_name = self.game_name + '_기본설정'
            if not default_config_name in self.configure.common_config[self.game_name]['my_work_list']:
                self.configure.common_config[self.game_name]['my_work_list'].insert(idx, default_config_name)

    def callback_my_wlist_init_button_stringvar(self, event):
        self.initialize_my_wlist()
        self.update_my_work_list()
        self.option_dic['advanced_my_work_list_listbox'].select_set(0)
        self.option_dic['advanced_my_work_list_listbox'].see(0)

    def callback_my_wlist_lock_button_stringvar(self, event):

        if 'false' in self.option_dic['my_wlist_lock_button'].config('style')[-1]:
            self.option_dic['my_wlist_lock_button'].config(style='toggle_true.TButton')
            self.option_dic['my_wlist_lock_button'].config(text='L')
            is_locked = True
        else:
            self.option_dic['my_wlist_lock_button'].config(style='toggle_false.TButton')
            self.option_dic['my_wlist_lock_button'].config(text='U')
            is_locked = False

        self.set_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST, is_locked)
        if self.get_game_config(lybconstant.LYB_DO_BOOLEAN_LOCK_MY_WLIST) == False:
            if self.my_wlist_lock_index != -1:
                self.option_dic['advanced_my_work_list_listbox'].selection_clear(self.my_wlist_lock_index)
                self.my_wlist_lock_index = -1

    def get_option_text(self, text, width=-1):
        if width == -1:
            return "%s" % self.preformat_cjk(text, lybconstant.LYB_OPTION_WIDTH) + ' '
        else:
            return "%s" % self.preformat_cjk(text, width) + ' '

    def callback_wait_for_next_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_notify_message_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_period_rest_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_restart_game_booleanvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_period_restart_game_schedule_booleanvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_period_restart_game_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_count_loop_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_reserved_hour_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_reserved_minute_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_reserved_second_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
