import likeyoubot_resource as lybrsc
import likeyoubot_message
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
import operator
import random
import likeyoubot_game as lybgame
import time
import copy
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_logger
import traceback
import pickle


class LYBScene():
    def __init__(self, scene_name):
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.scene_name = scene_name
        self.status = 0
        self.logging_queue = None
        self.game_object = None
        self.window_image = None
        self.window_pixels = None
        self.checkpoint = {}
        self.retry_count = 0
        self.just_drag_completed = False
        # self.threshold = 0
        self.window_title = ''
        # 재보니까 구글 계정 사이 간격이 54px 이다. 
        self.google_account_height = 54
        self.google_account_number = 0
        self.schedule_list = []
        self.tolerance_weight_factor = 1
        self.threshold_weight_factor = 1
        self.last_status = {}
        self.move_status = {}
        self.options = {}
        self.current_work = None
        self.callstack = []
        self.callstack_status = []

    def process(self, window_image, window_pixels):

        self.window_image = window_image
        self.window_pixels = window_pixels

        if self.status == 0:
            if self.get_option('enter_scene_done') != True:
                self.set_option('enter_scene_done', True)
                self.set_checkpoint('enter_scene')

            if self.is_done_wait_scene() != True:
                return 'return'
            else:
                self.set_option('enter_scene_done', False)

        return 0

    def main_scene(self):
        # self.logger.debug('main scene='+str(self.scene_name))

        if self.game_object.current_schedule_work != self.current_work:
            self.game_object.current_schedule_work = self.current_work

        if self.game_object.main_scene == None:
            self.game_object.main_scene = self

        self.schedule_list = self.get_game_config('schedule_list')
        if len(self.schedule_list) == 1:
            self.logger.info('스케쥴 작업이 없어서 종료합니다.')
            return -1

        return self.status

    def loggingStartWork(self, sWorkNumber, sWorkName):
        # self.logger.debug('callstack')
        self.logger.info('[스케쥴링 ] ' + sWorkNumber + '. ' + sWorkName)

    def set_depth_configname(self, config_name):
        self.game_object.depth_config = config_name

    def get_depth_configname(self):
        return self.game_object.depth_config

    def get_work_status(self, work_name):
        return 0

    def callback_logoff(self):
        pass

    def set_schedule_status(self):

        if self.current_work != None:
            if self.current_work in self.move_status:
                self.status = self.move_status[self.current_work]
                self.move_status.pop(self.current_work)

        while True:
            self.current_work = self.get_current_work()
            if self.current_work == '게임 시작':
                pass
            elif self.current_work == '로그인':
                pass
            else:
                break
            self.status += 1

        # self.logger.debug('CPXX: callstack - ' + str(self.callstack) + ', ' + str(len(self.current_work)))
        if len(self.callstack) == 0 and len(self.current_work) < 1:

            if self.get_option('schedule_done_enter') != True:
                self.set_option('schedule_done_enter', True)
                self.set_checkpoint('schedule_done')

            schedule_done_wait = int(self.get_game_config(lybconstant.LYB_DO_STRING_PERIOD_REST))
            # print('LYB_DO_STRING_PERIOD_REST: ', schedule_done_wait)
            elapsed_time = time.time() - self.get_checkpoint('schedule_done')
            if elapsed_time < schedule_done_wait:
                self.logger.info(
                    '[스케쥴링 ] 지정된 스케쥴 완료 후 대기 중 ' + str(int(elapsed_time)) + '/' + str(schedule_done_wait) + '초')
                return self.status
            else:
                self.set_option('schedule_done_enter', False)

            is_multi_account = self.get_window_config('multi_account')
            if is_multi_account == True:
                self.logger.info('다음 계정 작업을 위해 로그오프합니다')
                self.callback_logoff()
                self.status = 0
                return self.status
            else:

                is_restart = self.get_game_config(lybconstant.LYB_DO_BOOLEAN_RESTART_GAME)
                if is_restart:
                    self.logger.critical('[스케쥴링 ] 지정된 스케줄을 완료해서 게임을 종료합니다')
                    self.game_object.terminate_application()
                    self.status = 1000000
                else:
                    if self.get_option('loop_start') == None:
                        self.logger.critical('[스케쥴링 ] 지정된 스케줄을 완료해서 처음으로 돌아갑니다')
                        self.game_object.addStatistic(lybconstant.LYB_STATISTIC_0)
                        # 반복
                        self.status = 1
                    else:
                        self.logger.critical('[스케쥴링 ] 지정된 스케줄을 완료해서 [반복 시작]으로 돌아갑니다')
                        self.status = self.get_option('loop_start')
                return self.status
        else:
            # 복잡하다. callstack 다시 구현해보자.
            # self.logger.debug('callstack - scene status:' + str(self.status) + ', current_work:' + str(self.current_work))
            schedule_number = self.status
            if len(self.callstack) > 0:
                schedule_number = self.status + 1

            self.set_work_status()

            if len(self.callstack) > 0:
                iterator_key = self.game_object.build_iterator_key(len(self.callstack) - 1, self.callstack[-1])
                schedule_number = self.get_option(iterator_key)
            else:
                schedule_number = self.last_status[self.current_work]

            log_callstack = ''

            if len(self.current_work) > 0:
                if len(self.callstack) > 0:

                    prev_call = None
                    custom_config_dic = self.game_object.configure.window_config['custom_config_dic']
                    stack_index = 0
                    for each_call in self.callstack:
                        if prev_call != None:
                            schedule_list = custom_config_dic[prev_call]['schedule_list']
                        else:
                            schedule_list = self.schedule_list
                        log_callstack += ' ' + str(self.callstack_status[stack_index]) + '. '
                        log_callstack += '[' + each_call + ']'
                        prev_call = each_call
                        stack_index += 1

                    log_callstack += ' '
                else:
                    log_callstack = ' '

                self.logger.critical('[스케쥴링 ]' + log_callstack + str(schedule_number) + '. ' + self.current_work)
            return self.status
        self.status += 1

    def set_work_status(self):
        # self.loggingToGUI(work_name + ' 체크 시작')

        # print('DEBUG TEST1::::', self.current_work)
        status = self.get_work_status(self.current_work)
        # self.logger.debug('callstack 0:' + str(self.current_work) + ', self.status=' + str(self.status) + ', status=' + str(status))
        if status == 99999 or len(self.callstack) > 0:
            # not found
            custom_config_dic = self.game_object.configure.window_config['custom_config_dic']
            if self.current_work in custom_config_dic:
                # 동일한 이름의 설정이 콜스택에 있다고 가정하지 않는다.
                # self.logger.debug('callstack 1 - current_work:' + str(self.current_work) + ', callstack:' + str(self.callstack))
                if not self.current_work in self.callstack:
                    # self.logger.debug('callstack 2 - push:' + str(self.current_work) + ', status=' + str(self.status))
                    self.callstack.append(self.current_work)
                    self.callstack_status.append(self.status)

            iterator_key = self.game_object.build_iterator_key(len(self.callstack) - 1, self.callstack[-1])
            self.set_depth_configname(self.callstack[-1])
            # self.logger.debug('callstack 3 - iterator_key:' + str(iterator_key))
            # print('DEBUG TEST3::::', self.get_depth_configname())

            config_iterator = self.get_option(iterator_key)
            if config_iterator == None:
                config_iterator = 0
            # self.logger.debug('callstack 4 - iterator:' + str(config_iterator))

            schedule_list = custom_config_dic[self.callstack[-1]]['schedule_list']

            # print('DEBUG TEST3-1:::', schedule_list)
            # if '게임 시작' in schedule_list:
            # 	schedule_list.remove('게임 시작')
            # if '로그인' in schedule_list:
            # 	schedule_list.remove('로그인')

            work_name = schedule_list[config_iterator]
            # self.logger.debug('callstack 5 - work_name:' + str(work_name) + ', config_iterator:' + str(config_iterator))
            # self.logger.debug('callstack 5-0:' + str(self.callstack))
            if work_name == '':
                self.set_option(iterator_key, None)
                # pop 하고 스택이 있는지 없는지 검사

                pop_config = self.callstack.pop()
                pop_status = self.callstack_status.pop()
                self.status = pop_status

                # self.logger.debug('callstack Next Status:' + str(self.status))

                if len(self.callstack) > 0:
                    schedule_list = custom_config_dic[self.callstack[-1]]['schedule_list']
                    iterator_key = self.game_object.build_iterator_key(len(self.callstack) - 1, self.callstack[-1])

                    self.set_option(iterator_key, self.status)
                    self.current_work = schedule_list[self.status]
                    self.status += 1
                else:
                    schedule_list = self.get_game_config('schedule_list')
                    self.current_work = schedule_list[self.status]
                    self.status += 1

                # self.logger.debug('callstack 5-1:' + str(schedule_list))
                # self.logger.debug('callstack 6 - pop:' + str(pop_config) + ', status:' + str(self.status) + ', current_work:' + str(self.current_work))
                # status = self.status + 1
                # print('[DEBUG] callstack 7 - status:', status)
                return self.set_work_status()
            else:
                self.set_option(iterator_key, config_iterator + 1)
                self.current_work = work_name
                self.status = config_iterator + 1
                if work_name in custom_config_dic:
                    return self.set_work_status()
                else:
                    status = self.get_work_status(work_name)

                # self.loggingToGUI(self.callstack[-1] + ' 내부 스케쥴: ' +
                # 		str(config_iterator + 1) + '. ' + work_name, log_type='sub')				
        else:
            self.set_depth_configname(None)

        # self.logger.debug('callstack 8 - status:' + str(self.status) + ', work:' + str(self.current_work) + ', status:' + str(status))
        self.checkpoint[self.current_work + '_check_start'] = time.time()
        self.last_status[self.current_work] = self.status
        self.set_option('scene_start_flag', True)
        self.set_option(self.current_work + '_end_flag', False)
        self.status = status

        return status

    def get_current_work(self):
        if len(self.callstack) > 0:
            custom_config_dic = self.game_object.configure.window_config['custom_config_dic']
            schedule_list = custom_config_dic[self.callstack[-1]]['schedule_list']
        else:
            schedule_list = self.get_game_config('schedule_list')

        # self.logger.debug('callstack - status:' + str(self.status))
        # self.logger.debug('callstack - schedule_list:' + str(schedule_list))

        if self.status > len(schedule_list):
            # self.logger.debug('schedule_list:' + str(schedule_list) + ', status=' + str(self.status))
            self.status = len(schedule_list)

        return schedule_list[self.status - 1]

    def is_there_in_schedule_list(self, work_name, schedule_list=None):
        # print('[DEBUG] is_there_in_schedule_list 1', work_name)
        if schedule_list == None:
            schedule_list = self.get_game_config('schedule_list')

        custom_config_dic = self.game_object.configure.window_config['custom_config_dic']

        for each_schedule in schedule_list:
            if work_name == each_schedule:
                return True
            # print('[DEBUG] is_there_in_schedule_list 2', each_schedule)
            if each_schedule in custom_config_dic:
                # print('[DEBUG] is_there_in_schedule_list 3', work_name)
                is_there = self.is_there_in_schedule_list(work_name, custom_config_dic[each_schedule]['schedule_list'])
                if is_there == True:
                    return True
        return False

    def setLoggingQueue(self, logging_queue):
        self.logging_queue = logging_queue

    def setGameObject(self, game_object):
        self.game_object = game_object
        # self.threshold = float(self.game_object.common_config['threshold_entry'])
        self.window_title = self.game_object.window.get_title(self.game_object.hwnd)

    def logging_detect_scene(self, title):
        self.logger.debug(str(title) + ' 감지' + ' ( 매칭율: ' + str(self.game_object.current_matched_scene['rate']) + '% )')

    def loggingToGUI(self, log_message, log_type='log'):
        self.game_object.loggingToGUI(log_message, log_type=log_type)

    def lyb_mouse_click_location2(self, loc_x, loc_y):
        # 녹스가 아닌 앱플레이어에 대해서 보정이 필요한 값.
        (adj_x, adj_y) = self.game_object.mouse_click_location(loc_x, loc_y)

        # self.logger.debug('click location:' + str((adj_x, adj_y)))
        self.logger.debug('[클릭 좌표2] (' + str(adj_x) + ', ' + str(adj_y) + ')')

    def lyb_mouse_click_location(self, loc_x, loc_y):
        # 테스트 용으로 두번 클릭하게 해놨습니다. 지워주세요.
        # self.game_object.window.mouse_click(self.game_object.hwnd, loc_x, loc_y)
        self.game_object.window.mouse_click(self.game_object.hwnd, loc_x, loc_y)
        # self.logger.debug('보정되지 않은 좌표는 lyb_mouse_click_location2를 사용', (loc_x, loc_y))
        self.logger.info('[클릭 좌표] (' + str(loc_x) + ', ' + str(loc_y) + ')')

    def lyb_mouse_click(self, object_name, custom_tolerance=-1, custom_threshold=-1, delay=0, release=True):
        threshold = float(self.game_object.common_config['threshold_entry'])
        if not custom_threshold == -1:
            threshold = custom_threshold

        match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, object_name,
                                                          custom_tolerance=custom_tolerance)

        # self.loggingToGUI('클릭: [' + str(self.get_adjusted_name(object_name)) + \
        # 	'][' +  str(self.get_location(object_name)) + '][' + \
        # 	str(int(match_rate*100)) + '%' + ' > ' + str(int(threshold*100)) + '%]' \
        # 	% str(self.get_adjusted_name(object_name)) )

        if match_rate >= threshold:
            # 테스트 용으로 두번 클릭하게 해놨습니다. 지워주세요.
            # self.game_object.mouse_click(object_name)
            self.game_object.mouse_click(object_name, delay=delay, release=release)

            self.logger.info('[클릭 성공] %s %s %s%%' %
                             (str(self.get_adjusted_name(object_name)),
                              str(self.get_location(object_name)),
                              str(int(match_rate * 100))
                              # str(int(threshold*100)) 
                              )
                             )

            return True
        else:
            self.logger.info('[클릭 실패] %s %s %s%%' %
                             (str(self.get_adjusted_name(object_name)), str(self.get_location(object_name)),
                              str(int(match_rate * 100))
                              # , str(int(threshold*100)) 
                              )
                             )
            return False

    def get_center_pixel_info(self, object_name):
        return self.game_object.get_center_pixel_info(object_name)

    def get_location(self, object_name):
        return self.game_object.get_location(object_name)

    def get_adjusted_name(self, object_name):
        return self.game_object.get_adjusted_name(object_name)

    def lyb_mouse_move_location(self, loc_x, loc_y):
        self.game_object.move_mouse_location(loc_x, loc_y)

    def lyb_mouse_drag(self, from_pixelbox, to_pixelbox, delay=0.5, stop_delay=0):
        (from_x, from_y) = self.get_location(from_pixelbox)
        (to_x, to_y) = self.get_location(to_pixelbox)
        self.logger.info(
            '[마우스 드래그] %s -> %s' % (str(self.get_location(from_pixelbox)), str(self.get_location(to_pixelbox))))
        self.lyb_mouse_drag_location(from_x, from_y, to_x, to_y, delay=delay, stop_delay=stop_delay)

    def lyb_mouse_drag_location(self, from_x, from_y, to_x, to_y, delay=0.5, stop_delay=0):
        self.game_object.drag_mouse(from_x, from_y, to_x, to_y, delay, stop_delay=stop_delay)

    def get_checkpoint(self, time_key):
        if not time_key in self.checkpoint:
            self.checkpoint[time_key] = 0

        return self.checkpoint[time_key]

    def set_checkpoint(self, time_key, custom_time_key=-1):
        if custom_time_key != -1:
            self.checkpoint[time_key] = custom_time_key
        else:
            self.checkpoint[time_key] = time.time()

    def get_game_config(self, config_name, config_type='number'):
        game_name = self.game_object.window_config['games']

        if not game_name in self.game_object.window_config:
            config_value = self.game_object.common_config[game_name][config_name]
        else:

            if self.get_depth_configname() != None and config_name != 'schedule_list':
                custom_config_dic = self.game_object.configure.window_config['custom_config_dic']
                custom_config = custom_config_dic[self.get_depth_configname()]
                if not config_name in custom_config:
                    custom_config[config_name] = self.game_object.common_config[game_name][config_name]

                config_value = custom_config[config_name]
            else:
                if not config_name in self.game_object.window_config[game_name]:
                    self.game_object.window_config[game_name][config_name] = self.game_object.common_config[game_name][
                        config_name]

                config_value = self.game_object.window_config[game_name][config_name]

        if config_type == 'number':
            if config_value == None or config_value == '':
                config_value = 0

        return config_value

    def set_game_config(self, config_name, config_value):
        self.logger.warn('DEBUG - set_game_config 1: ' + str(config_name) + ':' + str(config_value))
        if config_name in self.game_object.game_tab.option_dic:
            self.logger.warn('DEBUG - set_game_config 2: ' + str(config_name) + ':' + str(config_value))
            self.game_object.game_tab.option_dic[config_name].set(config_value)
        # game_name = self.game_object.window_config['games']

        # if not game_name in self.game_object.window_config:
        # 	self.game_object.common_config[game_name][config_name] = config_value
        # else:
        # 	if self.get_depth_configname() != None and config_name != 'schedule_list':
        # 		custom_config_dic = self.game_object.configure.window_config['custom_config_dic']
        # 		custom_config = custom_config_dic[self.get_depth_configname()]
        # 		custom_config[config_name] = config_value
        # 	else:
        # 		self.game_object.window_config[game_name][config_name] = config_value

        try:
            with open(self.game_object.configure.path, 'wb') as dat_file:
                pickle.dump(self.game_object.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def get_window_config(self, config_name):
        if not config_name in self.game_object.window_config:
            return self.game_object.common_config[config_name]
        else:
            return self.game_object.window_config[config_name]

    def get_option(self, option_name):
        if not option_name in self.options:
            self.options[option_name] = None

        return self.options[option_name]

    def set_option(self, option_name, value):
        self.options[option_name] = value

    def get_elapsed_time(self):
        return time.time() - self.get_checkpoint(self.current_work + '_check_start')

    def loggingElapsedTime(self, title, elapsed_time, limit_time, period=2):
        self.game_object.loggingElapsedTime(title, elapsed_time, limit_time, period)

    def is_done_wait_scene(self):
        if 'main_scene' in self.scene_name:
            return True

        wait_limit = int(self.get_window_config(lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE))
        if wait_limit == 0:
            return True

        elapsed_time = time.time() - self.get_checkpoint('enter_scene')

        # self.logger.debug('게임 화면 전환. ' + str(int(elapsed_time)) + '/' + str(wait_limit) + '초 동안 대기 후 실행')
        if elapsed_time > wait_limit:
            return True
        return False

    def period_bot(self, weight):
        # print(self.get_window_config('wakeup_period_entry'))
        return self.game_object.period_bot(weight)
