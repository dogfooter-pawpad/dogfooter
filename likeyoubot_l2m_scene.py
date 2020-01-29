import traceback
import likeyoubot_l2m as lybgamel2m
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_scene
import time
import random


class LYBL2MScene(likeyoubot_scene.LYBScene):
    def __init__(self, scene_name):
        likeyoubot_scene.LYBScene.__init__(self, scene_name)

    def process(self, window_image, window_pixels):

        super(LYBL2MScene, self).process(window_image, window_pixels)

        if self.scene_name == 'login_scene':
            rc = self.login_scene()
        elif self.scene_name == 'main_scene':
            rc = self.main_scene()
        elif self.scene_name == 'quick_config_scene':
            rc = self.quick_config_scene()
        elif self.scene_name == 'jeoljeon_mode_scene':
            rc = self.jeoljeon_mode_scene()
        elif self.scene_name == 'potion_npc_scene':
            rc = self.potion_npc_scene()
        elif self.scene_name == 'item_buy_scene':
            rc = self.item_buy_scene()
        elif self.scene_name == 'jido_scene':
            rc = self.jido_scene()
        elif self.scene_name == 'mail_scene':
            rc = self.mail_scene()
        elif self.scene_name == 'recover_scene':
            rc = self.recover_scene()
        elif self.scene_name == 'not_enough_gem_scene':
            rc = self.not_enough_gem_scene()
        elif self.scene_name == 'daily_scene':
            rc = self.daily_scene()
        elif self.scene_name == 'quest_scene':
            rc = self.quest_scene()
        elif self.scene_name == 'sell_npc_scene':
            rc = self.sell_npc_scene()
        elif self.scene_name == 'stash_scene':
            rc = self.stash_scene()


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

    def stash_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.game_object.get_scene('main_scene').set_option('npc_ok', True)
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click('stash_scene_auto', custom_threshold=0)
            self.status += 1
        elif self.status == 2:
            self.game_object.get_scene('item_buy_scene').status = 100
            self.lyb_mouse_click('stash_scene_ok', custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def sell_npc_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.game_object.get_scene('main_scene').set_option('npc_ok', True)
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click('sell_npc_scene_auto', custom_threshold=0)
            self.status += 1
        elif self.status == 2:
            self.game_object.get_scene('item_buy_scene').status = 100
            self.lyb_mouse_click('sell_npc_scene_ok', custom_threshold=0)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def quest_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def daily_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.game_object.get_scene('main_scene').set_option('daily_check_ok', True)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            pb_name = 'daily_scene_new'
            (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                self.window_image,
                self.game_object.resource_manager.pixel_box_dic[pb_name],
                custom_top_level=(255, 50, 50),
                custom_below_level=(150, 0, 0),
                custom_rect=(760, 70, 800, 500),
                custom_threshold=0.7,
                custom_flag=1,
            )
            # self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.lyb_mouse_click_location(loc_x, loc_y)
                self.set_option('last_status', self.status)
                self.status = 100
                return self.status

            self.status = 99999
        elif 100 <= self.status < 110:
            self.status += 1
            rect_list = [
                (530, 230, 680, 300),
                (530, 400, 680, 470),
            ]
            resource_name = 'daily_scene_receive_loc'
            for rect in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_top_level=(255, 255, 255),
                    custom_below_level=(155, 155, 155),
                    custom_rect=rect,
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False
                )
                # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    return self.status

            self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def not_enough_gem_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.game_object.get_scene('recover_scene').set_option('option_gem', True)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def recover_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('option_gem', False)
            self.status += 1
        elif 1 <= self.status < 110:
            self.status += 1

            resource_name = 'recover_scene_free_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(430, 230, 480, 270),
                custom_threshold=0.85,
                custom_flag=1,
                average=False
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.logger.info('무료 복구 인식됨: 확인')
                self.lyb_mouse_click('recover_scene_ok', custom_threshold=0)
                return self.status

            pb_name = 'recover_scene_gold'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.logger.info('골드 복구 인식됨: 확인')
                self.lyb_mouse_click('recover_scene_ok', custom_threshold=0)
                return self.status

            pb_name = 'recover_scene_gem'
            match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.set_option('option_gem', True)
                self.logger.info('다이아 복구 인식됨: 취소')
                self.status = 99999
                return self.status
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def mail_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
            self.game_object.get_scene('main_scene').set_option('mail_check_ok', True)
        elif self.status == 1:
            self.lyb_mouse_click('mail_scene_all', custom_threshold=0)
            self.status += 1
        # elif 1 <= self.status < 10:
        #     self.status += 1
        #     pb_name = 'mail_scene_empty_2'
        #     match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
        #     self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
        #     if match_rate > 0.9:
        #         self.status = 10
        #         return self.status
        #
        #     if self.status % 2 == 1:
        #         self.lyb_mouse_click('mail_scene_receive_2', custom_threshold=0)
        # elif 10 <= self.status < 20:
        #     self.status += 1
        #     pb_name = 'mail_scene_empty'
        #     match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
        #     self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
        #     if match_rate > 0.9:
        #         self.status = 99999
        #         return self.status
        #
        #     if self.status % 2 == 1:
        #         self.lyb_mouse_click('mail_scene_receive', custom_threshold=0)
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def jido_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('aden_clicked', False)
            self.status += 1
        elif 1 <= self.status < 20:
            self.status += 1
            if self.get_option('aden_clicked') is not True:
                resource_name = 'jido_scene_aden_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=(40, 80, 100, 120),
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False
                )
                # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.set_option('aden_clicked', True)
                    return self.status

            cfg_area = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area')
            if cfg_area == '즐겨찾기':
                self.logger.info('즐겨찾기')
                self.lyb_mouse_click('jido_scene_bookmark', custom_threshold=0)
                self.status = 300
            else:
                self.logger.info('지역: ' + str(cfg_area))

                rect_list = [
                    (20, 130, 100, 200),
                    (20, 180, 100, 250),
                    (20, 230, 100, 300),
                    (20, 280, 100, 350),
                    (20, 330, 100, 400),
                    (20, 380, 100, 450),
                ]
                resource_name = 'jido_scene_area_' + str(cfg_area) + '_loc'
                for rect in rect_list:
                    (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                        self.window_image,
                        resource_name,
                        custom_rect=rect,
                        custom_threshold=0.7,
                        custom_flag=1,
                        average=False
                    )
                    # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                    if loc_x != -1:
                        self.status = 100
                        return self.status
                self.set_option('last_status', self.status)
                self.status = 30
        elif self.status == 30:
            self.lyb_mouse_drag('jido_scene_drag_bot', 'jido_scene_drag_top')
            self.status += 1
        elif self.status == 31:
            self.status += 1
        elif self.status == 32:
            self.status += 1
            self.status = self.get_option('last_status')
        elif self.status == 100:
            self.status += 1
        elif 101 <= self.status < 130:
            self.status += 1
            cfg_sub_area = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area')
            self.logger.info('서브 지역: ' + str(cfg_sub_area))
            rect_list = [
                (40, 130, 180, 190),
                (40, 170, 180, 230),
                (40, 210, 180, 270),
                (40, 250, 180, 310),
                (40, 290, 180, 350),
                (40, 330, 180, 390),
                (40, 370, 180, 430),
                (40, 410, 180, 470),
            ]
            resource_name = 'jido_scene_sub_area_' + str(cfg_sub_area) + '_loc'
            for rect in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=rect,
                    custom_threshold=0.8,
                    custom_flag=1,
                    average=False,
                    # debug=True,
                )
                # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 200
                    return self.status
            self.set_option('last_status', self.status)
            self.status = 30
        elif self.status == 200:
            self.status += 1
        elif self.status == 201:
            self.game_object.get_scene('main_scene').set_option('jido_move_ok', True)
            cfg_style = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style')
            elapsed_time = time.time() - self.get_checkpoint('teleport')
            if cfg_style == '자동 이동' or elapsed_time < self.period_bot(600):
                self.lyb_mouse_click('jido_scene_auto_move', custom_threshold=0)
            else:
                self.lyb_mouse_click('jido_scene_teleport', custom_threshold=0)
                self.set_checkpoint('teleport')
            self.status += 1
        elif self.status == 300:
            self.status += 1
        elif self.status == 301:
            cfg_sub_area = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area')
            pb_name = 'jido_scene_bookmark_list_' + str(cfg_sub_area)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.status = 200
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def item_buy_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.status += 1
            self.lyb_mouse_click('item_buy_scene_ok', custom_threshold=0)
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def potion_npc_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.game_object.get_scene('main_scene').set_option('npc_ok', True)
            cfg_auto = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto')
            if cfg_auto:
                self.status = 1000
            else:
                cfg_select_count = int(
                    self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'))
                if cfg_select_count == 0:
                    self.status = 99999
                else:
                    self.status = 1002
            # self.game_object.get_scene('main_scene').set_option('item_check', True)

            # for item_name in lybgamel2m.LYBL2M.item_list:
            #     self.set_option(item_name, False)
            # self.status = 99999
        elif self.status == 1:
            self.set_option('drag_pos', 0)
            self.game_object.get_scene('main_scene').set_option('npc_ok', True)
            self.set_option('item_index', 0)
            self.status += 1
        elif self.status == 2:
            item_index = self.get_option('item_index')
            for i in range(item_index, len(lybgamel2m.LYBL2M.default_item_list)):
                cfg_item = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(i))
                cfg_select_count = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(i)))
                if cfg_select_count > 0 and self.get_option(cfg_item):
                    break
                else:
                    item_index += 1

            if item_index >= len(lybgamel2m.LYBL2M.default_item_list):
                self.status = 99999
                return self.status

            self.set_option('item_index', item_index)
            self.status = 30
        elif 10 <= self.status < 15:
            self.status += 1
            self.lyb_mouse_drag('potion_npc_scene_drag_bot', 'potion_npc_scene_drag_top')
        elif self.status == 15:
            self.status = 30
        elif 20 <= self.status < 25:
            self.status += 1
            self.lyb_mouse_drag('potion_npc_scene_drag_top', 'potion_npc_scene_drag_bot')
        elif self.status == 25:
            self.status = 30
        elif self.status == 30:
            self.status += 1
        elif 31 <= self.status < 50:
            self.status += 1
            item_index = self.get_option('item_index')

            cfg_item = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(item_index))
            rect_list = [
                (70, 140, 120, 210),
                (70, 180, 120, 260),
                (70, 230, 120, 310),
                (70, 290, 120, 350),
                (70, 340, 120, 400),
            ]
            resource_name = 'potion_npc_scene_' + str(cfg_item) + '_loc'
            for rect in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=rect,
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False
                )
                # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 100
                    return self.status
            if self.status % 2 == 0:
                drag_pos = self.get_option('drag_pos')
                if drag_pos == 5:
                    drag_pos = 20
                elif drag_pos == 15:
                    drag_pos = 0

                if drag_pos < 10:
                    self.lyb_mouse_drag('potion_npc_scene_drag_bot', 'potion_npc_scene_drag_top')
                    self.set_option('drag_pos', drag_pos + 1)
                else:
                    self.lyb_mouse_drag('potion_npc_scene_drag_top', 'potion_npc_scene_drag_bot')
                    self.set_option('drag_pos', drag_pos - 1)
        elif self.status == 100:
            self.set_option('click_count', 0)
            self.status += 1
        elif 101 <= self.status < 120:
            self.status += 1
            item_index = self.get_option('item_index')
            click_count = self.get_option('click_count')
            cfg_select_count = int(
                self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(item_index)))
            if click_count >= cfg_select_count:
                self.status = 200
                return self.status

            self.set_option('click_count', click_count + 1)
            cfg_select = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_' + str(item_index))
            pb_name = 'potion_npc_scene_select_' + str(cfg_select)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
        elif self.status == 200:
            self.status += 1
        elif self.status == 201:
            self.status = 300
            self.game_object.get_scene('item_buy_scene').status = 100
            self.lyb_mouse_click('potion_npc_scene_buy', custom_threshold=0)
        elif self.status == 300:
            item_index = self.get_option('item_index')
            self.set_option('item_index', item_index + 1)
            self.status = 2
        elif self.status == 1000:
            self.status += 1
        elif self.status == 1001:
            self.lyb_mouse_click('potion_npc_scene_auto', custom_threshold=0)
            self.status += 1
        elif self.status == 1002:
            cfg_select_count = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'))
            if cfg_select_count == 0:
                self.status = 1200
                return self.status

            cfg_auto_last = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last')
            if '화살' in cfg_auto_last:
                self.status = 1010
            else:
                self.status = 1015
        elif 1010 <= self.status < 1015:
            self.status += 1
            self.lyb_mouse_drag('potion_npc_scene_drag_bot', 'potion_npc_scene_drag_top')
        elif self.status == 1015:
            self.status += 1
        elif 1016 <= self.status < 1030:
            self.status += 1

            cfg_item = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last')
            rect_list = [
                (70, 140, 120, 210),
                (70, 180, 120, 260),
                (70, 230, 120, 310),
                (70, 290, 120, 350),
                (70, 340, 120, 400),
            ]
            resource_name = 'potion_npc_scene_' + str(cfg_item) + '_loc'
            for rect in rect_list:
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=rect,
                    custom_threshold=0.7,
                    custom_flag=1,
                    average=False
                )
                # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.status = 1100
                    return self.status
        elif self.status == 1100:
            self.set_option('click_count', 0)
            self.status += 1
        elif 1101 <= self.status < 1120:
            self.status += 1
            click_count = self.get_option('click_count')
            cfg_select_count = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'))
            if click_count >= cfg_select_count:
                self.status = 1200
                return self.status

            self.set_option('click_count', click_count + 1)
            cfg_select = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select')
            pb_name = 'potion_npc_scene_select_' + str(cfg_select)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
        elif self.status == 1200:
            self.status += 1
        elif self.status == 1201:
            self.game_object.get_scene('item_buy_scene').status = 100
            self.lyb_mouse_click('potion_npc_scene_buy', custom_threshold=0)
            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)

            self.status = 0

        return self.status

    def jeoljeon_mode_scene(self):

        if self.status == 0:
            self.set_checkpoint('start')
            self.logger.info('scene: ' + self.scene_name)
            if self.get_option('check_auto'):
                self.set_option('check_auto', False)
                self.logger.info('[자동 전투 중] 체크')
                self.status = 2995
            else:
                self.status += 1
        elif 1 <= self.status < 3000:
            self.status += 1

            resource_name = 'jeoljeon_mode_scene_death_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_rect=(320, 320, 480, 360),
                custom_threshold=0.85,
                custom_flag=1,
                average=True
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.logger.info('절전 모드 사망 감지. 귀환서 클릭합니다.')
                self.game_object.get_scene('main_scene').set_option('is_home', True)
                self.lyb_mouse_click('jeoljeon_mode_scene_home', custom_threshold=0)
                png_name = self.game_object.save_image('절전모드 사망')
                self.game_object.telegram_send('', image=png_name)
                self.status = 99999
                return self.status

            for home in lybgamel2m.LYBL2M.home_list:
                resource_name = 'jeoljeon_mode_scene_area_' + str(home) + '_loc'
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_rect=(40, 70, 200, 140),
                    custom_threshold=0.85,
                    custom_flag=1,
                    average=False,
                    # debug=True,
                )
                # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                if loc_x != -1:
                    self.logger.info('안전 지대 인식됨: ' + str(home))
                    self.set_option('hp_200_message', False)
                    self.set_option('hp_100_message', False)
                    self.set_option('hp_10_message', False)
                    self.game_object.get_scene('main_scene').set_option('is_home', True)
                    self.status = 99999
                    return self.status

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration'))
            elapsed_time = time.time() - self.get_checkpoint('start')
            if elapsed_time > cfg_duration:
                self.status = 99999
                return self.status

            if self.is_not_auto_jeoljeon_mode():
                self.game_object.get_scene('main_scene').set_option('click_auto', True)
                self.status = 99999
                return self.status

            cfg_go_home_potion = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion')
            cfg_notify_potion = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion')
            cfg_notify_potion_message = str(
                self.get_game_config(lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message'))

            if len(cfg_notify_potion_message) == 0:
                cfg_notify_potion_message = ''

            max_number = 9999
            max_rate = 0.0
            # for i in range(10, 101, 10):
            #     pb_name = 'jeoljeon_mode_scene_hp_' + str(i)
            #     match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            #     self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            #     if match_rate > max_rate:
            #         max_rate = match_rate
            #         max_number = i

            # pb_name = 'jeoljeon_mode_scene_hp_low'
            # match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            # if match_rate > max_rate:
            #     max_rate = match_rate
            #     max_number = 0

            # pb_name = 'jeoljeon_mode_scene_hp_empty'
            # match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
            # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
            # if match_rate > max_rate:
            #     max_rate = match_rate
            #     max_number = -1

            resource_name = 'jeoljeon_mode_scene_hp_empty_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.9,
                custom_flag=1,
                custom_rect=(200, 400, 450, 460),
                average=True
            )
            # self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                max_rate = match_rate
                max_number = -1

            resource_name = 'jeoljeon_mode_scene_arrow_empty_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.85,
                custom_flag=1,
                custom_rect=(600, 270, 720, 380),
                average=True
            )
            # self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                max_rate = match_rate
                max_number = -2

            if max_rate > 0.85:
                if max_number == -1:
                    self.logger.info('물약 없음 감지됨')
                    if cfg_go_home_potion:
                        self.logger.info('귀환서 클릭합니다.')
                        self.game_object.get_scene('main_scene').set_option('is_home', True)
                        self.lyb_mouse_click('jeoljeon_mode_scene_home', custom_threshold=0)
                        if cfg_notify_potion:
                            self.game_object.telegram_send('HP 물약이 없습니다.' + cfg_notify_potion_message)
                elif max_number == -2:
                    self.logger.info('화살 없음 감지됨')
                    if cfg_go_home_potion:
                        self.logger.info('귀환서 클릭합니다.')
                        self.game_object.get_scene('main_scene').set_option('is_home', True)
                        self.lyb_mouse_click('jeoljeon_mode_scene_home', custom_threshold=0)
                # elif max_number == 0:
                #     self.logger.info('물약 10개 이하 감지됨')
                #     if cfg_go_home_potion:
                #         self.logger.info('귀환서 클릭합니다.')
                #         self.game_object.get_scene('main_scene').set_option('is_home', True)
                #         self.lyb_mouse_click('jeoljeon_mode_scene_home', custom_threshold=0)
                #     if self.get_option('hp_10_message') is not True:
                #         self.set_option('hp_10_message', True)
                #         if cfg_notify_potion:
                #             self.game_object.telegram_send('HP 물약이 10개 이하입니다. ' + cfg_notify_potion_message)
                # elif max_number == 100:
                #     if self.get_option('hp_200_message') is not True:
                #         self.logger.info('물약 200개 이하 감지됨')
                #         self.set_option('hp_200_message', True)
                #         if cfg_notify_potion:
                #             self.game_object.telegram_send('HP 물약이 200개 이하입니다. ' + cfg_notify_potion_message)
                # else:
                #     if cfg_go_home_potion >= 100:
                #         self.logger.info('귀환서 클릭합니다.')
                #         self.game_object.get_scene('main_scene').set_option('is_home', True)
                #         self.lyb_mouse_click('jeoljeon_mode_scene_home', custom_threshold=0)
                #
                #     if self.get_option('hp_100_message') is not True:
                #         self.logger.info('물약 100개 이하 감지됨')
                #         self.set_option('hp_100_message', True)
                #         if cfg_notify_potion:
                #             self.game_object.telegram_send('HP 물약이 100개 이하입니다. ' + cfg_notify_potion_message)
        elif 100000 <= self.status < 100010:
            self.status += 1
        elif self.status == 100010:
            elapsed_time = time.time() - self.get_checkpoint('closed')
            if elapsed_time < self.get_checkpoint(30):
                self.game_object.telegram_send("게임 가드 블럭 감지됨")
                return -1
            else:
                self.status = 0
        else:
            self.lyb_mouse_drag('jeoljeon_mode_scene_drag_right', 'jeoljeon_mode_scene_drag_left')
            self.set_checkpoint('closed')
            self.status = 100000

        return self.status

    def quick_config_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('changed', True)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            self.game_object.get_scene('jeoljeon_mode_scene').status = 0
            self.lyb_mouse_click('quick_config_scene_jeoljeon', custom_threshold=0)
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

            resource_name = 'l2m_icon_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            if self.game_object.player_type == 'nox':
                for each_icon in resource:
                    (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                        self.window_image,
                        self.game_object.resource_manager.pixel_box_dic[each_icon],
                        custom_threshold=0.8,
                        custom_flag=1,
                        custom_rect=(80, 110, 800, 450)
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
                        custom_rect=(50, 110, 800, 440)
                    )
                    # self.logger.debug(match_rate)
                    if loc_x != -1:
                        self.lyb_mouse_click_location(loc_x, loc_y)
                        break

            # if loc_x == -1:
            # 	self.loggingToGUI('테라 아이콘 발견 못함')

        return self.status

    #
    #
    # Main
    #
    #

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

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'main_quest_duration'))
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

        elif self.status == self.get_work_status('마우스 클릭'):

            loc_x = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x'))
            loc_y = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y'))

            self.lyb_mouse_click_location(loc_x, loc_y)
            self.status = self.last_status[self.current_work] + 1

        elif self.status == self.get_work_status('지도 이동'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=30)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            inner_status = self.get_option(self.current_work + '_inner_status')
            if inner_status is None:
                inner_status = 0

            # self.logger.debug('inner_status ' + str(inner_status))
            if inner_status == 0:
                self.set_option(self.current_work + '_inner_status', inner_status + 1)
                self.set_option('jido_move_ok', False)
            elif 1 <= inner_status < 10:
                self.set_option(self.current_work + '_inner_status', inner_status + 1)
                if self.is_open_npc():
                    self.lyb_mouse_click('main_scene_npc', custom_threshold=0)
                    return self.status
                else:
                    self.set_option(self.current_work + '_inner_status', 10)
            elif 10 <= inner_status < 20:
                self.set_option(self.current_work + '_inner_status', inner_status + 1)
                if self.get_option('jido_move_ok'):
                    self.set_option(self.current_work + '_inner_status', 20)
                else:
                    self.game_object.get_scene('jido_scene').status = 0
                    self.lyb_mouse_click('main_scene_map', custom_threshold=0)
            else:
                self.set_option(self.current_work + '_inner_status', inner_status + 1)

                cfg_style = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style')
                if cfg_style == "텔레포트":
                    self.set_option(self.current_work + '_end_flag', True)
                    self.logger.info('도착')
                else:
                    if self.is_not_moving():
                        self.set_option(self.current_work + '_end_flag', True)
                        self.logger.info('도착')

        elif self.status == self.get_work_status('자동 사냥'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration'))
            elapsed_time = self.get_elapsed_time()

            if elapsed_time > self.period_bot(cfg_duration):
                self.set_option(self.current_work + '_end_flag', True)

            self.loggingElapsedTime('[' + str(self.current_work) + '] 경과 시간', elapsed_time, cfg_duration, period=60)
            self.logger.info(str(self.get_option(self.current_work + '_end_flag')))
            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.process_auto()

        elif self.status == self.get_work_status('캐릭터 이동'):

            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time'))
            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(600):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            pb_name = self.character_move_direction()
            self.lyb_mouse_drag('main_scene_pad_c', pb_name, stop_delay=cfg_duration)
            self.set_option(self.current_work + '_end_flag', True)

        elif self.status == self.get_work_status('순간 이동'):

            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(30):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag'):
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1

            inner_status = self.get_option(self.current_work + '_inner_status')
            if inner_status is None:
                inner_status = 0

            # self.logger.debug('inner_status ' + str(inner_status))
            if inner_status == 0:
                self.lyb_mouse_click('main_scene_quick_config', custom_threshold=0)
                self.game_object.get_scene('quick_config_scene').status = 0
                self.game_object.get_scene('quick_config_scene').set_option('changed', False)
                self.set_option(self.current_work + '_inner_status', inner_status + 1)
            else:
                if self.game_object.get_scene('quick_config_scene').get_option('changed') is not True:
                    self.game_object.telegram_send("게임 가드 블럭 감지됨")
                    self.game_object.get_scene('quick_config_scene').set_option('changed', True)

                if self.get_option('is_home'):
                    self.logger.info('안전 지대입니다. 순간 이동 작업을 수행하지 않습니다.')
                    self.set_option(self.current_work + '_end_flag', True)
                else:
                    if self.move_item_slot_1() is False:
                        self.set_option(self.current_work + '_end_flag', True)
                        pb_name = 'main_scene_item_3'
                        match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                        if match_rate > 0.7:
                            self.lyb_mouse_click(pb_name, custom_threshold=0)

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

    def is_not_auto_jeoljeon_mode(self, limit=2):
        return self.is_status_by_resource('[자동 전투 중] 감지 실패', 'jeoljeon_mode_scene_auto_loc',
                                          custom_top_level=-1,
                                          custom_below_level=-1,
                                          custom_rect=(330, 310, 480, 360),
                                          custom_threshold=0.7,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def is_not_moving(self, limit=10):
        return self.is_status_by_resource('[자동 이동 중] 감지 실패', 'main_scene_auto_moving_loc',
                                          custom_top_level=(255, 110, 30),
                                          custom_below_level=(100, 0, 0),
                                          custom_rect=(330, 280, 480, 340),
                                          custom_threshold=0.4,
                                          limit_count=limit,
                                          reverse=False,
                                          )

    def get_work_status(self, work_name):
        if work_name in lybgamel2m.LYBL2M.work_list:
            return (lybgamel2m.LYBL2M.work_list.index(work_name) + 1) * 1000
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
            # debug=True,
            custom_flag=1)
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True, match_rate

        return False, match_rate

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
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
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

        if check_count > int(limit_count * 0.5):
            self.logger.debug(log_message + '..(' + str(check_count) + '/' + str(limit_count) + ')')
        self.set_option(resource_name + 'check_count', check_count + 1)

        return False

    def is_status_by_resource2(self, log_message, resource_name, custom_threshold, custom_top_level=-1,
                               custom_below_level=-1, limit_count=-1, reverse=False):
        match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name,
                                                          custom_top_level=custom_top_level,
                                                          custom_below_level=custom_below_level)
        # self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
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

    def pre_process_main_scene(self):

        # 메뉴
        if self.get_option('menu_work'):
            menu_status = self.get_option('menu_status')
            if menu_status is None:
                menu_status = 0

            # self.logger.debug('menu_status: ' + str(menu_status))

            if menu_status == 0:
                self.set_option('menu_status', menu_status + 1)
            elif 1 <= menu_status < 10:
                self.set_option('menu_status', menu_status + 1)
                if self.is_open_menu():
                    self.set_option('menu_status', 10)
                else:
                    self.lyb_mouse_click('main_scene_menu_close_icon', custom_threshold=0)
                    return True
            elif menu_status == 10:
                self.set_option('menu_status', menu_status + 1)
                self.set_option('mail_check_ok', False)
            elif 11 <= menu_status < 20:
                self.set_option('menu_status', menu_status + 1)
                if self.get_option('mail_check_ok'):
                    self.set_option('menu_status', 99999)
                else:
                    self.lyb_mouse_click('main_scene_menu_mail', custom_threshold=0)
                    self.game_object.get_scene('mail_scene').status = 0
            elif menu_status == 100:
                self.set_option('menu_status', menu_status + 1)
                self.set_option('daily_check_ok', False)
            elif 101 <= menu_status < 110:
                self.set_option('menu_status', menu_status + 1)
                if self.get_option('daily_check_ok'):
                    self.set_option('menu_status', 99999)
                else:
                    self.lyb_mouse_click('main_scene_menu_daily', custom_threshold=0)
                    self.game_object.get_scene('daily_scene').status = 0
            else:
                self.set_option('menu_status', 0)
                self.set_option('menu_work', False)
                if self.is_open_menu():
                    self.lyb_mouse_click('main_scene_menu_close_icon', custom_threshold=0)
                    return True

            return True
        else:
            elapsed_time = time.time() - self.get_checkpoint('menu_clicked')
            if elapsed_time > self.period_bot(5):
                self.set_checkpoint('menu_clicked')
                if self.is_open_menu():
                    self.lyb_mouse_click('main_scene_menu_close_icon', custom_threshold=0)
                    return True

        if self.get_option('is_home'):
            elapsed_time = time.time() - self.get_checkpoint('home_check')
            if elapsed_time < self.period_bot(60):
                self.set_option('is_home', False)
                return False

            # self.logger.info('마을입니다.')
            rect_list = [
                (40, 80, 140, 120),
                (40, 100, 140, 140),
                (40, 130, 140, 170),
                (40, 160, 140, 210),
                (40, 190, 140, 240),
                (40, 200, 140, 250),
            ]
            home_status = self.get_option('home_status')
            if home_status is None:
                home_status = 0

            # self.logger.debug('home_status: ' + str(home_status))

            if home_status == 0:
                self.logger.info('마을입니다. [자동 사냥] 작업을 종료합니다.')
                self.set_option('자동 사냥' + '_end_flag', True)
                self.set_option('home_status', home_status + 1)
            elif 1 <= home_status < 10:
                self.set_option('home_status', home_status + 1)
                if self.is_open_npc():
                    self.set_option('home_status', 100)
                else:
                    self.lyb_mouse_click('main_scene_npc', custom_threshold=0)
                    return True
            elif home_status == 100:
                cfg_go_npc = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move')
                if cfg_go_npc is False:
                    self.set_option('home_status', 200)
                else:
                    self.game_object.get_scene('sell_npc_scene').status = 0
                    self.lyb_mouse_drag('main_scene_npc_list_drag_top', 'main_scene_npc_list_drag_bot')
                    self.set_option('home_find_npc_resource_name', 'main_scene_npc_list_매입 상인_loc')
                    self.set_option('last_home_status', 200)
                    self.set_option('next_home_status', 1010)
                    self.set_option('home_status', 1000)
                    return True
            elif home_status == 200:
                cfg_go_npc = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move')
                if cfg_go_npc is False:
                    self.set_option('home_status', 300)
                else:
                    self.game_object.get_scene('stash_scene').status = 0
                    self.lyb_mouse_drag('main_scene_npc_list_drag_top', 'main_scene_npc_list_drag_bot')
                    self.set_option('home_find_npc_resource_name', 'main_scene_npc_list_창고지기_loc')
                    self.set_option('last_home_status', 300)
                    self.set_option('next_home_status', 1010)
                    self.set_option('home_status', 1000)
                    return True
            elif home_status == 300:
                cfg_go_npc = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move')
                if cfg_go_npc is False:
                    self.set_option('home_status', 99999)
                else:
                    self.set_option('item_check', False)
                    self.game_object.get_scene('potion_npc_scene').status = 0
                    self.set_option('home_find_npc_resource_name', 'main_scene_npc_list_잡화 상인_loc')
                    self.lyb_mouse_drag('main_scene_npc_list_drag_top', 'main_scene_npc_list_drag_bot')
                    self.set_option('last_home_status', 99999)
                    self.set_option('next_home_status', 1010)
                    self.set_option('home_status', 1000)
                    return True
            elif 1000 <= home_status < 1010:
                self.set_option('home_status', home_status + 1)
                resource_name = self.get_option('home_find_npc_resource_name')
                for rect in rect_list:
                    (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                        self.window_image,
                        resource_name,
                        custom_rect=rect,
                        custom_threshold=0.8,
                        custom_flag=1,
                        average=False,
                        # debug=True
                    )
                    # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
                    if loc_x != -1:
                        self.lyb_mouse_click_location(loc_x, loc_y)
                        self.set_option('npc_ok', False)
                        self.set_option('home_status', self.get_option('next_home_status'))
                        return True
                if home_status % 4 < 2:
                    self.lyb_mouse_drag('main_scene_npc_list_drag_bot', 'main_scene_npc_list_drag_top')
                else:
                    self.lyb_mouse_drag('main_scene_npc_list_drag_top', 'main_scene_npc_list_drag_bot')
            elif 1010 <= home_status < 1200:
                self.set_option('home_status', home_status + 1)
                if self.get_option('npc_ok'):
                    self.set_option('npc_ok', False)
                    self.set_option('home_status', self.get_option('last_home_status'))
                else:
                    if (home_status - 1009) % 10 == 0:
                        self.set_option('next_home_status', home_status + 1)
                        self.set_option('home_status', 1000)
                        direction = int(random.random() * 8)
                        self.lyb_mouse_drag('main_scene_pad_c', 'main_scene_pad_' + str(direction))
                        return True
            # elif home_status == 2000:
            #     self.set_option('home_status', home_status + 1)
            #     self.game_object.get_scene('potion_npc_scene').status = 1
            #     self.set_option('item_check_list', [])
            # elif 2001 <= home_status < 2100:
            #     self.set_option('home_status', home_status + 1)
            #     item_check_list = self.get_option('item_check_list')
            #     if len(item_check_list) >= 4:
            #         self.set_option('home_status', 1000)
            #         return True
            #
            #     item_slot_number = self.number_item_slot()
            #     self.logger.info('아이템 슬롯 번호: ' + str(item_slot_number))
            #     if home_status % 2 == 0:
            #         if item_slot_number == 1:
            #             self.process_item_slot_1()
            #         elif item_slot_number == 2:
            #             self.process_item_slot_2()
            #         elif item_slot_number == 3:
            #             self.process_item_slot_3()
            #         elif item_slot_number == 4:
            #             self.process_item_slot_4()
            #         else:
            #             item_slot_number = 1
            #             self.process_item_slot_1()
            #
            #         if item_slot_number not in item_check_list:
            #             item_check_list.append(item_slot_number)
            #
            #         self.lyb_mouse_drag('main_scene_item_slot_drag_right', 'main_scene_item_slot_drag_left')
            else:
                self.set_option('home_status', 0)
                self.set_checkpoint('home_check')
                self.set_option('is_home', False)
                return False

            return True
        else:
            if self.move_item_slot_1():
                return True

            if self.get_option('click_auto'):
                self.logger.info('[AUTO] 클릭')
                self.lyb_mouse_click('main_scene_auto', custom_threshold=0)
                self.set_option('click_auto', False)
                return True

            if self.process_skill():
                return True

            if self.process_item():
                return True

        cfg_period = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period'))
        if cfg_period > 0:
            elapsed_time = time.time() - self.get_checkpoint('check_mail_period')
            if elapsed_time > self.period_bot(81640):
                self.set_checkpoint('check_mail_period')
            elif elapsed_time > cfg_period:
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.set_option('menu_work', True)
                self.set_option('menu_status', 0)
                self.set_checkpoint('check_mail_period', time.time())
                return True

        cfg_period = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period'))
        if cfg_period > 0:
            elapsed_time = time.time() - self.get_checkpoint('check_daily_period')
            if elapsed_time > self.period_bot(81640):
                self.set_checkpoint('check_daily_period')
            elif elapsed_time > cfg_period:
                self.lyb_mouse_click('main_scene_menu', custom_threshold=0)
                self.set_option('menu_work', True)
                self.set_option('menu_status', 100)
                self.set_checkpoint('check_daily_period', time.time())
                return True

        if self.is_clicked_recover_icon():
            return True

        if self.is_detected_recover():
            recover_status = self.get_option('recover_status')
            if recover_status is None:
                recover_status = 0

            # self.logger.debug('recover_status: ' + str(recover_status))
            if recover_status == 0:
                self.set_option('recover_status', recover_status + 1)
            elif recover_status == 1:
                self.lyb_mouse_click('main_scene_recover_tab_0', custom_threshold=0)
                self.set_option('recover_last_status', 10)
                self.set_option('recover_status', 100)
                return True
            elif recover_status == 10:
                self.lyb_mouse_click('main_scene_recover_tab_1', custom_threshold=0)
                self.set_option('recover_last_status', 99999)
                self.set_option('recover_status', 100)
                return True
            elif recover_status == 100:
                self.set_option('recover_status', recover_status + 1)
            elif 101 <= recover_status < 110:
                self.set_option('recover_status', recover_status + 1)
                if self.game_object.get_scene('recover_scene').get_option('option_gem'):
                    self.game_object.get_scene('recover_scene').set_option('option_gem', False)
                    self.lyb_mouse_click('main_scene_recover_menu_0', custom_threshold=0)
                    return True

                if self.is_no_more_recover():
                    self.set_option('recover_status', self.get_option('recover_last_status'))
                else:
                    if self.is_recover_cross_active():
                        self.game_object.get_scene('recover_scene').status = 0
                        self.lyb_mouse_click('main_scene_recover_cross_active', custom_threshold=0)
                        return True
                    else:
                        self.lyb_mouse_click('main_scene_recover_list_top', custom_threshold=0)
                        return True
            else:
                self.lyb_mouse_click('main_scene_recover_close_icon', custom_threshold=0)
                return True

            return True
        else:
            self.set_option('recover_status', 0)

        return False

    def process_main_quest(self):

        return False

    def process_skill(self):

        if self.current_work == "자동 사냥" and self.get_option('자동 사냥' + '_end_flag') is not True:
            skill_queue = self.get_option('skill_queue')
            if skill_queue is None:
                skill_queue = []

            for i in range(1, 6):
                cfg_cooltime = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_' + str(i)))
                if cfg_cooltime != 0:
                    elapsed_time = time.time() - self.get_checkpoint('skill_cooltime_' + str(i))

                    if elapsed_time > self.period_bot(81640):
                        self.set_checkpoint('skill_cooltime_' + str(i), time.time() + self.period_bot(10))
                    elif elapsed_time > cfg_cooltime:
                        self.set_checkpoint('skill_cooltime_' + str(i))
                        if i not in skill_queue:
                            skill_queue.append(i)

            if len(skill_queue) > 0:
                elapsed_time = time.time() - self.get_checkpoint('skill_delay')
                if elapsed_time > self.period_bot(2):
                    self.set_checkpoint('skill_delay')
                    skill_index = skill_queue.pop(0)
                    pb_name = 'main_scene_skill_' + str(skill_index)
                    self.lyb_mouse_click(pb_name, custom_threshold=0)
                    time.sleep(0.5)
                    self.lyb_mouse_click(pb_name, custom_threshold=0)
                    return True

        return False

    def process_item(self):

        if self.current_work == "자동 사냥" and self.get_option('자동 사냥' + '_end_flag') is not True:
            item_queue = self.get_option('item_queue')
            if item_queue is None:
                item_queue = []

            cfg_cooltime = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion'))
            if cfg_cooltime != 0:
                elapsed_time = time.time() - self.get_checkpoint('use_item_premium_potion')

                if elapsed_time > self.period_bot(81640):
                    self.set_checkpoint('use_item_premium_potion', time.time() + self.period_bot(10))
                elif elapsed_time > cfg_cooltime:
                    self.set_checkpoint('use_item_premium_potion')
                    if 0 not in item_queue:
                        item_queue.append(0)

            if len(item_queue) > 0:
                elapsed_time = time.time() - self.get_checkpoint('item_delay')
                if elapsed_time > self.period_bot(2):
                    self.set_checkpoint('item_delay')
                    skill_index = item_queue.pop(0)
                    pb_name = 'main_scene_item_' + str(skill_index)
                    match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                    # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
                    if match_rate > 0.7:
                        self.lyb_mouse_click(pb_name, custom_threshold=0)
                    return True

        return False

    def process_auto(self):
        inner_status = self.get_option(self.current_work + '_inner_status')
        if inner_status is None:
            inner_status = 0

        # self.logger.debug('inner_status ' + str(inner_status))
        if inner_status == 0:
            self.lyb_mouse_click('main_scene_quick_config', custom_threshold=0)
            self.game_object.get_scene('quick_config_scene').status = 0
            self.game_object.get_scene('quick_config_scene').set_option('changed', False)
            self.set_option(self.current_work + '_inner_status', inner_status + 1)
            self.game_object.get_scene('jeoljeon_mode_scene').set_option('check_auto', True)
            self.set_checkpoint('auto_jeoljeon_period')
        elif 1 <= inner_status < 99999:
            if self.game_object.get_scene('quick_config_scene').get_option('changed') is not True:
                self.game_object.telegram_send("게임 가드 블럭 감지됨")
                self.game_object.get_scene('quick_config_scene').set_option('changed', True)

            self.set_option(self.current_work + '_inner_status', inner_status + 1)
            cfg_duration = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period'))
            elapsed_time = time.time() - self.get_checkpoint('auto_jeoljeon_period')
            if elapsed_time > cfg_duration:
                self.set_checkpoint('auto_jeoljeon_period')
                self.lyb_mouse_click('main_scene_quick_config', custom_threshold=0)
                self.game_object.get_scene('quick_config_scene').status = 0
                self.game_object.get_scene('quick_config_scene').set_option('changed', False)

            # 아이템 사용
            # 스킬 사용

        return False

    def is_open_npc(self):
        resource_name = 'main_scene_npc_open_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_rect=(40, 80, 180, 240),
            custom_threshold=0.7,
            custom_flag=1,
            average=True
        )
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            return True

        return False

    def is_open_menu(self):
        pb_name = 'main_scene_menu_close_icon'
        match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
        # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
        if match_rate > 0.75:
            return True

        return False

    def is_clicked_recover_icon(self):
        elapsed_time = time.time() - self.get_checkpoint('detected_recover_icon')
        if elapsed_time > self.period_bot(120):
            self.set_checkpoint('detected_recover_icon')
            resource_name = 'main_scene_recover_loc'
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_top_level=(255, 255, 200),
                custom_below_level=(220, 150, 100),
                custom_rect=(500, 35, 600, 80),
                custom_threshold=0.85,
                custom_flag=1,
                average=True
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                self.lyb_mouse_click_location(loc_x, loc_y)
                return True

        return False

    def is_detected_recover(self):
        resource_name = 'main_scene_recover_menu_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_rect=(150, 300, 220, 380),
            custom_threshold=0.85,
            custom_flag=1,
            average=True
        )
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            return True

        return False

    def is_no_more_recover(self):
        resource_name = 'main_scene_recover_no_more_loc'
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
            self.window_image,
            resource_name,
            custom_top_level=(150, 150, 150),
            custom_below_level=(50, 50, 50),
            custom_rect=(30, 220, 220, 260),
            custom_threshold=0.85,
            custom_flag=1,
            average=True
        )
        # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
        if loc_x != -1:
            return True

        return False

    def is_recover_cross_active(self):
        pb_name = 'main_scene_recover_cross_active'
        match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
        # self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
        if match_rate > 0.9:
            return True

        return False

    def move_item_slot_1(self):
        elapsed_time = time.time() - self.get_checkpoint('check_item_slot_1')
        if elapsed_time > self.period_bot(10):
            self.set_checkpoint('check_item_slot_1')
            slot_number = self.number_item_slot()

            if slot_number == 2:
                self.lyb_mouse_drag('main_scene_item_slot_drag_left', 'main_scene_item_slot_drag_right')
                return True
            elif slot_number == 3:
                self.lyb_mouse_drag('main_scene_item_slot_drag_left', 'main_scene_item_slot_drag_right')
                return True
            elif slot_number == 4:
                self.lyb_mouse_drag('main_scene_item_slot_drag_right', 'main_scene_item_slot_drag_left')
                return True

        return False

    def number_item_slot(self):
        rect_list = [
            (640, 450, 660, 475),
            (655, 450, 670, 475),
            (665, 450, 680, 475),
            (675, 450, 710, 475),
        ]
        resource_name = 'main_scene_item_slot_loc'
        slot_number = 1

        for rect in rect_list:
            (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_top_level=(255, 110, 10),
                custom_below_level=(240, 90, 0),
                custom_rect=rect,
                custom_threshold=0.85,
                custom_flag=1,
                average=True
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(round(match_rate, 2)))
            if loc_x != -1:
                return slot_number
            slot_number += 1

        return 0

    def character_move_direction(self):
        cfg_direction = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move')
        direction_index = lybgamel2m.LYBL2M.character_move_list.index(cfg_direction)
        pb_name = None
        if direction_index >= 0:
            pb_name = 'main_scene_pad_' + str(direction_index)

        return pb_name


    # def process_item_slot_1(self):
    #     cfg_item_list = lybgamel2m.LYBL2M.default_item_list
    #     for i in range(len(cfg_item_list)):
    #         cfg_item_name = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(i))
    #         cfg_item_cond = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_' + str(i)))
    #         cfg_item_count = int(
    #             self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(i)))
    #
    #         if cfg_item_cond > 0 and cfg_item_count > 0:
    #             if cfg_item_name == '상급 체력 회복제':
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_empty'
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_' + str(cfg_item_cond)
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    #             if cfg_item_name == '철화살' or cfg_item_name == '은화살':
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_ok'
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate < 0.9:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, False)
    #
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_empty'
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_10000'
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate < 0.8:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    # def process_item_slot_2(self):
    #     cfg_item_list = lybgamel2m.LYBL2M.default_item_list
    #     for i in range(len(cfg_item_list)):
    #         cfg_item_name = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(i))
    #         cfg_item_cond = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_' + str(i)))
    #         cfg_item_count = int(
    #             self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(i)))
    #
    #         if cfg_item_cond > 0 and cfg_item_count > 0:
    #             if cfg_item_name == '가속 물약':
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_empty'
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_' + str(cfg_item_cond)
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    #         if cfg_item_name == '마나 회복제':
    #             pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_empty'
    #             match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #             self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #             if match_rate > 0.95:
    #                 self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    #             pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_' + str(cfg_item_cond)
    #             match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #             self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #             if match_rate > 0.95:
    #                 self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    # def process_item_slot_3(self):
    #     cfg_item_list = lybgamel2m.LYBL2M.default_item_list
    #     for i in range(len(cfg_item_list)):
    #         cfg_item_name = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(i))
    #         cfg_item_cond = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_' + str(i)))
    #         cfg_item_count = int(
    #             self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(i)))
    #
    #         if cfg_item_cond > 0 and cfg_item_count > 0:
    #             if cfg_item_name == '상급 체력 회복제':
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_' + str(cfg_item_cond)
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
    #
    # def process_item_slot_4(self):
    #     cfg_item_list = lybgamel2m.LYBL2M.default_item_list
    #     for i in range(len(cfg_item_list)):
    #         cfg_item_name = self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(i))
    #         cfg_item_cond = int(self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_' + str(i)))
    #         cfg_item_count = int(
    #             self.get_game_config(lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(i)))
    #
    #         if cfg_item_cond > 0 and cfg_item_count > 0:
    #             if cfg_item_name == '상급 체력 회복제':
    #                 pb_name = 'main_scene_item_slot_' + str(cfg_item_name) + '_' + str(cfg_item_cond)
    #                 match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
    #                 self.logger.debug(pb_name + ' ' + str(round(match_rate, 2)))
    #                 if match_rate > 0.95:
    #                     self.game_object.get_scene('potion_npc_scene').set_option(cfg_item_name, True)
