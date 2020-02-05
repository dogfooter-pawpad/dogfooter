import traceback
import likeyoubot_v4 as lybgamev4
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_scene
import time
import random


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
        elif self.scene_name == 'monghwan_scene':
            rc = self.monghwan_scene()
        elif self.scene_name == 'ipjang_confirm_scene':
            rc = self.ipjang_confirm_scene()
        elif self.scene_name == 'upjeok_scene':
            rc = self.upjeok_scene()
        elif self.scene_name == 'mail_scene':
            rc = self.mail_scene()
        elif self.scene_name == 'shop_scene':
            rc = self.shop_scene()
        elif self.scene_name == 'sangpum_gume_scene':
            rc = self.sangpum_gume_scene()
        elif self.scene_name == 'guild_scene':
            rc = self.guild_scene()
        elif self.scene_name == 'guild_give_scene':
            rc = self.guild_give_scene()
        elif self.scene_name == 'guild_chulseok_bosang_scene':
            rc = self.guild_chulseok_bosang_scene()
        elif self.scene_name == 'jido_scene':
            rc = self.jido_scene()
        elif self.scene_name == 'deryuk_jido_scene':
            rc = self.deryuk_jido_scene()
        elif self.scene_name == 'lunatra_scene':
            rc = self.lunatra_scene()
        elif self.scene_name == 'lunatra_jido_scene':
            rc = self.lunatra_jido_scene()
        elif self.scene_name == 'stash_scene':
            rc = self.stash_scene()
        elif self.scene_name == 'stash_reserve_scene':
            rc = self.stash_reserve_scene()
        elif self.scene_name == 'ure_scene':
            rc = self.ure_scene()
        # 영혼석 성장 씬 추가
        elif self.scene_name == 'soul_scene':
            rc = self.soul_scene()

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

    def ure_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'ure_scene_auto_quest_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(410, 50, 550, 100),
                custom_threshold=0.8,
                custom_flag=1,
                average=False,
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.status = 99999
                self.game_object.get_scene('main_scene').set_option('의뢰 일지' + '_auto_ok', True)
                return self.status

            rect_list = [
                (170, 110, 200, 180),
                (170, 150, 200, 210),
                (170, 190, 200, 250),
                (170, 230, 200, 290),
                (170, 270, 200, 330),
                (170, 310, 200, 370),
                (170, 350, 200, 410),
                (170, 390, 200, 450),
                (170, 430, 200, 490),
                (170, 470, 200, 530),
                (170, 510, 200, 570),
            ]
            resource_name = 'ure_scene_need_accept_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.99:
                resource_name = 'ure_scene_point_loc'
                for each in rect_list:
                    (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                        self.window_image,
                        resource_name,
                        custom_rect=each,
                        custom_threshold=0.6,
                        custom_top_level=(255, 255, 255),
                        custom_below_level=(180, 180, 180),
                        custom_flag=1,
                        average=False,
                        debug=True,
                    )
                    self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                    if loc_x != -1:
                        self.lyb_mouse_click_location(loc_x, loc_y)
                        return self.status

            resource_name = 'ure_scene_view_location_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.98:
                self.lyb_mouse_click('ure_scene_view_location_0', custom_threshold=0)
                self.set_option('last_status', 0)
                self.status = 100
                self.game_object.get_scene('local_map_scene').status = 21000
                return self.status

            resource_name = 'ure_scene_bosang_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.98:
                self.lyb_mouse_click('ure_scene_bosang_0', custom_threshold=0)
                return self.status

            resource_name = 'ure_scene_complete_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.98:
                self.game_object.get_scene('main_scene').set_option('의뢰 일지' + '_end_flag', True)
                self.status = 99999
                return self.status

            resource_name = 'ure_scene_auto_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.98:
                self.lyb_mouse_click('ure_scene_auto_0', custom_threshold=0)
                self.game_object.get_scene('main_scene').set_option('의뢰 일지' + '_auto_ok', True)
                return self.status

            resource_name = 'ure_scene_auto_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.98:
                self.game_object.get_scene('main_scene').set_option('의뢰 일지' + '_end_flag', True)
                self.status = 99999
                return self.status

        elif 100 <= self.status < 105:
            self.status += 1
        elif self.status == 105:
            self.status = self.get_option('last_status')
        else:
            self.game_object.get_scene('quest_scene').status = 99999
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def stash_reserve_scene(self):

        self.lyb_mouse_click('stash_reserve_scene_ok', custom_threshold=0)

        return self.status

    def stash_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('page_number', 1)
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click('stash_scene_tab_3', custom_threshold=0)
            self.status += 1
        elif 2 <= self.status < 10:
            self.status += 1
            resource_name = 'stash_scene_sort_class_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.99:
                self.status = 10
            else:
                self.set_option('last_status', self.status)
                self.status = 100
                self.lyb_mouse_click('stash_scene_sort_class_0', custom_threshold=0)
        elif self.status == 10:
            self.set_option('last_row', 0)
            self.set_option('last_col', 0)
            self.status += 1
        elif 11 <= self.status < 50:
            self.status += 1
            last_row = self.get_option('last_row')
            last_col = self.get_option('last_col')

            pb_name = 'stash_scene_item_' + str(last_col) + str(last_row)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.set_option('last_status', self.status)
            self.status = 60
        elif self.status == 60:
            resource_name = 'stash_scene_enable_condition_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))

            resource_name = 'stash_scene_reserve_loc'
            (loc_x, loc_y), match_rate2 = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(550, 350, 650, 450),
                custom_threshold=0.85,
                custom_flag=1,
                average=False,
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate2, 2)))
            if match_rate > 0.99 and loc_x != -1:
                self.lyb_mouse_click_location(loc_x, loc_y)
            else:
                last_row = self.get_option('last_row')
                last_col = self.get_option('last_col')
                if last_col + 1 > 4:
                    if last_row + 1 > 4:
                        self.status = 200
                        return self.status
                    else:
                        self.set_option('last_row', last_row + 1)
                        self.set_option('last_col', 0)
                else:
                    self.set_option('last_col', last_col + 1)
            self.status = self.get_option('last_status')
        elif self.status == 100:
            self.status += 1
        elif self.status == 101:
            self.lyb_mouse_click('stash_scene_sort_2', custom_threshold=0)
            self.status = self.get_option('last_status')
        elif self.status == 200:
            cfg_page_number = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number'))
            page_number = self.get_option('page_number')
            if page_number >= cfg_page_number:
                self.status = 99999
            else:
                self.set_option('page_number', page_number + 1)
                self.lyb_mouse_drag('stash_scene_drag_bot', 'stash_scene_drag_top', delay=2.0)
                self.status += 1
        elif self.status == 201:
            self.status = 10
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def lunatra_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.status += 1
        elif self.status == 101:
            self.status += 1
            local_name = self.get_option('local_name')
            pb_name = 'lunatra_scene_list_' + local_name
            self.lyb_mouse_click(pb_name, custom_threshold=0)
        elif 102 <= self.status < 105:
            self.status += 1
            pb_name = 'lunatra_scene_ok'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.95:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('main_scene').set_option('지도 이동' + '_lunatra_ipjang_ok', True)
                return self.status
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def lunatra_jido_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.status = 104
        elif 104 <= self.status < 130:
            self.status += 1
            local_map = self.get_option('local_map')
            pb_name = 'lunatra_jido_scene_local_' + local_map
            if self.status % 5 == 0:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('local_map_scene').set_option('changed', True)
        else:
            self.game_object.get_scene('jido_scene').status = 99999
            self.game_object.get_scene('local_map_scene').status = 99999
            self.game_object.get_scene('lunatra_jido_scene').status = 99999
            self.game_object.get_scene('deryuk_jido_scene').status = 99999
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def deryuk_jido_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.status = 104
        elif 104 <= self.status < 130:
            self.status += 1
            map = self.get_option('map')
            local_map = self.get_option('local_map')
            pb_name = 'deryuk_jido_scene_' + map + '_' + local_map
            if self.status % 5 == 0:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('local_map_scene').set_option('changed', True)
        else:
            self.game_object.get_scene('jido_scene').status = 99999
            self.game_object.get_scene('local_map_scene').status = 99999
            self.game_object.get_scene('lunatra_jido_scene').status = 99999
            self.game_object.get_scene('deryuk_jido_scene').status = 99999
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def jido_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.status = 104
        elif 104 <= self.status < 130:
            self.status += 1
            local_map = self.get_option('local_map')
            pb_name = 'jido_scene_local_' + local_map
            if self.status % 5 == 0:
                self.lyb_mouse_click(pb_name, custom_threshold=0)

                self.game_object.get_scene('deryuk_jido_scene').status = 100
                cfg_local_map = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area')
                self.game_object.get_scene('deryuk_jido_scene').set_option('map', local_map)
                self.game_object.get_scene('deryuk_jido_scene').set_option('local_map', cfg_local_map)

                self.game_object.get_scene('lunatra_jido_scene').status = 100
                cfg_local_map = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area')
                self.game_object.get_scene('lunatra_jido_scene').set_option('map', local_map)
                self.game_object.get_scene('lunatra_jido_scene').set_option('local_map', cfg_local_map)
        elif self.status == 200:
            self.status = 204
        elif 204 <= self.status < 230:
            self.status += 1
            local_map = '실루나스'
            cfg_local_map = '차원의 경계'
            pb_name = 'jido_scene_local_' + local_map
            if self.status % 5 == 0:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('deryuk_jido_scene').status = 100
                self.game_object.get_scene('deryuk_jido_scene').set_option('map', local_map)
                self.game_object.get_scene('deryuk_jido_scene').set_option('local_map', cfg_local_map)
        else:
            self.game_object.get_scene('jido_scene').status = 99999
            self.game_object.get_scene('local_map_scene').status = 99999
            self.game_object.get_scene('lunatra_jido_scene').status = 99999
            self.game_object.get_scene('deryuk_jido_scene').status = 99999
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def guild_chulseok_bosang_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'guild_chulseok_bosang_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(510, 360, 580, 430)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                    return self.status

            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def guild_give_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            pb_name = 'guild_give_scene_gold_limit'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.95:
                self.status = 99999
            else:
                self.lyb_mouse_click('guild_give_scene_gold', custom_threshold=0)
        else:
            self.game_object.get_scene('guild_scene').set_option('give_ok', True)
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def guild_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('give_ok', False)
            self.status += 1
        elif 1 <= self.status < 10:
            if self.get_option('give_ok'):
                self.status = 10
            else:
                self.lyb_mouse_click('guild_scene_give', custom_threshold=0)
                self.game_object.get_scene('guild_give_scene').status = 0
                self.status += 1
        elif 10 <= self.status < 20:
            self.status += 1
            resource_name = 'guild_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(120, 500, 170, 550)
                )
                self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                    return self.status
            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def sangpum_gume_scene(self):

        pb_name = 'sangpum_gume_scene_gem'
        (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
            self.window_image,
            self.game_object.resource_manager.pixel_box_dic[pb_name],
            custom_threshold=0.7,
            custom_flag=1,
            custom_rect=(410, 430, 550, 480)
        )
        self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
            return self.status

        elapsed_time = time.time() - self.get_checkpoint('clicked')
        if elapsed_time < self.period_bot(5):
            self.lyb_mouse_click('sangpum_gume_scene_ok', custom_threshold=0)
        else:
            self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

        return self.status

    def shop_scene(self):

        rect_list = [
            (20, 100, 150, 190),
            (20, 160, 150, 220),
            (20, 200, 150, 260),
            (20, 240, 150, 300),
            (20, 280, 150, 340),
            (20, 320, 150, 390),
            (20, 360, 150, 430),
            (20, 410, 150, 470),
            (20, 440, 150, 510),
            (20, 480, 150, 550),
            (20, 530, 150, 565),
            (20, 530, 150, 565),
        ]
        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('drag_direction', False)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'shop_scene_list_탈것_loc'
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
                    self.set_option('last_status', 10)
                    self.status = 100
                    return self.status
            self.set_option('last_status', self.status)
            self.status = 40
        elif 10 <= self.status < 20:
            self.status += 1
            resource_name = 'shop_scene_list_소환수_loc'
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
                    self.set_option('last_status', 20)
                    self.status = 100
                    return self.status
            self.set_option('last_status', self.status)
            self.status = 40
        elif 20 <= self.status < 30:
            self.status += 1
            resource_name = 'shop_scene_list_일일 한정_loc'
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
                    self.set_option('last_status', 99999)
                    self.status = 100
                    return self.status
            self.set_option('last_status', self.status)
            self.status = 40
        elif self.status == 40:
            if self.get_option('drag_direction') is not True:
                self.lyb_mouse_drag('shop_scene_list_drag_bot', 'shop_scene_list_drag_top', stop_delay=0.0)
                self.set_option('drag_direction', True)
            else:
                self.lyb_mouse_drag('shop_scene_list_drag_top', 'shop_scene_list_drag_bot', stop_delay=0.0)
                self.set_option('drag_direction', False)
            self.status += 1
        elif 41 <= self.status < 43:
            self.status += 1
        elif self.status == 43:
            self.status = self.get_option('last_status')
        elif self.status == 100:
            self.set_option('content_drag', False)
            self.status += 1
        elif 101 <= self.status < 120:
            self.status += 1
            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha') is True:
                resource_name = 'shop_scene_화려한 탈것 소환_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status
                resource_name = 'shop_scene_빛나는 탈것 소환_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status
                resource_name = 'shop_scene_눈부신 탈것 소환_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha') is True:
                resource_name = 'shop_scene_화려한 소환수 부화_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status
                resource_name = 'shop_scene_빛나는 소환수 부화_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status
                resource_name = 'shop_scene_눈부신 소환수 부화_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion') is True:
                resource_name = 'shop_scene_상급 축복의 물약_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status
                resource_name = 'shop_scene_빛나는 흔적 상자_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha') is True:
                resource_name = 'shop_scene_화려한 동료 계약서_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status
                resource_name = 'shop_scene_리노어 동료 계약서_loc'
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    self.set_checkpoint(resource_name)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha') is True:
                resource_name = 'shop_scene_무기 강화 주문서 상자_loc'
                count = self.get_option(resource_name + '_count')
                if count is None:
                    count = 0
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    if count == 4:
                        self.set_checkpoint(resource_name)
                        self.set_option(resource_name + '_count', 0)
                    else:
                        self.set_option(resource_name + '_count', count + 1)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha') is True:
                resource_name = 'shop_scene_방어구 강화 주문서 상자_loc'
                count = self.get_option(resource_name + '_count')
                if count is None:
                    count = 0
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    if count == 4:
                        self.set_checkpoint(resource_name)
                        self.set_option(resource_name + '_count', 0)
                    else:
                        self.set_option(resource_name + '_count', count + 1)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha') is True:
                resource_name = 'shop_scene_장신구 강화 주문서 상자_loc'
                count = self.get_option(resource_name + '_count')
                if count is None:
                    count = 0
                elapsed_time = time.time() - self.get_checkpoint(resource_name)
                if elapsed_time > self.period_bot(3600) and self.click_shop_resource(resource_name):
                    if count == 4:
                        self.set_checkpoint(resource_name)
                        self.set_option(resource_name + '_count', 0)
                    else:
                        self.set_option(resource_name + '_count', count + 1)
                    self.game_object.get_scene('sangpum_gume_scene').set_checkpoint('clicked')
                    return self.status

            if self.get_option('content_drag') is not True:
                self.set_option('content_drag', True)
                self.lyb_mouse_drag('shop_scene_drag_right', 'shop_scene_drag_left', stop_delay=0.0)
                self.status = 130
            else:
                self.status = self.get_option('last_status')
        elif self.status == 130:
            self.status += 1
        elif self.status == 131:
            self.status = 101
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def mail_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 20:
            self.status += 1
            resource_name = 'mail_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(10, 70, 350, 130)
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
        elif 101 <= self.status < 120:
            self.status += 1
            resource_name = 'mail_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(840, 510, 955, 555)
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

    def upjeok_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 20:
            self.status += 1
            resource_name = 'upjeok_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(110, 70, 170, 555)
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
        elif 101 <= self.status < 120:
            self.status += 1
            resource_name = 'upjeok_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for each in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[each],
                    custom_threshold=0.6,
                    custom_flag=1,
                    custom_top_level=(220, 90, 90),
                    custom_below_level=(130, 40, 40),
                    custom_rect=(910, 510, 955, 555)
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

    def ipjang_confirm_scene(self):

        self.lyb_mouse_click('ipjang_confirm_scene_go', custom_threshold=0)

        return self.status

    def monghwan_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            monghwan_area_list = lybgamev4.LYBV4.sub_area_list[lybgamev4.LYBV4.area_list.index('몽환의 틈')]
            self.logger.info(str(monghwan_area_list))
            self.set_option('area_list', monghwan_area_list)
            self.lyb_mouse_drag('monghwan_scene_list_drag_top', 'monghwan_scene_list_drag_bot')
            self.set_option('list_index', 0)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            monghwan_area_list = self.get_option('area_list')
            list_index = self.get_option('list_index')
            if list_index >= len(monghwan_area_list):
                self.status = 99999
            else:
                cfg_order = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_' + str(list_index))
                if cfg_order == '안함':
                    self.set_option('list_index', list_index + 1)
                else:
                    resource_name = 'monghwan_scene_' + monghwan_area_list[list_index] + '_loc'
                    self.set_option('resource_name', resource_name)
                    self.set_option('list_index', list_index + 1)
                    self.set_option('location_index', 0)
                    self.lyb_mouse_drag('monghwan_scene_list_drag_top', 'monghwan_scene_list_drag_bot')
                    self.set_option('last_status', self.status)
                    self.status = 50
                    return self.status
        elif 50 <= self.status < 53:
            self.lyb_mouse_drag('monghwan_scene_list_drag_top', 'monghwan_scene_list_drag_bot')
            self.status += 1
        elif 53 <= self.status < 70:
            self.status += 1
            resource_name = self.get_option('resource_name')
            location_index = self.get_option('location_index')

            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.status = 100
                return self.status

            if location_index == 5 and self.status < 60:
                self.status = 80
                return self.status
            elif location_index > 9:
                self.status = 99999
                self.logger.warn(str(resource_name) + ' 탐색 실패. 오류 보고 필요.')
                return self.status

            pb_name = 'monghwan_scene_list_' + str(location_index)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.set_option('location_index', location_index + 1)
        elif 80 <= self.status < 83:
            self.lyb_mouse_drag('monghwan_scene_list_drag_bot', 'monghwan_scene_list_drag_top')
            self.status += 1
        elif self.status == 83:
            self.status = 60
        elif self.status == 100:
            self.status += 1
        elif 101 <= self.status < 110:
            self.status += 1
            resource_name = 'monghwan_scene_disable_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(325, 320, 550, 380),
                custom_threshold=0.6,
                custom_flag=1,
                average=False,
                debug=True,
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.status = 99998
                return self.status

            resource_name = 'monghwan_scene_time_end_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name, custom_top_level=255,
                                                              custom_below_level=160)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.99:
                self.status = self.get_option('last_status')
                return self.status

            pb_name = 'monghwan_scene_location'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.7:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 2000
                self.logger.info(str(self.status) + ' ' + str(self.get_option('last_status')))
                self.status = 200
                return self.status

            pb_name = 'monghwan_scene_ipjang'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.7:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('main_scene').set_option('몽환의 틈' + '_ipjang_ok', True)
                self.game_object.get_scene('main_scene').set_option('몽환의 틈' + '_list_index',
                                                                    self.get_option('list_index') - 1)
                self.status = 99999
        elif 200 <= self.status < 300:
            self.status += 1
        elif self.status == 300:
            self.status = 0
        elif self.status == 1000:
            resource_name = 'monghwan_scene_' + self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area') + '_loc'
            self.set_option('resource_name', resource_name)
            self.set_option('location_index', 0)
            self.lyb_mouse_drag('monghwan_scene_list_drag_top', 'monghwan_scene_list_drag_bot')
            self.status += 1
        elif 1001 <= self.status < 1003:
            self.status += 1
            self.lyb_mouse_drag('monghwan_scene_list_drag_top', 'monghwan_scene_list_drag_bot')
        elif 1003 <= self.status < 1023:
            self.status += 1
            resource_name = self.get_option('resource_name')
            location_index = self.get_option('location_index')

            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.status = 1100
                return self.status

            if location_index == 5 and self.status < 1013:
                self.status = 1030
                return self.status
            elif location_index > 9:
                self.status = 99999
                self.logger.warn(str(resource_name) + ' 탐색 실패. 오류 보고 필요.')
                return self.status

            pb_name = 'monghwan_scene_list_' + str(location_index)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.set_option('location_index', location_index + 1)
        elif 1030 <= self.status < 1033:
            self.lyb_mouse_drag('monghwan_scene_list_drag_bot', 'monghwan_scene_list_drag_top')
            self.status += 1
        elif self.status == 1033:
            self.status = 1013
        elif 1100 <= self.status < 1110:
            self.status += 1
            resource_name = 'monghwan_scene_disable_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(325, 320, 550, 380),
                custom_threshold=0.6,
                custom_flag=1,
                average=False,
                debug=True,
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.status = 99998
                return self.status

            resource_name = 'monghwan_scene_time_end_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name, custom_top_level=255,
                                                              custom_below_level=160)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.99:
                self.status = 99998
                return self.status

            pb_name = 'monghwan_scene_location'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.7:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 1900
                self.status = 200
                return self.status

            pb_name = 'monghwan_scene_ipjang'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.7:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.game_object.get_scene('main_scene').set_option('지도 이동' + '_monghwan_ipjang_ok', True)
                self.status = 99999
        elif self.status == 99998:
            self.game_object.get_scene('main_scene').set_option('몽환의 틈' + '_end_flag', True)
            self.game_object.get_scene('main_scene').set_option('지도 이동' + '_end_flag', True)
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
                    custom_top_level=(220, 90, 90),
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
            if self.get_option('resource_name') is None:
                self.set_option('resource_name', '쾌적')
            self.set_option('has_drag', False)
            self.set_option('done', False)
            if self.get_option('resource_name') == '파티' or self.get_option('resource_name') == '쾌적' or \
                    self.get_option('resource_name') == '원활' or self.get_option('resource_name') == '혼잡':
                self.status += 1
            else:
                self.set_option('has_drag', True)
                self.set_option('done', True)
                number = int(self.get_option('resource_name'))
                self.set_option('number', str(number - 1))
                if number < 6:
                    self.status = 20
                else:
                    self.status = 30
        elif 1 <= self.status < 4:
            self.status += 1
            resource_name = 'channel_scene_' + self.get_option('resource_name') + '_loc'
            rect_list = [
                (430, 220, 630, 270),
                (430, 250, 630, 310),
                (430, 290, 630, 340),
                (430, 320, 630, 370),
                (430, 350, 630, 400),
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
                    return self.status
        elif self.status == 4:
            if self.get_option('has_drag') is not True:
                self.lyb_mouse_drag('channel_scene_drag_bot', 'channel_scene_drag_top', stop_delay=0.0)
                self.set_option('has_drag', True)
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
                if self.get_option('resource_name') == '파티':
                    self.set_option('resource_name', '쾌적')
                    self.set_option('has_drag', False)
                else:
                    self.set_option('resource_name', '원활')
                    self.set_option('has_drag', False)
                    self.set_option('done', True)
                self.status = 1
        elif 20 <= self.status < 25:
            self.status += 1
            self.lyb_mouse_drag('channel_scene_drag_top', 'channel_scene_drag_bot', stop_delay=0.0)
        elif self.status == 25:
            self.status = 50
        elif 30 <= self.status < 35:
            self.status += 1
            self.lyb_mouse_drag('channel_scene_drag_bot', 'channel_scene_drag_top', stop_delay=0.0)
        elif self.status == 35:
            self.status = 50
        elif self.status == 50:
            pb_name = 'channel_scene_list_' + self.get_option('number')
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.status = 99999
        elif self.status == 100:
            self.lyb_mouse_click('channel_scene_move', custom_threshold=0)
            self.status += 1
        else:
            self.set_option('resource_name', None)
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
            # TODO 잠재력 모드 추가
            cfg_jamjeryeok_mode = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode')
            # TODO 잠재력모드 인내 강제설정
            # cfg_jamjeryeok_mode = '인내'
            if cfg_jamjeryeok_mode == '투지':
                self.lyb_mouse_click('jamjeryeok_scene_select_tuzi', custom_threshold=0)
            elif cfg_jamjeryeok_mode == '인내':
                self.lyb_mouse_click('jamjeryeok_scene_select_inne', custom_threshold=0)
            elif cfg_jamjeryeok_mode == '통찰':
                self.lyb_mouse_click('jamjeryeok_scene_select_tongchal', custom_threshold=0)
            elif cfg_jamjeryeok_mode == '의지':
                self.lyb_mouse_click('jamjeryeok_scene_select_uzi', custom_threshold=0)
            self.set_option('last_status', self.status)
            self.status = 20
        elif 20 <= self.status < 30:
            self.status += 1
            # 일괄등록 클릭
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

    def soul_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 5:
            self.status += 1
            pb_name = 'soul_scene_level_0'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.7:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 5
                return self.status
        elif 5 <= self.status < 10:
            self.status += 1
            pb_name = 'soul_scene_level_1'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.55:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 10
                return self.status
        elif 10 <= self.status < 15:
            self.status += 1
            rect_list = [
                (650, 300, 950, 390),
                (650, 390, 950, 480),
                (650, 480, 950, 560),
            ]
            resource_name = 'soul_scene_stonename_loc'
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(0, 0, 90),
                    custom_threshold=0.80,  # 기본값 0.85
                    custom_flag=1,
                    average=True,
                    debug=True,
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 15
                    return self.status
            self.lyb_mouse_drag('soul_scene_drag_bot', 'soul_scene_drag_top', stop_delay=1.0)
        elif 15 <= self.status < 20:
            self.status += 1

            pb_name = 'soul_scene_level_2'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.99:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 20
                return self.status
        elif 20 <= self.status < 25:
            self.status += 1
            pb_name = 'soul_scene_level_3'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                time.sleep(3)
                self.lyb_mouse_click('soul_scene_level_ok_click', custom_threshold=0)
                self.status = 25
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
            if self.get_option('equip'):
                self.lyb_mouse_click('gabang_scene_equip', custom_threshold=0)
                self.set_option('last_status', self.status)
                self.status = 20
                return self.status

            self.lyb_mouse_click('gabang_scene_jamjeryeok', custom_threshold=0)
            self.game_object.get_scene('jamjeryeok_scene').status = 0
        elif self.status == 20:
            self.set_option('equip', False)
            self.status += 1
        elif self.status == 21:
            self.set_option('equip', False)
            self.status = self.get_option('last_status')
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
            self.status = 1000
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
                    custom_threshold=0.8,
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

            if self.status % 3 == 0 and is_found is not True:
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
                self.set_option('search_order', 'bot')
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

            if self.get_option('search_order') == 'bot':
                self.lyb_mouse_drag('monster_josa_scene_drag_bot', 'monster_josa_scene_drag_top', stop_delay=0.0)
            else:
                self.lyb_mouse_drag('monster_josa_scene_drag_top', 'monster_josa_scene_drag_bot', stop_delay=0.0)
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
        elif self.status == 400:
            self.set_option('is_end', False)
            cfg_order = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order')
            if cfg_order == '아래에서부터 탐색':
                self.set_option('search_order', 'bot')
            else:
                self.set_option('search_order', 'top')
            self.status += 1
        elif 401 <= self.status < 410:
            self.set_option('init_status', self.status)
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
            if self.get_option('search_order') == 'bot':
                pb_name = 'monster_josa_scene_select_' + str(select_index)
            else:
                pb_name = 'monster_josa_scene_select_' + str(8 - select_index)
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
        elif self.status == 600:
            self.status += 1
        elif self.status == 601:
            pb_name = 'monster_josa_scene_max'
            pb_name2 = 'monster_josa_scene_search'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            match_rate2 = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name2)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            self.logger.debug(pb_name2 + ' ' + str(round(match_rate2, 2)))
            if match_rate < 0.6:
                if match_rate2 > 0.9:
                    # 보스 아님
                    is_named = 0.0
                    if self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named'):
                        resource_name = 'monster_josa_scene_named_loc'
                        is_named = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
                        self.logger.debug(resource_name + ' ' + str(round(is_named, 2)))

                    if is_named < 0.8:
                        # 네임드도 아니고
                        self.game_object.get_scene('local_map_scene').status = 1000
                        self.lyb_mouse_click(pb_name2, custom_threshold=0)
                        self.status += 1
                        return self.status

            self.status = self.get_option('last_status')
        elif 602 <= self.status < 620:
            self.status += 1
        elif self.status == 700:
            self.status += 1
        elif self.status == 701:
            if self.get_option('search_order') == 'bot':
                self.lyb_mouse_drag('monster_josa_scene_drag_top', 'monster_josa_scene_drag_bot', stop_delay=1.0)
            else:
                self.lyb_mouse_drag('monster_josa_scene_drag_bot', 'monster_josa_scene_drag_top', stop_delay=1.0)
            self.status = self.get_option('last_status')
        elif 1000 <= self.status < 1005:
            self.status += 1
            self.lyb_mouse_drag('monster_josa_scene_list_drag_top', 'monster_josa_scene_list_drag_bot', stop_delay=0.0)
        elif self.status == 1005:
            self.status = 1
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
            self.status += 1
            cfg_free = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free')
            pb_name = 'recover_scene_free'
            if cfg_free is False:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 10
                return self.status

            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9 and cfg_free is True:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
            else:
                self.status = 10
        elif self.status == 10:
            self.status += 1
            cfg_item_recover = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item')
            if cfg_item_recover is True or cfg_item_recover is False:
                self.status = 15
                return self.status
            else:
                self.status = 99999
        elif 15 <= self.status < 20:
            self.status += 1
            pb_name = 'recover_scene_item_2'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.8:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 20
                return self.status
            else:
                self.status = 99999
        elif 20 <= self.status < 25:
            self.status += 1
            pb_name = 'recover_scene_item_ok_0'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.8:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 25
                return self.status
            else:
                self.status = 99999
        elif 25 <= self.status < 30:
            self.status += 1
            pb_name = 'recover_scene_item_ok_popup_3'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.8:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 99999
                return self.status
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
            if self.fail_to_detect_m(limit=2) is True:
                pb_name = 'local_map_scene_follow'
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(890, 110, 950, 550)
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                else:
                    self.status = 99999
        elif self.status == 1000:
            self.status += 1
        elif 1001 <= self.status < 1010:
            self.status += 1
            if self.fail_to_detect_m(limit=2) is True:
                pb_name = 'local_map_scene_move'
                self.lyb_mouse_click(pb_name, custom_threshold=0)
        elif 1010 <= self.status < 1500:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.game_object.get_scene('main_scene').set_option('몬스터 조사' + '_move_ok', True)
                self.status = 99999
        elif self.status == 1900:
            self.game_object.get_scene('monghwan_scene').status = 1000
            self.status = 2001
        elif self.status == 2000:
            self.game_object.get_scene('recover_scene').status = 0
            self.game_object.get_scene('monghwan_scene').status = 0
            self.set_option('bug_defense', False)
            self.status += 1
        elif self.status == 2001:
            self.status += 1
            # V4 버그 대응: 일단 무조건 발자국 클릭한다.
            pb_name = 'local_map_scene_follow'
            (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                self.window_image,
                self.game_object.resource_manager.pixel_box_dic[pb_name],
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(890, 110, 950, 550)
            )
            self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.lyb_mouse_click_location(loc_x, loc_y)
        elif 2002 <= self.status < 2020:
            self.status += 1
            if self.fail_to_detect_m(limit=2) is True:
                pb_name = 'local_map_scene_follow'
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(890, 110, 950, 550)
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    if self.get_option('bug_defense'):
                        self.status = 2030
                    else:
                        self.set_option('bug_defense', True)
                        self.set_option('last_follow_location', (loc_x, loc_y))
                        self.set_option('last_status', self.status)
                        self.status = 2025
                else:
                    self.status = 99999
        elif self.status == 2025:
            (loc_x, loc_y) = self.get_option('last_follow_location')
            self.lyb_mouse_click_location(loc_x, loc_y)
            self.status = self.get_option('last_status')
        elif 2030 <= self.status < 2500:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.status = 99999
            else:
                # 전투중 안풀리는 현상 방어 로직
                if self.status % 30 == 0:
                    self.status = 2000
        elif self.status == 3000:
            self.status += 1
        elif 3001 <= self.status < 3300:
            self.status += 1
            pb_name = 'local_map_scene_close_detail'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                return self.status

            rect_list = [
                (650, 280, 690, 330),
                (650, 330, 690, 370),
                (650, 370, 690, 410),
                (650, 410, 690, 450),
                (650, 450, 690, 490),
                (650, 490, 690, 530),
            ]
            list_index = self.game_object.get_scene('main_scene').get_option('몽환의 틈' + '_list_index')
            if self.get_game_config(
                    lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_' + str(list_index)) == '아래에서':
                rect_list.reverse()

            self.logger.info(str(rect_list))
            cfg_number = int(
                self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_' + str(list_index)))

            resource_name = 'local_map_scene_detail_sanyang_loc'
            sanyang_index = 1
            last_location = (-1, -1)
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.7,
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(160, 160, 160),
                    custom_flag=1,
                    average=True
                )
                self.logger.debug(
                    resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    last_location = (loc_x, loc_y)
                    if sanyang_index == cfg_number:
                        self.lyb_mouse_click_location(loc_x, loc_y)
                        self.status = 3500
                        return self.status
                    else:
                        sanyang_index = sanyang_index + 1

            if last_location == (-1. - 1):
                self.logger.warn('발견한 사냥터가 없습니다')
                self.status = 99999
            else:
                self.lyb_mouse_click_location(last_location[0], last_location[1])
                self.status = 3500
        elif self.status == 3500:
            self.status += 1
        elif 3501 <= self.status < 3520:
            self.status += 1
            if self.fail_to_detect_m(limit=2) is True:
                resource_name = 'local_map_scene_detail_auto_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=(820, 310, 950, 570),
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                else:
                    self.lyb_mouse_drag('local_map_scene_detail_drag_bot', 'local_map_scene_detail_drag_top',
                                        stop_delay=0.0)
                    self.set_option('last_status', self.status)
                    self.status = 3700
        elif 3520 <= self.status < 3690:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.game_object.get_scene('main_scene').set_option('몽환의 틈' + '_move_ok', True)
                self.status = 99999
        elif self.status == 3700:
            self.status += 1
        elif self.status == 3701:
            self.status = self.get_option('last_status')
        elif self.status == 4000:
            self.set_option('tobeol_bosang', False)
            self.status += 1
        elif 4001 <= self.status < 4005:
            self.status += 1
            cfg_tobeol_limit = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit')
            if cfg_tobeol_limit:
                resource_name = 'local_map_scene_detail_tobeol_limit_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=(720, 270, 790, 320),
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=True
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.game_object.get_scene('main_scene').set_option('자동 사냥' + '_end_flag', True)
                    self.status = 99999

            if self.get_option('tobeol_bosang') is not True:
                resource_name = 'local_map_scene_detail_new_loc'
                resource = self.game_object.resource_manager.resource_dic[resource_name]
                for each in resource:
                    (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                        self.window_image,
                        self.game_object.resource_manager.pixel_box_dic[each],
                        custom_threshold=0.7,
                        custom_flag=1,
                        custom_top_level=(220, 90, 90),
                        custom_below_level=(130, 40, 40),
                        custom_rect=(640, 120, 950, 380)
                    )
                    self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                    if loc_x != -1:
                        self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                        self.set_option('tobeol_bosang', True)
                        self.status = 4001
                        return self.status

            resource_name = 'local_map_scene_detail_surak_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(820, 120, 920, 380),
                custom_threshold=0.7,
                custom_flag=1,
                average=True
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.lyb_mouse_click_location(loc_x, loc_y)
                self.status = 99999
            else:
                self.set_option('last_status', self.status)
                self.status = 4010
        elif self.status == 4010:
            self.lyb_mouse_drag('local_map_scene_detail_drag_top', 'local_map_scene_detail_drag_bot', stop_delay=0.0)
            self.status += 1
        elif self.status == 4011:
            self.status = self.get_option('last_status')
        elif self.status == 10000:
            self.logger.info('지도의 돋보기를 사용해서 축소시켜주세요.')
            self.logger.info('지도의 특정 위치를 클릭해서 캐릭터를 이동시키기 위함입니다.')
            self.logger.info('지도에 마우스 포인터를 올리고 좌표를 확인하세요.')
            self.logger.info('좌표는 통계 정보 버튼[스케쥴 완료 횟수]에 나옵니다.')
            self.logger.info('통계 정보 버튼은 매크로 홈 화면의 중앙에 있습니다.')
            self.logger.info('주의: 이동할 수 없는 지역인지 반드시 먼저 확인하세요!')
            self.logger.info('[지도 좌표] 작업은 5분 후에 종료됩니다.')
            self.status += 1
        elif 10001 <= self.status < 10300:
            self.status += 1
        elif self.status == 11000:
            self.set_option('changed', False)
            self.status += 1
        elif 11001 <= self.status < 11005:
            self.status += 1
            if self.get_option('changed'):
                self.status = 11010
            else:
                cfg_local_map = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area')
                self.game_object.get_scene('jido_scene').status = 100
                self.game_object.get_scene('jido_scene').set_option('local_map', cfg_local_map)
                self.lyb_mouse_click('local_map_scene_world', custom_threshold=0)
        elif self.status == 11010:
            # 네임드가 먼저 적용되게
            cfg_location = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location')
            cfg_named = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named')
            if cfg_named:
                self.status = 11500
            elif cfg_location:
                self.status = 11100
            else:
                self.game_object.get_scene('main_scene').set_option('지도 이동' + '_skip_auto', True)
                self.status = 11500
        elif 11100 <= self.status < 11110:
            resource_name = 'local_map_scene_zoom_plus_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            max_rate = 0.0
            for pb_name in resource:
                match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
                if max_rate < match_rate:
                    max_rate = match_rate

            if max_rate < 0.95:
                self.lyb_mouse_click('local_map_scene_zoom_plus', custom_threshold=0)
                self.status += 1
            else:
                self.status = 11110
        elif 11110 <= self.status < 11120:
            self.status += 1
            cfg_loc_x = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x'))
            cfg_loc_y = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y'))
            if self.fail_to_detect_m(limit=2) is True:
                self.lyb_mouse_click_location2(cfg_loc_x, cfg_loc_y)
        elif 11120 <= self.status < 11410:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.game_object.get_scene('main_scene').set_option('지도 이동' + '_move_ok', True)
                self.status = 99999
        elif 11500 <= self.status < 11502:
            self.status += 1
            pb_name = 'local_map_scene_close_detail'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                return self.status
        elif 11502 <= self.status < 11506:
            self.lyb_mouse_drag('local_map_scene_detail_drag_bot', 'local_map_scene_detail_drag_top', stop_delay=0.0)
            self.status += 1
        elif self.status == 11506:
            self.status += 1
            cfg_order = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order')
            if cfg_order == '위에서':
                self.status = 11510
            else:
                self.status = 11515
        elif self.status == 11507:
            self.status = self.get_option('last_status')
        elif 11510 <= self.status < 11515:
            self.status += 1
            rect_list = [
                (650, 120, 700, 170),
                (650, 150, 700, 210),
                (650, 190, 700, 250),
                (650, 230, 700, 290),
                (650, 270, 700, 340),
                (650, 320, 700, 380),
                (650, 360, 700, 420),
                (650, 400, 700, 460),
                (650, 440, 700, 500),
                (650, 480, 700, 550),
            ]
            resource_name = 'local_map_scene_detail_sanyang_title_loc'
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.6,
                    custom_top_level=(255, 240, 200),
                    custom_below_level=(120, 120, 100),
                    custom_flag=1,
                    average=False
                )
                self.logger.debug(resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.status = 11515
                    return self.status
            self.set_option('last_status', self.status)
            self.status = 11507
            self.lyb_mouse_drag('local_map_scene_detail_drag_little_top', 'local_map_scene_detail_drag_little_bot',
                                stop_delay=1.0)
        elif 11515 <= self.status < 11519:
            self.status += 1

            rect_list = [
                (650, 120, 690, 170),
                (650, 150, 690, 210),
                (650, 190, 690, 250),
                (650, 230, 690, 290),
                (650, 270, 690, 340),
                (650, 320, 690, 380),
                (650, 360, 690, 420),
                (650, 400, 690, 460),
                (650, 440, 690, 500),
                (650, 480, 690, 550),
            ]
            cfg_order = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order')
            if cfg_order != '위에서':
                rect_list.reverse()
            cfg_sanyang_number = int(
                self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number'))
            if cfg_sanyang_number == 0:
                cfg_sanyang_number = int(10 * random.random()) + 1
            self.logger.info('사냥터 번호: ' + str(cfg_order) + str(cfg_sanyang_number))

            resource_name = 'local_map_scene_detail_sanyang_loc'
            sanyang_index = 1
            last_location = (-1, -1)
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.7,
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(160, 160, 160),
                    custom_flag=1,
                    average=True
                )
                self.logger.debug(
                    resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    last_location = (loc_x, loc_y)
                    if sanyang_index == cfg_sanyang_number:
                        self.lyb_mouse_click_location(loc_x, loc_y)
                        self.status = 11520
                        return self.status
                    else:
                        sanyang_index = sanyang_index + 1

            if last_location == (-1. - 1):
                self.logger.warn('발견한 사냥터가 없습니다')
                self.status = 99999
            else:
                self.lyb_mouse_click_location(last_location[0], last_location[1])
                self.status = 11520
        elif self.status == 11520:
            cfg_named = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named')
            if cfg_named:
                self.status = 11700
            else:
                self.status += 1
        elif 11521 <= self.status < 11540:
            self.status += 1
            if self.fail_to_detect_m(limit=2) is True:
                resource_name = 'local_map_scene_detail_auto_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=(820, 310, 950, 570),
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                else:
                    self.lyb_mouse_drag('local_map_scene_detail_drag_bot', 'local_map_scene_detail_drag_top',
                                        stop_delay=0.0)
                    self.set_option('last_status', self.status)
                    self.status = 11600
        elif self.status == 11540:
            self.status = 11120
        elif self.status == 11600:
            self.status += 1
        elif self.status == 11601:
            self.status = self.get_option('last_status')
        elif self.status == 11700:
            self.status += 1
            self.logger.info("네임드 지도 이동")
        elif 11701 <= self.status < 11703:
            self.status += 1
            self.lyb_mouse_drag('local_map_scene_detail_drag_bot', 'local_map_scene_detail_drag_top', stop_delay=0.0)
        elif 11703 <= self.status < 11715:
            self.status += 1
            resource_name = 'local_map_scene_monster_detail_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.status = 11720
                return self.status

            resource_name = 'local_map_scene_monster_auto_move_single_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.status = 11720
                return self.status

            rect_list = [
                (650, 120, 730, 170),
                (650, 150, 730, 210),
                (650, 190, 730, 250),
                (650, 230, 730, 290),
                (650, 270, 730, 340),
                (650, 320, 730, 380),
                (650, 360, 730, 420),
                (650, 400, 730, 460),
            ]
            resource_name = 'local_map_scene_detail_monster_info_title_loc'
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.6,
                    custom_top_level=(255, 240, 200),
                    custom_below_level=(120, 120, 100),
                    custom_flag=1,
                    average=False
                )
                self.logger.debug(resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y + 30)
                    return self.status
            self.lyb_mouse_drag('local_map_scene_detail_drag_little_top', 'local_map_scene_detail_drag_little_bot',
                                stop_delay=1.0)
        elif 11720 <= self.status < 11725:
            self.status += 1
            pb_name = 'local_map_scene_monster_auto_move'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 11120
                return self.status

            pb_name = 'local_map_scene_monster_auto_move_single'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.lyb_mouse_click(pb_name, custom_threshold=0)
                self.status = 11120
        elif self.status == 12000:
            self.set_option('changed', False)
            self.status += 1
        elif 12001 <= self.status < 12005:
            if self.get_option('changed'):
                self.status = 12010
            else:
                self.game_object.get_scene('jido_scene').status = 200
                self.lyb_mouse_click('local_map_scene_world', custom_threshold=0)
        elif self.status == 12010:
            self.set_option('changed', False)
            self.status += 1
        elif 12011 <= self.status < 12015:
            self.status += 1
            rect_list = [
                (650, 120, 800, 170),
                (650, 150, 800, 210),
                (650, 190, 800, 250),
                (650, 230, 800, 290),
                (650, 270, 800, 340),
                (650, 320, 800, 380),
                (650, 360, 800, 420),
                (650, 400, 800, 460),
                (650, 440, 800, 500),
                (650, 480, 800, 550),
            ]

            resource_name = 'local_map_scene_detail_차원의 경계_loc'
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False,
                )
                self.logger.debug(
                    resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 12015
                    return self.status
        elif self.status == 12015:
            self.status += 1
        elif self.status == 12016:
            cfg_chawon_number = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number'))
            if cfg_chawon_number == 0:
                cfg_chawon_number = int(random.random() * 5) + 1
            pb_name = 'local_map_scene_detail_chawon_' + str(cfg_chawon_number)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.status += 1
        elif 12017 <= self.status < 12030:
            if self.fail_to_detect_m(limit=2) is True:
                pb_name = 'local_map_scene_follow'
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(890, 110, 950, 550)
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    cfg_local_map = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area')
                    self.game_object.get_scene('lunatra_scene').set_option('local_name', cfg_local_map)
                    self.game_object.get_scene('lunatra_scene').status = 100
                    self.status = 12050
                else:
                    self.status = 99999
        elif 12050 <= self.status < 12350:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.status = 99999
        elif self.status == 13000:
            self.set_option('changed', True)
            self.status = 11001
        elif self.status == 20000:
            self.status += 1
        elif 20001 <= self.status < 20005:
            self.status += 1

            rect_list = [
                (650, 120, 690, 170),
                (650, 150, 690, 210),
                (650, 190, 690, 250),
                (650, 230, 690, 290),
                (650, 270, 690, 340),
                (650, 320, 690, 380),
                (650, 360, 690, 420),
                (650, 400, 690, 460),
                (650, 440, 690, 500),
                (650, 480, 690, 550),
            ]

            resource_name = 'local_map_scene_detail_stash_loc'
            last_location = (-1, -1)
            for each in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=each,
                    custom_threshold=0.85,
                    custom_flag=1,
                    average=True
                )
                self.logger.debug(
                    resource_name + ' ' + str(each) + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 20020
                    return self.status
        elif self.status == 20005:
            self.logger.warn('발견한 사냥터가 없습니다')
            self.status = 99999
        elif 20020 <= self.status < 20030:
            self.status += 1
            if self.fail_to_detect_m(limit=2) is True:
                pb_name = 'local_map_scene_follow'
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(890, 110, 950, 550)
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 20100
                else:
                    self.status = 99999
        elif 20100 <= self.status < 20200:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.status = 99999
        elif self.status == 21000:
            self.status += 1
        elif 21001 <= self.status < 21010:
            self.status += 1
            if self.fail_to_detect_m(limit=2) is True:
                pb_name = 'local_map_scene_follow'
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(890, 110, 950, 550)
                )
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 21050
                else:
                    self.status = 99999
        elif 21050 <= self.status < 12350:
            self.status += 1
            if self.fail_to_detect_m() is True:
                self.status = 99999
        else:
            self.game_object.get_scene('jido_scene').status = 99999
            self.game_object.get_scene('local_map_scene').status = 99999
            self.game_object.get_scene('lunatra_jido_scene').status = 99999
            self.game_object.get_scene('deryuk_jido_scene').status = 99999
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
            if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage'):
                pb_name = 'potion_gume_scene_gage_ok'
                match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
                if match_rate < 0.95:
                    self.status = 10
                    return self.status

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
            current_work = self.game_object.get_scene('main_scene').current_work
            if current_work is not None:
                self.logger.warn('물약 상점이 인식됐습니다. 현재 작업[' + str(current_work) + ']을 종료합니다.')
                self.game_object.get_scene('main_scene').set_option(current_work + '_end_flag', True)

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
                self.logger.info(self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion'))
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
            if potion_index > len(potion_list) - 1:
                self.status = 99999
                return self.status

            self.game_object.get_scene('potion_gume_scene').status = 0
            self.game_object.get_scene('potion_gume_scene').set_option('overflow', False)
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
            if potion_index > len(potion_list) - 1:
                self.status = 99999
                return self.status

            if self.game_object.get_scene('potion_gume_scene').get_option('overflow'):
                self.status = 99999
                return self.status

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
                        average=False,
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
                            return self.status
        elif self.status == 110:
            potion_list = self.get_option('potion_list')
            potion_index = self.get_option('potion_index')
            if potion_index >= len(potion_list) - 1:
                self.status = 99999
            else:
                self.status = 1
                self.set_option('potion_index', potion_index + 1)
        elif self.status == 1000:
            self.logger.info('가방 비우러 창고 가기')
            self.status = 99999
        else:
            self.game_object.get_scene('main_scene').set_option('go_stash', True)
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

        resource_name = 'named_tobeol_scene_new_loc'
        resource = self.game_object.resource_manager.resource_dic[resource_name]
        for each in resource:
            (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                self.window_image,
                self.game_object.resource_manager.pixel_box_dic[each],
                custom_threshold=0.7,
                custom_flag=1,
                custom_top_level=(220, 90, 90),
                custom_below_level=(130, 40, 40),
                custom_rect=(470, 460, 950, 550)
            )
            self.logger.debug(each + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.lyb_mouse_click_location(loc_x - 5, loc_y + 5)
                return self.status

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
            self.game_object.get_scene('quest_scene').status = 99999
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def jeoljeon_mode_scene(self):
        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move'):
            resource_name = 'jeoljeon_mode_scene_potion_empty_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(700, 90, 950, 150),
                custom_threshold=0.7,
                custom_flag=1,
                average=True
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.status = 99997

            if self.is_hp_potion_low():
                self.status = 99997

            if self.is_hp_potion_empty():
                self.status = 99997

            if self.status == 99997:
                self.game_object.get_scene('main_scene').set_option('from_jeoljeon_hp_empty', True)
                self.status = 99999

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move'):
            resource_name = 'jeoljeon_mode_scene_gabang_full_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(540, 90, 950, 150),
                custom_threshold=0.7,
                custom_flag=1,
                average=True
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.game_object.get_scene('main_scene').set_option('from_jeoljeon_gabang_full', True)
                self.status = 99999

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move'):
            if self.is_empty_mp_potion_in_jeoljeon():
                self.game_object.get_scene('main_scene').set_option('from_jeoljeon_mp_empty', True)
                self.status = 99999

        if self.game_object.wait_for_start_reserved_work:
            self.logger.info('[작업 예약] 실행 시간 감지됨 > 절전 모드 해제')
            self.status = 99999

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
            self.set_checkpoint('auto_jeoljeon_duration')
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

            elapsed_time = time.time() - self.get_checkpoint('auto_jeoljeon_duration')
            current_work = self.game_object.get_scene('main_scene').current_work
            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration'))
            if current_work == '자동 사냥' and elapsed_time > cfg_duration:
                self.status = 99998
                return self.status

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'))
            if cfg_duration > 0:
                elapsed_time = time.time() - self.game_object.get_scene('main_scene').get_checkpoint('auto_jamjeryeok')
                current_work = self.game_object.get_scene('main_scene').current_work
                if current_work == '자동 사냥' and elapsed_time > cfg_duration:
                    self.status = 99998
                    return self.status

            auto_soul_cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'))
            if auto_soul_cfg_duration > 0:
                elapsed_time = time.time() - self.game_object.get_scene('main_scene').get_checkpoint('auto_soul_duration')
                current_work = self.game_object.get_scene('main_scene').current_work
                if current_work == '자동 사냥' and elapsed_time > auto_soul_cfg_duration:
                    self.status = 99998
                    return self.status

        elif self.status == 500:
            self.game_object.get_scene('main_scene').set_option('go_jeoljeon', 0)
            self.status += 1
        elif 501 <= self.status < 511:
            self.status += 1
            if self.status % 5 == 0:
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
                else:
                    self.status = 99990
        elif self.status == 99990:
            self.game_object.get_scene('main_scene').set_option('go_jeoljeon', 99)
            self.status += 1
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

            resource_name = 'quest_main_scene_limit_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(900, 240, 950, 280),
                custom_threshold=0.9,
                custom_flag=1,
                average=True
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.status = 99999
                self.game_object.get_scene('main_scene').set_option('메인 퀘스트' + '_end_flag', True)
                return self.status

            resource_name = 'quest_main_scene_auto_quest_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_top_level=(255, 255, 255),
                custom_below_level=(100, 100, 100),
                custom_rect=(400, 50, 540, 100),
                custom_threshold=0.8,
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
            self.game_object.get_scene('quest_scene').status = 99999
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
        elif self.status == 210:
            self.game_object.get_scene('main_scene').set_option('네임드 토벌' + '_end_flag', True)
            self.status = 99999
        elif 300 <= self.status < 310:
            if self.status % 5 == 0:
                self.lyb_mouse_click('quest_scene_ure', custom_threshold=0)
                self.game_object.get_scene('ure_scene').status = 0
            self.status += 1
        elif self.status == 310:
            self.game_object.get_scene('main_scene').set_option('의뢰 일지' + '_end_flag', True)
            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    # -menu_scene

    def menu_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 100 <= self.status < 105:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_quest', custom_threshold=0)
                self.game_object.get_scene('quest_scene').status = 100
            self.status += 1
        elif 110 <= self.status < 115:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_gabang', custom_threshold=0)
                self.game_object.get_scene('gabang_scene').status = 0
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
        elif 510 <= self.status < 515:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_upjeok', custom_threshold=0)
                self.game_object.get_scene('upjeok_scene').status = 0
            self.status += 1
        elif 520 <= self.status < 525:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_mail', custom_threshold=0)
                self.game_object.get_scene('mail_scene').status = 0
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
        elif 800 <= self.status < 805:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_monghwan', custom_threshold=0)
                self.game_object.get_scene('monghwan_scene').status = 0
            self.status += 1
        elif 900 <= self.status < 920:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 3000
            self.status += 1
        elif 1000 <= self.status < 1005:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 4000
            self.status += 1
        elif 1100 <= self.status < 1105:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_guild', custom_threshold=0)
                self.game_object.get_scene('guild_scene').status = 0
            self.status += 1
        elif 1200 <= self.status < 1205:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 10000
            self.status += 1
        elif 1210 <= self.status < 1215:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 11000
            self.status += 1
        elif 1220 <= self.status < 1225:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 12000
            self.status += 1
        elif 1230 <= self.status < 1235:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_monghwan', custom_threshold=0)
                self.game_object.get_scene('monghwan_scene').status = 1000
            self.status += 1
        elif 1240 <= self.status < 1245:
            if self.status % 5 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 13000
            self.status += 1
        elif 2000 <= self.status < 2005:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_jeoljeon', custom_threshold=0)
                self.game_object.get_scene('jeoljeon_mode_scene').status = 500
        elif 2100 <= self.status < 2105:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_jido', custom_threshold=0)
                self.game_object.get_scene('local_map_scene').status = 20000
            self.status += 1
        elif 2200 <= self.status < 2205:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_quest', custom_threshold=0)
                self.game_object.get_scene('quest_scene').status = 300
            self.status += 1
        elif 2300 <= self.status < 2305:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_character', custom_threshold=0)
                self.game_object.get_scene('character_scene').status = 0
            self.status += 1
        elif 2400 <= self.status < 2430:
            if self.status % 2 == 0:
                self.lyb_mouse_click('menu_scene_soul', custom_threshold=0)
                self.game_object.get_scene('soul_scene').status = 0
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
            cfg_index = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'character_number')
            self.lyb_mouse_click('character_scene_number_' + str(cfg_index), custom_threshold=0)
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

        if self.status == 0:
            self.set_checkpoint('check_init')
            self.status += 1
        elif 1 <= self.status < 3:
            self.status += 1
            elapsed_time = time.time() - self.get_checkpoint('check_init')
            if elapsed_time > 60:
                self.status = 0
        else:
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

        return self.status

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

        elif self.status == self.get_work_status('의뢰 일지'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=60)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.set_option(self.current_work + '_auto_ok', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            if self.get_option(self.current_work + '_auto_ok') is not True:
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.game_object.get_scene('menu_scene').status = 2200
                self.set_option(self.current_work + '_inner_status', 0)
            else:
                inner_status = self.get_option(self.current_work + '_inner_status')
                if inner_status is None:
                    inner_status = 0

                self.logger.debug('inner_status ' + str(inner_status))
                if inner_status == 0:
                    self.set_option('go_jeoljeon', 0)
                elif inner_status >= 1:
                    if inner_status % 10 == 0:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 110
                        self.game_object.get_scene('gabang_scene').status = 0
                        self.set_option(self.current_work + '_inner_status', inner_status + 1)
                        return True

                    go_jeoljeon = self.get_option('go_jeoljeon')
                    self.logger.debug('go_jeoljeon ' + str(go_jeoljeon))
                    if go_jeoljeon == 5:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 200
                        go_jeoljeon = 0
                    elif go_jeoljeon == 9:
                        go_jeoljeon = 0
                    elif go_jeoljeon == 10:
                        self.set_option(self.current_work + '_auto_ok', False)
                        go_jeoljeon = 0

                    self.set_option('go_jeoljeon', go_jeoljeon + 1)

                self.set_option(self.current_work + '_inner_status', inner_status + 1)

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
                if self.get_option('go_home') is not True:
                    self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                    self.game_object.get_scene('menu_scene').status = 300
                else:
                    self.set_option(self.current_work + '_inner_status', 0)
            else:
                inner_status = self.get_option(self.current_work + '_inner_status')
                if inner_status is None:
                    inner_status = 0

                self.logger.debug('inner_status ' + str(inner_status))
                if 0 <= inner_status < 5:

                    cfg_channel = self.get_game_config(
                        lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel')
                    if cfg_channel != '안함':
                        if inner_status == 0:
                            self.lyb_mouse_click('main_scene_party', custom_threshold=0)
                        elif inner_status == 1:
                            self.lyb_mouse_click('main_scene_map', custom_threshold=0)
                        elif inner_status == 2:
                            self.game_object.get_scene('channel_scene').set_option('resource_name', cfg_channel)
                            self.game_object.get_scene('channel_scene').status = 0
                            self.lyb_mouse_click('main_scene_channel', custom_threshold=0)

                    self.set_option('go_jeoljeon', 0)
                elif 5 <= inner_status < 20:
                    # if self.get_option(self.current_work + '_skip_auto') is not True:
                    if self.get_option('go_home') is not True and self.is_town() is not True:
                        # 자동사냥중인지 체크
                        if self.is_not_auto2():
                            self.lyb_mouse_click('main_scene_auto', custom_threshold=0)

                elif 20 <= inner_status < 150:
                    if inner_status % 10 == 0:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 110
                        self.game_object.get_scene('gabang_scene').status = 0
                        self.set_option(self.current_work + '_inner_status', inner_status + 1)
                        return True

                    go_jeoljeon = self.get_option('go_jeoljeon')
                    if go_jeoljeon == 5:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 400
                        go_jeoljeon = 0
                    elif go_jeoljeon == 10:
                        self.set_option(self.current_work + '_move_ok', False)
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)
                else:
                    self.set_option(self.current_work + '_move_ok', False)

                self.set_option(self.current_work + '_inner_status', inner_status + 1)

        elif self.status == self.get_work_status('몽환의 틈'):

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.set_option(self.current_work + '_ipjang_ok', False)
                self.set_option(self.current_work + '_move_ok', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            if self.get_option(self.current_work + '_ipjang_ok') is not True:
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.game_object.get_scene('menu_scene').status = 800
                self.set_option(self.current_work + '_inner_status', 0)
            else:
                inner_status = self.get_option(self.current_work + '_inner_status')
                if inner_status is None:
                    inner_status = 0

                self.logger.debug('inner_status ' + str(inner_status))

                if inner_status == 0:
                    self.lyb_mouse_click('main_scene_party', custom_threshold=0)
                    self.set_option('go_jeoljeon', 0)
                elif inner_status == 1:
                    self.lyb_mouse_click('main_scene_map', custom_threshold=0)
                elif 2 <= inner_status < 5:
                    pb_name = 'main_scene_timer'
                    match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                    self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
                    if match_rate < 0.7:
                        self.set_option(self.current_work + '_ipjang_ok', False)
                elif 5 <= inner_status < 150:
                    if self.get_option(self.current_work + '_move_ok') is not True:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 900
                    if self.get_option(self.current_work + '_move_ok') is True:
                        if self.get_option('go_home') is not True and self.is_town() is not True:
                            if self.is_not_auto2():
                                self.lyb_mouse_click('main_scene_auto', custom_threshold=0)

                    go_jeoljeon = self.get_option('go_jeoljeon')

                    if self.is_main_quest_complete():
                        self.set_option('go_jeoljeon', 0)
                        return True

                    if self.is_main_quest_new():
                        self.set_option('go_jeoljeon', 0)
                        return True

                    if inner_status % 10 == 0:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 110
                        self.game_object.get_scene('gabang_scene').status = 0
                        self.set_option(self.current_work + '_inner_status', inner_status + 1)
                        return True

                    if go_jeoljeon == 5:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 400
                        go_jeoljeon = 0
                    elif go_jeoljeon == 10:
                        inner_status = 2
                        self.set_option(self.current_work + '_move_ok', False)
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)
                else:
                    inner_status = 2
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

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 110
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

        elif self.status == self.get_work_status('업적'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 510

        elif self.status == self.get_work_status('우편함'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 520

        elif self.status == self.get_work_status('길드'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 1100

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
                    go_jeoljeon = 0

                if self.get_option('go_jeoljeon') == 10:
                    inner_status = 0
                else:
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)
            else:
                inner_status = 0

            self.set_option(self.current_work + '_inner_status', inner_status + 1)

        elif self.status == self.get_work_status('지도 좌표 확인'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 1200

        elif self.status == self.get_work_status('지도 이동'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(3600):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.set_option(self.current_work + '_move_ok', False)
                self.set_option(self.current_work + '_lunatra_ipjang_ok', False)
                self.set_option(self.current_work + '_monghwan_ipjang_ok', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            if self.get_option(self.current_work + '_move_ok') is not True:
                self.set_option(self.current_work + '_skip_auto', False)
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                cfg_world_map = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area')

                if cfg_world_map == '실루나스':
                    self.game_object.get_scene('menu_scene').status = 1210
                elif cfg_world_map == '루나트라':
                    if self.get_option(self.current_work + '_lunatra_ipjang_ok') is not True:
                        self.game_object.get_scene('menu_scene').status = 1220
                    else:
                        self.game_object.get_scene('menu_scene').status = 1210
                elif cfg_world_map == '몽환의 틈':
                    if self.get_option(self.current_work + '_monghwan_ipjang_ok') is not True:
                        self.game_object.get_scene('menu_scene').status = 1230
                    else:
                        self.game_object.get_scene('menu_scene').status = 1240
                elif cfg_world_map == '바트라':
                    # 업데이트 예정
                    self.set_option(self.current_work + '_end_flag', True)

                self.set_option(self.current_work + '_inner_status', 0)
            else:
                inner_status = self.get_option(self.current_work + '_inner_status')
                if inner_status is None:
                    inner_status = 0

                self.logger.debug('inner_status ' + str(inner_status))
                if 0 <= inner_status < 5:
                    cfg_channel = self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel')
                    if cfg_channel != '안함':
                        if inner_status == 0:
                            self.lyb_mouse_click('main_scene_party', custom_threshold=0)
                        elif inner_status == 1:
                            self.lyb_mouse_click('main_scene_map', custom_threshold=0)
                        elif inner_status == 2:
                            self.game_object.get_scene('channel_scene').set_option('resource_name', cfg_channel)
                            self.game_object.get_scene('channel_scene').status = 0
                            self.lyb_mouse_click('main_scene_channel', custom_threshold=0)
                    self.set_option('go_jeoljeon', 0)
                elif 5 <= inner_status < 20:
                    if self.get_option(self.current_work + '_skip_auto') is not True:
                        if self.get_option('go_home') is not True and self.is_town() is not True:
                            # 자동사냥중인지 체크
                            if self.is_not_auto2():
                                self.lyb_mouse_click('main_scene_auto', custom_threshold=0)
                elif 20 <= inner_status < 150:
                    go_jeoljeon = self.get_option('go_jeoljeon')
                    if go_jeoljeon == 5:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 2000
                        go_jeoljeon = 0
                    elif go_jeoljeon == 10:
                        self.set_option(self.current_work + '_move_ok', False)
                    elif go_jeoljeon == 99:
                        self.set_option(self.current_work + '_end_flag', True)
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)
                else:
                    self.set_option(self.current_work + '_move_ok', False)

                self.set_option(self.current_work + '_inner_status', inner_status + 1)

        elif self.status == self.get_work_status('자동 사냥'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=60)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            inner_status = self.get_option(self.current_work + '_inner_status')
            if inner_status is None:
                inner_status = 0

            self.logger.debug('inner_status ' + str(inner_status))
            if inner_status == 0:
                self.set_option('go_jeoljeon', 0)
                self.set_option('go_home', False)
                self.set_option(self.current_work + '_inner_status', inner_status + 1)
            elif inner_status >= 1:
                self.set_option(self.current_work + '_inner_status', inner_status + 1)
                cfg_auto_jamjeryeok = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'))
                if cfg_auto_jamjeryeok > 0:
                    jamjeryeok_elapsed_time = time.time() - self.get_checkpoint('auto_jamjeryeok')
                    if jamjeryeok_elapsed_time > cfg_auto_jamjeryeok:
                        self.set_checkpoint('auto_jamjeryeok')
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 110
                        self.game_object.get_scene('gabang_scene').status = 0
                        return True

                cfg_auto_soul = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'))
                if cfg_auto_soul > 0:
                    soul_elapsed_time = time.time() - self.get_checkpoint('auto_soul_duration')
                    if soul_elapsed_time > cfg_auto_soul:
                        self.set_checkpoint('auto_soul_duration')
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 2400
                        self.game_object.get_scene('soul_scene').status = 0
                        return True

                cfg_auto_jeoljeon = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon'))
                if cfg_auto_jeoljeon:
                    go_jeoljeon = self.get_option('go_jeoljeon')
                    self.logger.debug('go_jeoljeon ' + str(go_jeoljeon))
                    if go_jeoljeon == 5:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 400
                        self.set_option('go_jeoljeon', 0)
                        return self.status
                    elif go_jeoljeon == 9:
                        self.set_option('go_jeoljeon', 0)
                    elif go_jeoljeon == 10:
                        if self.get_option('go_home') is not True and self.is_town() is not True:
                            # 자동사냥중인지 체크
                            if self.is_not_auto2():
                                self.lyb_mouse_click('main_scene_auto', custom_threshold=0)
                        self.set_option('go_jeoljeon', 0)
                        return self.status
                    self.set_option('go_jeoljeon', go_jeoljeon + 1)

                if self.get_option('go_home') is not True and self.is_town() is not True:
                    if self.is_not_auto2():
                        self.lyb_mouse_click('main_scene_auto', custom_threshold=0)
                        return self.status

                if self.is_town():
                    self.logger.info('마을 인식됨 -> [자동 사냥] 작업 종료')
                    self.set_option(self.current_work + '_end_flag', True)
                    return self.status

        elif self.status == self.get_work_status('캐릭터 선택'):
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(10):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
            self.game_object.get_scene('menu_scene').status = 2300

        elif self.status == self.get_work_status('마을 이동'):
            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=60)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            inner_status = self.get_option(self.current_work + '_inner_status')
            if inner_status is None:
                inner_status = 0

            self.logger.debug('inner_status ' + str(inner_status))
            if inner_status % 5 == 0:
                is_clicked = self.click_resource('main_scene_menu_home_loc')
                if is_clicked is not True:
                    self.set_option(self.current_work + '_end_flag', True)
                else:
                    self.game_object.get_scene('go_home_scene').status = 100

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
                self.set_option(self.current_work + '_end_flag', True)

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

        if self.get_option('is_moving'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash') or self.get_option('go_stash_for_full'):
            if self.get_option('go_stash'):
                self.logger.info('물약 상점 인식됨 -> 창고 탐색 시작.')
                self.set_option('go_stash', False)
                self.set_option('go_stash_for_full', False)
                self.game_object.get_scene('stash_scene').status = 0
                self.game_object.get_scene('menu_scene').status = 2100
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move') is True:
            elapsed_time = time.time() - self.get_checkpoint('gabang_full_move')
            if elapsed_time > self.period_bot(5):
                self.set_checkpoint('gabang_full_move')
                if self.is_gabang_full() or self.get_option('gabang_full') or self.get_option(
                        'from_jeoljeon_gabang_full'):
                    self.set_option('go_jeoljeon', 0)
                    self.set_option('from_jeoljeon_gabang_full', False)
                    if self.click_potion_menu():
                        self.game_object.get_scene('move_potion_npc_scene').status = 100
                        self.game_object.get_scene('potion_npc_scene').status = 1000
                        self.set_option('go_stash_for_full', True)
                        self.set_option('gabang_full', False)
                        self.set_option('go_home', False)
                        return True
                    else:
                        if self.get_option('go_home') is not True:
                            self.click_resource('main_scene_menu_home_loc')
                            self.game_object.get_scene('go_home_scene').status = 100
                            self.set_option('gabang_full', True)
                            self.set_option('go_home', True)
                        return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move') is True:
            elapsed_time = time.time() - self.get_checkpoint('hp_potion_low')
            if elapsed_time > self.period_bot(3):
                self.set_checkpoint('hp_potion_low')
                if self.is_hp_potion_low() or self.get_option('hp_potion_low') or self.get_option('from_jeoljeon_hp_empty'):
                    self.set_option('go_jeoljeon', 0)
                    self.set_option('from_jeoljeon_hp_empty', False)
                    if self.click_potion_menu():
                        self.game_object.get_scene('move_potion_npc_scene').status = 100
                        self.game_object.get_scene('potion_npc_scene').status = 0
                        self.game_object.get_scene('potion_npc_scene').set_option('potion', 'hp')
                        self.set_option('hp_potion_low', False)
                        self.set_option('go_home', False)
                        return True
                    else:
                        if self.get_option('go_home') is not True:
                            self.click_resource('main_scene_menu_home_loc')
                            self.game_object.get_scene('go_home_scene').status = 100
                            self.set_option('hp_potion_low', True)
                            self.set_option('go_home', True)
                        return True

            elapsed_time = time.time() - self.get_checkpoint('hp_potion_empty')
            if elapsed_time > self.period_bot(3):
                self.set_checkpoint('hp_potion_empty')
                if self.is_hp_potion_empty() or self.get_option('hp_potion_empty') or self.get_option(
                        'from_jeoljeon_hp_empty'):
                    self.set_option('go_jeoljeon', 0)
                    self.set_option('from_jeoljeon_hp_empty', False)
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
            elapsed_time = time.time() - self.get_checkpoint('mp_potion_move')
            if elapsed_time > self.period_bot(5):
                self.set_checkpoint('mp_potion_move')
                if self.is_mp_potion_empty() or self.get_option('mp_potion_empty') or self.get_option(
                        'from_jeoljeon_mp_empty'):
                    self.set_option('go_jeoljeon', 0)
                    self.set_option('from_jeoljeon_mp_empty', False)
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
            elapsed_time = time.time() - self.get_checkpoint('recover_move')
            if elapsed_time > self.period_bot(30) and self.click_recover_menu():
                self.game_object.get_scene('local_map_scene').status = 100
                self.set_checkpoint('recover_move')
                self.game_object.interval = self.period_bot(5)
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

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite') is True:
            if self.click_party_accept():
                return True
        else:
            if self.click_party_decline():
                return True

        if self.is_main_quest_complete():
            self.set_option('go_jeoljeon', 0)
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol'):
            cfg_tobeol_period = int(self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period'))
            if cfg_tobeol_period < 60:
                cfg_tobeol_period = 60
            elapsed_time = time.time() - self.get_checkpoint('quest_tobeol')
            if elapsed_time > self.period_bot(81640):
                self.set_checkpoint('quest_tobeol')
            elif elapsed_time > cfg_tobeol_period:
                if self.is_new_tobeol_quest():
                    self.set_checkpoint('quest_tobeol')
                else:
                    self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                    self.game_object.get_scene('menu_scene').status = 1000
                    self.set_checkpoint('quest_tobeol')
                self.set_option('go_jeoljeon', 0)
                return True

        # 일일 체크리스트
        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check') is True:
            elapsed_time = time.time() - self.get_checkpoint('chulseok_check')
            if elapsed_time > self.period_bot(81640):
                self.set_checkpoint('chulseok_check')
            elif elapsed_time > self.period_bot(600):
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.game_object.get_scene('menu_scene').status = 700
                self.set_checkpoint('chulseok_check', time.time() + self.period_bot(36000))
                return True

        # 상점 체크리스트
        if self.is_checked_shop():
            elapsed_time = time.time() - self.get_checkpoint('shop_check')
            if elapsed_time > self.period_bot(81640):
                self.set_checkpoint('shop_check')
            elif elapsed_time > self.period_bot(60):
                self.lyb_mouse_click('main_scene_shop', custom_threshold=0)
                self.game_object.get_scene('shop_scene').status = 0
                self.set_checkpoint('shop_check', time.time() + self.period_bot(36000))
                return True
        # TODO 아이템 복구 옵션 활성화 & 자동장착 활성화시 300초마다 아이템 자동장착
        cfg_recover_item = self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item')
        # TODO 아이템 복구 옵션 강제 활성화
        if cfg_recover_item is True:
            elapsed_time = time.time() - self.get_checkpoint('recover_item')
            if elapsed_time > self.period_bot(30):
                self.set_checkpoint('recover_item')
                resource_name = 'event_scene_newitem_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    # custom_top_level=(255, 255, 255),
                    # custom_below_level=(150, 150, 150),
                    custom_rect=(828, 36, 947, 53),
                    custom_threshold=0.6,
                    custom_flag=1,
                    average=True
                )
                self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                        self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                        self.game_object.get_scene('menu_scene').status = 110
                        self.game_object.get_scene('gabang_scene').set_option('equip', True)
                        self.game_object.get_scene('gabang_scene').status = 0
                        self.set_option('go_jeoljeon', 0)
                        # self.game_object.interval = self.period_bot(5)
                        return True

        return False

    def process_main_quest(self):

        if self.is_main_quest_new():
            self.set_option('go_jeoljeon', 0)
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol') is True:
            if self.get_elapsed_time() > self.period_bot(60):
                elapsed_time = time.time() - self.get_checkpoint(self.current_work + '_tobeol_check')
                if elapsed_time > self.period_bot(120):
                    self.set_checkpoint(self.current_work + '_tobeol_check')
                    self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                    self.game_object.get_scene('menu_scene').status = 1000
                    self.set_option('go_jeoljeon', 0)
                    return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip') is True:
            if self.get_elapsed_time() > self.period_bot(60):
                elapsed_time = time.time() - self.get_checkpoint(self.current_work + '_main_quest_equip')
                if elapsed_time > self.period_bot(300):
                    self.set_checkpoint(self.current_work + '_main_quest_equip')
                    self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                    self.game_object.get_scene('menu_scene').status = 110
                    self.game_object.get_scene('gabang_scene').set_option('equip', True)
                    self.game_object.get_scene('gabang_scene').status = 0
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
                                          custom_threshold=0.4,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_hp_potion_low(self, limit_count=5):
        resource_name = 'hp_potion_count_loc'
        resource = self.game_object.resource_manager.resource_dic[resource_name]
        custom_threshold = 0.7
        reverse = True
        log_message = 'HP 물약 부족 감지'
        match_rate = 0.00

        for pb_name in resource:
            rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            # self.logger.debug(pb_name + ' ' + str(round(rate, 2)))
            if match_rate < rate:
                match_rate = rate

        if match_rate > custom_threshold and reverse is not True:
            self.set_option(resource_name + 'check_count', 0)
            return False

        if match_rate < custom_threshold and reverse is True:
            self.set_option(resource_name + 'check_count', 0)
            return False

        self.game_object.get_scene('main_scene').set_option('go_jeoljeon', 0)

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

    def is_mp_potion_empty(self, limit=3):
        return self.is_status_by_resource('MP 물약 없음 감지', 'main_scene_mp_potion_ok_loc',
                                          custom_top_level=(255, 255, 255),
                                          custom_below_level=(150, 150, 150),
                                          custom_rect=(690, 520, 745, 560),
                                          custom_threshold=0.4,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_not_auto(self, limit=5):
        return self.is_status_by_resource('자동 전투 꺼짐 감지', 'auto_loc',
                                          custom_top_level=(230, 230, 230),
                                          custom_below_level=(185, 180, 170),
                                          custom_rect=(900, 280, 960, 340),
                                          custom_threshold=0.5,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_not_auto2(self, limit=5):
        return self.is_status_by_resource('자동 전투 꺼짐 감지', 'auto2_loc',
                                          custom_top_level=-1,
                                          custom_below_level=-1,
                                          custom_rect=(430, 420, 550, 460),
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

    def fail_to_detect_m(self, limit=10):
        return self.is_status_by_resource('거리 감지 실패', 'local_map_scene_m_loc',
                                          custom_top_level=-1,
                                          custom_below_level=-1,
                                          custom_rect=(470, 60, 550, 100),
                                          custom_threshold=0.8,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_town(self):
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

    def click_party_accept(self):
        resource_name = 'party_accept_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_rect=(20, 170, 310, 250),
            custom_threshold=0.7,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def click_party_decline(self):
        resource_name = 'party_decline_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_rect=(20, 170, 310, 250),
            custom_threshold=0.7,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def click_shop_resource(self, resource_name):
        rect_list = [
            (150, 120, 375, 345),
            (380, 120, 600, 345),
            (600, 120, 820, 345),
            (150, 345, 375, 560),
            (380, 345, 600, 560),
            (600, 345, 820, 560),
            (290, 120, 510, 345),
            (510, 120, 730, 345),
            (730, 120, 950, 345),
            (290, 345, 510, 560),
            (510, 345, 730, 560),
            (730, 345, 950, 560),
        ]
        for each in rect_list:
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=each,
                custom_threshold=0.8,
                custom_flag=1,
                average=False
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.lyb_mouse_click_location(loc_x, loc_y + 50)
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

    def is_empty_mp_potion_in_jeoljeon(self, limit=3):
        return self.is_status_by_resource('MP 물약 없음 감지', 'jeoljeon_mode_scene_mp_potion_ok_loc',
                                          custom_top_level=(255, 255, 255),
                                          custom_below_level=(150, 150, 150),
                                          custom_rect=(695, 515, 750, 565),
                                          custom_threshold=0.6,
                                          limit_count=limit,
                                          reverse=False,
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

    def is_gabang_full(self, limit=3):
        return self.is_status_by_resource('가방 풀 감지', 'main_scene_gabang_full_loc',
                                          custom_top_level=(255, 30, 30),
                                          custom_below_level=(180, 0, 0),
                                          custom_rect=(790, 30, 860, 80),
                                          custom_threshold=0.6,
                                          limit_count=limit,
                                          reverse=True,
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
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def is_new_tobeol_quest(self):
        resource_name = 'main_scene_quest_tobeol_new_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_rect=(750, 140, 940, 300),
            custom_threshold=0.85,
            custom_flag=1,
            average=True
        )
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True

        return False

    def is_checked_shop(self):
        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha'):
            return True

        if self.get_game_config(lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha'):
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
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1 and reverse is not True:
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

    def is_status_by_resource2(self, log_message, resource_name, custom_threshold, custom_top_level=-1,
                               custom_below_level=-1, limit_count=-1, reverse=False):
        match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name,
                                                          custom_top_level=custom_top_level,
                                                          custom_below_level=custom_below_level)
        self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
        if match_rate > custom_threshold and reverse is not True:
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
