import traceback
import likeyoubot_eosred as lybgameeosred
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_scene
import time


class LYBEosRedScene(likeyoubot_scene.LYBScene):
    def __init__(self, scene_name):
        likeyoubot_scene.LYBScene.__init__(self, scene_name)

    def process(self, window_image, window_pixels):

        super(LYBEosRedScene, self).process(window_image, window_pixels)

        if self.scene_name == 'init_screen_scene':
            rc = self.init_screen_scene()
        elif self.scene_name == 'login_scene':
            rc = self.login_scene()
        elif self.scene_name == 'character_scene':
            rc = self.character_scene()
        elif self.scene_name == 'main_scene':
            rc = self.main_scene()
        elif self.scene_name == 'quest_complete_scene':
            rc = self.quest_complete_scene()
        elif self.scene_name == 'jeoljeon_mode_scene':
            rc = self.jeoljeon_mode_scene()
        elif self.scene_name == 'waiting_scene':
            rc = self.waiting_scene()
        elif self.scene_name == 'dogam_scene':
            rc = self.dogam_scene()
        elif self.scene_name == 'dogam_select_scene':
            rc = self.dogam_select_scene()
        elif self.scene_name == 'dogam_confirm_scene':
            rc = self.dogam_confirm_scene()
        elif self.scene_name == 'gabang_scene':
            rc = self.gabang_scene()
        elif self.scene_name == 'bunhe_scene':
            rc = self.bunhe_scene()
        else:
            rc = self.else_scene()

        return rc

    def else_scene(self):

        if self.status == 0:
            self.logger.info('unknown scene: ' + self.scene_name)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def bunhe_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click('bunhe_scene_tab_jangbi', custom_threshold=0)
            self.status += 1
        elif 2 <= self.status < 30:
            self.status += 1
            pb_name = 'bunhe_scene_bunhe_active'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                return self.status

            location_list = [
                # 2번째 라인
                (900, 260, 950, 290),
                (850, 260, 900, 290),
                (780, 260, 850, 290),
                (720, 260, 780, 290),
                (650, 260, 720, 290),

                # 1번째 라인
                (900, 190, 950, 220),
                (850, 190, 900, 220),
                (780, 190, 850, 220),
                (720, 190, 780, 220),
                (650, 190, 720, 220),
            ]

            is_found = False
            pb_name = 'gabang_scene_item_white'
            for each in location_list:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(150, 150, 150),
                    custom_flag=1,
                    custom_rect=each,
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    is_found = True
                    self.lyb_mouse_click_location(loc_x - 15, loc_y - 15)
                    break

            if is_found is False:
                self.status = 30
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def gabang_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click('gabang_scene_tab_jangbi', custom_threshold=0)
            self.status += 1
        elif self.status == 2:
            self.lyb_mouse_click('gabang_scene_sort', custom_threshold=0)
            self.status += 1
        elif 3 <= self.status < 5:
            location_list = [
                # 4번째 라인
                (900, 380, 950, 410),
                (850, 380, 900, 410),
                (780, 380, 850, 410),
                (720, 380, 780, 410),
                (650, 380, 720, 410),

                # 3번째 라인
                (900, 320, 950, 350),
                (850, 320, 900, 350),
                (780, 320, 850, 350),
                (720, 320, 780, 350),
                (650, 320, 720, 350),
            ]

            is_found = False
            pb_name = 'gabang_scene_item_white'
            for each in location_list:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(150, 150, 150),
                    custom_flag=1,
                    custom_rect=each,
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 15, loc_y - 15)
                    is_found = True
                    break

            if is_found:
                self.set_option('last_status', self.status + 1)
                self.status = 10
            else:
                self.status += 1
        elif self.status == 10:
            pb_name = 'gabang_scene_bunhe'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('bunhe_scene').status = 0
                self.status = 99999

            pb_name = 'gabang_scene_bunhe2'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('bunhe_scene').status = 0
                self.status = 99999
            else:
                self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def dogam_confirm_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 10:
            self.lyb_mouse_click('dogam_confirm_scene_ok', custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def dogam_select_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 5:
            location_list = [
                (250, 160, 320, 240),
                (250, 230, 320, 320),
                (250, 290, 320, 380),
                (250, 350, 320, 460),
                (250, 430, 320, 520),
            ]
            is_found = False
            for each in location_list:
                resource_name = 'dogam_scene_register_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_flag=1,
                    custom_rect=each,
                    average=True
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x + 350, loc_y - 15)
                    is_found = True
                    break
            if is_found:
                self.status = 5
                self.game_object.get_scene('dogam_confirm_scene').status = 10
            else:
                if self.status % 3 == 0:
                    self.lyb_mouse_drag('dogam_scene_register_drag_bot', 'dogam_scene_register_drag_top', stop_delay=0.1)
                self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def dogam_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('found', False)
            self.status += 1
        elif 1 <= self.status < 5:
            location_list = [
                (50, 200, 310, 280),
                (50, 280, 310, 360),
                (50, 350, 310, 430),
                (50, 430, 310, 510),
            ]
            is_found = False
            for each in location_list:
                resource_name = 'dogam_scene_register_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_flag=1,
                    custom_rect=each,
                    average=True
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    is_found = True
                    break
            if is_found:
                self.set_option('last_status', self.status + 1)
                self.status = 10
            else:
                self.status += 1
        elif 10 <= self.status < 25:
            pb_name = 'dogam_scene_replace'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.game_object.get_scene('dogam_select_scene').status = 0
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 25
            else:
                self.status = self.get_option('last_status')
        elif self.status == 25:
            self.set_option('found', True)
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def waiting_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1

        return self.status

    def jeoljeon_mode_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def quest_complete_scene(self):

        self.lyb_mouse_click('quest_complete_scene_touch', custom_threshold=0)

        return self.status

    def character_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 1:
            i = 1
            self.lyb_mouse_click('character_scene_number_' + str(i), custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def login_scene(self):
        self.game_object.current_matched_scene['name'] = ''
        self.schedule_list = self.get_game_config('schedule_list')

        if '로그인' not in self.schedule_list:
            return 0

        elapsed_time = time.time() - self.get_checkpoint('start')
        if elapsed_time > 120:
            self.status = 0

        if self.status == 0:
            self.set_checkpoint('start')
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click(self.scene_name + '_touch', custom_threshold=0)
            self.status += 1
        elif 2 <= self.status < 6:
            self.status += 1
        elif self.status == 6:
            self.lyb_mouse_click(self.scene_name + '_touch', custom_threshold=0)
            self.status += 1
        elif 7 <= self.status < 10:
            self.status += 1
        elif 10 <= self.status < 70:
            self.logger.info('로그인 화면 랙 인식: ' + str(self.status - 10) + '/60')
            if self.status % 10 == 0:
                self.lyb_mouse_click(self.scene_name + '_touch', custom_threshold=0)
            self.status += 1
        elif self.status == 70:
            self.game_object.terminate_application()
            self.status += 1
        else:
            self.status = 0

        return self.status

    def init_screen_scene(self):

        self.schedule_list = self.get_game_config('schedule_list')
        if '게임 시작' not in self.schedule_list:
            return 0

        loc_x = -1
        loc_y = -1

        resource_name = 'eosred_icon_loc'
        resource = self.game_object.resource_manager.resource_dic[resource_name]
        if self.game_object.player_type == 'nox':
            for each_icon in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each_icon],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(80, 110, 920, 500)
                )
                # self.logger.debug(match_rate)
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    break
        else:
            for each_icon in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each_icon],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(50, 110, 920, 440)
                )
                # self.logger.debug(match_rate)
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    break

        # if loc_x == -1:
        # 	self.loggingToGUI('테라 아이콘 발견 못함')

        return 0

    #################################
    #                               #
    #                               #
    #			MAIN SCENE 			#
    #                               #
    #                               #
    #################################

    def main_scene(self):

        if self.game_object.current_schedule_work != self.current_work:
            self.game_object.current_schedule_work = self.current_work

        self.game_object.main_scene = self

        is_clicked = self.pre_process_main_scene()
        if is_clicked is True:
            return self.status

        self.schedule_list = self.get_game_config('schedule_list')
        if len(self.schedule_list) == 1:
            self.logger.warn('스케쥴 작업이 없어서 종료합니다.')
            return -1

        if self.status == 0:
            self.status += 1
        elif 1 <= self.status < 1000:

            self.set_schedule_status()

        elif self.status == self.get_work_status('메인 퀘스트'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_EOSRED_WORK + 'main_quest_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=60)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.process_main_quest()

        elif self.status == self.get_work_status('도감'):

            elapsed_time = self.get_elapsed_time()

            if self.period_bot(5) < elapsed_time <= self.period_bot(120):
                if self.game_object.get_scene('dogam_scene').get_option('found') is not True:
                    self.set_option(self.current_work + '_end_flag', True)
            elif elapsed_time > self.period_bot(120):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            if self.is_open_menu():
                self.lyb_mouse_click('menu_dogam', custom_threshold=0)
                self.game_object.get_scene('dogam_scene').status = 0
            else:
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)

        elif self.status == self.get_work_status('분해'):

            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(5):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_gabang', custom_threshold=0)
            self.game_object.get_scene('gabang_scene').status = 0

        elif self.status == self.get_work_status('알림'):

            try:
                self.game_object.telegram_send(str(self.get_game_config(lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE)))
                self.status = self.last_status[self.current_work] + 1
            except:
                recovery_count = self.get_option(self.current_work + 'recovery_count')
                if recovery_count is None:
                    recovery_count = 0

                if recovery_count > 2:
                    self.status = self.last_status[self.current_work] + 1
                    self.set_option(self.current_work + 'recovery_count', 0)
                else:
                    self.logger.error(traceback.format_exc())
                    self.set_option(self.current_work + 'recovery_count', recovery_count + 1)

        elif self.status == self.get_work_status('[작업 예약]'):

            self.logger.warn('[작업 예약]')
            self.game_object.wait_for_start_reserved_work = False
            self.status = self.last_status[self.current_work] + 1

        elif self.status == self.get_work_status('[작업 대기]'):
            elapsed_time = self.get_elapsed_time()
            limit_time = int(self.get_game_config(lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT))
            if elapsed_time > limit_time:
                self.set_option(self.current_work + '_end_flag', True)
            else:
                self.loggingElapsedTime('[작업 대기]', int(elapsed_time), limit_time, period=10)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

        elif self.status == self.get_work_status('[반복 시작]'):

            self.set_option('loop_start', self.last_status[self.current_work])
            self.status = self.last_status[self.current_work] + 1

        elif self.status == self.get_work_status('[반복 종료]'):

            loop_count = self.get_option('loop_count')
            if loop_count is None:
                loop_count = 1

            self.logger.debug('[반복 종료] ' + str(loop_count) + ' 회 수행 완료, ' +
                              str(int(
                                  self.get_game_config(lybconstant.LYB_DO_STRING_COUNT_LOOP)) - loop_count) + ' 회 남음')
            if loop_count >= int(self.get_game_config(lybconstant.LYB_DO_STRING_COUNT_LOOP)):
                self.status = self.last_status[self.current_work] + 1
                self.set_option('loop_count', 1)
                self.set_option('loop_start', None)
            else:
                self.status = self.get_option('loop_start')
                # print('DEBUG LOOP STATUS = ', self.status )

                if self.status is None:
                    self.logger.debug('[반복 시작] 점을 찾지 못해서 다음 작업을 수행합니다')
                    self.status = self.last_status[self.current_work] + 1

                self.set_option('loop_count', loop_count + 1)

        else:
            self.status = self.last_status[self.current_work] + 1

        return self.status

    def pre_process_main_scene(self):
        # 체크 limit 값을 반드시 1보다 크게 해야 한다. 그렇지 않을 경우 이 루프를 못빠져나옴
        if self.is_gabang_full():
            self.game_object.get_scene('gabang_scene').status = 0
            self.lyb_mouse_click('main_scene_gabang', custom_threshold=0)
            return True

        return False

    def process_main_quest(self):
        if self.is_main_quest_not_working():
            self.set_option('check_quick_move', True)
            return

        if self.get_option('check_quick_move') is True:
            if self.is_quick_move():
                self.set_option('check_quick_move', False)

        return

    def get_work_status(self, work_name):
        if work_name in lybgameeosred.LYBEosRed.work_list:
            return (lybgameeosred.LYBEosRed.work_list.index(work_name) + 1) * 1000
        else:
            return 99999

    def is_open_main_quest(self, limit=0):
        resource_name = 'main_quest_loc'
        rect_list = [
            (800, 380, 850, 510),
            (800, 330, 850, 450),
            (800, 280, 850, 390),
            (800, 230, 850, 330)
        ]
        elapsed_time = time.time() - self.get_checkpoint(resource_name + '_clicked')
        if elapsed_time > 10:
            for rect in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_threshold=0.5,
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(150, 150, 150),
                    custom_flag=1,
                    custom_rect=rect,
                    average=True
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.logger.info('[메인] 퀘스트 감지됨')
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.set_checkpoint(resource_name + '_clicked')
                    return True

        return False

    def is_main_quest_not_working(self, limit=3):
        resource_name = 'main_quest_working_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_threshold=0.8,
            custom_top_level=(255, 255, 255),
            custom_below_level=(160, 140, 120),
            custom_flag=1,
            custom_rect=(880, 150, 950, 200),
            average=True
        )
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x == -1:
            threshold = self.get_option(resource_name + '_threshold')
            if threshold is None:
                threshold = 0

            self.logger.info('진행중 감지 실패: ' + str(threshold) + '/' + str(limit))

            if threshold >= limit:
                self.lyb_mouse_click('main_quest_working_0', custom_threshold=0)
                self.set_option(resource_name + '_threshold', 0)

                return True
            else:
                self.set_option(resource_name + '_threshold', threshold + 1)
        else:
            self.set_option(resource_name + '_threshold', 0)

        return False

    def is_quick_move(self, limit=0):
        resource_name = 'main_scene_quick_move_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_threshold=0.8,
            custom_top_level=(255, 255, 255),
            custom_below_level=(160, 140, 120),
            custom_flag=1,
            custom_rect=(640, 150, 730, 200),
            average=True
        )
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            threshold = self.get_option(resource_name + '_threshold')
            if threshold is None:
                threshold = 0

            self.logger.info('순간이동 감지: ' + str(threshold) + '/' + str(limit))

            if threshold >= limit:
                self.lyb_mouse_click_location(loc_x, loc_y)
                self.set_option(resource_name + '_threshold', 0)

                return True
            else:
                self.set_option(resource_name + '_threshold', threshold + 1)
        else:
            self.set_option(resource_name + '_threshold', 0)

        return False

    def is_open_menu(self, limit=-1):
        return self.is_status_by_resource2('메뉴 열림', 'menu_open_loc', 0.8, limit, reverse=True)

    def click_resource(self, resource_name, custom_threshold=0.7, near=32):
        is_matched, rate = self.click_resource2(resource_name, custom_threshold=custom_threshold, near=near)

        return is_matched

    def click_resource2(self, resource_name, custom_threshold=0.7, near=32):
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart2(
            self.window_image,
            resource_name,
            custom_threshold=custom_threshold,
            near=near,
            debug=True,
            custom_flag=1)
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True, match_rate

        return False, match_rate

    def is_auto(self, limit=2):
        return self.is_status_by_resource2('자동 꺼짐 감지', 'no_auto_loc', 0.7, limit, reverse=True)

    def is_gabang_full(self, limit=2):
        return self.is_status_by_resource(
            '[가방 100% 감지]',
            'main_scene_gabang_full_loc',
            custom_top_level=(255, 75, 75),
            custom_below_level=(200, 0, 0),
            custom_rect=(840, 70, 890, 100),
            custom_threshold=0.7,
            limit_count=limit,
            reverse=True,
        )

    def is_status_by_resource(self, log_message, resource_name, custom_threshold, custom_top_level, custom_below_level,
                           custom_rect, limit_count=-1, reverse=False):
        # if limit_count == -1:
        #     limit_count = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2R_ETC + 'auto_limit'))

        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_threshold=custom_threshold,
            custom_top_level=custom_top_level,
            custom_below_level=custom_below_level,
            custom_flag=1,
            custom_rect=custom_rect,
            average=True
        )
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1 and reverse == False:
            self.set_option(resource_name + 'check_count', 0)
            return False

        if loc_x == -1 and reverse == True:
            self.set_option(resource_name + 'check_count', 0)
            return False

        check_count = self.get_option(resource_name + 'check_count')
        if check_count is None:
            check_count = 0

        if check_count > limit_count:
            self.set_option(resource_name + 'check_count', 0)
            return True

        if check_count > 0:
            self.logger.debug(log_message + '..(' + str(check_count) + '/' + str(limit_count) + ')')
        self.set_option(resource_name + 'check_count', check_count + 1)

        return False

    def is_status_by_resource2(self, log_message, resource_name, custom_threshold, limit_count=-1, reverse=False):
        match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
        self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
        if match_rate > custom_threshold and reverse is False:
            self.set_option(resource_name + 'check_count', 0)
            return False

        if match_rate < custom_threshold and reverse is True:
            self.set_option(resource_name + 'check_count', 0)
            return False

        check_count = self.get_option(resource_name + 'check_count')
        if check_count is None:
            check_count = 0

        if check_count > limit_count:
            self.set_option(resource_name + 'check_count', 0)
            return True

        if check_count > 0:
            self.logger.debug(log_message + '..(' + str(check_count) + '/' + str(limit_count) + ')')
        self.set_option(resource_name + 'check_count', check_count + 1)

        return False
