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
        '임무',
        '업적',
        '길드',
        '우편함',
        '캐릭터 선택',
        '메인 퀘스트',
        '의뢰 일지',
        '몬스터 조사',
        '잠재력 개방',
        '네임드 토벌',
        '몽환의 틈',
        '지도 좌표 확인',
        '지도 이동',
        '자동 사냥',
        '마을 이동',

        '알림',
        '[반복 시작]',
        '[반복 종료]',
        '[작업 대기]',
        '[작업 예약]',
        '']

    area_list = [
        '실루나스',
        '루나트라',
        '몽환의 틈',
        '바트라',
    ]

    sub_area_list = [
        [
            '트랑제 숲',
            '오든 평야',
            '델라노르 숲',
            '유카비 사막',
            '데커스 화산',
            '비텐 고원',
        ],
        [
            '고독의 숲',
            '환각의 사막',
            '파멸의 화산',
            '허상의 고원',
            '오만의 평야',
            '좌절의 숲',
        ],
        [
            '기사의 후회 I',
            '기사의 후회 II',
            '소녀의 악몽 I',
            '소녀의 악몽 II',
            '소녀의 악몽 III',
            '상인의 소원 I',
            '상인의 소원 II',
        ],
        [
            '업데이트 예정',
        ]
    ]

    sub_area_dic = {
        area_list[0]: sub_area_list[0],
        area_list[1]: sub_area_list[1],
        area_list[2]: sub_area_list[2],
        area_list[3]: sub_area_list[3],
    }

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
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('건너뛰기: ' + str(round(match_rate, 2)))
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
                custom_rect=(350, 200, 500, 460),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('화면 터치: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'touch_screen_small_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_top_level=(255, 255, 255),
                custom_below_level=(120, 120, 120),
                custom_rect=(350, 200, 500, 460),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('화면 터치: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'touch_screen_small_20191212_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_top_level=(255, 255, 255),
                custom_below_level=(120, 120, 120),
                custom_rect=(350, 200, 500, 460),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('가방 및 재화 확인 터치: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'popup_close_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.65,
                custom_flag=1,
                custom_top_level=(255, 255, 255),
                custom_below_level=(190, 190, 190),
                custom_rect=(800, 40, 870, 120),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('팝업: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'popup_20200115_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(30):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.75,
                custom_flag=1,
                custom_top_level=(200, 170, 170),
                custom_below_level=(145, 110, 110),
                custom_rect=(25, 510, 100, 560),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('팝업: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'popup_20200115_1_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(30):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.75,
                custom_flag=1,
                custom_top_level=(255, 100, 50),
                custom_below_level=(140, 50, 20),
                custom_rect=(25, 510, 100, 560),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('팝업: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'popup_20200121_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(30):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.75,
                custom_flag=1,
                custom_rect=(25, 510, 100, 560),
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('팝업: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'confirm_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(10):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(440, 340, 520, 500)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('확인: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'move_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(10):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(440, 340, 520, 500)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('이동: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'resend_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(340, 340, 470, 500),
                average=False,
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('다시 보내기: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'receive_item_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(2):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(430, 370, 530, 450)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('필수품 받기: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'item_link_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(10):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(345, 90, 390, 130)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('아이템 상세정보: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x - 20, loc_y)
                return resource_name

        resource_name = 'show_result_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(3):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(430, 500, 560, 550)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('결과 보기: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x - 20, loc_y)
                return resource_name

        resource_name = 'nagagi_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(3):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(430, 500, 560, 550)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('나가기: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x - 20, loc_y)
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

        frame_label = ttk.LabelFrame(frame_l, text='체크 리스트')

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check'].trace(
            'w', lambda *args: self.chulseok_check(args, lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='출석 체크',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'chulseok_check'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha'].trace(
            'w',
            lambda *args: self.shop_gold_tal_gotcha(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='탈것 소환 구매(골드)',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_tal_gotcha'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha'].trace(
            'w',
            lambda *args: self.shop_gold_pet_gotcha(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='소환수 부화 구매(골드)',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_gold_pet_gotcha'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion'].trace(
            'w', lambda *args: self.shop_sang_potion(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='상급 축복의 물약 구매',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_sang_potion'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha'].trace(
            'w', lambda *args: self.shop_fellow_gotcha(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='화려한 동료계약서 구매',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_fellow_gotcha'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha'].trace(
            'w', lambda *args: self.shop_w_box_gotcha(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='무기 강화 주문서 상자 구매',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_w_box_gotcha'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha'].trace(
            'w', lambda *args: self.shop_s_box_gotcha(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='방어구 강화 주문서 상자 구매',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_s_box_gotcha'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha'].trace(
            'w', lambda *args: self.shop_a_box_gotcha(args, lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='장신구 강화 주문서 상자 구매',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'shop_a_box_gotcha'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_l, text='회복')
        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move'].trace(
            'w', lambda *args: self.recover_move(args, lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('회복 이동', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free'].trace(
            'w', lambda *args: self.recover_free(args, lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('무료인 경우만 회복하기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_free'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item'].trace(
            'w', lambda *args: self.recover_free(args, lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item'] = False

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('아이템 복구하기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'recover_item'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['common_tab_frame'])

        frame_label = ttk.LabelFrame(frame_m, text='물약 구매')
        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move'].trace(
            'w', lambda *args: self.hp_potion_move(args, lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move'
                                                   ))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('HP 물약 없을 경우 상점 이동', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'hp_potion_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move'].trace(
            'w', lambda *args: self.mp_potion_move(args, lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move'
                                                   ))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('MP 물약 없을 경우 상점 이동', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'mp_potion_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion'].trace(
            'w', lambda *args: self.remain_max_potion(args, lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion'
                                                      ))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('남은 무게 반대 물약 채우기(HP:MP)', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'remain_max_potion'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage'].trace(
            'w', lambda *args: self.prevent_overflow_gage(args, lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage'
                                                      ))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('무게가 70% 이상이면 구매하지 않기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'prevent_overflow_gage'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash'].trace(
            'w',
            lambda *args: self.go_stash(args, lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='물약 구매 후 창고 가기',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'go_stash'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('창고 재료 탐색 페이지', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number'].trace(
            'w', lambda *args: self.stash_page_number(args, lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number')
        )
        combobox_list = [
            '1',
            '2',
            '3',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'stash_page_number'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('구매할 HP 물약', width=16)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name'].trace(
            'w', lambda *args: self.potion_name(args, lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name')
        )
        combobox_list = [
            '구매 안함',
            '최하급 생명력 물약',
            '하급 생명력 물약',
            '중급 생명력 물약',
            '상급 생명력 물약',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name'] = \
                combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name'],
            state="readonly",
            height=10,
            width=18,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('- 구매 물약 갯수', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count'].trace(
            'w', lambda *args: self.potion_count(args, lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count')
        )
        combobox_list = [
            '100',
            '200',
            '300',
            '400',
            '500',
            '600',
            'Max',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count'] = \
                combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('구매할 MP 물약', width=16)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2'].trace(
            'w', lambda *args: self.potion_name2(args, lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2')
        )
        combobox_list = [
            '구매 안함',
            '하급 정신력 물약',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2'] = \
                combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2'],
            state="readonly",
            height=10,
            width=18,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_name2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('- 구매 물약 갯수', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2'].trace(
            'w', lambda *args: self.potion_count2(args, lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2')
        )
        combobox_list = [
            '100',
            '200',
            '300',
            '400',
            '500',
            '600',
            'Max',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2'] = \
                combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'potion_count2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_m, text='이벤트')

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite'].trace(
            'w', lambda *args: self.party_invite(args, lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='파티 초대 수락하기',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'party_invite'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil'].trace(
            'w', lambda *args: self.event_devil(args, lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='데빌 체이서 변신하기',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'event_devil'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'event_check'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'event_check'].trace(
            'w', lambda *args: self.event_check(args, lybconstant.LYB_DO_STRING_V4_ETC + 'event_check'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'event_check' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'event_check'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('미니맵 우측 이벤트 알림 감지하기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'event_check'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move'].trace(
            'w', lambda *args: self.gabang_full_move(args, lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move'))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('가방 풀 감지되면 창고 가기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'gabang_full_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('휴식 보상', width=19)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang'].trace(
            'w', lambda *args: self.hyusik_bosang(args, lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang')
        )
        combobox_list = [
            '경험치',
            '골드',
            '각인석',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang'],
            state="readonly",
            height=10,
            width=15,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'hyusik_bosang'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['common_tab_frame'])

        frame_label = ttk.LabelFrame(frame_r, text='사냥 관련 설정')
        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol'].trace(
            'w',
            lambda *args: self.quest_tobeol(args, lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol'
                                            ))
        if not lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('현재 지역 토벌퀘 수락하기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('토벌 퀘스트 확인 주기(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period'].trace(
            'w', lambda *args: self.quest_tobeol_period(args,
                                                     lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period')
        )
        combobox_list = []
        for i in range(60, 300, 30):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period'] = 60

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_ETC + 'quest_tobeol_period'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 좌측
        frame_l = ttk.Frame(self.inner_frame_dic['work_tab_frame'])

        frame_label = ttk.LabelFrame(frame_l, text='캐릭터 선택')
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('선택할 캐릭터 번호', width=31)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'character_number'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'character_number'].trace(
            'w', lambda *args: self.character_number(args,
                                                     lybconstant.LYB_DO_STRING_V4_WORK + 'character_number')
        )
        combobox_list = []
        for i in range(1, 7):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'character_number' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'character_number'] = 1

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'character_number'],
            state="readonly",
            height=10,
            width=3,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'character_number'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_l, text='메인 퀘스트')

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip'].trace(
            'w',
            lambda *args: self.main_quest_equip(args, lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip'
                                                ))
        if not lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text='자동 장착하기',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_equip'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

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
                lybconstant.LYB_DO_STRING_V4_WORK + 'main_quest_duration'] = 600

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

        frame_label = ttk.LabelFrame(frame_l, text='의뢰 일지')

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('진행 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration'].trace(
            'w', lambda *args: self.ure_quest_duration(args,
                                                       lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration')
        )
        combobox_list = []
        for i in range(0, 86401, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration'] = 600

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'ure_quest_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_l, text='마을 이동')

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('진행 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration'].trace(
            'w', lambda *args: self.go_home_duration(args,
                                                       lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration')
        )
        combobox_list = []
        for i in range(0, 86401, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration'] = 60

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'go_home_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_l, text='지도 이동')

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('월드', width=16)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area'].trace(
            'w', lambda *args: self.jido_move_area(args, lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area')
        )
        combobox_list = LYBV4.area_list

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area'],
            state="readonly",
            height=10,
            width=18,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('지역', width=16)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area'].trace(
            'w', lambda *args: self.jido_move_sub_area(args,
                                                       lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area')
        )

        try:
            area_index = LYBV4.area_list.index(
                self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area'])
            combobox_list = LYBV4.sub_area_list[area_index]
            if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area' in self.configure.common_config[
                self.game_name]:
                self.configure.common_config[self.game_name][
                    lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area'] = combobox_list[0]
        except ValueError:
            area_index = 0
            combobox_list = LYBV4.sub_area_list[area_index]
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area'] = \
                combobox_list[0]

        self.jido_move_sub_area_combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area'],
            state="readonly",
            height=10,
            width=18,
            font=lybconstant.LYB_FONT
        )
        self.jido_move_sub_area_combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area'])
        self.jido_move_sub_area_combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('사냥터', width=16),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order'].trace(
            'w', lambda *args: self.jido_move_area_order(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order')
        )
        combobox_list = [
            '위에서',
            '아래에서'
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order'] = combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_area_order'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number'].trace(
            'w', lambda *args: self.jido_move_sanyang_number(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number')
        )
        combobox_list = []
        for i in range(0, 11):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number'] = \
                combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sanyang_number'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('루나트라 차원문 번호', width=31)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number'].trace(
            'w', lambda *args: self.jido_move_chawon_number(args,
                                                            lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number')
        )
        combobox_list = []
        for i in range(0, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number'] = \
                combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number'],
            state="readonly",
            height=10,
            width=3,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_chawon_number'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        s = ttk.Style()
        s.configure('Warning.TLabel', foreground='#ff0000')
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('※ 주의: 발견한 사냥터만 탐색합니다', width=12),
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame = ttk.Frame(frame_label)
        frame.pack(anchor=tkinter.W)
        label = ttk.Label(
            master=frame,
            text='※ 0 은 무작위로 설정됩니다',
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        s = ttk.Style()
        s.configure('Warning.TLabel', foreground='#ff0000')
        label = ttk.Label(
            master=frame,
            text='※ [지도 좌표 확인]작업으로 좌표 확인',
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named'].trace(
            'w',
            lambda *args: self.jido_move_named(args, lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named'
                                                  ))
        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named'] = False

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('네임드로 이동하기(우선 적용)', width=10),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_named'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame = ttk.Frame(frame_label)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location'].trace(
            'w',
            lambda *args: self.jido_move_location(args, lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location'
                                                  ))
        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location'] = False

        check_box = ttk.Checkbutton(

            master=frame,
            text=self.get_option_text('좌표로 이동하기', width=10),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_location'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('이동할 좌표:', width=19)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x'].trace(
            'w', lambda *args: self.jido_move_x(args,
                                                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x')
        )
        combobox_list = []
        for i in range(10, 636):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x'] = 300

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x'],
            state="readonly",
            height=10,
            width=4,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_x'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text=self.get_option_text(',', width=1)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y'].trace(
            'w', lambda *args: self.jido_move_y(args,
                                                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y')
        )
        combobox_list = []
        for i in range(90, 556):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y'] = 300

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y'],
            state="readonly",
            height=10,
            width=4,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_y'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('도착 후 채널 변경', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel'].trace(
            'w', lambda *args: self.jido_move_change_channel(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel')
        )
        combobox_list = [
            '안함',
            '쾌적',
            '원활',
            '혼잡',
            '파티',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel'] = combobox_list[4]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_change_channel'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['work_tab_frame'])
        frame_label = ttk.LabelFrame(frame_m, text='몬스터 조사')

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('도착 후 채널 변경', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel'].trace(
            'w', lambda *args: self.monster_josa_change_channel(args,
                                                                lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel')
        )
        combobox_list = [
            '안함',
            '쾌적',
            '원활',
            '혼잡',
            '파티',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel'] = combobox_list[4]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_change_channel'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('진행 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration'].trace(
            'w', lambda *args: self.monster_josa_duration(args,
                                                          lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration')
        )
        combobox_list = []
        for i in range(0, 86401, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration'] = 600

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('몬스터 조사 지역', width=16)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area'].trace(
            'w', lambda *args: self.monster_josa_area(args, lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area')
        )
        combobox_list = [
            '트랑제 숲',
            '오든 평야',
            '델라노르 숲',
            '유카비 사막',
            '데커스 화산',
            '비텐 고원',
            '기사의 후회 I',
            '기사의 후회 II',
            '소녀의 악몽 I',
            '소녀의 악몽 II',
            '소녀의 악몽 III',
            '상인의 소원 I',
            '상인의 소원 II',
            '광란의 숲',
            '저주의 평야',
            '상실의 숲',
            '환각의 사막',
            '파멸의 화산',
            '허상의 고원',
            '오만의 평야',
            '좌절의 숲',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area'],
            state="readonly",
            height=10,
            width=18,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('탐색 기준', width=16),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order'].trace(
            'w', lambda *args: self.monster_josa_area_order(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order')
        )
        combobox_list = [
            '위에서부터 탐색',
            '아래에서부터 탐색'
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order'] = combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order'],
            state="readonly",
            height=10,
            width=18,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_area_order'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named'].trace(
            'w', lambda *args: self.monster_josa_named(args, lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named'))
        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='네임드 제외하기',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monster_josa_named'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_m, text='몽환의 틈')
        frame = ttk.Frame(frame_label)
        s = ttk.Style()
        s.configure('Warning.TLabel', foreground='#ff0000')
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('※ 주의: 발견한 사냥터만 탐색합니다', width=12),
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # 1
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('기사의 후회 I', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_0(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0'] = combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_0'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_0(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_0'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # 2
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('기사의 후회 II', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_1(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_1'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_1(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_1'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # 3

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('소녀의 악몽 I', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_2(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_2(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # 4
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('소녀의 악몽 II', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_3(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_3'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_3(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_3'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # 5
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('소녀의 악몽 III', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_4(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_4'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_4(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_4'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 6
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('상인의 소원 I', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_5(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_5'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_5(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_5'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 6
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('상인의 소원 II', width=15),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6'].trace(
            'w', lambda *args: self.monghwan_sanyang_order_6(args,
                                                             lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6')
        )
        combobox_list = [
            '위에서',
            '아래에서',
            '안함',
        ]

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6'],
            state="readonly",
            height=10,
            width=8,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_order_6'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6'].trace(
            'w', lambda *args: self.monghwan_sanyang_number_6(args,
                                                              lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6')
        )
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'monghwan_sanyang_number_6'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='번째'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['work_tab_frame'])

        frame_label = ttk.LabelFrame(frame_r, text='자동 사냥')

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit'].trace(
            'w', lambda *args: self.auto_tobeol_limit(args, lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit'))
        if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='토벌 완료가 감지되면 작업 종료하기',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_tobeol_limit'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('진행 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'].trace(
            'w', lambda *args: self.auto_duration(args,
                                                  lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration')
        )
        combobox_list = []
        for i in range(0, 86401, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'] = 600

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'auto_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon'].trace(
            'w', lambda *args: self.auto_jeoljeon(args, lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon'))
        if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text='절전모드 변환하기(추천)',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('절전 모드 해제 주기(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration'].trace(
            'w', lambda *args: self.auto_jeoljeon_duration(args,
                                                  lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration')
        )
        combobox_list = []
        for i in range(10, 301, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration'] = 10

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jeoljeon_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 잠재력 모드 시작 ----------------
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('잠재력 모드', width=15)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode'].trace(
            'w', lambda *args: self.hyusik_bosang(args, lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode')
        )
        combobox_list = [
            '투지',
            '인내',
            '통찰',
            '의지',
        ]

        if not lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_ETC + 'jamjeryeok_mode'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # 잠재력 모드 끝----------------------------------

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('잠재력 개방 주기(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'].trace(
            'w', lambda *args: self.auto_jamjeryeok_duration(args,
                                                  lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration')
        )
        combobox_list = []
        for i in range(0, 3601, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'] = 300

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'auto_jamjeryeok_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 영혼석 ------------------------
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('영혼석 주기(초)', width=15)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'].trace(
            'w', lambda *args: self.auto_soul_duration(args,lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration')
        )
        combobox_list = []
        for i in range(0, 500, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'] = 300

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_V4_WORK + 'auto_soul_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 영혼석 끝 ----------------

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

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

    def main_quest_equip(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def ure_quest_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def go_home_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def character_number(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_x(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_y(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monster_josa_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_order_6(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monghwan_sanyang_number_6(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def hyusik_bosang(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def recover_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def event_check(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def gabang_full_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def event_devil(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def party_invite(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def recover_free(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def quest_tobeol_period(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def hp_potion_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def mp_potion_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monster_josa_change_channel(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_change_channel(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def remain_max_potion(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_name(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_count(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_name2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_count2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monster_josa_area(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def chulseok_check(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_area_order(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_gold_tal_gotcha(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_gold_pet_gotcha(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def go_stash(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def prevent_overflow_gage(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_sang_potion(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_fellow_gotcha(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_w_box_gotcha(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_s_box_gotcha(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def shop_a_box_gotcha(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def quest_tobeol(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_jeoljeon_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_jamjeryeok_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_area(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
        new_list = LYBV4.sub_area_dic[self.option_dic[option_name].get()]

        self.jido_move_sub_area_combobox['values'] = new_list
        try:
            if not self.get_game_config(lybconstant.LYB_DO_STRING_V4_WORK + 'jido_move_sub_area') in new_list:
                self.jido_move_sub_area_combobox.set(new_list[0])
        except KeyError:
            pass

    def jido_move_sub_area(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_chawon_number(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_sanyang_number(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_location(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_named(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monster_josa_area_order(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monster_josa_named(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_tobeol_limit(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_jeoljeon(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def stash_page_number(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())


