import likeyoubot_game as lybgame
import likeyoubot_v4_scene as lybscene
from likeyoubot_configure import LYBConstant as lybconstant
import time
import sys
import tkinter
from tkinter import ttk
from tkinter import font
import copy


class LYBV4(lybgame.LYBGame):
    work_list = [
        '게임 시작',
        '로그인',
        '메인 퀘스트',

        '알림',
        '[반복 시작]',
        '[반복 종료]',
        '[작업 대기]',
        '[작업 예약]',
        '']

    def __init__(self, game_name, game_data_name, window):
        lybgame.LYBGame.__init__(self, lybconstant.LYB_GAME_V4, lybconstant.LYB_GAME_DATA_V4, window)

    def process(self, window_image):
        rc = super(LYBV4, self).process(window_image)
        if rc < 0:
            return rc

        return rc

    def custom_check(self, window_image, window_pixel):

        resource_name = 'skip_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_rect=(400, 30, 950, 80)
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('건너뛰기: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'touch_screen_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_top_level=(255, 255, 255),
                custom_below_level=(120, 120, 120),
                custom_rect=(350, 350, 500, 420)
            )
            self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('화면 터치: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name
        # resource_name = 'equip_loc'
        # elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        # if elapsed_time > self.period_bot(2):
        #     (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
        #         self.window_image,
        #         resource_name,
        #         custom_threshold=0.7,
        #         custom_flag=1,
        #         custom_rect=(840, 310, 920, 370)
        #     )
        #     self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        #     if loc_x != -1:
        #         self.get_scene('main_scene').set_checkpoint(resource_name)
        #         self.logger.info('장착: ' + str(match_rate))
        #         self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
        #         return resource_name

        return ''

    def get_screen_by_location(self, window_image):

        scene_name = self.scene_init_screen(window_image)
        if len(scene_name) > 0:
            return scene_name

        # scene_name = self.jeontoo_scene(window_image)
        # if len(scene_name) > 0:
        # 	return scene_name

        # scene_name = self.scene_google_play_account_select(window_image)
        # if len(scene_name) > 0:
        # 	return scene_name

        return ''

    # def jeontoo_scene(self, window_image):
    # 	(loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
    # 						self.window_image,
    # 						'jeontoo_scene_loc',
    # 						custom_below_level=(100, 100, 100),
    # 						custom_top_level=(255, 255, 255),
    # 						custom_threshold=0.7,
    # 						custom_flag=1,
    # 						custom_rect=(5, 90, 80, 130)
    # 						)
    # 	if match_rate > 0.7:
    # 		return 'jeontoo_scene'

    # 	return ''

    def scene_init_screen(self, window_image):

        loc_x = -1
        loc_y = -1

        resource_name = 'v4_icon_loc'
        resource = self.resource_manager.resource_dic[resource_name]
        if self.player_type == 'nox':
            for each_icon in resource:
                (loc_x, loc_y), match_rate = self.locationOnWindowPart(
                    window_image,
                    self.resource_manager.pixel_box_dic[each_icon],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(80, 110, 920, 500)
                )
                # print('[DEBUG] nox yh icon:', (loc_x, loc_y), match_rate)
                if loc_x != -1:
                    break
        else:
            for each_icon in resource:
                (loc_x, loc_y), match_rate = self.locationOnWindowPart(
                    window_image,
                    self.resource_manager.pixel_box_dic[each_icon],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(50, 110, 920, 440)
                )
                # print('[DEBUG] momo yh icon:', (loc_x, loc_y), match_rate)
                if loc_x != -1:
                    break

        if loc_x == -1:
            return ''

        return 'init_screen_scene'

    def scene_google_play_account_select(self, window_image):
        loc_x_list = []
        loc_y_list = []

        (loc_x, loc_y) = lybgame.LYBGame.locationOnWindow(
            window_image,
            self.resource_manager.pixel_box_dic['google_play_letter']
        )
        loc_x_list.append(loc_x)
        loc_y_list.append(loc_y)

        for i in range(6):
            (loc_x, loc_y) = lybgame.LYBGame.locationOnWindow(
                window_image,
                self.resource_manager.pixel_box_dic['google_play_letter_' + str(i)]
            )

            loc_x_list.append(loc_x)
            loc_y_list.append(loc_y)

        for each_loc in loc_x_list:
            if each_loc == -1:
                return ''
            else:
                continue

        return 'google_play_account_select_scene'

    def clear_scene(self):
        last_scene = self.scene_dic
        self.scene_dic = {}
        for scene_name, scene in last_scene.items():
            if ('google_play_account_select_scene' in scene_name or
                    'logo_screen_scene' in scene_name or
                    'connect_account_scene' in scene_name
            ):
                self.scene_dic[scene_name] = last_scene[scene_name]

    def add_scene(self, scene_name):
        self.scene_dic[scene_name] = lybscene.LYBV4Scene(scene_name)
        self.scene_dic[scene_name].setLoggingQueue(self.logging_queue)
        self.scene_dic[scene_name].setGameObject(self)


class LYBV4Tab(lybgame.LYBGameTab):
    def __init__(self, root_frame, configure, game_options, inner_frame_dics, width, height,
                 game_name=lybconstant.LYB_GAME_V4):
        lybgame.LYBGameTab.__init__(self, root_frame, configure, game_options, inner_frame_dics, width, height,
                                    game_name)

    def set_work_list(self):
        lybgame.LYBGameTab.set_work_list(self)

        for each_work in LYBV4.work_list:
            self.option_dic['work_list_listbox'].insert('end', each_work)
            self.configure.common_config[self.game_name]['work_list'].append(each_work)

    def set_option(self):
        # PADDING
        frame = ttk.Frame(
            master=self.master,
            relief=self.frame_relief
        )
        frame.pack(pady=5)

        self.inner_frame_dic['options'] = ttk.Frame(
            master=self.master,
            relief=self.frame_relief
        )

        self.option_dic['option_note'] = ttk.Notebook(
            master=self.inner_frame_dic['options']
        )

        self.inner_frame_dic['common_tab_frame'] = ttk.Frame(
            master=self.option_dic['option_note'],
            relief=self.frame_relief
        )

        self.inner_frame_dic['common_tab_frame'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['option_note'].add(self.inner_frame_dic['common_tab_frame'], text='일반')

        self.inner_frame_dic['work_tab_frame'] = ttk.Frame(
            master=self.option_dic['option_note'],
            relief=self.frame_relief
        )
        self.inner_frame_dic['work_tab_frame'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['option_note'].add(self.inner_frame_dic['work_tab_frame'], text='작업')

        self.inner_frame_dic['notify_tab_frame'] = ttk.Frame(
            master=self.option_dic['option_note'],
            relief=self.frame_relief
        )
        self.inner_frame_dic['notify_tab_frame'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['option_note'].add(self.inner_frame_dic['notify_tab_frame'], text='알림')

        # ------

        # 일반 탭 좌측
        frame_l = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 좌측
        frame_l = ttk.Frame(self.inner_frame_dic['work_tab_frame'])

        frame_label = ttk.LabelFrame(frame_l, text='메인 퀘스트')

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('진행 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'].trace(
            'w', lambda *args: self.main_quest_duration(args,
                                                        lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration')
        )
        combobox_list = []
        for i in range(0, 86401, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'] = 3600

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        # frame_label = ttk.LabelFrame(frame_l, text='자동 사냥')
        #
        # frame = ttk.Frame(frame_label)
        # label = ttk.Label(
        #     master=frame,
        #     text=self.get_option_text('진행 시간(초)', width=27)
        # )
        # label.pack(side=tkinter.LEFT)
        #
        # self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'] = tkinter.StringVar(frame)
        # self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'].trace(
        #     'w', lambda *args: self.auto_duration(args,
        #                                           lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration')
        # )
        # combobox_list = []
        # for i in range(0, 86401, 60):
        #     combobox_list.append(str(i))
        #
        # if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration' in self.configure.common_config[
        #     self.game_name]:
        #     self.configure.common_config[self.game_name][
        #         lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'] = 3600
        #
        # combobox = ttk.Combobox(
        #     master=frame,
        #     values=combobox_list,
        #     textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'],
        #     state="readonly",
        #     height=10,
        #     width=7,
        #     font=lybconstant.LYB_FONT
        # )
        # combobox.set(self.configure.common_config[self.game_name][
        #                  lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'])
        # combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        # frame.pack(anchor=tkinter.W)
        #
        # frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['work_tab_frame'])
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['work_tab_frame'])
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 알림 탭 좌
        frame_l = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])
        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # 알림 탭 중
        frame_m = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # 알림 탭 우
        frame_r = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # ------

        self.option_dic['option_note'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.inner_frame_dic['options'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

        self.set_game_option()

    def main_quest_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    # def auto_duration(self, args, option_name):
    #     self.set_game_config(option_name, self.option_dic[option_name].get())
