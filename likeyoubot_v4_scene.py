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
        elif self.scene_name == 'named_tobeol_scene':
            rc = self.named_tobeol_scene()
        elif self.scene_name == 'move_potion_npc_scene':
            rc = self.move_potion_npc_scene()
        elif self.scene_name == 'potion_npc_scene':
            rc = self.potion_npc_scene()
        elif self.scene_name == 'potion_gume_scene':
            rc = self.potion_gume_scene()
        elif self.scene_name == 'go_home_scene':
            rc = self.go_home_scene()
        elif self.scene_name == 'local_map_scene':
            rc = self.local_map_scene()
        elif self.scene_name == 'recover_scene':
            rc = self.recover_scene()
        elif self.scene_name == 'monster_josa_scene':
            rc = self.monster_josa_scene()
        elif self.scene_name == 'gabang_scene':
            rc = self.gabang_scene()
        elif self.scene_name == 'jamjeryeok_scene':
            rc = self.jamjeryeok_scene()
        elif self.scene_name == 'immu_scene':
            rc = self.immu_scene()
        elif self.scene_name == 'channel_scene':
            rc = self.channel_scene()
        elif self.scene_name == 'hyusik_bosang_scene':
            rc = self.hyusik_bosang_scene()
        elif self.scene_name == 'event_scene':
            rc = self.event_scene()
        elif self.scene_name == 'chulseok_scene':
            rc = self.chulseok_scene()

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

    def chulseok_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'chulseok_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(230, 80, 740, 485)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                    self.status = 0
                    return self.status

            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def event_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'event_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(100, 80, 165, 555)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                    self.set_option('last_status', self.status)
                    self.status = 100
                    return self.status

            self.status = 99999
        elif self.status == 100:
            self.status += 1
        elif 101 <= self.status < 110:
            self.status += 1
            resource_name = 'event_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(180, 90, 955, 555)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                    self.status = 100
                    return self.status
            self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def hyusik_bosang_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 5:
            pb_name = 'hyusik_bosang_select_' + self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang')
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.status += 1
            self.set_option('last_status', self.status)
            self.status = 10
        elif self.status == 10:
            pb_name = 'hyusik_bosang_receive'
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def channel_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('resource_name', '쾌적')
            self.set_option('has_drag', False)
            self.set_option('done', False)
            self.status += 1
        elif 1 <= self.status < 4:
            self.status += 1
            resource_name = 'channel_scene_' + self.get_option('resource_name') + '_loc'
            rect_list = [
                (480, 220, 520, 270),
                (480, 250, 520, 310),
                (480, 290, 520, 340),
                (480, 320, 520, 370),
                (480, 350, 520, 400),
            ]
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.85,
                    custom_flag=1,
                    average=False,
                    debug=True,
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 100
        elif self.status == 4:
            if self.get_option('has_drag') is False:
                self.lyb_mouse_drag('channel_scene_drag_bot', 'channel_scene_drag_top', stop_delay=0.0)
                self.status += 1
            else:
                self.status = 10
        elif self.status == 5:
            self.status += 1
        elif self.status == 6:
            self.status = 1
        elif self.status == 10:
            if self.get_option('done') is True:
                self.status = 99999
            else:
                self.set_option('resource_name', '원활')
                self.set_option('has_drag', False)
                self.set_option('done', True)
                self.status = 1
        elif self.status == 100:
            self.lyb_mouse_click('channel_scene_move', custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def immu_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'immu_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(110, 70, 610, 120)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                    self.set_option('last_status', self.status)
                    self.status = 100
                    return self.status

            self.status = 99999
        elif self.status == 100:
            self.status += 1
        elif 101 <= self.status < 130:
            self.status += 1
            if self.status % 3 == 0:
                resource_name = 'immu_scene_new_loc'
                resource = self.game_object.resource_manager.resource_dic[resource_name]
                for each in resource:
                    (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                        self.window_image,
                        self.game_object.resource_manager.pixel_box_dic[each],
                        custom_threshold=0.6,
                        custom_flag=1,
                        custom_top_level=(220, 60, 60),
                        custom_below_level=(130, 40, 40),
                        custom_rect=(910, 500, 950, 550)
                    )
                    self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                    if loc_x != -1:
                        self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                        return self.status

                self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def jamjeryeok_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            self.lyb_mouse_click('jamjeryeok_scene_all', custom_threshold=0)
            self.set_option('last_status', self.status)
            self.status = 100
        elif self.status == 100:
            self.status += 1
        elif self.status == 101:
            pb_name = 'jamjeryeok_scene_open'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.7:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status += 1
            else:
                self.status = 99999
        elif self.status == 102:
            self.status += 1
        elif self.status == 103:
            self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def gabang_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            self.lyb_mouse_click('gabang_scene_jamjeryeok', custom_threshold=0)
            self.game_object.get_scene('jamjeryeok_scene').status = 0
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def monster_josa_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('is_end', False)
            self.set_option('select_index', 0)
            self.set_option('init_status', 1)
            self.status += 1
        elif 1 <= self.status < 5:
            self.status += 1
            resource_name = 'monster_josa_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(160, 140, 650, 200)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    return self.status

            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(120, 110, 165, 550)
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.set_option('init_status', self.status)
                    self.status = 100
                    return self.status

            cfg_area = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area')

            resource_name = 'monster_josa_scene_area_' + cfg_area + '_loc'
            rect_list = [
                (5, 110, 150, 220),
                (5, 140, 150, 270),
                (5, 210, 150, 340),
                (5, 270, 150, 400),
                (5, 320, 150, 450),
                (5, 380, 150, 510),
                (5, 430, 150, 555),
                (5, 490, 150, 555),
            ]
            is_found = False
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.85,
                    custom_flag=1,
                    average=False,
                    debug=True,
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 400
                    is_found = True
                    break

            if self.status % 3 == 0 and is_found is False:
                self.set_option('last_status', self.status)
                self.status = 55
        elif self.status == 55:
            self.lyb_mouse_drag('monster_josa_scene_list_drag_bot', 'monster_josa_scene_list_drag_top', stop_delay=0.0)
            self.status = self.get_option('last_status')
        elif 100 <= self.status < 130:
            self.status += 1
            resource_name = 'monster_josa_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.7,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(260, 230, 640, 550),
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 200
                    return self.status

            if self.status % 3 == 0:
                self.set_option('last_status', self.status)
                self.status = 300

        elif 200 <= self.status < 210:
            self.status += 1

            resource_name = 'monster_josa_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.7,
                    custom_flag=1,
                    custom_top_level=(220, 60, 60),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(800, 500, 850, 540),
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 100
                    return self.status
        elif self.status == 300:
            resource_name = 'monster_josa_scene_end_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y) = self.get_location(each)
                self.set_option('last_pixel_' + each, self.game_object.window_pixels[loc_x, loc_y])
                self.logger.debug(str((loc_x, loc_y)) + ' ' + str(self.get_option('last_pixel_' + each)) + ' ' + str(
                    self.game_object.window_pixels[loc_x, loc_y]))

            self.lyb_mouse_drag('monster_josa_scene_drag_bot', 'monster_josa_scene_drag_top', stop_delay=0.0)
            self.status += 1
        elif self.status == 301:
            is_end = True
            resource_name = 'monster_josa_scene_end_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y) = self.get_location(each)
                last_pixel = self.get_option('last_pixel_' + each)
                self.logger.debug(str((loc_x, loc_y)) + ' ' + str(last_pixel) + ' ' + str(
                    self.game_object.window_pixels[loc_x, loc_y]))
                if last_pixel != self.game_object.window_pixels[loc_x, loc_y]:
                    is_end = False
            if is_end is True:
                self.set_option('is_end', True)
                self.status = self.get_option('init_status')
            else:
                self.status = self.get_option('last_status')
        elif 400 <= self.status < 410:
            self.status += 1
            if self.get_option('is_end') is True:
                self.set_option('select_index', 0)
                self.status = 500
            else:
                self.set_option('is_end', False)
                self.set_option('last_status', self.status)
                self.status = 300
        elif 500 <= self.status < 550:
            self.status += 1
            select_index = self.get_option('select_index')
            pb_name = 'monster_josa_scene_select_' + str(select_index)
            select_index = select_index + 1
            if select_index >= 10:
                self.set_option('select_index', 0)
                self.set_option('last_status', self.status)
                self.status = 700
            else:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.set_option('select_index', select_index)
                self.set_option('last_status', self.status)
                self.status = 600
        elif 600 <= self.status < 603:
            self.status += 1
        elif self.status == 603:
            pb_name = 'monster_josa_scene_max'
            pb_name2 = 'monster_josa_scene_search'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            match_rate2 = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name2)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            self.logger.debug(pb_name2 + ' ' + str(round(match_rate2, 2)))
            if match_rate < 0.9 < match_rate2:
                self.game_object.get_scene('local_map_scene').status = 1000
                self.lyb_mouse_click(pb_name2, custom_threshold=0)
                self.status += 1
            else:
                self.status = self.get_option('last_status')
        elif 604 <= self.status < 620:
            self.status += 1
        elif self.status == 700:
            self.status += 1
        elif self.status == 701:
            self.lyb_mouse_drag('monster_josa_scene_drag_top', 'monster_josa_scene_drag_bot', delay=0.1, stop_delay=0.0)
            self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def recover_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            cfg_free = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free')
            pb_name = 'recover_scene_free'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9 and cfg_free is True:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
            else:
                self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def local_map_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.game_object.get_scene('recover_scene').status = 0
            self.status += 1
        elif 101 <= self.status < 300:
            self.status += 1
            if self.status % 3 == 0:
                if self.is_detected_m() is False:
                    pb_name = 'local_map_scene_follow'
                    (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                        self.window_image,
                        self.game_object.resource_manager.pixel_box_dic[pb_name],
                        custom_threshold=0.8,
                        custom_flag=1,
                        custom_rect=(890, 150, 950, 550)
                    )
                    self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                    if loc_x != -1:
                        self.lyb_mouse_click_location(loc_x, loc_y)
        elif self.status == 1000:
            self.status += 1
        elif 1001 <= self.status < 1010:
            self.status += 1
            if self.status % 3 == 0:
                if self.is_detected_m() is False:
                    pb_name = 'local_map_scene_move'
                    self.lyb_mouse_click(pb_name, custom_threshold=0)
        elif 1010 <= self.status < 1500:
            if self.is_detected_m() is False:
                self.game_object.get_scene('main_scene').set_option('몬스터 조사' + '_move_ok', True)
                self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def go_home_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.lyb_mouse_click('go_home_scene_walk', custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def potion_gume_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 1:
            potion_count = self.get_option('potion_count')
            pb_name = 'potion_gume_scene_count_100'
            press_count = 1
            if potion_count == '200':
                press_count = 2
            elif potion_count == '300':
                press_count = 3
            elif potion_count == '400':
                press_count = 4
            elif potion_count == '500':
                press_count = 5
            elif potion_count == '600':
                press_count = 6
            elif potion_count == 'Max':
                pb_name = 'potion_gume_scene_count_max'

            self.set_option('pb_name', pb_name)
            self.set_option('press_count', press_count)
            self.status += 1
        elif 2 <= self.status < 10:
            press_count = self.get_option('press_count')
            pb_name = self.get_option('pb_name')
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            press_count = press_count - 1
            if press_count <= 0:
                self.status = 10
            else:
                self.set_option('press_count', press_count)
                self.status += 1
        elif self.status == 10:
            self.lyb_mouse_click('potion_gume_scene_ok', custom_threshold=0)
            self.game_object.get_scene('potion_npc_scene').set_option('gume_ok', True)
            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def potion_npc_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            potion = self.get_option('potion')

            cfg_hp_potion_name = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name')
            hp_resource_name = 'potion_npc_scene_potion_' + cfg_hp_potion_name + '_loc'
            hp_cfg_potion_count = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count')

            cfg_mp_potion_name = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2')
            mp_resource_name = 'potion_npc_scene_potion_' + cfg_mp_potion_name + '_loc'
            mp_cfg_potion_count = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2')

            potion_list = []
            if potion == 'mp':
                if cfg_mp_potion_name != '구매 안함':
                    potion_list.append({
                        'resource_name': mp_resource_name,
                        'count': mp_cfg_potion_count,
                        'last': False
                    })
                if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion') is True:
                    if cfg_hp_potion_name != '구매 안함':
                        potion_list.append({
                            'resource_name': hp_resource_name,
                            'count': hp_cfg_potion_count,
                            'last': True
                        })
            else:
                if cfg_hp_potion_name != '구매 안함':
                    potion_list.append({
                        'resource_name': hp_resource_name,
                        'count': hp_cfg_potion_count,
                        'last': False
                    })
                if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion') is True:
                    if cfg_mp_potion_name != '구매 안함':
                        potion_list.append({
                            'resource_name': mp_resource_name,
                            'count': mp_cfg_potion_count,
                            'last': True
                        })
            self.set_option('potion_list', potion_list)
            self.set_option('potion_index', 0)
            self.status += 1
        elif self.status == 1:
            potion_list = self.get_option('potion_list')
            potion_index = self.get_option('potion_index')
            self.logger.info(str(potion_list))
            self.game_object.get_scene('potion_gume_scene').status = 0
            if potion_list[potion_index]['last'] is True:
                self.game_object.get_scene('potion_gume_scene').set_option('potion_count', 'Max')
            else:
                self.game_object.get_scene('potion_gume_scene').set_option('potion_count',
                                                                           potion_list[potion_index]['count'])
            self.set_option('gume_ok', False)
            self.status = 101
        elif 101 <= self.status < 110:
            self.status += 1
            potion_list = self.get_option('potion_list')
            potion_index = self.get_option('potion_index')
            if self.get_option('gume_ok') is True:
                self.status = 110
            else:
                resource_name = potion_list[potion_index]['resource_name']
                rect_list = [
                    (70, 120, 320, 190),
                    (70, 190, 320, 260),
                    (70, 260, 320, 330),
                    (70, 330, 320, 400),
                    (70, 400, 320, 470),
                    (70, 470, 320, 540),
                ]
                for each in rect_list:
                    (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                        self.window_image,
                        resource_name,
                        custom_rect=each,
                        custom_threshold=0.85,
                        custom_flag=1,
                        average=False
                    )
                    self.logger.debug(
                        resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                    if loc_x != -1:
                        resource_name2 = 'potion_npc_scene_gume_loc'
                        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                            self.window_image,
                            resource_name2,
                            custom_rect=each,
                            custom_threshold=0.7,
                            custom_flag=1,
                            average=False
                        )
                        self.logger.debug(
                            resource_name2 + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                        if loc_x != -1:
                            self.lyb_mouse_click_location(loc_x, loc_y)
        elif self.status == 110:
            potion_list = self.get_option('potion_list')
            potion_index = self.get_option('potion_index')
            if potion_index >= len(potion_list) - 1:
                self.status = 99999
            else:
                self.status = 1
                self.set_option('potion_index', potion_index + 1)
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def move_potion_npc_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 100 <= self.status < 105:
            self.lyb_mouse_click('move_potion_npc_scene_go', custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def named_tobeol_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('done', False)
            self.status += 1
        elif self.status == 1:
            resource_name = 'named_tobeol_scene_done_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.status = 99999
                self.game_object.get_scene('main_scene').set_option('네임드 토벌' + '_end_flag', True)
                return self.status

            pb_name = 'named_tobeol_scene_quest_surak'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)

            self.status += 1
        elif 2 <= self.status < 5:
            self.lyb_mouse_click('named_tobeol_scene_auto', custom_threshold=0)
            self.set_option('done', True)
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
        elif self.status == 100:
            self.game_object.get_scene('main_scene').set_option('go_jeoljeon', 0)
            self.status += 1
        elif 101 <= self.status < 360:
            self.status += 1
            if self.status % 3 == 0:
                resource_name = 'jeoljeon_mode_scene_auto_combat_loc'
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
        elif 200 <= self.status < 210:
            if self.status % 5 == 0:
                self.lyb_mouse_click('quest_scene_named_tobeol', custom_threshold=0)
                self.game_object.get_scene('named_tobeol_scene').status = 0
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
        elif 300 <= self.status < 305:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_monster_josa', custom_threshold=0)
                self.game_object.get_scene('monster_josa_scene').status = 0
            self.status += 1
        elif 400 <= self.status < 405:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_jeoljeon', custom_threshold=0)
                self.game_object.get_scene('jeoljeon_mode_scene').status = 100
            self.status += 1
        elif 500 <= self.status < 505:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_immu', custom_threshold=0)
                self.game_object.get_scene('immu_scene').status = 0
            self.status += 1
        elif 600 <= self.status < 605:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_quest', custom_threshold=0)
                self.game_object.get_scene('quest_scene').status = 200
            self.status += 1
        elif 700 <= self.status < 705:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_chulseok', custom_threshold=0)
                self.game_object.get_scene('chulseok_scene').status = 0
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

        elif self.status == self.get_work_status('몬스터 조사'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=60)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.set_option(self.current_work + '_move_ok', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            if self.get_option(self.current_work + '_move_ok') is not True:
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.game_object.get_scene('menu_scene').status = 300
                self.set_option(self.current_work + '_inner_status', 0)
            else:
                inner_status = self.get_option(self.current_work + '_inner_status')
                if inner_status is None:
                    inner_status = 0

                self.logger.debug('inner_status ' + str(inner_status))
                if 0 <= inner_status < 5:
                    if self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monster_change_channel') is True:
                        if inner_status == 0:
                            self.lyb_mouse_click('main_scene_party', custom_threshold=0)
                        elif inner_status == 1:
                            self.lyb_mouse_click('main_scene_map', custom_threshold=0)
                        elif inner_status == 2:
                            self.game_object.get_scene('channel_scene').status = 0
                            self.lyb_mouse_click('main_scene_channel', custom_threshold=0)

                    self.set_option('go_jeoljeon', 0)
                elif inner_status == 5:
                    self.lyb_mouse_click('main_scene_auto', custom_threshold=0)
                elif 6 <= inner_status < 150:
                    go_jeoljeon = self.get_option('go_jeoljeon')
                    if go_jeoljeon == 5:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 400
                        self.set_option('go_jeoljeon', 0)
                    elif go_jeoljeon == 10:
                        self.set_option(self.current_work + '_move_ok', False)
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)
                else:
                    self.set_option(self.current_work + '_move_ok', False)

                self.set_option(self.current_work + '_inner_status', inner_status + 1)

        elif self.status == self.get_work_status('잠재력 개방'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_gabang', custom_threshold=0)
            self.game_object.get_scene('gabang_scene').status = 0

        elif self.status == self.get_work_status('임무'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 500

        elif self.status == self.get_work_status('네임드 토벌'):
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(3600):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, 3600, period=60)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            inner_status = self.get_option(self.current_work + '_inner_status')
            if inner_status is None:
                inner_status = 0

            self.logger.debug('inner_status ' + str(inner_status))

            if 0 <= inner_status < 10:
                if self.game_object.get_scene('named_tobeol_scene').get_option('done') is True:
                    self.game_object.get_scene('named_tobeol_scene').set_option('done', False)
                    inner_status = 10
                else:
                    self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                    self.game_object.get_scene('menu_scene').status = 600
                    self.set_option('go_jeoljeon', 0)
            elif 10 <= inner_status < 60:
                go_jeoljeon = self.get_option('go_jeoljeon')
                if go_jeoljeon == 5:
                    self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                    self.game_object.get_scene('menu_scene').status = 200
                    self.set_option('go_jeoljeon', 0)

                if self.get_option('go_jeoljeon') == 10:
                    inner_status = 0
                else:
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)
            else:
                inner_status = 0

            self.set_option(self.current_work + '_inner_status', inner_status + 1)

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

        if self.get_option('is_moving') is True:
            return True

        # 일일 체크리스트
        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check') is True:
            elapsed_time = time.time() - self.get_checkpoint('chulseok_check')
            if elapsed_time > self.period_bot(81640):
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.game_object.get_scene('menu_scene').status = 700
                self.set_checkpoint('chulseok_check')
                return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move') is True:
            if self.is_hp_potion_empty() is True or self.get_option('hp_potion_empty') is True:
                if self.click_potion_menu():
                    self.game_object.get_scene('move_potion_npc_scene').status = 100
                    self.game_object.get_scene('potion_npc_scene').status = 0
                    self.game_object.get_scene('potion_npc_scene').set_option('potion', 'hp')
                    self.set_option('hp_potion_empty', False)
                    self.set_option('go_home', False)
                    return True
                else:
                    if self.get_option('go_home') is not True:
                        self.click_resource('main_scene_menu_home_loc')
                        self.game_object.get_scene('go_home_scene').status = 100
                        self.set_option('hp_potion_empty', True)
                        self.set_option('go_home', True)
                    return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move') is True:
            if self.is_mp_potion_empty() is True or self.get_option('mp_potion_empty') is True:
                if self.click_potion_menu():
                    self.game_object.get_scene('move_potion_npc_scene').status = 100
                    self.game_object.get_scene('potion_npc_scene').status = 0
                    self.game_object.get_scene('potion_npc_scene').set_option('potion', 'mp')
                    self.set_option('mp_potion_empty', False)
                    self.set_option('go_home', False)
                    return True
                else:
                    if self.get_option('go_home') is not True:
                        self.click_resource('main_scene_menu_home_loc')
                        self.game_object.get_scene('go_home_scene').status = 100
                        self.set_option('mp_potion_empty', True)
                        self.set_option('go_home', True)
                    return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move') is True:
            if self.click_recover_menu():
                self.game_object.get_scene('local_map_scene').status = 100
                return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil') is True:
            elapsed_time = time.time() - self.get_checkpoint('event_devil')
            if elapsed_time > self.period_bot(300) and self.is_charged():
                self.lyb_mouse_click('main_scene_devil', custom_threshold=0)
                self.set_checkpoint('event_devil')
                return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'event_check') is True:
            elapsed_time = time.time() - self.get_checkpoint('event_check')
            if elapsed_time > self.period_bot(30) and self.click_event():
                self.game_object.get_scene('hyusik_bosang_scene').status = 0
                self.game_object.get_scene('event_scene').status = 0
                self.set_checkpoint('event_check')
                return True

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

    def is_hp_potion_empty(self, limit=3):
        return self.is_status_by_resource('HP 물약 없음 감지', 'main_scene_potion_ok_loc',
                                          custom_top_level=(255, 255, 255),
                                          custom_below_level=(150, 150, 150),
                                          custom_rect=(645, 520, 695, 560),
                                          custom_threshold=0.5,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_mp_potion_empty(self, limit=3):
        return self.is_status_by_resource('MP 물약 없음 감지', 'main_scene_mp_potion_ok_loc',
                                          custom_top_level=(255, 255, 255),
                                          custom_below_level=(150, 150, 150),
                                          custom_rect=(690, 520, 745, 560),
                                          custom_threshold=0.5,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_auto(self, limit=3):
        return self.is_status_by_resource('자동 꺼짐 감지', 'no_auto_loc',
                                          custom_top_level=(180, 180, 180),
                                          custom_below_level=(100, 100, 100),
                                          custom_rect=(240, 500, 300, 550),
                                          custom_threshold=0.3,
                                          limit_count=limit,
                                          reverse=True,
                                          )

    def is_detected_m(self):
        pb_name = 'local_map_scene_m'
        (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
            self.window_image,
            self.game_object.resource_manager.pixel_box_dic[pb_name],
            custom_threshold=0.8,
            custom_flag=1,
            custom_rect=(470, 60, 550, 100)
        )
        self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            return True

        return False

    def click_potion_menu(self):
        resource_name = 'main_scene_menu_potion_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_top_level=(255, 255, 255),
            custom_below_level=(150, 150, 150),
            custom_rect=(600, 70, 950, 130),
            custom_threshold=0.7,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def click_recover_menu(self):
        resource_name = 'main_scene_menu_recover_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_top_level=(255, 90, 80),
            custom_below_level=(190, 70, 40),
            custom_rect=(600, 70, 950, 130),
            custom_threshold=0.7,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def click_event(self):
        pb_name = 'main_scene_event_new'
        (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
            self.window_image,
            self.game_object.resource_manager.pixel_box_dic[pb_name],
            custom_threshold=0.6,
            custom_flag=1,
            custom_top_level=(210, 60, 60),
            custom_below_level=(180, 40, 40),
            custom_rect=(210, 80, 330, 240),
        )
        self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
            return True

        (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
            self.window_image,
            self.game_object.resource_manager.pixel_box_dic[pb_name],
            custom_threshold=0.6,
            custom_flag=1,
            custom_top_level=(210, 60, 60),
            custom_below_level=(180, 40, 40),
            custom_rect=(10, 80, 130, 240),
        )
        self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
            return True

        return False

    def is_charged(self, limit=3):
        return self.is_status_by_resource('데빌 체이서 감지', 'main_scene_charged_loc',
                                          custom_top_level=(255, 80, 80),
                                          custom_below_level=(145, 0, 0),
                                          custom_rect=(310, 460, 370, 530),
                                          custom_threshold=0.4,
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
