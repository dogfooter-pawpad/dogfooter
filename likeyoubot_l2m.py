import likeyoubot_game as lybgame
import likeyoubot_l2m_scene as lybscene
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_configure
import time
import sys
import tkinter
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import copy


class LYBL2M(lybgame.LYBGame):
    work_list = [
        '게임 시작',
        '로그인',
        '지도 이동',
        '캐릭터 이동',
        '순간 이동',
        '자동 사냥',
        '마우스 클릭',

        '알림',
        '[반복 시작]',
        '[반복 종료]',
        '[작업 대기]',
        '[작업 예약]',
        '']

    home_list = [
        '글루딘 마을',
        '경비대 초소',
        '글루디오성 마을',
        '디온성 마을',
        '플로란 마을',
        '기란 항구',
        '기란성 마을',
        '하딘의 사숙',
    ]

    area_list = [
        '즐겨찾기',
        '글루디오',
        '디온',
        '기란'
    ]
    sub_area_list = [
        [
            '1',
            '2',
            '3',
            '4',
            '5',
            '6'
        ],
        [
            '글루딘 마을',
            '경비대 초소',
            '글루디오성 마을',
            '글루딘 해안',
            '사자머리 언덕',
            '랑크 리자드맨 서식지',
            '버려진 야영지',
            '투렉 오크 야영지',
            '체르투바의 막사',
            '비탄의 폐허',
            '절망의 폐허',
            '황무지 북부',
            '베레스의 봉인터',
            '황무지 남부',
            '버림받은 신전 입구',
            '개미굴 입구',
        ],
        [
            '디온성 마을',
            '플로란 마을',
            '디온 목초지',
            '비하이브',
            '반란군 아지트',
            '디온 구릉지',
            '플로란 개간지',
            '델루 리자드맨 서식지',
            '크루마 습지',
            '거인의 흔적',
            '처형터',
            '시체 처리소',
            '하수구',
            '화장터',
            '크루마 탑 입구',
        ],
        [
            '기란 항구',
            '기란성 마을',
            '하딘의 사숙',
            '기란 무역로',
            '약탈자의 야영지',
            '브래카 소굴',
            '고르곤의 화원',
            '돌아오지 않는 숲',
            '메두사의 정원',
            '죽음의 회랑',
            '용의 계곡 입구',
            '용의 무덤',
            '용의 계곡 북부',
            '용의 계곡 동부',
            '안타라스의 동굴 입구',
        ],
    ]

    sub_area_dic = {
        area_list[0]: sub_area_list[0],
        area_list[1]: sub_area_list[1],
        area_list[2]: sub_area_list[2],
        area_list[3]: sub_area_list[3],
    }

    item_list = [
        '체력 회복제',
        '상급 체력 회복제',
        '가속 물약',
        '정령탄',
        '마나 회복제',
        '고르곤 스테이크',
        '날치 꼬치구이',
        '만드라고라 수프',
        '귀환 주문서',
        '순간 이동 주문서',
        '경량화 주문서',
        '각성의 주문서',
        '방어의 주문서',
        '융해제',
        '숫돌',
        '철화살',
        '은화살',
    ]
    default_item_list = [
        '철화살',
        '가속 물약',
        '귀환 주문서',
        '순간 이동 주문서',
        '정령탄',

        '고르곤 스테이크',
        '만드라고라 수프',
        '경량화 주문서',
        '각성의 주문서',
        '방어의 주문서',

        '마나 회복제',
        '융해제',
        '숫돌',
        '체력 회복제',
    ]
    character_move_list = [
        "↑",
        "↗",
        "→",
        "↘",
        "↓",
        "↙",
        "←",
        "↖"
    ]
    def __init__(self, game_name, game_data_name, window):
        lybgame.LYBGame.__init__(self, lybconstant.LYB_GAME_L2M, lybconstant.LYB_GAME_DATA_L2M, window)

    def process(self, window_image):
        rc = super(LYBL2M, self).process(window_image)
        if rc < 0:
            return rc

        return rc

    def custom_check(self, window_image, window_pixel):

        # resource_name = 'skip_loc'
        # elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        # if elapsed_time > self.period_bot(2):
        #     (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
        #         self.window_image,
        #         resource_name,
        #         custom_threshold=0.7,
        #         custom_flag=1,
        #         custom_rect=(840, 110, 920, 150)
        #     )
        #     self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        #     if loc_x != -1:
        #         self.get_scene('main_scene').set_checkpoint(resource_name)
        #         self.logger.info('건너뛰기: ' + str(round(match_rate, 2)))
        #         self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
        #         return resource_name

        resource_name = 'confirm_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(5):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_rect=(360, 200, 450, 420)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('확인: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return resource_name

        resource_name = 'today_stop_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(5):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_rect=(10, 400, 90, 430)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('오늘 그만 보기: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x - 10, loc_y)
                return resource_name

        resource_name = 'today_stop_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(5):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_rect=(10, 400, 90, 430)
            )
            # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('오늘 그만 보기: ' + str(round(match_rate, 2)))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x - 10, loc_y)
                return resource_name
        #
        # resource_name = 'touch_screen_loc'
        # elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        # if elapsed_time > self.period_bot(2):
        #     (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
        #         self.window_image,
        #         resource_name,
        #         custom_threshold=0.7,
        #         custom_flag=1,
        #         custom_top_level=(255, 255, 255),
        #         custom_below_level=(120, 120, 120),
        #         custom_rect=(350, 200, 500, 460),
        #     )
        #     # self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        #     if loc_x != -1:
        #         self.get_scene('main_scene').set_checkpoint(resource_name)
        #         self.logger.info('화면 터치: ' + str(round(match_rate, 2)))
        #         self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
        #         return resource_name

        return ''

    def get_screen_by_location(self, window_image):

        # scene_name = self.scene_init_screen(window_image)
        # if len(scene_name) > 0:
        #     return scene_name

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

        resource_name = 'l2m_icon_loc'
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
        self.scene_dic[scene_name] = lybscene.LYBL2MScene(scene_name)
        self.scene_dic[scene_name].setLoggingQueue(self.logging_queue)
        self.scene_dic[scene_name].setGameObject(self)


class LYBL2MTab(lybgame.LYBGameTab):
    def __init__(self, root_frame, configure, game_options, inner_frame_dics, width, height,
                 game_name=lybconstant.LYB_GAME_L2M):
        lybgame.LYBGameTab.__init__(self, root_frame, configure, game_options, inner_frame_dics, width, height,
                                    game_name)

    def set_work_list(self):
        lybgame.LYBGameTab.set_work_list(self)

        for each_work in LYBL2M.work_list:
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
        #
        # self.inner_frame_dic['common_tab_frame2'] = ttk.Frame(
        #     master=self.option_dic['option_note'],
        #     relief=self.frame_relief
        # )
        #
        # self.inner_frame_dic['common_tab_frame2'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        # self.option_dic['option_note'].add(self.inner_frame_dic['common_tab_frame2'], text='일반2')

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

        frame_label = ttk.LabelFrame(frame_l, text='스킬 슬롯 셋팅')
        frame = ttk.Frame(frame_label)
        s = ttk.Style()
        s.configure('Warning.TLabel', foreground='#ff0000')
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('※ 수동으로 사용할 스킬 번호', width=12),
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        im = Image.open(likeyoubot_configure.LYBConfigure.resource_path("images/skill_slot_1.png"))
        if im.size != (240, 58):
            im = im.resize((240, 58), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(im)

        label = ttk.Label(
            master=frame_label,
            image=im,
        )
        label.image = im
        label.place(x=0, y=0)
        label.pack()
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('1번 스킬 쿨타임(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1'].trace(
            'w', lambda *args: self.skill_cooltime_1(args,
                                                     lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1')
        )
        combobox_list = []
        for i in range(0, 601):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1'] = 10

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_1'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('2번 스킬 쿨타임(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2'].trace(
            'w', lambda *args: self.skill_cooltime_2(args,
                                                     lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2')
        )
        combobox_list = []
        for i in range(0, 601):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2'] = 0

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('3번 스킬 쿨타임(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3'].trace(
            'w', lambda *args: self.skill_cooltime_3(args,
                                                     lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3')
        )
        combobox_list = []
        for i in range(0, 601):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3'] = 0

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_3'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('4번 스킬 쿨타임(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4'].trace(
            'w', lambda *args: self.skill_cooltime_4(args,
                                                     lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4')
        )
        combobox_list = []
        for i in range(0, 601):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4'] = 0

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_4'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('5번 스킬 쿨타임(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5'].trace(
            'w', lambda *args: self.skill_cooltime_5(args,
                                                     lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5')
        )
        combobox_list = []
        for i in range(0, 601):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5'] = 0

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'skill_cooltime_5'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_l, text='아이템 슬롯 셋팅')

        frame = ttk.Frame(frame_label)
        im = Image.open(likeyoubot_configure.LYBConfigure.resource_path("images/item_slot_1.png"))
        if im.size != (240, 58):
            im = im.resize((240, 58), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(im)

        label = ttk.Label(
            master=frame_label,
            image=im,
        )
        label.image = im
        label.place(x=0, y=0)
        label.pack()
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('상급 체력 회복제 쿨타임(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion'].trace(
            'w', lambda *args: self.use_item_premium_potion(args,
                                                            lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion')
        )
        combobox_list = []
        for i in range(0, 601):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion'] = 30

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'use_item_premium_potion'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        # frame = ttk.Frame(frame_label)
        # s = ttk.Style()
        # s.configure('Warning.TLabel', foreground='#ff0000')
        # label = ttk.Label(
        #     master=frame,
        #     text=self.get_option_text('※ 자동 사용 설정된 것만 인식', width=12),
        #     style='Warning.TLabel',
        # )
        # label.pack(side=tkinter.LEFT)
        # frame.pack(anchor=tkinter.W)
        #
        # frame = ttk.Frame(frame_label)
        # im = Image.open(likeyoubot_configure.LYBConfigure.resource_path("images/item_slot_2.png"))
        # if im.size != (240, 58):
        #     im = im.resize((240, 58), Image.ANTIALIAS)
        #     im = ImageTk.PhotoImage(im)
        #
        # label = ttk.Label(
        #     master=frame_label,
        #     image=im,
        # )
        # label.image = im
        # label.place(x=0, y=0)
        # label.pack()
        # frame.pack(anchor=tkinter.W)
        #
        # frame = ttk.Frame(frame_label)
        # s = ttk.Style()
        # s.configure('Warning.TLabel', foreground='#ff0000')
        # label = ttk.Label(
        #     master=frame,
        #     text=self.get_option_text('※ 자동 사용 설정된 것만 인식', width=12),
        #     style='Warning.TLabel',
        # )
        # label.pack(side=tkinter.LEFT)
        # frame.pack(anchor=tkinter.W)
        #
        # frame = ttk.Frame(frame_label)
        # im = Image.open(likeyoubot_configure.LYBConfigure.resource_path("images/item_slot_3.png"))
        # if im.size != (240, 58):
        #     im = im.resize((240, 58), Image.ANTIALIAS)
        #     im = ImageTk.PhotoImage(im)
        #
        # label = ttk.Label(
        #     master=frame_label,
        #     image=im,
        # )
        # label.image = im
        # label.place(x=0, y=0)
        # label.pack()
        # frame.pack(anchor=tkinter.W)
        #
        # frame = ttk.Frame(frame_label)
        # im = Image.open(likeyoubot_configure.LYBConfigure.resource_path("images/item_slot_4.png"))
        # if im.size != (240, 58):
        #     im = im.resize((240, 58), Image.ANTIALIAS)
        #     im = ImageTk.PhotoImage(im)
        #
        # label = ttk.Label(
        #     master=frame_label,
        #     image=im,
        # )
        # label.image = im
        # label.place(x=0, y=0)
        # label.pack()
        # frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_label = ttk.LabelFrame(frame_m, text='마을 행동 설정')

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move'].trace(
            'w', lambda *args: self.sell_npc_move(args, lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move'
                                                   ))
        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('매입 상인한테 가서 자동 담기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'sell_npc_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move'].trace(
            'w', lambda *args: self.stash_npc_move(args, lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move'
                                                   ))
        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('창고지기한테 가서 자동 보관', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'stash_npc_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto'].trace(
            'w', lambda *args: self.potion_npc_auto(args, lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto'
                                                    ))
        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('잡화 상인한테 가서 자동 담기', width=1),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 자동 담기 후 마지막 액션

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('잡화 상점 추가 구매', width=2),
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)

        label = ttk.Label(
            master=frame,
            text=self.get_option_text('1.', width=2),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last'].trace(
            'w', lambda *args: self.potion_npc_auto_last(args,
                                                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last')
        )
        combobox_list = [
            '체력 회복제',
            '정령탄',
            '철화살',
            '은화살',
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last'],
            state="readonly",
            height=10,
            width=14,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select'].trace(
            'w', lambda *args: self.potion_npc_auto_last_select(args,
                                                                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select')
        )
        combobox_list = [
            '+10',
            '+100',
            '+1000',
            'Max 49.9%',
            'Max 79.9%'
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select'] = combobox_list[3]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select'],
            state="readonly",
            height=10,
            width=10,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_select'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'] = tkinter.StringVar(
            frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'].trace(
            'w', lambda *args: self.potion_npc_auto_last_count_select(args,
                                                                      lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select')
        )
        combobox_list = []
        for i in range(0, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'] = \
                combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_auto_last_count_select'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('', width=14),
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)
        frame_m.pack(anchor=tkinter.NW)

        # 일반 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['common_tab_frame'])

        # frame_label = ttk.LabelFrame(frame_r, text='아이템 구매 조건 설정')
        # frame = ttk.Frame(frame_label)
        # s = ttk.Style()
        # s.configure('Warning.TLabel', foreground='#ff0000')
        # label = ttk.Label(
        #     master=frame,
        #     text=self.get_option_text('       구매 순서                  구매 조건                 클릭 버튼          횟수'),
        #     style='Warning.TLabel',
        # )
        # label.pack(side=tkinter.LEFT)
        # frame.pack(anchor=tkinter.W)
        #
        # for item_index in range(len(LYBL2M.default_item_list)):
        #     frame = ttk.Frame(frame_label)
        #
        #     label = ttk.Label(
        #         master=frame,
        #         text=self.get_option_text(str(item_index + 1), 2),
        #     )
        #     label.pack(side=tkinter.LEFT)
        #
        #     combobox_list = LYBL2M.item_list
        #     default_item_list = LYBL2M.default_item_list
        #
        #     if item_index == 0:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_0'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_0'].trace(
        #             'w', lambda *args: self.item_name_0(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_0')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_0' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_0'] = default_item_list[item_index]
        #     elif item_index == 1:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_1'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_1'].trace(
        #             'w', lambda *args: self.item_name_1(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_1')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_1' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_1'] = default_item_list[item_index]
        #     elif item_index == 2:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_2'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_2'].trace(
        #             'w', lambda *args: self.item_name_2(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_2')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_2' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_2'] = default_item_list[item_index]
        #     elif item_index == 3:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_3'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_3'].trace(
        #             'w', lambda *args: self.item_name_3(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_3')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_3' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_3'] = default_item_list[item_index]
        #     elif item_index == 4:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_4'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_4'].trace(
        #             'w', lambda *args: self.item_name_4(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_4')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_4' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_4'] = default_item_list[item_index]
        #     elif item_index == 5:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_5'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_5'].trace(
        #             'w', lambda *args: self.item_name_5(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_5')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_5' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_5'] = default_item_list[item_index]
        #     elif item_index == 6:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_6'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_6'].trace(
        #             'w', lambda *args: self.item_name_6(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_6')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_6' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_6'] = default_item_list[item_index]
        #     elif item_index == 7:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_7'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_7'].trace(
        #             'w', lambda *args: self.item_name_7(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_7')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_7' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_7'] = default_item_list[item_index]
        #     elif item_index == 8:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_8'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_8'].trace(
        #             'w', lambda *args: self.item_name_8(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_8')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_8' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_8'] = default_item_list[item_index]
        #     elif item_index == 9:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_9'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_9'].trace(
        #             'w', lambda *args: self.item_name_9(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_9')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_9' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_9'] = default_item_list[item_index]
        #     elif item_index == 10:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_10'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_10'].trace(
        #             'w', lambda *args: self.item_name_10(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_10')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_10' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_10'] = default_item_list[item_index]
        #     elif item_index == 11:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_11'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_11'].trace(
        #             'w', lambda *args: self.item_name_11(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_11')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_11' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_11'] = default_item_list[item_index]
        #     elif item_index == 12:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_12'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_12'].trace(
        #             'w', lambda *args: self.item_name_12(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_12')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_12' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_12'] = default_item_list[item_index]
        #     elif item_index == 13:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_13'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_13'].trace(
        #             'w', lambda *args: self.item_name_13(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_13')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_13' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_13'] = default_item_list[item_index]
        #
        #     combobox = ttk.Combobox(
        #         master=frame,
        #         values=combobox_list,
        #         textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(item_index)],
        #         state="readonly",
        #         height=10,
        #         width=17,
        #         font=lybconstant.LYB_FONT
        #     )
        #     combobox.set(self.configure.common_config[self.game_name][
        #                      lybconstant.LYB_DO_STRING_L2M_ETC + 'item_name_' + str(item_index)])
        #     combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        #
        #     label = ttk.Label(
        #         master=frame,
        #         text=self.get_option_text('      보유량 <', 7),
        #     )
        #     label.pack(side=tkinter.LEFT)
        #
        #     combobox_list = [
        #         '0',
        #         '10',
        #         '100',
        #         '1000',
        #         '10000',
        #     ]
        #
        #     if item_index == 0:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_0'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_0'].trace(
        #             'w', lambda *args: self.item_cond_0(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_0')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_0' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_0'] = combobox_list[4]
        #     elif item_index == 1:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_1'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_1'].trace(
        #             'w', lambda *args: self.item_cond_1(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_1')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_1' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_1'] = combobox_list[1]
        #     elif item_index == 2:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_2'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_2'].trace(
        #             'w', lambda *args: self.item_cond_2(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_2')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_2' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_2'] = combobox_list[1]
        #     elif item_index == 3:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_3'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_3'].trace(
        #             'w', lambda *args: self.item_cond_3(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_3')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_3' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_3'] = combobox_list[1]
        #     elif item_index == 4:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_4'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_4'].trace(
        #             'w', lambda *args: self.item_cond_4(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_4')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_4' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_4'] = combobox_list[4]
        #     elif item_index == 5:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_5'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_5'].trace(
        #             'w', lambda *args: self.item_cond_5(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_5')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_5' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_5'] = combobox_list[1]
        #     elif item_index == 6:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_6'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_6'].trace(
        #             'w', lambda *args: self.item_cond_6(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_6')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_6' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_6'] = combobox_list[1]
        #     elif item_index == 7:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_7'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_7'].trace(
        #             'w', lambda *args: self.item_cond_7(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_7')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_7' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_7'] = combobox_list[1]
        #     elif item_index == 8:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_8'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_8'].trace(
        #             'w', lambda *args: self.item_cond_8(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_8')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_8' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_8'] = combobox_list[1]
        #     elif item_index == 9:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_9'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_9'].trace(
        #             'w', lambda *args: self.item_cond_9(args,
        #                                                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_9')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_9' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_9'] = combobox_list[1]
        #     elif item_index == 10:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_10'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_10'].trace(
        #             'w', lambda *args: self.item_cond_10(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_10')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_10' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_10'] = combobox_list[1]
        #     elif item_index == 11:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_11'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_11'].trace(
        #             'w', lambda *args: self.item_cond_11(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_11')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_11' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_11'] = combobox_list[1]
        #     elif item_index == 12:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_12'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_12'].trace(
        #             'w', lambda *args: self.item_cond_12(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_12')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_12' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_12'] = combobox_list[1]
        #     elif item_index == 13:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_13'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_13'].trace(
        #             'w', lambda *args: self.item_cond_13(args,
        #                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_13')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_13' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_13'] = combobox_list[3]
        #
        #     combobox = ttk.Combobox(
        #         master=frame,
        #         values=combobox_list,
        #         textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_' + str(item_index)],
        #         state="readonly",
        #         height=10,
        #         width=7,
        #         font=lybconstant.LYB_FONT
        #     )
        #     combobox.set(self.configure.common_config[self.game_name][
        #                      lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_' + str(item_index)])
        #     combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        #
        #     label = ttk.Label(
        #         master=frame,
        #         text=self.get_option_text('', 5),
        #     )
        #     label.pack(side=tkinter.LEFT)
        #
        #     combobox_list = [
        #         '+10',
        #         '+100',
        #         '+1000',
        #         'Max 49.9%',
        #         'Max 79.9%'
        #     ]
        #     if item_index == 0:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_0'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_0'].trace(
        #             'w', lambda *args: self.item_cond_select_0(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_0')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_0' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_0'] = combobox_list[2]
        #     elif item_index == 1:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_1'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_1'].trace(
        #             'w', lambda *args: self.item_cond_select_1(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_1')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_1' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_1'] = combobox_list[0]
        #     elif item_index == 2:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_2'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_2'].trace(
        #             'w', lambda *args: self.item_cond_select_2(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_2')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_2' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_2'] = combobox_list[0]
        #     elif item_index == 3:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_3'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_3'].trace(
        #             'w', lambda *args: self.item_cond_select_3(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_3')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_3' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_3'] = combobox_list[0]
        #     elif item_index == 4:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_4'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_4'].trace(
        #             'w', lambda *args: self.item_cond_select_4(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_4')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_4' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_4'] = combobox_list[2]
        #     elif item_index == 5:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_5'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_5'].trace(
        #             'w', lambda *args: self.item_cond_select_5(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_5')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_5' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_5'] = combobox_list[0]
        #     elif item_index == 6:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_6'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_6'].trace(
        #             'w', lambda *args: self.item_cond_select_6(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_6')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_6' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_6'] = combobox_list[0]
        #     elif item_index == 7:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_7'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_7'].trace(
        #             'w', lambda *args: self.item_cond_select_7(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_7')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_7' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_7'] = combobox_list[0]
        #     elif item_index == 8:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_8'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_8'].trace(
        #             'w', lambda *args: self.item_cond_select_8(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_8')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_8' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_8'] = combobox_list[0]
        #     elif item_index == 9:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_9'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_9'].trace(
        #             'w', lambda *args: self.item_cond_select_9(args,
        #                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_9')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_9' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_9'] = combobox_list[0]
        #     elif item_index == 10:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_10'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_10'].trace(
        #             'w', lambda *args: self.item_cond_select_10(args,
        #                                                         lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_10')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_10' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_10'] = combobox_list[0]
        #     elif item_index == 11:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_11'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_11'].trace(
        #             'w', lambda *args: self.item_cond_select_11(args,
        #                                                         lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_11')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_11' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_11'] = combobox_list[0]
        #     elif item_index == 12:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_12'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_12'].trace(
        #             'w', lambda *args: self.item_cond_select_12(args,
        #                                                         lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_12')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_12' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_12'] = combobox_list[0]
        #     elif item_index == 13:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_13'] = tkinter.StringVar(frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_13'].trace(
        #             'w', lambda *args: self.item_cond_select_13(args,
        #                                                         lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_13')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_13' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_13'] = combobox_list[3]
        #
        #     combobox = ttk.Combobox(
        #         master=frame,
        #         values=combobox_list,
        #         textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_' + str(item_index)],
        #         state="readonly",
        #         height=10,
        #         width=10,
        #         font=lybconstant.LYB_FONT
        #     )
        #     combobox.set(self.configure.common_config[self.game_name][
        #                      lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_select_' + str(item_index)])
        #     combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        #
        #     label = ttk.Label(
        #         master=frame,
        #         text=self.get_option_text('', 5),
        #     )
        #     label.pack(side=tkinter.LEFT)
        #
        #     combobox_list = []
        #     for i in range(0, 10):
        #         combobox_list.append(str(i))
        #
        #     if item_index == 0:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_0'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_0'].trace(
        #             'w', lambda *args: self.item_cond_count_select_0(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_0')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_0' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_0'] = combobox_list[0]
        #     elif item_index == 1:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_1'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_1'].trace(
        #             'w', lambda *args: self.item_cond_count_select_1(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_1')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_1' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_1'] = combobox_list[5]
        #     elif item_index == 2:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_2'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_2'].trace(
        #             'w', lambda *args: self.item_cond_count_select_2(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_2')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_2' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_2'] = combobox_list[1]
        #     elif item_index == 3:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_3'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_3'].trace(
        #             'w', lambda *args: self.item_cond_count_select_3(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_3')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_3' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_3'] = combobox_list[1]
        #     elif item_index == 4:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_4'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_4'].trace(
        #             'w', lambda *args: self.item_cond_count_select_4(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_4')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_4' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_4'] = combobox_list[5]
        #     elif item_index == 5:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_5'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_5'].trace(
        #             'w', lambda *args: self.item_cond_count_select_5(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_5')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_5' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_5'] = combobox_list[0]
        #     elif item_index == 6:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_6'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_6'].trace(
        #             'w', lambda *args: self.item_cond_count_select_6(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_6')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_6' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_6'] = combobox_list[0]
        #     elif item_index == 7:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_7'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_7'].trace(
        #             'w', lambda *args: self.item_cond_count_select_7(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_7')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_7' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_7'] = combobox_list[0]
        #     elif item_index == 8:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_8'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_8'].trace(
        #             'w', lambda *args: self.item_cond_count_select_8(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_8')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_8' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_8'] = combobox_list[0]
        #     elif item_index == 9:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_9'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_9'].trace(
        #             'w', lambda *args: self.item_cond_count_select_9(args,
        #                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_9')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_9' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_9'] = combobox_list[0]
        #     elif item_index == 10:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_10'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_10'].trace(
        #             'w', lambda *args: self.item_cond_count_select_10(args,
        #                                                               lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_10')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_10' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_10'] = combobox_list[0]
        #     elif item_index == 11:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_11'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_11'].trace(
        #             'w', lambda *args: self.item_cond_count_select_11(args,
        #                                                               lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_11')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_11' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_11'] = combobox_list[0]
        #     elif item_index == 12:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_12'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_12'].trace(
        #             'w', lambda *args: self.item_cond_count_select_12(args,
        #                                                               lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_12')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_12' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_12'] = combobox_list[0]
        #     elif item_index == 13:
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_13'] = tkinter.StringVar(
        #             frame)
        #         self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_13'].trace(
        #             'w', lambda *args: self.item_cond_count_select_13(args,
        #                                                               lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_13')
        #         )
        #         if not lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_13' in self.configure.common_config[
        #             self.game_name]:
        #             self.configure.common_config[self.game_name][
        #                 lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_13'] = combobox_list[1]
        #
        #     combobox = ttk.Combobox(
        #         master=frame,
        #         values=combobox_list,
        #         textvariable=self.option_dic[
        #             lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(item_index)],
        #         state="readonly",
        #         height=10,
        #         width=2,
        #         font=lybconstant.LYB_FONT
        #     )
        #     combobox.set(
        #         self.configure.common_config[self.game_name][
        #             lybconstant.LYB_DO_STRING_L2M_ETC + 'item_cond_count_select_' + str(item_index)])
        #     combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        #
        #     frame.pack(anchor=tkinter.W)
        #
        # frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_r, text='잡화 상점 구매 설정')
        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move'].trace(
            'w', lambda *args: self.potion_npc_move(args, lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move'
                                                    ))
        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('잡화 상인한테 가기', width=27),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_move'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        s = ttk.Style()
        s.configure('Warning.TLabel', foreground='#ff0000')
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('※ 구매할 아이템     클릭 버튼     횟수', width=12),
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 1

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('1.', width=2),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0'].trace(
            'w', lambda *args: self.potion_item_0(args,
                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0')
        )
        combobox_list = [
            '체력 회복제',
            '정령탄',
            '철화살',
            '은화살',
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0'],
            state="readonly",
            height=10,
            width=14,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_0'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0'].trace(
            'w', lambda *args: self.potion_npc_select_0(args,
                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0')
        )
        combobox_list = [
            '+10',
            '+100',
            '+1000',
            'Max 49.9%',
            'Max 79.9%'
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0'] = combobox_list[3]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0'],
            state="readonly",
            height=10,
            width=10,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_0'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0'].trace(
            'w', lambda *args: self.potion_npc_count_select_0(args,
                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0')
        )
        combobox_list = []
        for i in range(0, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0'] = \
                combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_0'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 2

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('2.', width=2),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1'].trace(
            'w', lambda *args: self.potion_item_1(args,
                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1')
        )
        combobox_list = [
            '체력 회복제',
            '정령탄',
            '철화살',
            '은화살',
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1'] = combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1'],
            state="readonly",
            height=10,
            width=14,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_1'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1'].trace(
            'w', lambda *args: self.potion_npc_select_1(args,
                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1')
        )
        combobox_list = [
            '+10',
            '+100',
            '+1000',
            'Max 49.9%',
            'Max 79.9%'
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1'] = combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1'],
            state="readonly",
            height=10,
            width=10,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_1'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1'].trace(
            'w', lambda *args: self.potion_npc_count_select_1(args,
                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1')
        )
        combobox_list = []
        for i in range(0, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_1'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # 3

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('3.', width=2),
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2'].trace(
            'w', lambda *args: self.potion_item_2(args,
                                                  lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2')
        )
        combobox_list = [
            '체력 회복제',
            '정령탄',
            '철화살',
            '은화살',
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2'] = combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2'],
            state="readonly",
            height=10,
            width=14,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_item_2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2'].trace(
            'w', lambda *args: self.potion_npc_select_2(args,
                                                        lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2')
        )
        combobox_list = [
            '+10',
            '+100',
            '+1000',
            'Max 49.9%',
            'Max 79.9%'
        ]

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2'] = combobox_list[2]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2'],
            state="readonly",
            height=10,
            width=10,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_select_2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2'].trace(
            'w', lambda *args: self.potion_npc_count_select_2(args,
                                                              lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2')
        )
        combobox_list = []
        for i in range(0, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2'],
            state="readonly",
            height=10,
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'potion_npc_count_select_2'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('', width=14),
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        # frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)
        frame_label = ttk.LabelFrame(frame_r, text='체크 리스트')

        frame = ttk.Frame(frame_label)
        s = ttk.Style()
        s.configure('Warning.TLabel', foreground='#ff0000')
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('※ 0 : 체크 안함', width=12),
            style='Warning.TLabel',
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('데일리 확인 주기(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period'].trace(
            'w', lambda *args: self.check_daily_period(args,
                                                       lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period')
        )
        combobox_list = []
        for i in range(0, 86401, 600):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period'] = 3600

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'check_daily_period'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('우편함 확인 주기(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period'].trace(
            'w', lambda *args: self.check_mail_period(args,
                                                      lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period')
        )
        combobox_list = []
        for i in range(0, 86401, 600):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period'] = 1200

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period'],
            state="readonly",
            height=10,
            width=9,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_ETC + 'check_mail_period'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # frame_l = ttk.Frame(self.inner_frame_dic['common_tab_frame2'])
        # frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # # 일반 탭 중
        # frame_m = ttk.Frame(self.inner_frame_dic['common_tab_frame2'])
        # frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # # 일반 탭 우
        # frame_r = ttk.Frame(self.inner_frame_dic['common_tab_frame2'])
        # frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 좌측
        frame_l = ttk.Frame(self.inner_frame_dic['work_tab_frame'])

        frame_label = ttk.LabelFrame(frame_l, text='마우스 클릭')
        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text="X 좌표:"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x'].trace(
            'w', lambda *args: self.mouse_click_location_x(args,
                                                           lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x')
        )
        combobox_list = []
        for i in range(1, 640):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x'] = 320

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x'],
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox. \
            set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_x'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text=" "
        )
        label.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text="Y 좌표:"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y'].trace(
            'w', lambda *args: self.mouse_click_location_y(args,
                                                           lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y')
        )
        combobox_list = []
        for i in range(1, 360):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y'] = 100

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y'],
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox. \
            set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'mouse_click_location_y'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text=" "
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=5, pady=5)

        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['work_tab_frame'])

        frame_label = ttk.LabelFrame(frame_m, text='자동 사냥')
        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion'].trace(
            'w', lambda *args: self.auto_go_home_potion(args, lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion'
                                                    ))
        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion'] = True

        check_box = ttk.Checkbutton(
            master=frame,
            text=self.get_option_text('HP 물약 부족시 귀환하기', width=1),
            variable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_go_home_potion'],
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

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration'].trace(
            'w', lambda *args: self.auto_duration(args,
                                                  lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration')
        )
        combobox_list = []
        for i in range(60, 86401, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration'] = 3600

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('절전 모드 체크 주기(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period'].trace(
            'w', lambda *args: self.auto_jeoljeon_period(args,
                                                         lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period')
        )
        combobox_list = []
        for i in range(10, 3601, 5):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period'] = 120

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_period'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('절전 모드 지속 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration'].trace(
            'w', lambda *args: self.auto_jeoljeon_duration(args,
                                                           lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration')
        )
        combobox_list = []
        for i in range(10, 3601, 10):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration'] = 10

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_WORK + 'auto_jeoljeon_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['work_tab_frame'])

        frame_label = ttk.LabelFrame(frame_r, text='지도 이동')
        frame = ttk.Frame(frame_label)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area'].trace(
            'w', lambda *args: self.jido_move_area(args, lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area')
        )
        combobox_list = LYBL2M.area_list

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area'] = \
                combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area'],
            state="readonly",
            height=10,
            width=10,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area'].trace(
            'w', lambda *args: self.jido_move_sub_area(args,
                                                       lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area')
        )

        try:
            area_index = LYBL2M.area_list.index(
                self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_area'])
            combobox_list = LYBL2M.sub_area_list[area_index]
            if not lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area' in self.configure.common_config[
                self.game_name]:
                self.configure.common_config[self.game_name][
                    lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area'] = combobox_list[0]
        except ValueError:
            area_index = 0
            combobox_list = LYBL2M.sub_area_list[area_index]
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area'] = \
                combobox_list[0]

        self.jido_move_sub_area_combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area'],
            state="readonly",
            height=10,
            width=22,
            font=lybconstant.LYB_FONT
        )
        self.jido_move_sub_area_combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area'])
        self.jido_move_sub_area_combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('이동 방식', width=22)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style'].trace(
            'w', lambda *args: self.jido_move_style(args,
                                                       lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style')
        )
        combobox_list = [
            '자동 이동',
            '텔레포트',
        ]

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style'] = combobox_list[1]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style'],
            state="readonly",
            height=10,
            width=12,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_style'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text=self.get_option_text('최대 진행 시간(초)', width=27)
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration'].trace(
            'w', lambda *args: self.jido_move_duration(args,
                                                       lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration')
        )
        combobox_list = []
        for i in range(60, 3600, 60):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration'] = 900

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration'],
            state="readonly",
            height=10,
            width=7,
            font=lybconstant.LYB_FONT
        )
        combobox.set(self.configure.common_config[self.game_name][
                         lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_duration'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

        frame_label = ttk.LabelFrame(frame_r, text='캐릭터 이동')
        frame = ttk.Frame(frame_label)

        label = ttk.Label(
            master=frame,
            text="방향:"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move'].trace(
            'w', lambda *args: self.character_move(args, lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move')
        )
        combobox_list = LYBL2M.character_move_list

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move'] = combobox_list[0]

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move'],
            # justify 			= tkinter.CENTER,
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text=" "
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(side=tkinter.LEFT, anchor=tkinter.W)

        frame = ttk.Frame(frame_label)
        label = ttk.Label(
            master=frame,
            text="이동 시간(초):"
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time'].trace(
            'w',
            lambda *args: self.character_move_time(args, lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time')
        )

        combobox_list = []
        for i in range(1, 11):
            combobox_list.append(str(i))

        if not lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time'] = 5

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time'],
            state="readonly",
            height=10,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.set(
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_WORK + 'character_move_time'])
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 알림 탭 좌
        frame_l = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])

        frame_label = ttk.LabelFrame(frame_l, text='절전 모드 알림')

        frame = ttk.Frame(frame_label)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion'] = tkinter.BooleanVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion'].trace(
            'w', lambda *args: self.notify_potion(args, lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion')
        )

        if not lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion' in self.configure.common_config[self.game_name]:
            self.configure.common_config[self.game_name][lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion'] = True

        check_box = ttk.Checkbutton(

            master=frame,
            text='물약 부족',
            variable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion'],
            onvalue=True,
            offvalue=False
        )
        check_box.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message'] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message'].trace(
            'w', lambda *args: self.notify_potion_message(args,
                                                          lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message')
        )
        if not lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message' in self.configure.common_config[
            self.game_name]:
            self.configure.common_config[self.game_name][
                lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message'] = ''

        entry = ttk.Entry(
            master=frame,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_L2M_NOTIFY + 'notify_potion_message'],
            width=50,
            font=lybconstant.LYB_FONT
        )

        entry.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W, pady=5)

        frame.pack(side=tkinter.LEFT, anchor=tkinter.W)
        frame_label.pack(anchor=tkinter.NW, padx=5, pady=5)

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

    def mouse_click_location_x(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def mouse_click_location_y(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_jeoljeon_period(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_jeoljeon_duration(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def auto_go_home_potion(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def notify_potion(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def stash_npc_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def sell_npc_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def monitoring(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def check_mail_period(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_item_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_item_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_item_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_select_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_select_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_select_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_count_select_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_count_select_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_count_select_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def notify_potion_message(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_area(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
        new_list = LYBL2M.sub_area_dic[self.option_dic[option_name].get()]

        self.jido_move_sub_area_combobox['values'] = new_list
        try:
            if not self.get_game_config(lybconstant.LYB_DO_STRING_L2M_WORK + 'jido_move_sub_area') in new_list:
                self.jido_move_sub_area_combobox.set(new_list[0])
        except KeyError:
            pass

    def jido_move_sub_area(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def check_daily_period(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def skill_cooltime_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def skill_cooltime_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def skill_cooltime_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def skill_cooltime_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def skill_cooltime_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def use_item_premium_potion(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_0(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_1(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_2(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_3(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_4(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_5(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_6(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_6(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_6(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_6(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_7(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_7(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_7(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_7(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_8(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_8(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_8(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_8(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_9(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_9(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_9(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_9(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_10(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_10(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_10(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_10(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_11(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_11(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_11(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_11(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_12(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_12(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_12(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_12(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_13(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_13(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_13(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_13(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_14(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_14(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_14(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_14(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_15(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_15(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_15(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_15(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_name_16(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_16(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_select_16(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def item_cond_count_select_16(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_auto(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_auto_last(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_auto_last_select(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def potion_npc_auto_last_count_select(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
    
    def character_move(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
        
    def character_move_time(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def jido_move_style(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
