import traceback
import likeyoubot_v4 as lybgamev4
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_scene
import time


class LYBV4Scene(likeyoubot_scene.LYBScene):
    def __init__(self, scene_name):
        likeyoubot_scene.LYBScene.__init__(self, scene_name)

    def process(self, window_image, window_pixels):

        super(LYBV4Scene, self).process(window_image, window_pixels)

        if self.scene_name == 'init_screen_scene':
            rc = self.init_screen_scene()
        elif self.scene_name == 'login_scene':
            rc = self.login_scene()
        elif self.scene_name == 'character_scene':
            rc = self.character_scene()
        elif self.scene_name == 'main_scene':
            rc = self.main_scene()
        elif self.scene_name == 'login_scene':
            rc = self.login_scene()
        elif self.scene_name == 'menu_scene':
            rc = self.menu_scene()
        elif self.scene_name == 'quest_scene':
            rc = self.quest_scene()
        elif self.scene_name == 'quest_main_scene':
            rc = self.quest_main_scene()
        elif self.scene_name == 'jeoljeon_mode_scene':
            rc = self.jeoljeon_mode_scene()
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

    def jeoljeon_mode_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.game_object.get_scene('main_scene').set_option('go_jeoljeon', 0)
            self.status += 1
        elif 1 <= self.status < 30:
            self.status += 1
            if self.status % 3 == 0:
                resource_name = 'jeoljeon_mode_scene_auto_quest_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(100, 100, 100),
                    custom_rect=(420, 410, 540, 480),
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=True
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x == -1:
                    self.status = 99998
                    return self.status
        elif self.status == 99998:
            self.game_object.get_scene('main_scene').set_option('go_jeoljeon', 10)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def quest_main_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 5:
            self.status += 1

            resource_name = 'quest_main_scene_auto_quest_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_top_level=(255, 255, 255),
                custom_below_level=(100, 100, 100),
                custom_rect=(400, 50, 540, 100),
                custom_threshold=0.7,
                custom_flag=1,
                average=True
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.status = 99999
                return self.status

            pb_name_list = [
                'quest_main_scene_auto',
                'quest_main_scene_surak',
                'quest_main_scene_bosang',
            ]
            for pb_name in pb_name_list:
                match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
                if match_rate > 0.9:
                    self.lyb_mouse_click(pb_name, custom_threshold=0)
                    self.status = 99999
                    break
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def quest_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 100 <= self.status < 110:
            if self.status % 5 == 0:
                self.lyb_mouse_click('quest_scene_main', custom_threshold=0)
                self.game_object.get_scene('quest_main_scene').status = 0
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def menu_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 100 <= self.status < 105:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_quest', custom_threshold=0)
                self.game_object.get_scene('quest_scene').status = 100
            self.status += 1
        elif 200 <= self.status < 205:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_jeoljeon', custom_threshold=0)
                self.game_object.get_scene('jeoljeon_mode_scene').status = 0
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

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

        resource_name = 'v4_icon_loc'
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

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'))
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

        return False

    def process_main_quest(self):

        if self.is_main_quest_complete():
            self.set_option('go_jeoljeon', 0)
            return True

        if self.is_main_quest_new():
            self.set_option('go_jeoljeon', 0)
            return True

        go_jeoljeon = self.get_option('go_jeoljeon')
        if go_jeoljeon is None:
            go_jeoljeon = 0

        self.set_option('go_jeoljeon', go_jeoljeon + 1)

        if go_jeoljeon < 5:
            return True
        elif go_jeoljeon == 5:
            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 200
            return True

        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
        self.game_object.get_scene('menu_scene').status = 100
        self.set_option('go_jeoljeon', 0)

        return

    def get_work_status(self, work_name):
        if work_name in lybgamev4.LYBV4.work_list:
            return (lybgamev4.LYBV4.work_list.index(work_name) + 1) * 1000
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
                    custom_threshold=0.7,
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

    def is_main_quest_action(self, limit=1):
        resource_name = 'quest_action_loc'
        resource = self.game_object.resource_manager.resource_dic[resource_name]
        for pb_name in resource:
            (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                self.window_image,
                self.game_object.resource_manager.pixel_box_dic[pb_name],
                custom_threshold=0.9,
                custom_flag=1,
                custom_rect=(670, 320, 730, 530)
            )
            self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                threshold = self.get_option(pb_name + '_threshold')
                if threshold is None:
                    threshold = 0

                self.logger.info('메인 퀘스트 대화 감지됨: ' + str(threshold) + '/' + str(limit))

                if threshold >= limit:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.set_option(pb_name + '_threshold', 0)

                    return True
                else:
                    self.set_option(pb_name + '_threshold', threshold + 1)
            else:
                self.set_option(pb_name + '_threshold', 0)
        return False

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

    def is_auto(self, limit=3):
        return self.is_status_by_resource('자동 꺼짐 감지', 'no_auto_loc',
                                          custom_top_level=(180, 180, 180),
                                          custom_below_level=(100, 100, 100),
                                          custom_rect=(240, 500, 300, 550),
                                          custom_threshold=0.3,
                                          limit_count=limit,
                                          reverse=True,
                                          )

    def is_auto_quest(self, limit=3):
        return self.is_status_by_resource('자동 퀘스트 감지 실패', 'auto_quest_loc',
                                          custom_top_level=-1,
                                          custom_below_level=-1,
                                          custom_rect=(420, 400, 540, 460),
                                          custom_threshold=0.5,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_main_quest_complete(self):
        resource_name = 'main_scene_quest_complete_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_top_level=(255, 255, 255),
            custom_below_level=(210, 210, 210),
            custom_rect=(720, 140, 780, 300),
            custom_threshold=0.6,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def is_main_quest_new(self):
        resource_name = 'main_scene_quest_new_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_top_level=(255, 255, 255),
            custom_below_level=(120, 120, 120),
            custom_rect=(750, 140, 940, 300),
            custom_threshold=0.7,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def is_status_by_resource(self, log_message, resource_name, custom_threshold, custom_top_level, custom_below_level,
                              custom_rect, limit_count=-1, reverse=False):
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
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1 and reverse is False:
            self.set_option(resource_name + 'check_count', 0)
            return False

        if loc_x == -1 and reverse is True:
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
