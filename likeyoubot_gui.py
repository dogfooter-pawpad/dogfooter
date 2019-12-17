import tkinter
from tkinter import ttk
import time

import websocket

import likeyoubot_worker
import queue
import pickle
import os
import likeyoubot_message

import likeyoubot_v4 as LYBV4

from likeyoubot_configure import LYBConstant as lybconstant
import datetime
import copy
import webbrowser
import likeyoubot_license
from belfrywidgets import ToolTip
from PIL import Image, ImageTk, ImageGrab
import likeyoubot_rest
import likeyoubot_logger
import traceback
import random
import string
import shutil
import requests

from subprocess import Popen, PIPE

ct = [255, 255, 0]
brightness = int(round(0.299 * ct[0] + 0.587 * ct[1] + 0.114 * ct[2]))
ct_hex = "%02x%02x%02x" % tuple(ct)
bg_colour = '#' + "".join(ct_hex)


def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


class LYBGUI:
    def __init__(self, master, configure, httplogin=None):
        self.master = master
        self.configure = configure
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        try:
            self.log_fp = open(likeyoubot_logger.LYBLogger.logPath)
        except:
            self.logger.error(traceback.format_exc())

        self.rest = httplogin
        self.last_check_telegram = time.time()
        self.last_check_ip = time.time()
        self.last_check_server = 0
        self.master.geometry('%dx%d+%d+%d' % self.configure.getGeometry())

        self.width = self.configure.getGeometry()[0]
        self.height = self.configure.getGeometry()[1]

        # self.master.configure(background='black')
        self.master.title(self.configure.window_title + ' ' + str(lybconstant.LYB_VERSION))

        self.note = ttk.Notebook(self.master,
                                 width=self.width,
                                 height=self.height
                                 )
        self.note.bind('<Button-1>', self.clicked_main_tab)

        self.tab_frame = []
        self.game_frame = {}
        self.game_options = {}
        self.gui_config_dic = {}
        self.option_dic = {}
        self.game_object = {}
        self.monitor_check_point = {}
        self.wlist_stringvar_dic = {}
        self.wlist_stringvar_skip_dic = {}
        self.wlist_combobox_dic = {}
        self.current_work_dic = {}
        self.ready_to_search_queue = []
        self.ready_to_start_queue = []
        self.stop_app_player_list = []
        self.restart_app_player_list = []
        self.restart_app_player_count = 0
        self.restart_app_player_search = False
        self.timeClickedAds = 0
        self.mb_point = None
        self.first_for_ads = True
        self.ws = None
        # --- COMMON TAB

        self.monitor_button_index = [-1, -1, -1, -1, -1]
        # TEST = 'groov', RELEASE = 'flat'
        self.frame_relief = 'flat'
        frame_relief = self.frame_relief

        self.gui_style = ttk.Style()
        # print(self.gui_style.layout("TNotebook.Tab"))
        # self.gui_style.layout("Tab",
        # 	[	('Notebook.tab', {'sticky': 'nswe', 'children':
        # 		[	('Notebook.padding', { 'side': 'top', 'sticky': 'nswe', 'children':
        # 			#[	('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
        # 				[	('Notebook.label', {'side': 'top', 'sticky': ''
        # 				})]
        # 		#	})]
        # 		})]
        # 	})]
        # 	)

        self.gui_style.theme_use('vista')
        self.gui_style.configure('.', font=lybconstant.LYB_FONT)
        self.gui_style.configure("Tab", focuscolor=self.gui_style.configure(".")["background"])
        self.gui_style.configure("TButton", focuscolor=self.gui_style.configure(".")["background"])
        self.gui_style.configure("TCheckbutton", focuscolor=self.gui_style.configure(".")["background"])
        self.tab_frame.append(ttk.Frame(
            master=self.note,
            width=self.width * 0.2 + 10 * lybconstant.LYB_PADDING,
            height=self.height - lybconstant.LYB_PADDING,
            relief=frame_relief
        ))
        self.note.add(self.tab_frame[-1], text='일반')

        # 녹스 창 이름
        # frame = ttk.Frame(self.tab_frame[-1], relief=frame_relief)
        # frame.pack(pady=5)

        # frame = ttk.Frame(
        # 	master 				= self.tab_frame[-1],
        # 	relief 				= frame_relief
        # 	)

        # s = ttk.Style()
        # s.configure('label_0.TLabel', foreground='red')
        # label_begging = ttk.Label(
        # 	master 				= frame,
        # 	text 				= "※ 개발자에게 고마움을 느끼셨다면 홈페이지 광고 한 번 클릭해주세요 → ",
        # 	justify 			= tkinter.LEFT,
        # 	style 				= 'label_0.TLabel'
        # 	# fg='White' if brightness < 120 else 'Black',
        # 	# bg=bg_colour
        # 	)
        # label_begging.pack(side=tkinter.LEFT)

        # s = ttk.Style()
        # s.configure('label_link.TLabel', foreground='blue', font=('굴림체', 9, 'underline'))
        # link_url = "www.dogfooter.com"

        # label_hompage = ttk.Label(
        # 	master 				= frame,
        # 	text 				= link_url,
        # 	justify 			= tkinter.LEFT,
        # 	style 				= 'label_link.TLabel',
        # 	cursor 				= 'hand2'
        # 	# fg='White' if brightness < 120 else 'Black',
        # 	# bg=bg_colour
        # 	)

        # # f = font.Font(label_hompage, label_hompage.cget("font"))
        # # f.configure(underline = True)
        # # f.configure(weight='bold')
        # # label_hompage.configure(font=f)

        # label_hompage.pack(side=tkinter.LEFT)
        # label_hompage.bind("<Button-1>", self.callback_hompage)

        # frame.pack(anchor=tkinter.W, fill=tkinter.BOTH)

        # frame = ttk.Frame(self.tab_frame[-1], relief=frame_relief)
        # label_begging = ttk.Label(
        # 	master 				= frame,
        # 	text 				= "※ 소스가 궁금하신 분들은 오른쪽 링크를 클릭하세요                 → ",
        # 	justify 			= tkinter.LEFT
        # 	)
        # label_begging.pack(side=tkinter.LEFT)

        # link_url = "www.bitbucket.org/dogfooter/dogfooter"

        # label_hompage = ttk.Label(
        # 	master 				= frame,
        # 	text 				= link_url,
        # 	justify 			= tkinter.LEFT,
        # 	style 				= 'label_link.TLabel',
        # 	cursor 				= 'hand2'
        # 	)

        # f = font.Font(label_hompage, label_hompage.cget("font"))
        # f.configure(underline = True)
        # f.configure(weight='bold')
        # label_hompage.configure(font=f)

        # label_hompage.pack(side=tkinter.LEFT)
        # label_hompage.bind("<Button-1>", self.callbac_bitbucket)

        # frame.pack(anchor=tkinter.W, fill=tkinter.BOTH, pady=5)

        # s = ttk.Style()
        # s.configure('blue_label.TLabel', foreground='blue')

        frame = ttk.Frame(self.tab_frame[-1])
        # self.keyword_label = ttk.Label(
        # 	master 				= frame,
        # 	text 				= "앱 플레이어 창 이름",
        # 	justify 			= tkinter.LEFT,
        # 	style 				= 'blue_label.TLabel'
        # 	)
        # self.keyword_label.pack(side=tkinter.LEFT)

        # self.tooltip(self.keyword_label, lybconstant.LYB_TOOLTIP_APP_TITLE)

        # self.keyword_entry = ttk.Entry(
        # 	master 				= frame,
        # 	# relief 				= 'sunken',
        # 	justify 			= tkinter.LEFT,
        # 	# font				= lybconstant.LYB_FONT,
        # 	width 				= 32
        # 	)
        # self.keyword_entry.pack(side=tkinter.LEFT, padx=10)
        # self.keyword_entry.insert(0, self.configure.keyword)
        # self.keyword_entry.focus()

        label = ttk.Label(
            master=frame,
            text="앱 플레이어: "
        )
        label.pack(side=tkinter.LEFT)

        self.app_player_process = tkinter.StringVar(frame)
        self.app_player_process.set('')
        self.app_player_process.trace('w', lambda *args: self.callback_select_app_player_process_stringvar(args))

        self.app_player_process_list = ttk.Combobox(
            master=frame,
            values=[],
            textvariable=self.app_player_process,
            state="readonly",
            height=20,
            width=30,
            font=lybconstant.LYB_FONT
        )
        self.app_player_process_list.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.keyword_entry = ttk.Entry(
            master=frame,
            justify=tkinter.LEFT,
            font=lybconstant.LYB_FONT,
            width=20
        )
        self.keyword_entry.pack(side=tkinter.LEFT, padx=10)
        self.keyword_entry.insert(0, self.configure.keyword)
        self.tooltip(self.keyword_entry, lybconstant.LYB_TOOLTIP_APP_TITLE)

        s = ttk.Style()
        s.configure('button_0.TButton', font=('굴림체', 9))

        self.search_button = ttk.Button(
            master=frame,
            text="갱신",
            width=10,
            style='button_0.TButton',
            command=lambda: self.searchWindow(None)
        )
        self.search_button.pack(side=tkinter.LEFT, padx=5)

        lybhttp = self.login()
        base_point = lybhttp.get_elem('dogfootermacro_point')
        if base_point is None:
            base_point = 0
        else:
            base_point = int(base_point)

        if int(self.get_mb_point()) >= base_point:
            self.dogfootermacro_button = ttk.Button(
                master=frame,
                text="라이트버전",
                width=10,
                style='button_0.TButton',
                # bg = 'red',
                # fg = 'yellow',
                # relief = 'flat',
                # style				= 'button_dogfootermacro.TButton',
                command=lambda: self.callback_fork_dogfootermacro(None)
            )
            self.dogfootermacro_button.pack(side=tkinter.LEFT, padx=5)

        lybhttp = self.login()
        base_point = lybhttp.get_elem('lybcfg_point')
        if base_point == None:
            base_point = 0
        else:
            base_point = int(base_point)

        if int(self.get_mb_point()) >= base_point:
            # s = ttk.Style()
            # s.configure('button_dogfootermacro.TButton', font=('굴림체', 9, 'bold'), foreground='blue', background='red')

            self.dogfootermacro_button = ttk.Button(
                master=frame,
                text="설정받기",
                width=10,
                style='button_0.TButton',
                # bg = 'red',
                # fg = 'yellow',
                # relief = 'flat',
                # style				= 'button_dogfootermacro.TButton',
                command=lambda: self.callback_download_lybcfg(None)
            )
            self.dogfootermacro_button.pack(side=tkinter.LEFT, padx=5)

        # ads_image = Image.open(resource_path("ads_image.jpg"))
        # # if ads_image.size != (128, 32):
        # # 	ads_image = ads_image.resize((128, 32), Image.ANTIALIAS)
        # ads_image = ImageTk.PhotoImage(ads_image)

        # frame_ads = ttk.Frame(frame)
        # label = ttk.Label(
        # 	master 				= frame_ads,
        # 	image 				= ads_image,
        # 	cursor 				= 'hand2'
        # 	)
        # label.image = ads_image
        # label.place(x=0, y=0)
        # label.pack()
        # label.bind("<Button-1>", self.callback_hompage)
        # frame_ads.pack(fill=tkinter.X, expand=True, anchor=tkinter.E)

        # self.security_authority = False

        # self.keyword_label = ttk.Label(
        # 	master 				= frame,
        # 	text 				= "실행 인증 코드",
        # 	justify 			= tkinter.LEFT,
        # 	font				= lybconstant.LYB_FONT
        # 	)
        # self.keyword_label.pack(side=tkinter.LEFT, padx=10)

        # self.security_code = tkinter.StringVar(frame)
        # security_code_entry = tkinter.Entry(
        # 	master 				= frame,
        # 	relief 				= 'sunken',
        # 	justify 			= tkinter.LEFT,
        # 	font				= lybconstant.LYB_FONT,
        # 	textvariable 		= self.security_code,
        # 	width 				= 32
        # 	)

        # self.security_code.trace(
        # 	'w', lambda *args: self.callback_security_code_stringvar(args)
        # 	)
        # security_code_entry.pack(side=tkinter.LEFT)
        # if not 'security_code' in self.configure.common_config:
        # 	self.configure.common_config['security_code'] = ''
        # security_code_entry.insert(0, self.configure.common_config['security_code'])

        frame.pack(side=tkinter.TOP, pady=5)

        frame_s = ttk.Frame(
            master=self.tab_frame[-1],
            relief=frame_relief
        )
        frame_l = ttk.Frame(frame_s, relief=frame_relief)

        # s = ttk.Style()
        # s.configure('label_1.TLabel', font=('굴림체', 9, 'underline'))

        # self.configure_label = ttk.Label(
        # 	master				= frame_l,
        # 	text 				= lybconstant.LYB_LABEL_SELECT_WINDOW_TEXT,
        # 	style 				= 'label_1.TLabel'
        # 	)
        # self.configure_label.pack(side=tkinter.TOP)

        # label_font = tkinter.font.Font(self.configure_label, self.configure_label.cget('font'))
        # label_font.configure(underline=True)
        # self.configure_label.configure(font=label_font)

        self.gui_config_dic = {}

        self.games = [
            lybconstant.LYB_GAME_V4,
            # lybconstant.LYB_GAME_LIN2REV,
            # lybconstant.LYB_GAME_CLANS,
            # lybconstant.LYB_GAME_YEOLHYUL
        ]
        # 헌드레드 소울
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('hundredsoul_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        #
        # if int(self.get_mb_point()) >= base_point:
        #     self.games.append(lybconstant.LYB_GAME_HUNDREDSOUL)

        # # 검은사막
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('blackdesert_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        #
        # if int(self.get_mb_point()) >= base_point:
        #     self.games.append(lybconstant.LYB_GAME_BLACKDESERT)
        #
        # # 블레이드2
        # base_point = lybhttp.get_elem('blade2_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        # 
        # if int(self.get_mb_point()) >= base_point:
        #     self.games.append(lybconstant.LYB_GAME_BLADE2)
        #
        # # 이카루스
        # base_point = lybhttp.get_elem('icarus_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        #
        # if int(self.get_mb_point()) >= base_point:
        #     self.games.append(lybconstant.LYB_GAME_ICARUS)
        #
        # # TALION
        # base_point = lybhttp.get_elem('talion_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        #
        # if int(self.get_mb_point()) >= base_point:
        #     self.games.append(lybconstant.LYB_GAME_TALION)

        frame_app_player_config = ttk.LabelFrame(frame_l, text='앱 플레이어 설정')
        frame_inner = ttk.Frame(frame_app_player_config)
        frame_game = ttk.Frame(frame_inner)

        s = ttk.Style()
        s.configure('fgWhite_bgGreen.TLabel', foreground='white', background='blue')

        label = ttk.Label(
            master=frame_game,
            text="게임 선택 ☞ ",
            style="fgWhite_bgGreen.TLabel"
        )
        label.pack(side=tkinter.LEFT)

        self.gui_config_dic['games'] = tkinter.StringVar(frame_l)
        if not 'games' in self.configure.common_config:
            self.configure.common_config['games'] = self.games[0]

        self.gui_config_dic['games'].set(self.configure.common_config['games'])
        self.gui_config_dic['games'].trace('w',
                                           lambda *args: self.selected_game(args))

        combobox = ttk.Combobox(
            master=frame_game,
            values=self.games,
            textvariable=self.gui_config_dic['games'],
            state='readonly',
            width=22,
            font=lybconstant.LYB_FONT
        )
        # self.inactive_flag_option_menu.set(inactive_mode_flag_list[0])
        # combobox.configure(stat=tkinter.DISABLED)
        combobox.pack(anchor=tkinter.W, padx=2)
        frame_game.pack(anchor=tkinter.W)

        # option_menu = ttk.OptionMenu(
        # 	frame_l,
        # 	self.gui_config_dic['games'],
        # 	'',
        # 	*self.games,
        # 	command 			= self.selected_game

        # 	)
        # option_menu.configure(width=20)
        # # option_menu.configure(font=lybconstant.LYB_FONT)
        # option_menu.pack(side=tkinter.TOP)

        if not 'multi_account' in self.configure.common_config:
            self.configure.common_config['multi_account'] = False

        # 로컬변수로 선언하면 안된다. 가비지컬렉터한테 먹혀서 안됨.. UI 는 계속 루프를 도니까
        self.gui_config_dic['multi_account'] = tkinter.BooleanVar()
        self.gui_config_dic['multi_account'].set(self.configure.common_config['multi_account'])

        check_box = ttk.Checkbutton(

            master=frame_inner,
            text='구글 멀티 계정 사용',
            variable=self.gui_config_dic['multi_account'],
            onvalue=True,
            offvalue=False,
            command=lambda: self.toggleCommonCheckBox('multi_account')

        )

        check_box.pack(anchor=tkinter.W)

        if not 'debug_booleanvar' in self.configure.common_config:
            self.configure.common_config['debug_booleanvar'] = True

        self.gui_config_dic['debug_booleanvar'] = tkinter.BooleanVar()
        self.gui_config_dic['debug_booleanvar'].set(self.configure.common_config['debug_booleanvar'])

        # check_box = ttk.Checkbutton(

        # 	master 				= frame_l,
        # 	text 				= '디버깅 모드',
        # 	variable 			= self.gui_config_dic['debug_booleanvar'],
        # 	onvalue 			= True,
        # 	offvalue 			= False,
        # 	command 			= lambda: self.toggle_debug_checkbox('debug_booleanvar')

        # 	)

        # check_box.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_inner, relief=frame_relief)
        if not lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE] = True

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE] = tkinter.BooleanVar()
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE])

        check_box = ttk.Checkbutton(

            master=frame,
            text='비활성 모드',
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE],
            onvalue=True,
            offvalue=False,
            command=lambda: self.callback_use_inactive_mode_booleanvar()

        )

        check_box.pack(side=tkinter.LEFT)

        inactive_mode_flag_list = [
            '윈7',
            '윈10'
        ]

        self.gui_config_dic[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG] = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG] = inactive_mode_flag_list[1]
        self.gui_config_dic[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG].set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG])
        self.gui_config_dic[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG].trace('w',
                                                                                lambda
                                                                                    *args: self.callback_inactive_mode_flag_stringvar(
                                                                                    args))
        # self.inactive_flag_option_menu = ttk.OptionMenu(
        # 	frame,
        # 	self.gui_config_dic[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG],
        # 	'',
        # 	*inactive_mode_flag_list,
        # 	command 			= self.callback_inactive_mode_flag_stringvar

        # 	)
        # self.inactive_flag_option_menu.configure(width=4)
        # self.inactive_flag_option_menu.configure(stat=tkinter.DISABLED)
        # # self.inactive_flag_option_menu.configure(font=lybconstant.LYB_FONT)
        # self.inactive_flag_option_menu.pack(side=tkinter.LEFT, anchor=tkinter.SW)
        s = ttk.Style()
        s.map('TCombobox', fieldbackground=[('disabled', '#afafaf')])
        s.map('TCombobox', foreground=[('disabled', '#424242')])

        self.inactive_flag_option_menu = ttk.Combobox(
            master=frame,
            values=inactive_mode_flag_list,
            textvariable=self.gui_config_dic[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG],
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        # self.inactive_flag_option_menu.set(inactive_mode_flag_list[0])
        # self.inactive_flag_option_menu.configure(stat=tkinter.DISABLED)
        self.inactive_flag_option_menu.pack(anchor=tkinter.W, side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_inner, relief=frame_relief)
        if not lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'] = True

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'] = tkinter.BooleanVar()
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'])
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'].trace('w',
                                                                                              lambda
                                                                                                  *args: self.callback_fix_window_location_booleanvar(
                                                                                                  args))

        check_box = ttk.Checkbutton(

            master=frame,
            text='창 고정',
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'],
            onvalue=True,
            offvalue=False

        )

        check_box.pack(side=tkinter.LEFT)

        combobox_list = []
        for i in range(0, 7681):
            combobox_list.append(str(i))

        label = ttk.Label(
            master=frame,
            text="X:"
        )
        label.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'] = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'] = 5
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'])
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'].trace('w',
                                                                                        lambda
                                                                                            *args: self.callback_fix_window_location_x_stringvar(
                                                                                            args))

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'],
            state="readonly",
            height=20,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        combobox_list = []
        for i in range(0, 2161):
            combobox_list.append(str(i))

        label = ttk.Label(
            master=frame,
            text=" Y:"
        )
        label.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'] = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'] = 5
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'])
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'].trace('w',
                                                                                        lambda
                                                                                            *args: self.callback_fix_window_location_y_stringvar(
                                                                                            args))

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'],
            state="readonly",
            height=20,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        self.get_location_window_button = ttk.Button(
            master=frame,
            text="GET",
            width=3,
            style='button_0.TButton',
            command=lambda: self.get_window_location(None)
        )
        self.get_location_window_button.pack(side=tkinter.LEFT, padx=1)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(frame_inner, relief=frame_relief)
        combobox_list = []
        for i in range(1, 6):
            combobox_list.append(str(i))

        label = ttk.Label(
            master=frame,
            text="멀티 플레이어에 설치된 순서:"
        )
        label.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number'] = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number'] = 1
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number'])
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number'].trace('w', lambda
            *args: self.callback_fix_window_location_number_stringvar(
            args))

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number'],
            state="readonly",
            height=20,
            width=1,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(anchor=tkinter.W, side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame_inner.pack(side=tkinter.LEFT, padx=5, pady=3)
        frame_app_player_config.pack(anchor=tkinter.NW, pady=5)
        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=2)

        # frame_c = ttk.Frame(frame_s, relief=frame_relief)
        # ----- WINDOW LIST -----
        # self.search_window = tkinter.Listbox(

        # 	master				= frame_c,
        # 	selectmode			= tkinter.MULTIPLE,
        # 	font				= ("돋움", 10),
        # 	height 				= 8,
        # 	activestyle			= 'none',
        # 	selectbackground	= "#BC80CC"

        # 	)
        # self.search_window.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # self.selected_window_list = []
        # self.search_window.insert('end', '')
        # self.search_window.bind('<<ListboxSelect>>', self.selectedWindowList)
        # self.is_clicked_common_tab = False
        # frame_c.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10)

        frame_r = ttk.Frame(frame_s, relief=frame_relief)
        frame_label = ttk.LabelFrame(
            master=frame_r,
            text='스폰서 광고'
        )

        image1 = Image.open(resource_path("images/skinny_lab_ad_1.jpg"))
        if image1.size != (96, 96):
            image1 = image1.resize((96, 96), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)

        label = ttk.Label(
            master=frame_label,
            image=image1,
            cursor='hand2',
        )
        label.bind("<Button-1>", lambda e, url=r"http://me2.do/xjhbMJcw": self.callback_helper_url(url))
        label.image = image1
        label.place(x=0, y=0)
        label.pack(padx=1, side=tkinter.LEFT)

        image1 = Image.open(resource_path("images/skinny_lab_ad_2.png"))
        if image1.size != (96, 96):
            image1 = image1.resize((96, 96), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)

        label = ttk.Label(
            master=frame_label,
            image=image1,
            cursor='hand2',
        )
        label.bind("<Button-1>", lambda e, url=r"http://me2.do/xjhbMJcw": self.callback_helper_url(url))
        label.image = image1
        label.place(x=0, y=0)
        label.pack(padx=1, side=tkinter.LEFT)

        image1 = Image.open(resource_path("images/skinny_lab_ad_3.png"))
        if image1.size != (96, 96):
            image1 = image1.resize((96, 96), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)

        label = ttk.Label(
            master=frame_label,
            image=image1,
            cursor='hand2',
        )
        label.bind("<Button-1>", lambda e, url=r"http://me2.do/xjhbMJcw": self.callback_helper_url(url))
        label.image = image1
        label.place(x=0, y=0)
        label.pack(padx=1, side=tkinter.LEFT)

        image1 = Image.open(resource_path("images/skinny_lab_ad_4.png"))
        if image1.size != (96, 96):
            image1 = image1.resize((96, 96), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)

        label = ttk.Label(
            master=frame_label,
            image=image1,
            cursor='hand2',
        )
        label.bind("<Button-1>", lambda e, url=r"http://me2.do/xjhbMJcw": self.callback_helper_url(url))
        label.image = image1
        label.place(x=0, y=0)
        label.pack(padx=1, side=tkinter.LEFT)

        image1 = Image.open(resource_path("images/skinny_lab_ad_5.png"))
        if image1.size != (96, 96):
            image1 = image1.resize((96, 96), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)

        label = ttk.Label(
            master=frame_label,
            image=image1,
            cursor='hand2',
        )
        label.bind("<Button-1>", lambda e, url=r"http://me2.do/xjhbMJcw": self.callback_helper_url(url))
        label.image = image1
        label.place(x=0, y=0)
        label.pack()
        # label_font = tkinter.font.Font(label, label.cget('font'))
        # label_font.configure(underline=True)
        # label_font.configure(weight='bold')
        # label.configure(font=label_font)
        # usage_text = tkinter.Text(
        # 	master 				= frame_r,
        # 	spacing1 			= 3,
        # 	height 				= 6,
        # 	font 				= lybconstant.LYB_FONT
        # 	)

        # vsb = tkinter.Scrollbar(
        # 	master 				= usage_text,
        # 	orient 				= 'vertical',
        # 	command 			= usage_text.yview
        # 	)
        # usage_text.configure(yscrollcommand=vsb.set)
        # vsb.pack(side='right', fill='y')

        # hsb = tkinter.Scrollbar(
        # 	master 				= usage_text,
        # 	orient				= 'horizontal',
        # 	command 			= usage_text.xview
        # 	)
        # usage_text.configure(xscrollcommand=hsb.set)
        # hsb.pack(side='bottom', fill='x')

        # usage_text.pack(anchor=tkinter.NW, fill=tkinter.X, expand=True)

        # usage_list = lybconstant.LYB_USAGE.split('\n')

        # lybhttp = self.login()
        # notice_count = int(lybhttp.get_elem('notice_count'))
        # notice_index = int(lybhttp.get_elem('notice_index'))
        # notice_dic = lybhttp.get_notice()

        # self.notice_link_list = []
        # self.notice_subject_list = []
        # i = 0
        # for key, value in notice_dic.items():
        #     label = ttk.Label(
        #         master=frame_label,
        #         text=key,
        #         font=lybconstant.LYB_FONT,
        #         cursor='hand2',
        #         width=17
        #     )
        #     label.pack(anchor=tkinter.NW)
        #
        #     f = font.Font(label, label.cget("font"))
        #     f.configure(underline=True)
        #     label.configure(font=f)
        #     self.notice_subject_list.append(key)
        #     self.notice_link_list.append(value)
        #     if i == 0:
        #         label.bind("<Button-1>", lambda event: self.callback_link_url0(event, url=self.notice_link_list[0]))
        #     elif i == 1:
        #         label.bind("<Button-1>", lambda event: self.callback_link_url1(event, url=self.notice_link_list[1]))
        #     elif i == 2:
        #         label.bind("<Button-1>", lambda event: self.callback_link_url2(event, url=self.notice_link_list[2]))
        #     elif i == 3:
        #         label.bind("<Button-1>", lambda event: self.callback_link_url3(event, url=self.notice_link_list[3]))
        #     elif i == 4:
        #         label.bind("<Button-1>", lambda event: self.callback_link_url3(event, url=self.notice_link_list[4]))
        #     elif i == 5:
        #         label.bind("<Button-1>", lambda event: self.callback_link_url4(event, url=self.notice_link_list[5]))
        #     else:
        #         break
        #
        #     if i == notice_index:
        #         label.configure(foreground='red')
        #
        #     i += 1
        #
        #     if i >= notice_count:
        #         break
        #
        #     # usage_text.insert('end', usage_list)
        #     # for each_usage in usage_list:
        #     # usage_text.insert('end', each_usage + '\n')
        #
        frame_label.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        # frame_inner = ttk.Frame(frame_r)
        # frame_inner.pack(side=tkinter.LEFT, padx=2)
        #
        # self.notice_frame_label = ttk.LabelFrame(
        #     master=frame_r,
        #     text='공지'
        # )
        #
        # frame_notice_text = ttk.Frame(self.notice_frame_label)
        # self.notice_text = tkinter.Text(
        #     master=frame_notice_text,
        #     spacing1=3,
        #     wrap=None,
        #     height=6,
        #     font=lybconstant.LYB_FONT
        # )
        #
        # vsb = tkinter.Scrollbar(
        #     master=frame_notice_text,
        #     orient='vertical',
        #     command=self.notice_text.yview
        # )
        # self.notice_text.configure(yscrollcommand=vsb.set)
        # vsb.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # self.information_scrollbar = ttk.Scrollbar(self.information_frame)
        # self.information.configure(yscrollcommand=self.information_scrollbar.set)
        # self.information_scrollbar.configure(command=self.information.yview)
        # self.information_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # hsb = tkinter.Scrollbar(
        # 	master 				= frame_notice_text,
        # 	orient				= 'horizontal',
        # 	command 			= frame_notice_text.xview
        # 	)
        # frame_notice_text.configure(xscrollcommand=hsb.set)
        # hsb.pack(side='bottom', fill='x')

        # self.notice_text.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        #
        # content_list = lybhttp.get_notice_content(self.notice_link_list[notice_index])
        #
        # # usage_text.insert('end', usage_list)
        # # for each_usage in usage_list:
        # # usage_text.insert('end', each_usage + '\n')
        # for each_line in content_list:
        #     self.notice_text.insert('end', each_line + '\n')
        #
        # frame_notice_text.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        # self.notice_frame_label.pack(anchor=tkinter.NW, side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        #
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        frame_s.pack(anchor=tkinter.NW, fill=tkinter.BOTH, pady=5)

        # - TAB

        # 탭 추가
        self.option_dic['common_tab'] = ttk.Notebook(
            master=self.tab_frame[-1]
        )

        self.option_dic['common_tab'].bind('<Button-1>', self.clicked_common_tab)
        # 모니터링 탭
        self.option_dic['monitoring_tab'] = ttk.Frame(
            master=self.option_dic['common_tab']
        )

        # self.gui_config_dic['monitoring_tab'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['common_tab'].add(self.option_dic['monitoring_tab'], text='모니터링')

        # 공통 설정 탭
        self.option_dic['common_config_tab'] = ttk.Frame(
            master=self.option_dic['common_tab']
        )

        # self.gui_config_dic['common_config_tab'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['common_tab'].add(self.option_dic['common_config_tab'], text='공통 설정')

        # 로그 탭
        # self.option_dic['logging_tab'] = ttk.Frame(
        # 	master 				= self.option_dic['common_tab']
        # 	)
        # self.option_dic['common_tab'].add(self.option_dic['logging_tab'], text='로그')

        self.option_dic['common_tab'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

        self.option_dic['monitor_master'] = ttk.Frame(self.option_dic['monitoring_tab'])

        # frame_label = self.add_monitor_master_frame()

        self.option_dic['monitor_master'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, padx=2, pady=2)

        frame_bottom = ttk.Frame(self.option_dic['monitoring_tab'])
        frame_log = ttk.Frame(frame_bottom)
        # ----- INFORMATION LOGGING ------

        # self.logger.critical('CRITICAL')
        # self.logger.error('ERROR')
        # self.logger.warn('WARN')
        # self.logger.info('INFO')
        # self.logger.debug('DEBUG')

        # frame = ttk.Frame(frame_log)
        # frame.pack(pady=2)
        frame = ttk.Frame(frame_log)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'] = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'] = True
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical']
        )
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'].trace('w',
                                                                                     lambda
                                                                                         *args: self.callback_log_level_critical(
                                                                                         args)
                                                                                     )

        s = ttk.Style(frame)
        s.configure('green_checkbutton.TCheckbutton', foreground='green')
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="필수정보",
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'],
            style='green_checkbutton.TCheckbutton',
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'] = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'] = True
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error']
        )
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'].trace('w',
                                                                                  lambda
                                                                                      *args: self.callback_log_level_error(
                                                                                      args)
                                                                                  )
        s = ttk.Style(frame)
        s.configure('red_checkbutton.TCheckbutton', foreground='red')
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="에러",
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'],
            style='red_checkbutton.TCheckbutton',
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'] = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'] = True
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn']
        )
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'].trace('w',
                                                                                 lambda
                                                                                     *args: self.callback_log_level_warn(
                                                                                     args)
                                                                                 )

        s = ttk.Style(frame)
        s.configure('orange_checkbutton.TCheckbutton', foreground='#f97436')
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="경고",
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'],
            style='orange_checkbutton.TCheckbutton',
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'] = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'] = True
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info']
        )
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'].trace('w',
                                                                                 lambda
                                                                                     *args: self.callback_log_level_info(
                                                                                     args)
                                                                                 )

        checkbutton = ttk.Checkbutton(
            master=frame,
            text="게임정보",
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'],
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'] = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'] = False
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug']
        )
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'].trace('w',
                                                                                  lambda
                                                                                      *args: self.callback_log_level_debug(
                                                                                      args)
                                                                                  )

        checkbutton = ttk.Checkbutton(
            master=frame,
            text="디버깅",
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'],
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text=' '
        )
        label.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text='필터링:'
        )
        label.pack(side=tkinter.LEFT)

        self.log_filter_entry = tkinter.StringVar(frame)
        self.log_filter_entry.trace('w', lambda *args: self.callback_log_filter_entry_stringvar(args))

        self.configure.common_config[lybconstant.LYB_DO_STRING_LOG_FILTER] = ''

        entry = ttk.Entry(
            master=frame,
            textvariable=self.log_filter_entry,
            justify=tkinter.LEFT,
            font=lybconstant.LYB_FONT,
            width=15
        )

        entry.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text=' '
        )
        label.pack(side=tkinter.LEFT)

        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'] = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'] = False
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock']
        )
        self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'].trace('w',
                                                                                 lambda *args: self.callback_log_lock(
                                                                                     args)
                                                                                 )
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="스크롤 잠금",
            variable=self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'],
            onvalue=True,
            offvalue=False
        )
        checkbutton.pack(side=tkinter.LEFT)

        # self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'] = tkinter.BooleanVar(frame)
        # if not lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove' in self.configure.common_config:
        # 	self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'] = False
        # self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'].set(
        # 	self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove']
        # 	)
        # self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'].trace('w',
        # 	lambda *args: self.callback_log_remove(args)
        # 	)
        # checkbutton = ttk.Checkbutton(
        # 	master 				= frame,
        # 	text 				= "로그 파일 자동 삭제",
        # 	variable 			= self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'],
        # 	onvalue 			= True,
        # 	offvalue 			= False
        # 	)
        # checkbutton.pack(side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W, padx=2)

        self.information_frame = ttk.Frame(frame_log)

        self.information = tkinter.Text(
            master=self.information_frame,
            width=90,
            height=25,
            # spacing1 			= 3,
            font=('Consolas', 8),

            # font 				= lybconstant.LYB_FONT
        )
        # self.vsb = tkinter.Scrollbar(self.information_frame,
        # 	orient='vertical',
        # 	command=self.information.yview)
        # self.hsb = tkinter.Scrollbar(self.information_frame,
        # 	orient='horizontal',
        # 	command=self.information.xview)
        # self.information.configure(
        # 	wrap=tkinter.NONE
        # 	)
        # yscrollcommand=self.vsb.set,
        # xscrollcommand=self.hsb.set)
        self.information.tag_configure('FAIL', foreground='red')
        self.information.tag_configure('SUCCESS', foreground='green')
        self.information.tag_configure('GOOD', foreground='#ad42f4')
        self.information.tag_configure('NICE', foreground='#00ad56')
        self.information.tag_configure('SUB', foreground='#d13e83')
        self.information.tag_configure('BAD', foreground='#fcab97')
        # self.information.tag_configure('GOOD', foreground='#ad42f4')
        self.information.tag_configure('INFO', foreground='blue')

        self.information.tag_configure('D', foreground='black')
        self.information.tag_configure('I', foreground='black')
        self.information.tag_configure('E', foreground='red')
        self.information.tag_configure('C', foreground='green')
        self.information.tag_configure('W', foreground='#f97436')

        # self.vsb.pack(side='right', fill='y')
        # self.hsb.pack(side='bottom', fill='x')

        self.information_scrollbar = ttk.Scrollbar(self.information_frame)
        self.information.configure(yscrollcommand=self.information_scrollbar.set)
        self.information_scrollbar.configure(command=self.information.yview)
        self.information_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # self.information_scrollbar_h = ttk.Scrollbar(self.information_frame, orient=tkinter.HORIZONTAL)
        # self.information.configure(xscrollcommand=self.information_scrollbar_h.set)
        # self.information_scrollbar_h.configure(command=self.information.xview)
        # self.information_scrollbar_h.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.information.pack(side=tkinter.BOTTOM)
        self.information_frame.pack(side=tkinter.LEFT, anchor=tkinter.SW, padx=2, pady=2)

        frame_log.pack(side=tkinter.LEFT)
        frame_log = ttk.Frame(frame_bottom)
        s = ttk.Style()
        s.configure('button_1.TButton', justify=tkinter.CENTER)
        s = ttk.Style()
        s.configure('button_homepage.TButton', justify=tkinter.CENTER, background='green')
        s = ttk.Style()
        s.configure('button_kakao.TButton', justify=tkinter.CENTER, background='yellow')

        frame = ttk.Frame(frame_log)
        frame_sub = ttk.LabelFrame(frame, text='바로가기')
        button = ttk.Button(
            master=frame_sub,
            text="홈페이지",
            width=14,
            style='button_homepage.TButton',
            command=lambda: self.callback_homepage(None)
        )
        button.pack()

        # button = ttk.Button(
        #     master=frame_sub,
        #     text="블로그",
        #     width=14,
        #     style='button_homepage.TButton',
        #     command=lambda: self.callback_blog(None)
        # )
        # button.pack()

        # button = ttk.Button(
        #     master=frame_sub,
        #     text="기능명세서",
        #     width=14,
        #     style='button_homepage.TButton',
        #     command=lambda: self.callback_docs(None)
        # )
        # button.pack()

        frame_sub.pack()
        frame_sub = ttk.LabelFrame(frame, text='오픈채팅방')
        # button = ttk.Button(
        #     master=frame_sub,
        #     text="테라M",
        #     width=14,
        #     style='button_kakao.TButton',
        #     command=lambda: self.callback_tera_kakaotalk(None)
        # )
        # button.pack()

        # button = ttk.Button(
        #     master=frame_sub,
        #     text="검은사막M",
        #     width=14,
        #     style='button_kakao.TButton',
        #     command=lambda: self.callback_blackdesert_kakaotalk(None)
        # )
        # button.pack()

        # button = ttk.Button(
        # 	master 				= frame_sub,
        # 	text 				= "카이저",
        # 	width 				= 14,
        # 	style 				= 'button_kakao.TButton',
        # 	command 			= lambda: self.callback_kaiser_kakaotalk(None)
        # 	)
        # button.pack()

        # button = ttk.Button(
        #     master=frame_sub,
        #     text="블레이드2",
        #     width=14,
        #     style='button_kakao.TButton',
        #     command=lambda: self.callback_blade2_kakaotalk(None)
        # )
        # button.pack()
        #
        # button = ttk.Button(
        #     master=frame_sub,
        #     text="이카루스M",
        #     width=14,
        #     style='button_kakao.TButton',
        #     command=lambda: self.callback_icarus_kakaotalk(None)
        # )
        # button.pack()
        #
        # button = ttk.Button(
        #     master=frame_sub,
        #     text="탈리온",
        #     width=14,
        #     style='button_kakao.TButton',
        #     command=lambda: self.callback_talion_kakaotalk(None)
        # )
        # button.pack()

        # button = ttk.Button(
        # 	master 				= frame_sub,
        # 	text 				= "소스보기",
        # 	width 				= 14,
        # 	command 			= lambda: self.callback_bitbucket(None)
        # 	)
        # button.pack()

        frame_sub.pack()
        frame.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=7)
        # ----- BUTTON FRAME -----

        frame_br = ttk.Frame(frame_log)

        login_frame = ttk.LabelFrame(frame_br, text='계정')
        user_account = self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id']
        if len(user_account) > 10:
            user_account = user_account[0:10]

        label = ttk.Label(
            master=login_frame,
            text=user_account
        )
        label.pack()
        login_frame.pack(fill=tkinter.X, padx=2)

        self.mb_point_label = tkinter.StringVar(frame_br)

        login_frame = ttk.LabelFrame(frame_br, text='포인트')
        label = ttk.Label(
            master=login_frame,
            textvariable=self.mb_point_label
        )
        label.pack()
        self.mb_point_label.set(self.get_mb_point())

        # self.mb_ip_label = tkinter.StringVar(frame_bottom)
        # login_frame = ttk.LabelFrame(frame_bottom, text='IP 주소')
        # label = ttk.Label(
        # 	master 				= login_frame,
        # 	textvariable 		= self.mb_ip_label
        # 	)
        # label.pack()
        # self.mb_ip_label.set(self.get_mb_ip())

        login_frame.pack(fill=tkinter.X, padx=2, pady=1)

        login_frame = ttk.LabelFrame(frame_br, text='뒷통수조심')
        self.hide_button = ttk.Button(
            master=login_frame,
            text="숨기기",
            width=14,
            style='button_1.TButton',
            command=lambda: self.callback_hide_window(None, None)
        )

        self.show_button = ttk.Button(
            master=login_frame,
            text="보이기",
            width=14,
            style='button_1.TButton',
            command=lambda: self.callback_show_window(None, None)
        )

        self.hide_button.pack(pady=lybconstant.LYB_PADDING)
        self.show_button.pack(pady=lybconstant.LYB_PADDING)

        login_frame.pack(fill=tkinter.X, padx=2)

        login_frame = ttk.LabelFrame(frame_br, text='텔레그램')
        image1 = Image.open(resource_path("images/t_logo.png"))
        if image1.size != (32, 32):
            image1 = image1.resize((32, 32), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)

        label = ttk.Label(
            master=login_frame,
            image=image1
        )
        label.image = image1
        label.place(x=0, y=0)
        label.pack()
        self.tooltip(label, lybconstant.LYB_TOOLTIP_TELEGRAM)

        self.telegram_entry = tkinter.StringVar(login_frame)
        entry = ttk.Entry(
            master=login_frame,
            textvariable=self.telegram_entry,
            justify=tkinter.LEFT,
            font=lybconstant.LYB_FONT,
            width=15
        )
        entry.pack(anchor=tkinter.W, fill=tkinter.X)
        self.telegram_entry.set('')

        self.telegram_button_label = tkinter.StringVar(login_frame)
        button = ttk.Button(
            master=login_frame,
            textvariable=self.telegram_button_label,
            command=lambda: self.callback_telegram(None)
        )
        button.pack(anchor=tkinter.W, fill=tkinter.X)

        cfg_chat_id = str(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_chat_id'])
        if len(cfg_chat_id) < 3:
            self.telegram_button_label.set('연동하기')
            self.telegram_entry.set(self.generate_token())
            cfg_chat_id = ''
        # entry.select_range(0, tkinter.END)
        else:
            self.telegram_button_label.set('연동해제')

        s = ttk.Style(login_frame)
        s.configure('green_label.TLabel', foreground="green")
        self.telegram_chat_id_label = tkinter.StringVar(login_frame)
        label = ttk.Label(
            master=login_frame,
            textvariable=self.telegram_chat_id_label,
            justify=tkinter.LEFT,
            style='green_label.TLabel'
        )
        label.pack()
        self.telegram_chat_id_label.set(cfg_chat_id)
        login_frame.pack(fill=tkinter.X, padx=2)

        button_frame = ttk.Frame(frame_br)

        self.start_button = ttk.Button(
            master=button_frame,
            text="시작",
            width=14,
            style='button_1.TButton',
            command=lambda: self.startWorkerWrapper(None)
        )

        self.pause_button = ttk.Button(
            master=button_frame,
            text="일시정지",
            width=14,
            style='button_1.TButton',
            command=lambda: self.pauseWorker(None)
        )

        self.stop_button = ttk.Button(
            master=button_frame,
            text="정지",
            width=14,
            style='button_1.TButton',
            command=lambda: self.terminateWorker(None)
        )

        self.start_button.pack(pady=lybconstant.LYB_PADDING)
        self.pause_button.pack(pady=lybconstant.LYB_PADDING)
        self.stop_button.pack(pady=lybconstant.LYB_PADDING)

        button_frame.pack(side=tkinter.BOTTOM, padx=2)

        frame_br.pack(fill=tkinter.BOTH, anchor=tkinter.NW, expand=True, padx=2)
        frame_log.pack(fill=tkinter.BOTH, anchor=tkinter.NW, expand=True)
        frame_bottom.pack(side=tkinter.BOTTOM, anchor=tkinter.NW)

        # ----- CONFIGURATION -----
        self.common_top_frame = ttk.Frame(self.option_dic['common_config_tab'])
        self.configure_frame = ttk.LabelFrame(
            master=self.common_top_frame,
            text='봇 설정'
        )

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)

        threshold_label = ttk.Label(
            master=frame,
            text="이미지를 인식할 때 비교 대상과 ",
            anchor=tkinter.W,
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )

        # countif.place(
        # 	x=lybconstant.LYB_PADDING,
        # 	y=lybconstant.LYB_PADDING,
        # 	width=lybconstant.LYB_LABEL_WIDTH, height=lybconstant.LYB_LABEL_HEIGHT
        # 	)

        threshold_label.pack(side=tkinter.LEFT)

        self.threshold_entry = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.threshold_entry,
            width=3
        )
        entry.pack(side=tkinter.LEFT)

        if not 'threshold_entry' in self.configure.common_config:
            self.configure.common_config['threshold_entry'] = 0.7

        self.threshold_entry.set(str(int(self.configure.common_config['threshold_entry'] * 100)))
        self.threshold_entry.trace('w', lambda *args: self.callback_threshold_entry(args))

        label = ttk.Label(
            master=frame,
            text="% 이상 동일하면 감지하도록 설정합니다",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        label = ttk.Label(
            master=frame,
            text="이미지를 인식할 때 RGB 값의 차이가 ",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        self.pixel_tolerance_entry = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.pixel_tolerance_entry,
            width=3
        )
        entry.pack(side=tkinter.LEFT)

        if not 'pixel_tolerance_entry' in self.configure.common_config:
            self.configure.common_config['pixel_tolerance_entry'] = 30

        self.pixel_tolerance_entry.set(str(int(self.configure.common_config['pixel_tolerance_entry'])))
        self.pixel_tolerance_entry.trace('w', lambda *args: self.callback_pixel_tolerance_entry(args))

        label = ttk.Label(
            master=frame,
            text="이하는 같은 이미지로 간주합니다.",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        label = ttk.Label(
            master=frame,
            text="이미지 인식이 안 될 경우 찾을 때까지 지속적으로",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        self.adjust_entry = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.adjust_entry,
            width=3
        )
        entry.pack(side=tkinter.LEFT)

        if not 'adjust_entry' in self.configure.common_config:
            self.configure.common_config['adjust_entry'] = 1

        self.adjust_entry.set(str(int(self.configure.common_config['adjust_entry'])))
        self.adjust_entry.trace('w', lambda *args: self.callback_adjust_entry(args))

        label = ttk.Label(
            master=frame,
            text="% 씩 가중치를 줍니다",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)
        # frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        label = ttk.Label(
            master=frame,
            text="봇의 작업 주기를 ",
            anchor=tkinter.W,
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )

        # countif.place(
        # 	x=lybconstant.LYB_PADDING,
        # 	y=lybconstant.LYB_PADDING,
        # 	width=lybconstant.LYB_LABEL_WIDTH, height=lybconstant.LYB_LABEL_HEIGHT
        # 	)
        label.pack(side=tkinter.LEFT)

        self.wakeup_period_entry = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.wakeup_period_entry,
            width=6
        )
        entry.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text="초로 설정합니다",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)

        if not 'wakeup_period_entry' in self.configure.common_config:
            self.configure.common_config['wakeup_period_entry'] = float(1.0)

        frame.pack(anchor=tkinter.W)
        self.wakeup_period_entry.set(str(self.configure.common_config['wakeup_period_entry']))
        self.wakeup_period_entry.trace('w', lambda *args: self.callback_wakeup_period_entry(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        label = ttk.Label(
            master=frame,
            text="UI 갱신 주기를 ",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)

        self.update_period_ui_entry = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.update_period_ui_entry,
            width=6
        )
        entry.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text="초로 설정합니다",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        if not lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI] = float(0.5)

        frame.pack(anchor=tkinter.W)
        self.update_period_ui_entry.set(str(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI]))
        self.update_period_ui_entry.trace('w', lambda *args: self.callback_update_period_ui_entry(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        self.use_monitoring_flag = tkinter.BooleanVar(frame)

        label = ttk.Checkbutton(
            master=frame,
            text="모니터링 기능을 사용합니다",
            variable=self.use_monitoring_flag,
            onvalue=True,
            offvalue=False
        )

        label.pack(side=tkinter.LEFT)

        if not lybconstant.LYB_DO_BOOLEAN_USE_MONITORING in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_MONITORING] = True

        frame.pack(anchor=tkinter.W)
        self.use_monitoring_flag.set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_MONITORING]
        )
        self.use_monitoring_flag.trace('w',
                                       lambda *args: self.callback_use_monitoring_booleanvar(args)
                                       )

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)

        label = ttk.Label(
            master=frame,
            text="게임 화면 전환 후",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)
        self.gui_config_dic[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE] = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.gui_config_dic[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE],
            width=3
        )
        entry.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text="초 동안 대기합니다",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)

        if not lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE] = 0

        frame.pack(anchor=tkinter.W)
        self.gui_config_dic[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE].set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE])
        self.gui_config_dic[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE].trace('w', lambda
            *args: self.callback_wait_time_scene_change(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        label = ttk.Label(
            master=frame,
            text="매크로 실행 중 에러가 발생하면 최대",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        self.recovery_count_stringvar = tkinter.StringVar(frame)

        combobox_list = []
        for i in range(10, 1000, 10):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.recovery_count_stringvar,
            state='readonly',
            justify=tkinter.RIGHT,
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text="회 재실행 시킵니다",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)

        if not lybconstant.LYB_DO_STRING_RECOVERY_COUNT in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT] = 999

        frame.pack(anchor=tkinter.W)
        self.recovery_count_stringvar.set(self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT])
        self.recovery_count_stringvar.trace('w', lambda *args: self.callback_recovery_count_stringvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        label = ttk.Label(
            master=frame,
            text="APP 종료 행동을 ",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        self.close_app_stringvar = tkinter.StringVar(frame)
        entry = ttk.Entry(
            master=frame,
            justify=tkinter.RIGHT,
            textvariable=self.close_app_stringvar,
            width=3
        )
        entry.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text="회 실행 시킵니다",
            justify=tkinter.LEFT
            # fg='White' if brightness < 120 else 'Black',
            # bg=bg_colour
        )
        label.pack(side=tkinter.LEFT)

        if not lybconstant.LYB_DO_STRING_CLOSE_APP_COUNT in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_COUNT] = 5

        frame.pack(anchor=tkinter.W)
        self.close_app_stringvar.set(self.configure.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_COUNT])
        self.close_app_stringvar.trace('w', lambda *args: self.callback_close_app_stringvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)

        self.random_click_booleanvar = tkinter.BooleanVar(frame)
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="마우스 랜덤 좌표 클릭(오차 범위:",
            variable=self.random_click_booleanvar,
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)

        self.random_click_pixel_stringvar = tkinter.StringVar(frame)
        combobox_list = []
        for i in range(1, 11):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.random_click_pixel_stringvar,
            state='readonly',
            width=2,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text="픽셀)",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK + 'pixel' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK + 'pixel'] = 5

        self.random_click_pixel_stringvar.set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK + 'pixel'])
        self.random_click_pixel_stringvar.trace('w', lambda *args: self.callback_random_click_pixel_stringvar(args))

        if not lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK] = False
        self.random_click_booleanvar.set(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK])
        self.random_click_booleanvar.trace('w', lambda *args: self.callback_random_click_booleanvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)

        self.random_click_delay_stringvar = tkinter.StringVar(frame)
        label = ttk.Label(
            master=frame,
            text="마우스 클릭 지연 시간(범위 내 랜덤값): ",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        combobox_list = []
        for i in range(1, 11):
            combobox_list.append(i * 0.01)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.random_click_delay_stringvar,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text="초",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_STRING_RANDOM_CLICK_DELAY in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_RANDOM_CLICK_DELAY] = 0.01

        self.random_click_delay_stringvar.set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_RANDOM_CLICK_DELAY])
        self.random_click_delay_stringvar.trace('w', lambda *args: self.callback_random_click_delay_stringvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        self.thumbnail_shortcut_booleanvar = tkinter.BooleanVar(frame)
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="썸네일 단축키로 닫기 활성화",
            variable=self.thumbnail_shortcut_booleanvar,
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'shortcut' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'shortcut'] = True

        self.thumbnail_shortcut_booleanvar.set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'shortcut'])
        self.thumbnail_shortcut_booleanvar.trace('w', lambda *args: self.callback_thumbnail_shortcut_booleanvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        self.thumbnail_width_stringvar = tkinter.StringVar(frame)
        label = ttk.Label(
            master=frame,
            text="썸네일 크기 - 가로 ",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)
        combobox_list = []
        for i in range(10, 1921, 10):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.thumbnail_width_stringvar,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)

        self.thumbnail_height_stringvar = tkinter.StringVar(frame)
        label = ttk.Label(
            master=frame,
            text=" 세로",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        combobox_list = []
        for i in range(10, 1281, 10):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.thumbnail_height_stringvar,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'width' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'width'] = 320
        self.thumbnail_width_stringvar.set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'width'])
        self.thumbnail_width_stringvar.trace('w', lambda *args: self.callback_thumbnail_width_stringvar(args))

        if not lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'height' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'height'] = 180
        self.thumbnail_height_stringvar.set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'height'])
        self.thumbnail_height_stringvar.trace('w', lambda *args: self.callback_thumbnail_height_stringvar(args))

        # self.threshold_entry.place(
        # 	x=lybconstant.LYB_LABEL_WIDTH + 5*lybconstant.LYB_PADDING,
        # 	y=lybconstant.LYB_PADDING,
        # 	width=2*lybconstant.LYB_LABEL_WIDTH - 8*lybconstant.LYB_PADDING,
        # 	height=lybconstant.LYB_LABEL_HEIGHT
        # 	)
        # self.keyword_entry.insert(0, self.configure.keyword)

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        self.mouse_pointer_away_booleanvar = tkinter.BooleanVar(frame)
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="마우스 드래그 실행할 때 강제 커서 치우기(체크 해제시 오동작할 수 있음)",
            variable=self.mouse_pointer_away_booleanvar,
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away'] = True

        self.mouse_pointer_away_booleanvar.set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away'])
        self.mouse_pointer_away_booleanvar.trace('w', lambda *args: self.callback_mouse_pointer_away_booleanvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        self.close_app_nox_new_booleanvar = tkinter.BooleanVar(frame)
        checkbutton = ttk.Checkbutton(
            master=frame,
            text="녹스 최신 버전 사용 중(앱 종료 기능이 구버전과 다름)",
            variable=self.close_app_nox_new_booleanvar,
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_STRING_CLOSE_APP_NOX_NEW in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_NOX_NEW] = True

        self.close_app_nox_new_booleanvar.set(self.configure.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_NOX_NEW])
        self.close_app_nox_new_booleanvar.trace('w', lambda *args: self.callback_close_app_nox_new_booleanvar(args))

        frame = ttk.Frame(self.configure_frame, relief=frame_relief)
        self.freezing_limit_stringvar = tkinter.StringVar(frame)

        label = ttk.Label(
            master=frame,
            text="화면 프리징 감지 제한 시간(0: 사용 안함)",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)

        combobox_list = []
        for i in range(0, 1801):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.freezing_limit_stringvar,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)

        label = ttk.Label(
            master=frame,
            text="초",
            justify=tkinter.LEFT
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        if not lybconstant.LYB_DO_STRING_RECOVERY_COUNT + 'freezing_limit' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT + 'freezing_limit'] = 600

        self.freezing_limit_stringvar.set(
            self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT + 'freezing_limit'])
        self.freezing_limit_stringvar.trace('w', lambda *args: self.callback_freezing_limit_stringvar(args))

        self.configure_frame.pack(anchor=tkinter.NW, side=tkinter.LEFT, padx=5, pady=5)

        label_frame = ttk.LabelFrame(master=self.common_top_frame, text="앱플레이어 재시작 설정")

        frame = ttk.Frame(label_frame)
        self.use_restart_app_player = tkinter.BooleanVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER] = False

        self.use_restart_app_player.set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER])
        self.use_restart_app_player.trace('w',
                                          lambda *args: self.callback_use_restart_app_player_booleanvar(args))

        checkbutton = ttk.Checkbutton(
            master=frame,
            text="앱 플레이어(녹스, 모모) 재시작 기능을 사용합니다",
            variable=self.use_restart_app_player,
            onvalue=True,
            offvalue=False
        )

        checkbutton.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(label_frame)
        label = ttk.Label(
            master=frame,
            text="앱 플레이어 재시작 주기:",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)

        self.use_restart_app_player_period = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'period' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'period'] = 4800

        self.use_restart_app_player_period.set(
            str(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'period']))
        self.use_restart_app_player_period.trace('w',
                                                 lambda *args: self.callback_use_restart_app_player_period_stringvar(
                                                     args))

        combobox_list = []
        for i in range(0, 86401, 5):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.use_restart_app_player_period,
            state='readonly',
            width=6,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='초',
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(label_frame)
        label = ttk.Label(
            master=frame,
            text="앱 플레이어 종료 후 재시작 대기 시간:",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)

        self.restart_app_player_delay = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay'] = 10

        self.restart_app_player_delay.set(
            str(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay']))
        self.restart_app_player_delay.trace('w', lambda *args: self.callback_restart_app_player_delay_stringvar(args))

        combobox_list = []
        for i in range(10, 3601, 5):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.restart_app_player_delay,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='초',
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(label_frame)
        label = ttk.Label(
            master=frame,
            text="앱 플레이어 종료 후 재시작 시도 횟수:",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)

        self.restart_app_player_retry = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'retry' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'retry'] = 5

        self.restart_app_player_retry.set(
            str(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'retry']))
        self.restart_app_player_retry.trace('w', lambda *args: self.callback_restart_app_player_retry_stringvar(args))

        combobox_list = []
        for i in range(1, 101):
            combobox_list.append(i)

        combobox = ttk.Combobox(
            master=frame,
            values=combobox_list,
            textvariable=self.restart_app_player_retry,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='회',
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

        label_frame.pack(anchor=tkinter.NW, padx=5, pady=5)
        self.common_top_frame.pack(anchor=tkinter.NW)

        self.telegram_frame = ttk.LabelFrame(
            master=self.option_dic['common_config_tab'],
            text='텔레그램'
        )

        frame = ttk.Frame(self.telegram_frame)

        if not lybconstant.LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY + 'recovery' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY + 'recovery'] = True

        self.recovery_telegram_checkbox = tkinter.BooleanVar()
        self.recovery_telegram_checkbox.set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY + 'recovery'])
        self.recovery_telegram_checkbox.trace('w',
                                              lambda *args: self.callback_common_telegram_notify_recovery(args))

        check_box = ttk.Checkbutton(

            master=frame,
            text='프로그램 오류 발생 알림',
            variable=self.recovery_telegram_checkbox,
            onvalue=True,
            offvalue=False

        )

        check_box.pack(anchor=tkinter.W)

        frame.pack(anchor=tkinter.W)

        frame = ttk.Frame(self.telegram_frame)
        label = ttk.Label(
            master=frame,
            text="텔레그램 메세지 수신 확인 주기:",
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)

        self.period_telegram_entry = tkinter.StringVar(frame)
        combobox = ttk.Combobox(
            master=frame,
            values=[5, 10, 30, 99999],
            textvariable=self.period_telegram_entry,
            state='readonly',
            width=5,
            font=lybconstant.LYB_FONT
        )
        combobox.pack(side=tkinter.LEFT)
        label = ttk.Label(
            master=frame,
            text='초',
            anchor=tkinter.W,
            justify=tkinter.LEFT
        )

        label.pack(side=tkinter.LEFT)
        if not lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM] = 10

        frame.pack(anchor=tkinter.W)
        self.period_telegram_entry.set(str(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM]))
        self.period_telegram_entry.trace('w', lambda *args: self.callback_period_telegram_entry(args))

        self.telegram_frame.pack(anchor=tkinter.W, padx=5, pady=5)

        self.failover_frame = ttk.LabelFrame(
            master=self.option_dic['common_config_tab'],
            text='비정상 복구'
        )
        self.failover_frame.pack(anchor=tkinter.W, padx=5, pady=5)

        for i in range(len(self.games)):
            self.game_options[self.games[i]] = {}
            self.game_frame[self.games[i]] = {}
            self.tab_frame.append(ttk.Frame(self.note,
                                            width=self.width - lybconstant.LYB_PADDING,
                                            height=self.height - lybconstant.LYB_PADDING,
                                            relief='groove'
                                            ))
            self.note.add(self.tab_frame[i + 1], text='  ' + self.games[i] + '  ')

        # self.configure.common_config[self.games[0]] = {}
        # self.configure.common_config[self.games[0]]['work_list'] = []

        # for each_work in LYBLIN2REV.LYBLineage2Revolution.work_list:
        # 	self.game_options[self.games[0]]['work_list_listbox'].insert('end', each_work)
        # 	self.configure.common_config[self.games[0]]['work_list'].append(each_work)

        self.game_tab_dic = {
        }
        # 다크에덴M

        game_index = 0
        lyb_game_tab = LYBV4.LYBV4Tab(
            self.tab_frame[game_index + 1],
            self.configure,
            self.game_options[self.games[game_index]],
            self.game_frame[self.games[game_index]],
            self.width,
            self.height
        )
        self.game_tab_dic[lybconstant.LYB_GAME_V4] = lyb_game_tab

        # # 헌드레드 소울
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('hundredsoul_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        #
        # if int(self.get_mb_point()) >= base_point:
        #     game_index += 1
        #     lyb_game_tab = LYBHUNDREDSOUL.LYBHundredSoulTab(
        #         self.tab_frame[game_index + 1],
        #         self.configure,
        #         self.game_options[self.games[game_index]],
        #         self.game_frame[self.games[game_index]],
        #         self.width,
        #         self.height
        #     )
        #     self.game_tab_dic[lybconstant.LYB_GAME_HUNDREDSOUL] = lyb_game_tab

        # # 테라M
        #
        # game_index = 0
        # lyb_l2r_tab = LYBTERA.LYBTeraTab(
        #     self.tab_frame[game_index + 1],
        #     self.configure,
        #     self.game_options[self.games[game_index]],
        #     self.game_frame[self.games[game_index]],
        #     self.width,
        #     self.height
        # )
        # self.game_tab_dic[lybconstant.LYB_GAME_TERA] = lyb_l2r_tab
        #
        # # 검은 사막M
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('blackdesert_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        # if int(self.get_mb_point()) >= base_point:
        #     game_index += 1
        #     lyb_game_tab = LYBBLACKDESERT.LYBBlackDesertTab(
        #         self.tab_frame[game_index + 1],
        #         self.configure,
        #         self.game_options[self.games[game_index]],
        #         self.game_frame[self.games[game_index]],
        #         self.width,
        #         self.height
        #     )
        #     self.game_tab_dic[lybconstant.LYB_GAME_BLACKDESERT] = lyb_game_tab
        #
        # # 블레이드2
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('blade2_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        # if int(self.get_mb_point()) >= base_point:
        #     game_index += 1
        #     lyb_game_tab = LYBBLADE2.LYBBlade2Tab(
        #         self.tab_frame[game_index + 1],
        #         self.configure,
        #         self.game_options[self.games[game_index]],
        #         self.game_frame[self.games[game_index]],
        #         self.width,
        #         self.height
        #     )
        #     self.game_tab_dic[lybconstant.LYB_GAME_BLADE2] = lyb_game_tab
        #
        # # 이카루스
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('icarus_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        # if int(self.get_mb_point()) >= base_point:
        #     game_index += 1
        #     lyb_game_tab = LYBICARUS.LYBIcarusTab(
        #         self.tab_frame[game_index + 1],
        #         self.configure,
        #         self.game_options[self.games[game_index]],
        #         self.game_frame[self.games[game_index]],
        #         self.width,
        #         self.height
        #     )
        #     self.game_tab_dic[lybconstant.LYB_GAME_ICARUS] = lyb_game_tab
        #
        # # 탈리온
        # lybhttp = self.login()
        # base_point = lybhttp.get_elem('talion_point')
        # if base_point == None:
        #     base_point = 0
        # else:
        #     base_point = int(base_point)
        # if int(self.get_mb_point()) >= base_point:
        #     game_index += 1
        #     lyb_game_tab = LYBTALION.LYBTalionTab(
        #         self.tab_frame[game_index + 1],
        #         self.configure,
        #         self.game_options[self.games[game_index]],
        #         self.game_frame[self.games[game_index]],
        #         self.width,
        #         self.height
        #     )
        #     self.game_tab_dic[lybconstant.LYB_GAME_TALION] = lyb_game_tab

        # game_index = 1
        # lyb_l2r_tab = LYBLIN2REV.LYBLineage2RevolutionTab(
        # 	self.tab_frame[game_index+1],
        # 	self.configure,
        # 	self.game_options[self.games[game_index]],
        # 	self.game_frame[self.games[game_index]],
        # 	self.width,
        # 	self.height
        # 	)

        # 클랜즈: 달의 그림자

        # game_index += 1
        # lyb_clans_tab = LYBCLANS.LYBClansTab(
        # 	self.tab_frame[game_index+1],
        # 	self.configure,
        # 	self.game_options[self.games[game_index]],
        # 	self.game_frame[self.games[game_index]],
        # 	self.width,
        # 	self.height
        # 	)

        # 열혈강호M

        # game_index += 1
        # lyb_yeolhyul_tab = LYBYEOLHYUL.LYBYeolhyulTab(
        # 	self.tab_frame[game_index+1],
        # 	self.configure,
        # 	self.game_options[self.games[game_index]],
        # 	self.game_frame[self.games[game_index]],
        # 	self.width,
        # 	self.height
        # 	)

        # self.game_options[self.games[0]]['window_list_option_menu'] = tkinter.OptionMenu(

        # 	self.game_frame[self.games[0]]['window_list'],
        # 	self.game_options[self.games[0]]['window_list_stringvar'],
        # 	''

        # 	)

        # self.game_options[self.games[0]]['window_list_stringvar'].trace('w', lambda *args: self.select_window_list(args, game_name=self.games[0]))
        # self.game_options[self.games[0]]['window_list_option_menu'].configure(width=18)
        # self.game_options[self.games[0]]['window_list_option_menu'].pack(side=tkinter.TOP)

        # self.game_frame[self.games[0]]['window_list'].place(

        # 	x  					= 6*lybconstant.LYB_PADDING + self.width*0.5,
        # 	y 					= 2*lybconstant.LYB_PADDING,
        # 	width 				= self.width*0.5 - 10*lybconstant.LYB_PADDING,
        # 	height 				= lybconstant.LYB_BUTTON_HEIGHT

        # 	)

        # -- 워크 리스트 라벨
        # w_name = 'work_list_label'
        # self.game_frame[self.games[0]][w_name] = ttk.Frame(self.tab_frame[-1], relief=frame_relief)
        # self.game_options[self.games[0]][w_name] = ttk.Label(

        # 	master				= self.game_frame[self.games[0]][w_name] ,
        # 	text 				= lybconstant.LYB_LABEL_AVAILABLE_WORK_LIST,
        # 	relief				= 'flat',

        # 	)

        # self.game_options[self.games[0]][w_name].pack(side=tkinter.TOP)
        # self.game_frame[self.games[0]][w_name].place(

        # 	x  					= 2*lybconstant.LYB_PADDING,
        # 	y 					= lybconstant.LYB_BUTTON_HEIGHT + 4*lybconstant.LYB_PADDING,
        # 	width 				= self.width*0.5 - 10*lybconstant.LYB_PADDING,
        # 	height 				= lybconstant.LYB_BUTTON_HEIGHT

        # 	)

        # -- 스케쥴 리스트 라벨
        # w_name = 'schedule_list_label'
        # self.game_frame[self.games[0]][w_name] = ttk.Frame(self.tab_frame[-1], relief=frame_relief)
        # self.game_options[self.games[0]][w_name] = ttk.Label(

        # 	master				= self.game_frame[self.games[0]][w_name] ,
        # 	text 				= lybconstant.LYB_LABEL_SCHEDULE_WORK_LIST,
        # 	relief				= 'flat',

        # 	)
        # self.game_options[self.games[0]][w_name].pack(side=tkinter.TOP)
        # self.game_frame[self.games[0]][w_name].place(

        # 	x  					= 6*lybconstant.LYB_PADDING + self.width*0.5,
        # 	y 					= lybconstant.LYB_BUTTON_HEIGHT + 4*lybconstant.LYB_PADDING,
        # 	width 				= self.width*0.5 - 10*lybconstant.LYB_PADDING,
        # 	height 				= lybconstant.LYB_BUTTON_HEIGHT

        # 	)

        # -- 작업 목록
        # self.game_frame[self.games[0]]['work_list'] = ttk.Frame(self.tab_frame[-1], relief=frame_relief)
        # self.game_options[self.games[0]]['work_list_listbox'] = tkinter.Listbox(

        # 	master				= self.game_frame[self.games[0]]['work_list'],
        # 	font				= ("돋움", 10),
        # 	activestyle			= 'none'

        # 	)
        # self.game_options[self.games[0]]['work_list_listbox'].pack(side=tkinter.TOP)
        # self.game_options[self.games[0]]['work_list_listbox'].bind(
        # 	'<<ListboxSelect>>',
        # 	lambda event: self.select_work_list(event, game_name=self.games[0])
        # 	)

        # self.game_frame[self.games[0]]['work_list'].place(

        # 	x  					= 2 * lybconstant.LYB_PADDING,
        # 	y 					= 2 * lybconstant.LYB_BUTTON_HEIGHT + 4 * lybconstant.LYB_PADDING,
        # 	width 				= self.width*0.5 - 10*lybconstant.LYB_PADDING,
        # 	height 				= self.height*0.4

        # 	)

        # -- 스케쥴 목록
        # self.game_frame[self.games[0]]['schedule_list'] = ttk.Frame(self.tab_frame[-1], relief=frame_relief)
        # self.game_options[self.games[0]]['schedule_list_listbox'] = tkinter.Listbox(

        # 	master				= self.game_frame[self.games[0]]['schedule_list'],
        # 	font				= ("돋움", 10),
        # 	activestyle			= 'none'

        # 	)
        # self.game_options[self.games[0]]['schedule_list_listbox'].pack(side=tkinter.TOP)
        # self.game_options[self.games[0]]['schedule_list_listbox'].bind(
        # 	'<<ListboxSelect>>',
        # 	lambda event: self.select_schedule_list(event, game_name=self.games[0])
        # 	)

        # self.game_frame[self.games[0]]['schedule_list'].place(

        # 	x  					= 6 * lybconstant.LYB_PADDING + self.width * 0.5,
        # 	y 					= 2 * lybconstant.LYB_BUTTON_HEIGHT + 4 * lybconstant.LYB_PADDING,
        # 	width 				= self.width * 0.5 - 10*lybconstant.LYB_PADDING,
        # 	height 				= self.height * 0.4

        # 	)
        # self.configure.common_config[self.games[0]]['schedule_list'] = copy.deepcopy(self.configure.common_config[self.games[0]]['work_list'])

        # for each_work in self.configure.common_config[self.games[0]]['schedule_list']:
        # 	self.game_options[self.games[0]]['schedule_list_listbox'].insert('end', each_work)

        # self.game_frame[self.games[0]]['options'] = ttk.Frame(self.tab_frame[-1], relief=frame_relief)

        # self.game_frame[self.games[0]]['left_option'] = ttk.Frame(
        # 	master 				= self.game_frame[self.games[0]]['options'],
        # 	relief 				= frame_relief
        # 	)
        # self.game_frame[self.games[0]]['left_option'].place(
        # 	x 					= 2 * lybconstant.LYB_PADDING,
        # 	y					= 2 * lybconstant.LYB_PADDING,
        # 	width 				= self.width * 0.5 - 8 * lybconstant.LYB_PADDING,
        # 	height 				= self.height * 0.4 - 4 * lybconstant.LYB_PADDING
        # 	)
        # self.game_frame[self.games[0]]['right_option'] = ttk.Frame(
        # 	master 				= self.game_frame[self.games[0]]['options'],
        # 	relief 				= frame_relief
        # 	)
        # self.game_frame[self.games[0]]['right_option'].place(
        # 	x 					= self.width * 0.5,
        # 	y					= 2 * lybconstant.LYB_PADDING,
        # 	width 				= self.width * 0.5 - 8 * lybconstant.LYB_PADDING,
        # 	height 				= self.height * 0.4 - 4 * lybconstant.LYB_PADDING
        # 	)

        # self.game_frame[self.games[0]]['options'].place(

        # 	x  					= 2 * lybconstant.LYB_PADDING,
        # 	y 					= self.height * 0.5,
        # 	width 				= self.width - 6 * lybconstant.LYB_PADDING,
        # 	height 				= self.height * 0.4 + 10 * lybconstant.LYB_PADDING

        # 	)

        self.note.pack()

        # self.master.bind('<Return>', lambda event, a=0:

        self.master.bind('<Return>', self.searchWindow)
        # self.master.bind('<F1>', self.startWorker)
        # self.master.bind('<F2>', self.pauseWorker)
        # self.master.bind('<F3>', self.terminateWorker)

        # -----------------------------------------------------
        # Thread variable
        # -----------------------------------------------------

        self.workers = []
        self.worker_dic = {}
        self.recovery_count_dic = {}
        self.search_worker = True
        self.start_worker = True
        self.hwnds = {}
        self.side_hwnds = {}
        self.parent_hwnds = {}
        self.multi_hwnds = {}
        self.start_flag = 0
        # self.ready_to_start = False

        self.logger.critical('Successfully initialized')

        self.start_long_polling_worker()
        self.start_websocket_worker()
        self.manage_workers()

    def manage_workers(self):
        # self.information.insert("end", time.ctime() + "\n")
        # self.information.see("end")
        # print('[DEBUG] REMOVE ME:', self.gui_config_dic[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG].get())

        if self.search_worker:
            self.searchWindow(None)
            self.search_worker = False

        if len(self.ready_to_start_queue) > 0:
            for elem in self.ready_to_start_queue:
                self.start_each_worker(elem)
            self.ready_to_start_queue = []

        self.workers = [worker for worker in self.workers if worker.isAlive()]

        # print('Thread count:', threading.activeCount())
        for worker in self.workers:
            while True:
                try:
                    response_message = worker.response_queue.get_nowait()
                    # if worker.response_queue.qsize() < 1:
                    # 	print('task done')
                    worker.response_queue.task_done()
                    self.process_message(worker, response_message)
                except queue.Empty:
                    break
                except:
                    self.logger.error(traceback.format_exc())

        self.update_information()
        # self.update_server_information()

        try:
            self.update_monitor_master()
        except:
            self.logger.error(traceback.format_exc())

        self.update_restart_app_player()

        currentHour = int(datetime.datetime.today().hour)

        if self.first_for_ads == True:
            self.check_ads()
            self.first_for_ads = False
        else:
            if currentHour >= 9 and currentHour < 24 and len(self.workers) > 0:
                if self.check_ads() == False:
                    self.terminateWorker(None)
                    rest = self.login()
                    chat_id = rest.get_chat_id()
                    rest.send_telegram_message(chat_id, '※ 광고가 팝업되면서 프로그램이 중지되었습니다.')

        # self.update_telegram()

        # if self.ready_to_start == True and self.search_flag == True:
        # 	self.startWorker(None)

        try:
            period_update_ui = float(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI]) * 1000
        except:
            period_update_ui = 1000

        # print(period_update_ui)
        self.master.after(int(period_update_ui), self.manage_workers)

    def check_ads(self):

        return True

        rest = self.login()
        ads_interval = int(rest.get_elem('ads_interval'))
        # 한 시간에 한 번만 뜨게, 10초 이상 광고를 보지 않았다면 계속 뜰 것이다!!
        elapsedTimeAdsClicked = time.time() - self.timeClickedAds
        if elapsedTimeAdsClicked > ads_interval:
            ads_file_path = resource_path('dogfooterads.exe')
            if os.path.isfile(ads_file_path) == False:
                ads_file_path = resource_path('dist/dogfooterbot/dogfooterads.exe')
                if os.path.isfile(ads_file_path) == False:
                    self.logger.error('dogfooterads.exe 파일 없음')
                    return False

            if likeyoubot_license.LYBLicense().is_done_ads_info() == False:
                cmd = [
                    resource_path(ads_file_path),
                    "dogfooter"
                ]
                p = Popen(cmd)

                self.logger.critical('하루에 한 번만 하시면 됩니다')
                self.timeClickedAds = time.time()
                return False

            self.timeClickedAds = time.time()

        return True

    def update_restart_app_player(self):
        if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER] == False:
            return

        if (not 'restart_app_player_status' in self.option_dic or
                self.option_dic['restart_app_player_status'] == False):
            self.option_dic['restart_app_player_status'] = False

        if self.option_dic['restart_app_player_status'] == False:
            return

        try:
            # self.logger.warn('self.stop_app_player_list:' + str(self.stop_app_player_list))

            game_object = self.stop_app_player_list.pop(0)
            restart_info = {}
            restart_info['player_type'] = copy.deepcopy(game_object.player_type)
            restart_info['multi_hwnd_dic'] = copy.deepcopy(game_object.multi_hwnd_dic)
            restart_info['window_title'] = copy.deepcopy(game_object.window_title)
            self.restart_app_player_list.append(restart_info)

            window_name = game_object.window_title
            self.logger.warn(window_name + str(' 종료 시도'))

            if window_name in self.game_object:
                # self.logger.warn(window_name + str(' before process_restart_app_player'))
                game_object.process_restart_app_player()
                # self.logger.warn(window_name + str(' after process_restart_app_player'))
                self.restart_app_player_count += 1
                self.terminate_each_worker(window_name)
                self.game_object.pop(window_name)
                # self.logger.warn('DEBUG1: ' + str(self.game_object))
                self.option_dic['restart_app_player_delay'] = time.time()
                self.option_dic['restart_app_player_retry'] = 0
                return
        except:
            pass
        # self.logger.warn('모든 윈도우 종료함')

        period_restart = int(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'period'])
        delay_restart = int(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay'])
        retry_restart = int(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'retry'])

        # self.logger.warn('DEBUG99: [' + str(self.restart_app_player_count) + ':' +str(len(self.game_object)) + ']')
        # self.logger.warn(self.game_object)
        # self.logger.warn('DEBUG35 restart_app_player_search: ' + str(self.restart_app_player_search))

        if self.restart_app_player_count <= len(self.game_object):
            self.restart_app_player_count = 0
            self.option_dic['restart_app_player_status'] = False
            return

        self.logger.warn(
            '재시작 지연 시간: ' + str(int(time.time() - self.option_dic['restart_app_player_delay'])) + ' / ' + str(
                delay_restart) + ' 초')
        # self.logger.warn(self.option_dic['restart_app_player_retry'])

        # 종료된 앱플레이어들이 전부 다시 서치됐는가?
        if self.restart_app_player_search == True:
            self.searchWindow(None)
            if self.restart_app_player_count <= len(self.app_player_process_list['values']):
                self.startWorker(None)
                self.restart_app_player_search = False
            return

        # 앱플레이어를 재실행하는 로직(대기시간이 지났는가?)
        if time.time() - self.option_dic['restart_app_player_delay'] < delay_restart:
            return

        # 앱플레이어를 재실행하라고 워커에게 전달(한 개씩 한개씩)
        # self.logger.warn('DEBUG55 restart_app_player_list:' + str(self.restart_app_player_list))
        if len(self.restart_app_player_list) > 0:
            worker_thread = self.executeThread()
            if worker_thread == None:
                return

            elem = self.restart_app_player_list.pop(0)
            message = []
            message.append(elem['player_type'])
            message.append(elem['multi_hwnd_dic'])
            message.append(elem['window_title'])
            message.append(self.configure)
            worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('start_app_player', message))
            # self.logger.warn('DEBUG12: ' + str(message))
            return

        self.option_dic['restart_app_player_delay'] = time.time()
        self.option_dic['restart_app_player_retry'] += 1

        self.search_worker = True
        self.ready_to_search_queue.append('__all__')

    def check_ip(self):
        rest = self.login()
        if time.time() - self.last_check_ip < int(rest.get_elem('ip_check_period')):
            return

        game_count_sub_title = ""
        for each_game in self.games:
            game_count_on_playing = int(rest.getGameCountOnPlaying(each_game))
            if game_count_on_playing > 0:
                game_count_sub_title += " " + each_game[0] + "(" + str(game_count_on_playing) + ")"

        self.master.title(self.configure.window_title + ' ' + str(
            lybconstant.LYB_VERSION) + ' ' + rest.getConnectCount() + game_count_sub_title)

        self.last_check_ip = time.time()
        base_point = rest.get_elem('ip_free_point')
        # 로그인 요청 보내려고
        self.mb_point = None
        if int(self.get_mb_point()) < int(base_point):
            if rest.is_ip_free() == False:
                self.logger.error('프로그램이 다른 컴퓨터에서 사용 중입니다.')
                # '(포인트 ' + str(self.get_mb_point()) + '점 필요)')
                self.terminateWorker(None)

    def update_telegram(self):
        if time.time() - self.last_check_telegram < int(
                self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM]):
            # if time.time() - self.last_check_telegram < 1:
            return
        self.last_check_telegram = time.time()

        rest = self.login()
        chat_id = rest.get_chat_id()
        if chat_id is None or len(str(chat_id)) == 0:
            return

        update = rest.getTelegramUpdates(chat_id, adjust_time=int(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM]))
        if update is None:
            return

        command = update.message.text
        self.logger.debug('command: ' + str(command))
        self.process_command(command)

    def update_server_information(self):
        if time.time() - self.last_check_server < 60:
            return

        self.last_check_server = time.time()

        game_count_sub_title = ""
        for each_game in self.games:
            game_count_on_playing = int(self.rest.getGameCountOnPlaying(each_game))
            if game_count_on_playing > 0:
                game_count_sub_title += " " + each_game[0] + "(" + str(game_count_on_playing) + ")"

        self.master.title(self.configure.window_title + ' ' + str(
            lybconstant.LYB_VERSION) + ' ' + self.rest.getConnectCount() + game_count_sub_title)

    def update_information(self):

        fp = self.log_fp
        defense_limit = 0
        while True:
            line = fp.readline()
            try:
                last_pos = fp.tell()
            except UnicodeDecodeError:
                continue
            except:
                self.logger.error(traceback.format_exc())
                break

            if line == '':
                break

            fp.seek(last_pos)
            line_split = line.split()
            if len(line_split) > 3:
                debug_level = line.split()[1]
            else:
                debug_level = 'D'

            if debug_level == 'C':
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'] == False:
                    continue
            elif debug_level == 'E':
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'] == False:
                    continue
            elif debug_level == 'W':
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'] == False:
                    continue
            elif debug_level == 'I':
                # try:
                #     self.ws.send(line.split('\n')[0].split('FileInfo')[0])
                # except:
                #     pass
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'] == False:
                    continue
            elif debug_level == 'D':
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'] == False:
                    continue
            else:
                debug_level = 'E'
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'] == False:
                    continue

            if len(self.configure.common_config[lybconstant.LYB_DO_STRING_LOG_FILTER]) > 0:
                if not self.configure.common_config[lybconstant.LYB_DO_STRING_LOG_FILTER] in line:
                    continue

            self.information.insert("end", line.split('\n')[0].split('FileInfo')[0] + '\n', debug_level)
            if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'] == False:
                self.information.see('end')

            defense_limit += 1
            if defense_limit > 1000:
                break

    def process_command(self, command):
        message_to_return = None

        if command is None or command[0] != '/':
            self.logger.error('올바르지 않은 형식의 명령: ' + str(command))
        else:
            rest = self.login()
            base_point = rest.get_elem('telegram_point')
            if base_point is None:
                base_point = 0
            else:
                base_point = int(base_point)

            if int(self.get_mb_point()) < base_point:
                message_to_return = '텔레그램 원격 제어 기능은 ' + str(base_point) + \
                                    ' 포인트 이상 회원들만 사용 가능합니다. 현재 포인트: ' + str(self.get_mb_point())
            else:
                if command.upper() == '/SEARCH' or command.upper() == '/SEA':
                    self.searchWindow(None)
                    message_to_return = '매크로 검색 완료'
                elif command.upper() == '/START' or command.upper() == '/STA':
                    self.startWorker(None)
                    message_to_return = '매크로 시작 완료'
                elif command.upper() == '/STOP' or command.upper() == '/STO':
                    self.terminateWorker(None)
                    message_to_return = '매크로 정지 완료'
                elif command.upper() == '/SS':
                    self.send_screenshot_telegram()
                    message_to_return = '전체 화면 스크린샷 전송 완료'

        if message_to_return is None:
            message_to_return = \
                '지원하지 않는 명령: ' + str(command) + '\n\n' + \
                '도그푸터 지원 명령어 목록:\n\n' + \
                '/SEA(RCH): 검색\n' + \
                '/STA(RT): 시작\n' + \
                '/STO(P): 정지\n' + \
                '/SS: 전체 화면 스크린샷 전송\n\n' \
                '※ 짧은 시간에 너무 많은 명령어를 입력하면 매크로가 중지될 수 있습니다.\n' \
                '※ 명령어 입력 후 응답까지 1 ~ 20초가 걸립니다. 응답이 올 때까지 기다리세요.\n' \
                '※ 명령어 입력 후 응답이 오지 않는다면 전송에 실패 한 것입니다. 다시 입력하세요.\n'

        rest = self.login()
        chat_id = rest.get_chat_id()
        rest.send_telegram_message(chat_id, message_to_return)

    def process_message(self, worker, message):

        if message.type == 'end_return':
            self.logging_message('INFO', message.message + " 작업 종료")
            if message.message != None and len(message.message) > 0 and not message.message in self.worker_dic:
                if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY + 'recovery'] == True:
                    rest = self.login()
                    chat_id = rest.get_chat_id()
                    rest.send_telegram_message(chat_id, '매크로 재실행됨 - ' + str(message.message))

                max_recovery_count = self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT]
                for window_name, worker_thread in self.worker_dic.items():
                    if worker == worker_thread:
                        if not window_name in self.recovery_count_dic:
                            self.recovery_count_dic[window_name] = 0

                        self.logger.warn('매크로 재실행 횟수 - ' + str(self.recovery_count_dic[window_name]) + ' / ' + str(
                            self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT]) + ' 회')

                        if self.recovery_count_dic[window_name] < max_recovery_count:
                            self.update_monitor_master()
                            self.logging_message('INFO',
                                                 "[" + window_name + "] 에서 에러 감지됨. 재실행 합니다." +
                                                 str(self.recovery_count_dic[window_name] + 1) + '/' + str(
                                                     max_recovery_count))
                            self.search_worker = True
                            self.start_worker = True
                            self.ready_to_search_queue.append(window_name)
                            self.recovery_count_dic[window_name] += 1
                            break
                        else:
                            self.recovery_count_dic[window_name] = 0

        elif message.type == 'search_hwnd_return':
            self.hwnds = copy.deepcopy(message.message)
        elif message.type == 'search_side_hwnd_return':
            self.side_hwnds = copy.deepcopy(message.message)
        elif message.type == 'search_parent_hwnd_return':
            self.parent_hwnds = copy.deepcopy(message.message)
        elif message.type == 'search_multi_hwnd_return':
            self.multi_hwnds = copy.deepcopy(message.message)
        elif message.type == 'search_title_return':
            # self.search_window.delete(0, 'end')
            new_app_player_list = []
            if len(message.message) > 0:

                for each_title in message.message:
                    new_app_player_list.append(each_title)
                    if self.start_worker == True:
                        for elem in self.ready_to_search_queue:
                            if elem == '__all__' or elem == each_title:
                                self.ready_to_start_queue.append(each_title)

                    self.logger.critical(str(each_title) + " 검색됨")

                # self.search_window.insert('end', each_title)
                # self.search_window.select_set('end')
                self.ready_to_search_queue = []
                self.start_worker = False

                self.app_player_process_list['values'] = new_app_player_list
                self.app_player_process.set(new_app_player_list[0])
                # self.selectedWindowList(None)
                self.search_flag = True
            else:
                self.app_player_process_list['values'] = []
                self.app_player_process.set('')
                if len(self.configure.keyword) > 0:
                    self.logging_message("FAIL", "[" + self.configure.keyword + "]" + " 단어가 포함된 창 검색 실패")
                self.logging_message("FAIL", "창 사이즈( 960 x 540 ), 창이 최소화 상태인지 확인")
            self.refresh_window_game()
        elif message.type == 'log':
            self.logging_message(None, message.message)
        elif message.type.upper() == 'GOOD':
            self.logging_message("GOOD", message.message)
        elif message.type.upper() == 'BAD':
            self.logging_message("BAD", message.message)
        elif message.type.upper() == 'NICE':
            self.logging_message("NICE", message.message)
        elif message.type.upper() == 'SUB':
            self.logging_message("SUB", message.message)
        elif message.type.upper() == 'INFO':
            self.logging_message("INFO", message.message)
        elif message.type == 'error':
            if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY + 'recovery'] == True:
                rest = self.login()
                chat_id = rest.get_chat_id()
                rest.send_telegram_message(chat_id, '[오류 발생] ' + message.message)

            self.logging_message("FAIL", message.message)
        elif message.type == 'game_object':
            game = message.message
            self.game_object[game.window_title] = game
        elif message.type == 'stop_app':
            game = message.message
            self.option_dic['restart_app_player_status'] = True
            self.stop_app_player_list.append(game)
        # self.terminateWorker(None)
        elif message.type == 'end_start_app_player':
            if len(self.restart_app_player_list) == 0:
                self.restart_app_player_search = True

    def logging_message(self, tag, logging_message):

        if tag == 'GOOD' or tag == 'NICE' or tag == 'SUB' or tag == 'SUCCESS':
            self.logger.info(logging_message)
        elif tag == 'BAD' or tag == 'FAIL':
            self.logger.warn(logging_message)
        else:
            self.logger.debug(logging_message)

        # if len(self.configure.common_config[lybconstant.LYB_DO_STRING_LOG_FILTER]) > 0:
        # 	if not self.configure.common_config[lybconstant.LYB_DO_STRING_LOG_FILTER] in logging_message:
        # 		return

        # if int(self.information.index('end').split('.')[0]) > 1000000:
        #  	self.information.delete(1.0, tkinter.END)

        # self.information.insert("end", "[" + time.strftime("%H:%M:%S") + "] ", tag)
        # self.information.insert("end", logging_message + "\n", tag)
        # self.information.see("end")

    def executeThread(self, is_system=False):

        # if self.configure.common_config['security_code'] != lybconstant.LYB_SECURITY_CODE:
        # 	self.logging_message('FAIL', '실행 인증 코드 [' + self.configure.common_config['security_code'] + '] 거부됨')
        # 	self.security_authority = False
        # 	return None
        # else:
        # 	if self.security_authority == False:
        # 		self.logging_message('SUCCESS', '실행 인증 코드 [' + self.configure.common_config['security_code'] + '] 승인됨')
        # 		self.security_authority = True

        # license_limit = lybconstant.LYB_LICENSE_LIMIT - time.time()

        # 20180210
        # try:
        # 	license_limit = likeyoubot_license.LYBLicense().read_license()
        # 	if license_limit > 0:
        # 		self.logging_message('SUCCESS', str(lybconstant.LYB_VERSION) + ' 라이센스가 ' +
        # 			str(int(license_limit/(24*60*60))) + '일 ' + str(int((license_limit/(60*60))%24)) + '시간 ' + str(int((license_limit/60)%60)) + '분 후에 종료됩니다.')
        # 	else:
        # 		self.logging_message('FAIL', str(lybconstant.LYB_VERSION) + ' 라이센스가 종료 되었습니다. www.dogfooter.com 사이트에서 무료로 새버전을 다운로드 받으세요.')
        # 		return None
        # except:
        # 	self.logging_message('FAIL', str(lybconstant.LYB_VERSION) + ' 라이센스 정보를 찾을 수 없습니다. 라이센스 정보를 www.dogfooter.com 에서 확인하세요.')
        # 	return None

        worker_thread = likeyoubot_worker.LYBWorker('Thread-' + str(self.start_flag), self.configure, queue.Queue(),
                                                    queue.Queue())
        worker_thread.daemon = True
        worker_thread.start()
        if is_system == False:
            self.workers.append(worker_thread)

        return worker_thread

    def startWorkerWrapper(self, e):
        self.logger = likeyoubot_logger.LYBLogger.getLogger(refresh=True)
        self.startWorker(None)

    def startWorker(self, e):

        # if self.ready_to_start == False:
        # 	self.search_flag = False
        # 	self.ready_to_start = True
        # 	self.searchWindow(None)
        # else:

        # for i in range(self.search_window.size()):
        # 	if not self.search_window.get(i) in self.configure.window_config:
        # 		self.configure.window_config[self.search_window.get(i)] = copy.deepcopy(self.configure.common_config)

        # 	for each_config, each_value in self.configure.common_config.items():
        # 		if not each_config in self.configure.window_config[self.search_window.get(i)]:
        # 			self.configure.window_config[self.search_window.get(i)][each_config] = self.configure.common_config[each_config]


        for each_app_player in self.app_player_process_list['values']:
            if not each_app_player in self.configure.window_config:
                self.configure.window_config[each_app_player] = copy.deepcopy(self.configure.common_config)

            for each_config, each_value in self.configure.common_config.items():
                if not each_config in self.configure.window_config[each_app_player]:
                    self.configure.window_config[each_app_player][each_config] = self.configure.common_config[
                        each_config]

            self.start_each_worker(each_app_player)

        # items = map(int, self.search_window.curselection())
        # count = 0
        # for item in items:

        # 	#self.configure.common_config['threshold_entry'] = float(int(self.threshold_entry.get()) / 100)

        # 	# if float(self.pixel_tolerance_entry.get()) >= 50.0:
        # 	# 	self.pixel_tolerance_entry.delete(0, 'end')
        # 	# 	self.pixel_tolerance_entry.insert(0, '50.0')
        # 	# elif float(self.pixel_tolerance_entry.get()) <= 0.0:
        # 	# 	self.pixel_tolerance_entry.delete(0, 'end')
        # 	# 	self.pixel_tolerance_entry.insert(0, '0.0')

        # 	# self.configure.common_config['pixel_tolerance_entry'] = self.pixel_tolerance_entry.get()

        # 	# if int(self.wakeup_period_entry.get()) <= 0:
        # 	# 	self.wakeup_period_entry.set('1')

        # 	# self.configure.common_config['wakeup_period_entry'] = self.wakeup_period_entry.get()

        # 	# if float(self.wait_time_scene_change.get()) <= 0.0:
        # 	# 	self.wait_time_scene_change.delete(0, 'end')
        # 	# 	self.wait_time_scene_change.insert(0, '0')

        # 	# self.configure.common_config[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE] = self.wait_time_scene_change.get()

        # 	self.start_each_worker(self.search_window.get(item))
        # 	count += 1

        # if count == 0:
        # 	self.logging_message('FAIL', '작업을 수행할 창이 선택되지 않았습니다.' )
        # 	# self.ready_to_start = False
        # 	return

        # self.start_button.configure(stat='disabled')
        # self.search_button.configure(stat='disabled')
        # self.keyword_entry.configure(stat='disabled')
        # for i in range(len(self.tab_frame)):
        # 		if i !=0:
        # 			self.note.tab(i, stat='disabled')

        # self.ready_to_start = False

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def start_each_worker(self, window_name):

        if self.check_ads() == False:
            return

        if window_name in self.worker_dic:
            self.logger.debug('start: already started ' + window_name + ' ' + str(self.worker_dic))
            self.logging_message('INFO', window_name + ' 이미 실행 중입니다.')
            return

        try:
            each_hwnd = self.hwnds[window_name]
        except:
            self.logging_message('FAIL', '싱크 오류 발생!! 창을 검색한 후 다시 시작해주세요.')
            return

        self.configure.common_config['threshold_entry'] = float(int(self.threshold_entry.get()) / 100)

        started_window_name = window_name
        started_game_name = self.configure.get_window_config(started_window_name, 'games')
        if started_game_name in self.configure.window_config[started_window_name]:
            started_option = self.configure.get_window_config(started_window_name, started_game_name)
        else:
            started_option = self.configure.common_config[started_game_name]

        started_config = self.configure
        started_window_config = self.configure.window_config[started_window_name]

        # if 'schedule_list' in self.configure.window_config[started_window_name]:
        # 	started_option = self.configure.window_config[started_window_name]['schedule_list']

        worker_thread = self.executeThread()
        if worker_thread == None:
            return

        self.worker_dic[started_window_name] = worker_thread

        side_window_handle = None
        if each_hwnd in self.side_hwnds:
            side_window_handle = self.side_hwnds[each_hwnd]

        parent_window_handle = None
        if each_hwnd in self.parent_hwnds:
            parent_window_handle = self.parent_hwnds[each_hwnd]

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('start',
                                                                             [
                                                                                 self.start_flag,
                                                                                 each_hwnd,
                                                                                 started_window_name,
                                                                                 started_game_name,
                                                                                 started_option,
                                                                                 started_config,
                                                                                 started_window_config,
                                                                                 side_window_handle,
                                                                                 parent_window_handle,
                                                                                 self.multi_hwnds,
                                                                                 self.game_tab_dic[started_game_name],
                                                                             ]
                                                                             )
                                               )
        self.logging_message('INFO', window_name + ' 작업 시작')

        rest = self.login()
        error_message = rest.login()
        self.last_check_server = 0

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def pause_each_worker(self, window_name):
        if not window_name in self.worker_dic:
            self.logger.debug('Not found worker ' + window_name + ' ' + str(self.worker_dic))
            return

        worker = self.worker_dic[window_name]

        if worker.isAlive():
            worker.command_queue.put_nowait(likeyoubot_message.LYBMessage('pause', None))

    def terminate_each_worker(self, window_name):
        if not window_name in self.worker_dic:
            self.logger.debug('DEBUG terminate: Not found worker ' + window_name + ' ' + str(self.worker_dic))
            return

        worker = self.worker_dic[window_name]

        if worker.isAlive():
            worker.command_queue.put_nowait(likeyoubot_message.LYBMessage('end', None))

    def pauseWorker(self, e):
        if len(self.workers) < 1:
            return

        if self.pause_button['text'] == '일시정지':
            self.pause_button.configure(text='다시시작')
        else:
            self.pause_button.configure(text='일시정지')

        for worker in self.workers:
            worker.command_queue.put_nowait(likeyoubot_message.LYBMessage('pause', None))

    def terminateWorker(self, e):
        for worker in self.workers:
            worker.command_queue.put_nowait(likeyoubot_message.LYBMessage('end', None))
        # self.start_button.configure(stat='normal')
        # self.search_button.configure(stat='normal')
        # self.keyword_entry.configure(stat='normal')

        if self.pause_button['text'] != '일시정지':
            self.pause_button.configure(text='일시정지')

        # for i in range(len(self.tab_frame)):
        # 	if i !=0:
        # 		self.note.tab(i, stat='normal')

    def start_long_polling_worker(self):
        worker_thread = self.executeThread(is_system=True)
        if worker_thread is None:
            return

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('long_polling', self))

    def start_websocket_worker(self):


        worker_thread = self.executeThread(is_system=True)
        if worker_thread is None:
            return

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://localhost:18091",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('websocket', self))

    def on_message(self, message):
        self.logger.debug(str(message))

    def on_error(self, error):
        self.logger.error(str(error))

    def on_close(self):
        self.logger.debug("Closed")

    def on_open(self):
        self.logger.debug('onopen')
        self.ws.send('Connected')
        time.sleep(1)

    def get_window_location(self, e):
        worker_thread = self.executeThread()
        if worker_thread is None:
            return

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('GetWindowLocation', self))

    def searchWindow(self, e):
        self.configure.keyword = self.keyword_entry.get()
        self.master.focus()

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

        worker_thread = self.executeThread()
        if worker_thread == None:
            return

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('search', self.configure.window_config))

    def callback_download_lybcfg(self, e):
        dropbox_access_token = self.rest.get_elem('dropbox_access_token')

        file_name = "lyb.cfg.merge"

        try:
            os.remove(resource_path(file_name + '.bak'))
        except FileNotFoundError:
            pass
        except:
            self.logger.error(traceback.format_exc())

        try:
            shutil.move(resource_path(file_name), resource_path(file_name + '.bak'))
        except FileNotFoundError:
            pass
        except:
            self.logger.error(traceback.format_exc())
            self.logger.debug('New file: ' + file_name)

        self.logger.debug(file_name)

        lybcfg_information = self.rest.get_elem('lybcfg')

        self.logger.debug('TEST: ' + str(lybcfg_information))
        path = resource_path(file_name)

        try:
            response = requests.get(lybcfg_information, allow_redirects=True)
            CHUNK_SIZE = 1024
            size = 0
            with open(path, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        size += CHUNK_SIZE
            self.logger.critical("개발자가 사용 중인 설정 파일 다운로드 완료(파일 이름: lyb.cfg.merge)")
            self.logger.critical("프로그램을 재실행하면 반영됩니다")

        except:
            self.logger.error(traceback.format_exc())
            shutil.move(resource_path(file_name + '.bak'), resource_path(file_name))
            return

        try:
            os.remove(resource_path(file_name + '.bak'))
        except:
            self.logger.debug('This is exe file: skip')

    def callback_fork_dogfootermacro(self, e):

        file_path = resource_path('dogfootermacro.exe')
        if os.path.isfile(file_path) is False:
            cmd = [
                'python',
                'dogfootermacro.py',
                "dogfooter"
            ]
            for each_game in self.games:
                cmd.append(each_game)

            p = Popen(cmd)

            return

        self.logger.debug(file_path)
        cmd = [
            resource_path(file_path),
            "dogfooter"
        ]
        for each_game in self.games:
            cmd.append(each_game)

        p = Popen(cmd)

    def callback_fix_window_location_number_stringvar(self, args):
        self.set_config(lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number')

    def callback_fix_window_location_x_stringvar(self, args):
        self.set_config(lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x')

    def callback_fix_window_location_y_stringvar(self, args):
        self.set_config(lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y')

    def callback_fix_window_location_booleanvar(self, args):
        self.set_config(lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean')

    def callback_inactive_mode_flag_stringvar(self, args):
        self.set_config(lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG)

    def callback_use_inactive_mode_booleanvar(self):
        self.set_config(lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE)

    def callback_common_telegram_notify_recovery(self, args):

        self.configure.common_config[
            lybconstant.LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY + 'recovery'] = self.recovery_telegram_checkbox.get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def toggleCommonCheckBox(self, value):
        self.set_config(value)

    def toggle_debug_checkbox(self, value):
        self.set_config(value)

    # def selectedWindowList(self, event):
    # 	# print(self.configure.window_config)
    # 	# print(self.configure.common_config)
    # 	# self.search_window.selection_clear(self.search_window.size() - 1)
    # 	# self.search_window.selection_clear( 0 )
    # 	self.logger.debug('selectedWindowList 1')

    # 	if event != None:
    # 		if self.note.tk.call(self.note._w, "identify", "tab", event.x, event.y) != 0:
    # 			self.logger.debug(str(self.note.tk.call(self.note._w, "identify", "tab", event.x, event.y)))
    # 			return

    # 	if len(self.search_window.curselection()) == 0 and len(self.selected_window_list) > 0 and self.is_clicked_common_tab == True:
    # 		for each_window in self.selected_window_list:
    # 			for i in range(self.search_window.size()):
    # 				if each_window == self.search_window.get(i):
    # 					self.search_window.select_set(i)
    # 		self.is_clicked_common_tab == False
    # 		# 성능상 이슈로 return 추가함
    # 		return

    # 	return
    # 	items = map(int, self.search_window.curselection())
    # 	c_label = ''

    # 	count = 0
    # 	for item in items:

    # 		# if self.search_window.get(item) == '':
    # 		# 	continue
    # 		if not '...' in c_label:
    # 			if not c_label == '':
    # 				c_label += ', '
    # 			if len(c_label + self.search_window.get(item)) > 20:
    # 				c_label += '...'
    # 			else:
    # 				c_label += self.search_window.get(item)
    # 		count += 1

    # 	if c_label == '':
    # 		c_label = lybconstant.LYB_LABEL_SELECT_WINDOW_TEXT
    # 	elif count > 1 and count == self.search_window.size():
    # 		c_label = lybconstant.LYB_LABEL_SELECTED_ALL

    # 	# print('count=', count, 'search_window=', self.search_window.size(), c_label)

    # 	self.configure_label.configure(
    # 		text 				= c_label
    # 		)

    # 	for each_config, each_value in self.gui_config_dic.items():
    # 		is_selected = False
    # 		items = map(int, self.search_window.curselection())

    # 		for item in items:
    # 			is_selected = True
    # 			# if self.search_window.get(item) == '':
    # 			# 	continue
    # 			window_name = self.search_window.get(item)
    # 			if window_name in self.configure.window_config:
    # 				if self.configure.get_window_config(window_name, each_config) != self.gui_config_dic[each_config].get():
    # 					self.gui_config_dic[each_config].set(self.configure.get_window_config(window_name, each_config))

    # 		if is_selected == False:
    # 			if self.configure.common_config[each_config] != self.gui_config_dic[each_config].get():
    # 				self.gui_config_dic[each_config].set(self.configure.common_config[each_config])

    def selected_game(self, args):

        # self.logger.warn(args)
        # if len(self.search_window.curselection()) > 0:
        # 	self.selected_window_list = []
        # 	items = map(int, self.search_window.curselection())
        # 	for i in items:
        # 		self.selected_window_list.append(self.search_window.get(i))
        # self.logger.debug('[DEBUG] 1: ' + str(self.selected_window_list))
        self.set_config('games')

        # self.logger.warn(self.gui_config_dic['games'].get())
        # self.logger.warn(self.configure.get_window_config(self.app_player_process.get(), 'games'))

        # if self.gui_config_dic['games'].get() != self.configure.get_window_config(self.app_player_process.get(), 'games'):
        self.refresh_window_game()

    # self.is_clicked_common_tab = True

    # 이게 왜 있는거지??
    # self.selectedWindowList(None)

    def set_config(self, value):

        # print('[COMMON CONFIG]', value, self.configure.common_config[value])

        # items = map(int, self.search_window.curselection())

        # is_selected = False
        # for item in items:
        # 	is_selected = True
        # 	self.configure.set_window_config(self.search_window.get(item), value, self.gui_config_dic[value].get())

        window_name = self.app_player_process.get()
        if len(window_name) > 0:
            self.configure.set_window_config(window_name, value, self.gui_config_dic[value].get())

        # if is_selected == False:
        # 	# 공통적용
        # 	self.configure.common_config[value] = self.gui_config_dic[value].get()

        # print(self.configure.window_config)
        # print(self.configure.common_config)

        # self.refresh_window_game()

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    # def select_window_list(self, *args, game_name):
    # 	# TODO: 같은 게임안에서 윈도우마다 다르게 설정가능

    # 	selected_window_name = self.game_options[game_name]['window_list_stringvar'].get()
    # 	if len(selected_window_name) > 0:
    # 		if not game_name in self.configure.window_config[selected_window_name]:
    # 			self.configure.window_config[selected_window_name][game_name] = copy.deepcopy(self.configure.common_config[game_name])
    # 			print('DEBUGXX', selected_window_name, game_name, self.configure.window_config[selected_window_name][game_name])

    # 		self.set_game_config(game_name)

    def refresh_window_game(self):

        # self.logger.warn('refresh_window_game')
        # return

        # if self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE].get() == True:
        # 	self.inactive_flag_option_menu.configure(stat=tkinter.NORMAL)
        # else:
        # 	self.inactive_flag_option_menu.configure(stat=tkinter.DISABLED)
        # 사용자가 윈도우를 검색하면 각 게임탭에서 어떤 윈도우에 어떤 게임을 실행할 지에 대한 정보를 채워준다.
        # 게임 탭에서는 게임을 키로 윈도우 리스트를 붙여준다.
        for each_game in self.games:
            if not each_game in self.game_options:
                continue

            # print('DEBUGXX --- 1')
            self.game_options[each_game]['window_list_stringvar'].set('')
            # self.game_options[each_game]['window_list_option_menu']['menu'].delete(0, 'end')
            # print('DEBUGXX --- 1')

            new_window_list = []
            for each_app_player in self.app_player_process_list['values']:
                game_name = self.configure.get_window_config(each_app_player, 'games')
                if each_game == game_name:
                    new_window_list.append(each_app_player)

            # new_window_list = []
            # for i in range(self.search_window.size()):
            # 	game_name = self.configure.get_window_config(self.search_window.get(i), 'games')
            # 	if each_game == game_name:
            # 		new_window_list.append(self.search_window.get(i))

            self.game_options[each_game]['window_list_option_menu']['values'] = new_window_list
            if len(new_window_list) > 0:
                self.game_options[each_game]['window_list_stringvar'].set(new_window_list[0])
            # if len(new_window_list) == 0:
            # 	self.game_options[each_game]['window_list_option_menu']['menu'].add_command(
            # 		label 				= '',
            # 		command 			= tkinter._setit(self.game_options[each_game]['window_list_stringvar'], '')
            # 		)
            # else:
            # 	self.game_options[each_game]['window_list_stringvar'].set(new_window_list[0])
            # 	for each_window in new_window_list:
            # 		self.game_options[each_game]['window_list_option_menu']['menu'].add_command(
            # 			label 				= each_window,
            # 			command 			= tkinter._setit(self.game_options[each_game]['window_list_stringvar'], each_window)
            # 			)

    def get_game_schedule_list(self, game_name):

        window_name = self.game_options[game_name]['window_list_stringvar'].get()

        if len(window_name) > 0:
            if not game_name in self.configure.window_config[window_name]:
                self.configure.window_config[window_name][game_name] = copy.deepcopy(
                    self.configure.common_config[game_name])

            schedule_list = self.configure.window_config[window_name][game_name]['schedule_list']
        else:
            schedule_list = self.configure.common_config[game_name]['schedule_list']

        return schedule_list

    # 리스트박스를 클릭하면 선택되는 거 같다. 그래서 마지막에 공백을 넣었다.
    # def select_work_list(self, event, game_name):
    # 	last_index = self.game_options[game_name]['work_list_listbox'].size() - 1
    # 	self.game_options[game_name]['work_list_listbox'].selection_clear(last_index)

    # 	schedule_list = self.get_game_schedule_list(game_name)

    # 	if len(self.game_options[game_name]['work_list_listbox'].curselection()) > 0:
    # 		item_index = self.game_options[game_name]['work_list_listbox'].curselection()[0]
    # 		# 공백이면 리턴
    # 		if item_index == last_index:
    # 			return

    # 		selected_work_name = self.game_options[game_name]['work_list_listbox'].get(item_index)

    # 		print('DEBUG88:', self.game_options[game_name]['schedule_list_listbox'].size())

    # 		if not selected_work_name in schedule_list:
    # 			#schedule_list.append(selected_work_name)
    # 			schedule_list.insert(len(schedule_list) - 1, selected_work_name)
    # 			self.game_options[game_name]['schedule_list_listbox'].insert(self.game_options[game_name]['schedule_list_listbox'].size() - 1, selected_work_name)

    # def select_schedule_list(self, event, game_name):

    # 	last_index = self.game_options[game_name]['schedule_list_listbox'].size() - 1
    # 	self.game_options[game_name]['schedule_list_listbox'].selection_clear(last_index)

    # 	schedule_list = self.get_game_schedule_list(game_name)

    # 	if len(self.game_options[game_name]['schedule_list_listbox'].curselection()) > 0:
    # 		item_index = self.game_options[game_name]['schedule_list_listbox'].curselection()[0]
    # 		if item_index == last_index:
    # 			return
    # 		selected_schedule_work_name = self.game_options[game_name]['schedule_list_listbox'].get(item_index)
    # 		schedule_list.remove(selected_schedule_work_name)
    # 		self.game_options[game_name]['schedule_list_listbox'].delete(item_index)
    # 		print('DEBUG77:', self.game_options[game_name]['schedule_list_listbox'].size())

    # 	window_name = self.game_options[game_name]['window_list_stringvar'].get()

    # TODO: Game 설정 갱신 함수
    def set_game_config(self, game_name):
        size = self.game_options[game_name]['schedule_list_listbox'].size()
        self.game_options[game_name]['schedule_list_listbox'].delete(0, size - 1)

        schedule_work_list = self.get_game_schedule_list(game_name)

        window_name = self.game_options[game_name]['window_list_stringvar'].get()

        for each_work in schedule_work_list:
            self.game_options[game_name]['schedule_list_listbox'].insert('end', each_work)

    def clicked_main_tab(self, e):
        # self.logger.warn('Main')
        return

    def clicked_common_tab(self, e):
        # self.logger.warn('Common')
        # tab_index = self.option_dic['common_tab'].tk.call(self.option_dic['common_tab']._w, "identify", "tab", e.x, e.y)

        return

    # def clicked_tab(self, event):
    # 	self.logger.debug('clicked_tab')
    # 	s = time.time()
    # 	tab_index = self.note.tk.call(self.note._w, "identify", "tab", event.x, event.y)

    # 	self.is_clicked_common_tab = False
    # 	if tab_index != 0:
    # 		if len(self.search_window.curselection()) > 0:
    # 			self.selected_window_list = []
    # 			items = map(int, self.search_window.curselection())
    # 			for i in items:
    # 				self.selected_window_list.append(self.search_window.get(i))
    # 	else:
    # 		if len(self.selected_window_list) > 0:
    # 			self.is_clicked_common_tab = True
    # 			# 이 부분을 주석 처리하면 선택된 윈도우들이 사라진다. 일단 주석 처리해보자.
    # 			# self.selectedWindowList(None)
    # 	e = time.time()
    # 	self.logger.debug(str(round(e-s,2)))

    def callback_security_code_stringvar(self, args):
        self.logger.debug(self.security_code.get())
        self.configure.common_config['security_code'] = self.security_code.get()

    def callback_reopen_log(self):
        self.information.delete(1.0, tkinter.END)
        if self.log_fp == None:
            self.log_fp = open(likeyoubot_logger.LYBLogger.logPath)
        self.log_fp.seek(0)

    # self.log_fp.close()
    # self.log_fp = open(likeyoubot_logger.LYBLogger.logPath)

    def callback_log_level_critical(self, args):
        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'] = self.gui_config_dic[
            lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical'].get()
        self.callback_reopen_log()
        self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'critical')

    def callback_log_level_error(self, args):
        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'] = self.gui_config_dic[
            lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error'].get()
        self.callback_reopen_log()
        self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'error')

    def callback_log_level_warn(self, args):
        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'] = self.gui_config_dic[
            lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn'].get()
        self.callback_reopen_log()
        self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'warn')

    def callback_log_level_info(self, args):
        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'] = self.gui_config_dic[
            lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info'].get()
        self.callback_reopen_log()
        self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'info')

    def callback_log_level_debug(self, args):
        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'] = self.gui_config_dic[
            lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug'].get()
        self.callback_reopen_log()
        self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'debug')

    def callback_log_lock(self, args):
        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'] = self.gui_config_dic[
            lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock'].get()
        self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'lock')

    # def callback_log_remove(self, args):
    # 	self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'] = self.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'].get()
    # 	try:
    # 		with open(self.configure.path, 'wb') as dat_file:
    # 			pickle.dump(self.configure, dat_file)
    # 	except:
    # 		self.logger.error(traceback.format_exc())
    # 	self.set_config(lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove')

    def callback_homepage(self, event):
        rest = likeyoubot_rest.LYBRest(self.configure.root_url, "", "")
        public_token = rest.get_public_elem("public_token")
        webbrowser.open_new(r"https://pawpad.kr/bbs/" + public_token)

    def callback_helper_url(self, url):
        webbrowser.open_new(url)

    def callback_blog(self, event):
        webbrowser.open_new(r"https://pawpad.kr/bbs/")

    def callback_docs(self, event):
        rest = self.login()
        docs_url = rest.get_elem('docs_url')
        webbrowser.open_new(docs_url)

    def callback_tera_kakaotalk(self, event):
        rest = self.login()
        kakao_url = rest.get_elem('tera_kakao_url')
        webbrowser.open_new(kakao_url)

    def callback_blackdesert_kakaotalk(self, event):
        rest = self.login()
        kakao_url = rest.get_elem('blackdesert_kakao_url')
        webbrowser.open_new(kakao_url)

    def callback_kaiser_kakaotalk(self, event):
        rest = self.login()
        kakao_url = rest.get_elem('kaiser_kakao_url')
        webbrowser.open_new(kakao_url)

    def callback_blade2_kakaotalk(self, event):
        rest = self.login()
        kakao_url = rest.get_elem('blade2_kakao_url')
        webbrowser.open_new(kakao_url)

    def callback_icarus_kakaotalk(self, event):
        rest = self.login()
        kakao_url = rest.get_elem('icarus_kakao_url')
        webbrowser.open_new(kakao_url)

    def callback_talion_kakaotalk(self, event):
        rest = self.login()
        kakao_url = rest.get_elem('talion_kakao_url')
        webbrowser.open_new(kakao_url)

    def callback_bitbucket(self, event):
        webbrowser.open_new(r"https://bitbucket.org/dogfooter/dogfooter/src")

    def callback_link_url0(self, event, url):
        self.common_link_url(url)

    # webbrowser.open_new(url)

    def callback_link_url1(self, event, url):
        self.common_link_url(url)

    # webbrowser.open_new(url)

    def callback_link_url2(self, event, url):
        self.common_link_url(url)

    # webbrowser.open_new(url)

    def callback_link_url3(self, event, url):
        self.common_link_url(url)

    # webbrowser.open_new(url)

    def callback_link_url4(self, event, url):
        self.common_link_url(url)

    # webbrowser.open_new(url)

    def common_link_url(self, url):
        return
        # index = self.notice_link_list.index(url)
        # self.notice_frame_label.configure(text=self.notice_subject_list[index])
        #
        # self.notice_text.delete(1.0, tkinter.END)

        # rest = self.login()
        # # self.logger.warn(self.notice_link_list[index])
        # content_list = rest.get_notice_content(self.notice_link_list[index])
        # for each_line in content_list:
        #     # self.logger.warn(each_line)
        #     self.notice_text.insert('end', each_line + '\n')

    def callback_wakeup_period_entry(self, args):

        try:
            if len(self.wakeup_period_entry.get()) < 0:
                wakeup_period_entry = 0
            else:
                wakeup_period_entry = float(self.wakeup_period_entry.get())

            # if wakeup_period_entry < 0:
            # 	self.wakeup_period_entry.set('0')

            self.configure.common_config['wakeup_period_entry'] = wakeup_period_entry
        except:
            self.configure.common_config['wakeup_period_entry'] = 1.0

        # print(self.configure.common_config['wakeup_period_entry'])

    def callback_restart_app_player_retry_stringvar(self, args):
        self.configure.common_config[
            lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'retry'] = self.restart_app_player_retry.get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_restart_app_player_delay_stringvar(self, args):
        self.configure.common_config[
            lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay'] = self.restart_app_player_delay.get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_use_restart_app_player_period_stringvar(self, args):
        self.configure.common_config[
            lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'period'] = self.use_restart_app_player_period.get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_use_restart_app_player_booleanvar(self, args):
        self.configure.common_config[
            lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER] = self.use_restart_app_player.get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())
        # print(self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_MONITORING])

    def callback_use_monitoring_booleanvar(self, args):
        use_monitoring_flag = self.use_monitoring_flag.get()

        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_MONITORING] = use_monitoring_flag

    def callback_select_app_player_process_stringvar(self, args):
        window_name = self.app_player_process.get()
        # self.logger.warn(window_name)

        for each_config, each_value in self.gui_config_dic.items():

            if window_name in self.configure.window_config:
                if self.configure.get_window_config(window_name, each_config) != self.gui_config_dic[each_config].get():
                    self.gui_config_dic[each_config].set(self.configure.get_window_config(window_name, each_config))
            else:
                if self.configure.common_config[each_config] != self.gui_config_dic[each_config].get():
                    self.gui_config_dic[each_config].set(self.configure.common_config[each_config])

    def callback_period_telegram_entry(self, args):
        self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM] = self.period_telegram_entry.get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_update_period_ui_entry(self, args):

        try:
            if len(self.update_period_ui_entry.get()) < 0:
                update_period_ui = 0
            else:
                update_period_ui = float(self.update_period_ui_entry.get())

            # if update_period_ui < 0:
            # 	self.update_period_ui_entry.set('0')

            self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI] = update_period_ui
        except:
            self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI] = float(1.0)

        # print(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI])

    def callback_random_click_booleanvar(self, args):

        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK] = self.random_click_booleanvar.get()

    def callback_thumbnail_shortcut_booleanvar(self, args):

        self.configure.common_config[
            lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'shortcut'] = self.thumbnail_shortcut_booleanvar.get()

    def callback_mouse_pointer_away_booleanvar(self, args):

        self.configure.common_config[
            lybconstant.LYB_DO_BOOLEAN_MOUSE_POINTER + 'away'] = self.mouse_pointer_away_booleanvar.get()

    def callback_close_app_nox_new_booleanvar(self, args):

        self.configure.common_config[
            lybconstant.LYB_DO_STRING_CLOSE_APP_NOX_NEW] = self.close_app_nox_new_booleanvar.get()

    def callback_random_click_pixel_stringvar(self, args):

        if len(self.random_click_pixel_stringvar.get()) < 1:
            config_value = 0
        else:
            config_value = int(self.random_click_pixel_stringvar.get())

        self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_RANDOM_CLICK + 'pixel'] = config_value

    def callback_random_click_delay_stringvar(self, args):

        if len(self.random_click_delay_stringvar.get()) < 1:
            config_value = 0.05
        else:
            config_value = float(self.random_click_delay_stringvar.get())

        self.configure.common_config[lybconstant.LYB_DO_STRING_RANDOM_CLICK_DELAY] = config_value

    def callback_thumbnail_width_stringvar(self, args):

        if len(self.thumbnail_width_stringvar.get()) < 1:
            config_value = 0
        else:
            config_value = int(self.thumbnail_width_stringvar.get())

        self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'width'] = config_value

    def callback_thumbnail_height_stringvar(self, args):

        if len(self.thumbnail_height_stringvar.get()) < 1:
            config_value = 0
        else:
            config_value = int(self.thumbnail_height_stringvar.get())

        self.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'height'] = config_value

    def callback_freezing_limit_stringvar(self, args):

        if len(self.freezing_limit_stringvar.get()) < 1:
            config_value = 0
        else:
            config_value = int(self.freezing_limit_stringvar.get())

        self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT + 'freezing_limit'] = config_value

    def callback_close_app_stringvar(self, args):

        if len(self.close_app_stringvar.get()) < 1:
            config_value = 0
        else:
            config_value = int(self.close_app_stringvar.get())

        # if config_value <= 0:
        # 	self.close_app_stringvar.set('0')

        self.configure.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_COUNT] = config_value

    # print(self.configure.common_config[lybconstant.LYB_DO_STRING_CLOSE_APP_COUNT])

    def callback_recovery_count_stringvar(self, args):

        if len(self.recovery_count_stringvar.get()) < 1:
            config_value = 0
        else:
            config_value = int(self.recovery_count_stringvar.get())

        # if config_value <= 0:
        # 	self.recovery_count_stringvar.set('0')

        self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT] = config_value

    # print(self.configure.common_config[lybconstant.LYB_DO_STRING_RECOVERY_COUNT])

    def callback_wait_time_scene_change(self, args):

        if len(self.gui_config_dic[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE].get()) < 1:
            wait_time_scene_change = 0
        else:
            wait_time_scene_change = int(self.gui_config_dic[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE].get())

        # if wait_time_scene_change <= 0:
        # 	self.wait_time_scene_change.set('0')

        self.configure.common_config[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE] = wait_time_scene_change
        self.set_config(lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE)

    # print(self.configure.common_config[lybconstant.LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE])

    def callback_threshold_entry(self, args):

        if len(self.threshold_entry.get()) < 1:
            threshold_entry = 0.7
        else:
            threshold_entry = float(self.threshold_entry.get()) / 100.0

        self.configure.common_config['threshold_entry'] = threshold_entry

        window_name = self.app_player_process.get()
        if len(window_name) > 0:
            self.configure.set_window_config(window_name, 'threshold_entry', threshold_entry)

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_pixel_tolerance_entry(self, args):

        if len(self.pixel_tolerance_entry.get()) < 1:
            pixel_tolerance_entry = 30
        else:
            pixel_tolerance_entry = int(self.pixel_tolerance_entry.get())

        if pixel_tolerance_entry > 255:
            pixel_tolerance_entry = 255

        # if pixel_tolerance_entry <= 0:
        # 	self.pixel_tolerance_entry.set('0')
        # elif pixel_tolerance_entry > 255:
        # 	self.pixel_tolerance_entry.set('255')

        self.configure.common_config['pixel_tolerance_entry'] = pixel_tolerance_entry

    # print(self.configure.common_config['pixel_tolerance_entry'])

    def callback_adjust_entry(self, args):

        if len(self.adjust_entry.get()) < 1:
            adjust_entry = 10
        else:
            adjust_entry = int(self.adjust_entry.get())

        # if adjust_entry <= 0:
        # 	self.adjust_entry.set('0')
        # elif adjust_entry > 100:
        # 	self.adjust_entry.set('100')

        if adjust_entry > 100:
            adjust_entry = 100

        self.configure.common_config['adjust_entry'] = adjust_entry

    # print(self.configure.common_config['adjust_entry'])

    def callback_log_filter_entry_stringvar(self, args):
        self.configure.common_config[lybconstant.LYB_DO_STRING_LOG_FILTER] = self.log_filter_entry.get()
        self.callback_reopen_log()

    def update_monitor_master(self):
        # print('DEBUG:', self.worker_dic)

        remove_list = []
        for key, value in self.worker_dic.items():
            if self.worker_dic[key].isAlive() == False:
                remove_list.append(key)
                if key in self.game_object:
                    self.game_object.pop(key)

        for each_remove in remove_list:
            self.worker_dic.pop(each_remove)

        remove_list = []
        if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_USE_MONITORING] == False:
            for key, value in self.option_dic.items():
                if '_monitor' in key:
                    self.option_dic[key].pack_forget()
                    window_name = key.split('_')[0]
                    remove_list.append(window_name + '_monitor')

            for each_remove in remove_list:
                self.option_dic.pop(each_remove)

            return

        remove_list = []
        for key, value in self.option_dic.items():
            if '_monitor' in key:
                window_name = key.split('_')[0]

                # is_there = False
                # for i in range(self.search_window.size()):
                # 	if window_name == self.search_window.get(i):
                # 		is_there = True

                # if is_there == False:
                # 	self.option_dic[window_name + '_monitor'].pack_forget()
                # 	remove_list.append(window_name + '_monitor')
                if not window_name in self.app_player_process_list['values']:
                    self.option_dic[window_name + '_monitor'].pack_forget()
                    remove_list.append(window_name + '_monitor')

        for each_remove in remove_list:
            self.option_dic.pop(each_remove)

        # for i in range(self.search_window.size()):
        for window_name in self.app_player_process_list['values']:

            if not window_name + '_monitor' in self.option_dic:
                try:
                    self.option_dic[window_name + '_monitor'] = self.add_monitor_master_frame(
                        title=window_name,
                        subject='통계 정보가 출력됩니다',
                        workname='',
                        status='stop'
                    )
                except:
                    self.logger.error(traceback.format_exc())

            try:
                if window_name in self.game_object:
                    game_object = self.game_object[window_name]
                    total_elapsed_time = time.time() - game_object.start_time

                    if game_object.main_scene != None:
                        restart_period = int(
                            game_object.main_scene.get_game_config(lybconstant.LYB_DO_STRING_PERIOD_RESTART_GAME)) * 60
                        if restart_period != 0:
                            if total_elapsed_time > restart_period:
                                self.logger.warn('주기적으로 게임을 재시작합니다. 설정값: ' + str(restart_period) + '분')
                                game_object.request_terminate = True
                                game_object.start_time = time.time()
                                return

                    click_loc = str(game_object.cursor_loc)
                    split_str_list = click_loc.split(',')
                    click_loc = 'X:%5s Y:%5s' % (split_str_list[0].split('(')[1].replace(' ', '', 5),
                                                 split_str_list[1].split(')')[0].replace(' ', '', 5))

                    scene_name = self.adjust_monitor_name(
                        game_object.get_adjusted_name(game_object.current_matched_scene['name']), adj_length=10)
                    if len(scene_name) > 0:
                        scene_rate = '(' + str(game_object.current_matched_scene['rate']) + '%)'
                        scene_status = game_object.get_scene(game_object.current_matched_scene['name']).status
                        scene_name += scene_rate
                    else:
                        scene_rate = ''
                        scene_status = ''

                    if game_object.main_scene and game_object.current_schedule_work:

                        wlist = game_object.get_game_config(game_object.game_name, 'schedule_list')
                        work_name = game_object.current_schedule_work

                        # if work_name in game_object.main_scene.move_status:
                        # 	work_index = game_object.main_scene.move_status[work_name]
                        # 	try:
                        # 		work_name = game_object.main_scene.get_game_config('schedule_list')[work_index - 1]
                        # 	except:
                        # 		work_name = ''
                        # else:
                        if not work_name in game_object.main_scene.last_status:
                            return

                        work_index = game_object.main_scene.last_status[work_name]

                        new_work_name = str(work_index) + '. ' + game_object.current_schedule_work

                        # if game_object.main_scene.get_option('hero_current_hp') == None:
                        # 	hero_current_hp = ''
                        # else:
                        # 	hero_current_hp = str(game_object.main_scene.get_option('hero_current_hp'))

                        # if game_object.main_scene.get_option('target_current_hp') == None:
                        # 	target_current_hp = ''
                        # else:
                        # 	target_current_hp = str(game_object.main_scene.get_option('target_current_hp'))
                        hero_current_hp = ''
                        target_current_hp = ''
                    else:
                        wlist = []
                        work_index = ''
                        new_work_name = ''

                        hero_current_hp = ''
                        target_current_hp = ''

                    self.update_monitor_master_frame(
                        self.option_dic[window_name + '_monitor'],
                        arg_list=[
                            window_name,
                            '통계 정보가 출력됩니다',
                            new_work_name,
                            'start'
                        ],
                        wlist=wlist
                    )
                else:
                    self.update_monitor_master_frame(
                        self.option_dic[window_name + '_monitor'],
                        arg_list=[
                            window_name,
                            '통계 정보가 출력됩니다',
                            '',
                            'stop',
                        ]
                    )
            except KeyError:
                self.logger.error(traceback.format_exc())
                pass
            except:
                self.logger.error(traceback.format_exc())
                return
            # else:
            # 	self.update_monitor_master_frame(
            # 		self.option_dic[window_name + '_monitor']
            # 		)

            # for window_name, thread in self.worker_dic.items():
            # 	if not window_name + '_monitor' in self.option_dic:
            # 		self.option_dic[window_name + '_monitor'] = self.add_monitor_master(window_name)

    def update_monitor_master_frame(self,
                                    frame,
                                    arg_list=[],
                                    wlist=[]
                                    ):

        label_list = frame.winfo_children()

        i = 0
        elapsed_time = 0
        game_object = None
        window_name = None
        for each_arg in arg_list:
            if i == 0:
                text_arg = each_arg
                window_name = each_arg
            # elif i == 3 or i == 4:
            # 	text_arg = each_arg
            # 	if len(text_arg) > 0:
            # 		s = ttk.Style()
            # 		s.configure('stable.TLabel', foreground='green')
            # 		s.configure('danger.TLabel', foreground='red')
            # 		s.configure('warning.TLabel', foreground='#bc750a')
            # 		hp = int(text_arg)
            # 		if hp > 75:
            # 			label_list[i].configure(style='stable.TLabel')
            # 		elif hp > 30 and hp <= 75:
            # 			label_list[i].configure(style='warning.TLabel')
            # 		else:
            # 			label_list[i].configure(style='danger.TLabel')

            # 		if hp == 0:
            # 			text_arg = ''
            elif i == 1:
                if window_name in self.game_object:
                    game_object = self.game_object[window_name]
                    key = list(game_object.statistics)[game_object.statistics_iterator]
                    value = game_object.statistics[key]
                    text_arg = game_object.getCurrentStatistic()
                else:
                    text_arg = each_arg
            elif i == 2:
                if (not window_name in self.current_work_dic or
                        self.current_work_dic[window_name] != each_arg
                ):
                    self.logger.debug(
                        'wlist work: ' + self.wlist_stringvar_dic[window_name].get() + ' game work: ' + each_arg)
                    if window_name in self.current_work_dic:
                        self.logger.debug(str(self.current_work_dic[window_name]))
                    self.current_work_dic[window_name] = each_arg
                    new_wlist = []
                    windex = 1
                    for each_w in wlist:
                        if len(each_w) < 1:
                            continue
                        new_wlist.append(str(windex) + '. ' + each_w)
                        windex += 1
                    self.wlist_combobox_dic[window_name]['values'] = new_wlist
                    self.wlist_stringvar_skip_dic[window_name] = True
                    self.wlist_stringvar_dic[window_name].set(each_arg)
                # print('[DEBUG ----- ]', self.current_work_dic[window_name],
                # 	self.wlist_stringvar_dic[window_name].get(),
                # 	 each_arg)

                i += 1
                continue
            elif i == 3:

                s = ttk.Style()
                s.configure('stop.TLabel', foreground='#ff3826')
                s.configure('start.TLabel', foreground='#008e09')
                s.configure('work.TLabel', foreground='#00FF00')

                if each_arg == 'stop':
                    text_arg = ' ■'
                    label_list[i].configure(style='stop.TLabel')
                elif each_arg == 'start':
                    if window_name != None:
                        if window_name in self.game_object:
                            game_object = self.game_object[window_name]

                        if game_object != None and game_object.interval != None:
                            bot_period = game_object.interval
                        else:
                            bot_period = float(self.configure.common_config['wakeup_period_entry'])

                        if not window_name in self.monitor_check_point:
                            self.monitor_check_point[window_name] = 0

                        elapsed_time = time.time() - self.monitor_check_point[window_name]
                        if elapsed_time > bot_period:
                            self.monitor_check_point[window_name] = time.time()
                    else:
                        bot_period = 1

                    if bot_period < 0.11:
                        bot_period = 0.15

                    update_ui_period = float(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_UPDATE_UI])
                    text_arg = ' ●'
                    if bot_period < update_ui_period:
                        if elapsed_time > update_ui_period:
                            label_list[i].configure(style='start.TLabel')
                        else:
                            label_list[i].configure(style='work.TLabel')
                    else:
                        if elapsed_time > bot_period:
                            label_list[i].configure(style='start.TLabel')
                        else:
                            label_list[i].configure(style='work.TLabel')

                else:
                    text_arg = each_arg
            # elif i == 8:
            # 	label_list[i].configure(style='stable.TLabel')
            # 	text_arg = each_arg
            else:
                continue

            label_list[i].config(text=text_arg)
            i += 1

    def add_monitor_master_frame(self,
                                 title,
                                 subject,
                                 workname,
                                 status,
                                 ):

        s = ttk.Style()
        s.configure('LYB.TFrame', background='#3f74c6')

        frame_label = ttk.Frame(
            master=self.option_dic['monitor_master']
            # style 				= 'LYB.TFrame'
        )

        column_count = 0

        button = ttk.Button(
            master=frame_label,
            text=title,
            width=18,
            command=lambda: self.callback_monitoring_title_button(None, window_name=title)
        )
        button.pack(side=tkinter.LEFT)
        column_count += 1

        button = ttk.Button(
            master=frame_label,
            text=subject,
            width=38,
            command=lambda: self.callback_monitoring_subject_button(None, window_name=title)
        )
        button.pack(side=tkinter.LEFT, padx=5)
        column_count += 1

        monitor_font = ('굴림체', 9)

        combo_list = [
            '없음'
        ]

        self.wlist_stringvar_dic[title] = tkinter.StringVar(frame_label)
        self.wlist_stringvar_dic[title].trace('w',
                                              lambda *args: self.callback_select_wlist_stringvar(args,
                                                                                                 option_name=title))

        self.wlist_stringvar_dic[title].set(combo_list[0])
        self.wlist_combobox_dic[title] = ttk.Combobox(
            master=frame_label,
            values=combo_list,
            textvariable=self.wlist_stringvar_dic[title],
            state="readonly",
            height=10,
            width=24,
            # font 				= lybconstant.LYB_FONT,
            font=monitor_font,
            justify=tkinter.LEFT
        )
        self.wlist_combobox_dic[title].set(combo_list[0])
        self.wlist_combobox_dic[title].pack(anchor=tkinter.W, side=tkinter.LEFT)
        column_count += 1

        label = ttk.Label(
            master=frame_label,
            text=status,
            width=4
        )

        label.pack(side=tkinter.LEFT, fill=tkinter.Y)
        column_count += 1

        # label = ttk.Label(
        # 	master 				= frame_label,
        # 	text 				= arg10,
        # 	anchor 				= tkinter.N,
        # 	justify 			= tkinter.CENTER,
        # 	width 				= 11
        # 	)
        # label.pack(side=tkinter.LEFT, fill=tkinter.Y)
        # column_count += 1

        # s = ttk.Style()
        # s.configure('mouse_up.TLabel', foreground='black', background='#f7f796', relief='groove')
        # s.configure('mouse_down.TLabel', foreground='#f7f796', background='black', relief='groove')
        # s = ttk.Style()
        # s.configure('monitor_button.TButton', highlightbackground='green')

        self.monitor_button_index[0] = column_count
        button = ttk.Button(
            master=frame_label,
            text='보이기',
            width=8,
            # style 				= 'monitor_button.TButton',
            command=lambda: self.callback_monitoring_execute_worker(None, window_name=title,
                                                                    index=self.monitor_button_index[0])
        )
        button.pack(side=tkinter.RIGHT)
        column_count += 1

        self.monitor_button_index[1] = column_count
        button = ttk.Button(
            master=frame_label,
            text='정지',
            width=8,
            # style 				= 'monitor_button.TButton',
            command=lambda: self.callback_monitoring_execute_worker(None, window_name=title,
                                                                    index=self.monitor_button_index[1])
        )
        button.pack(side=tkinter.RIGHT)
        column_count += 1

        self.monitor_button_index[2] = column_count
        button = ttk.Button(
            master=frame_label,
            text='일시정지',
            width=8,
            # style 				= 'monitor_button.TButton',
            command=lambda: self.callback_monitoring_execute_worker(None, window_name=title,
                                                                    index=self.monitor_button_index[2])
        )
        button.pack(side=tkinter.RIGHT)
        column_count += 1

        self.monitor_button_index[3] = column_count
        button = ttk.Button(
            master=frame_label,
            text='시작',
            width=8,
            # style 				= 'monitor_button.TButton',
            command=lambda: self.callback_monitoring_execute_worker(None, window_name=title,
                                                                    index=self.monitor_button_index[3])
        )
        button.pack(side=tkinter.RIGHT)
        column_count += 1

        # if arg111 != None:
        # 	self.monitor_button_index[1] = column_count
        # 	button = ttk.Button(
        # 		master 				= frame_label,
        # 		text 				= '보이기',
        # 		command 			= lambda e: self.callback_monitoring_execute_worker(e, window_name=arg1, index=self.monitor_button_index[2])
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # column_count += 1

        # if arg112 != None:
        # 	self.monitor_button_index[3] = column_count
        # 	button = ttk.Button(
        # 		master 				= frame_label,
        # 		text 				= '숨기기',
        # 		command 			= lambda e: self.callback_monitoring_execute_worker(e, window_name=arg1, index=self.monitor_button_index[3])
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # column_count += 1

        # if arg113 != None:
        # 	self.monitor_button_index[4] = column_count
        # 	button = ttk.Button(
        # 		master 				= frame_label,
        # 		text 				= '보이기',
        # 		command 			= lambda e: self.callback_monitoring_execute_worker(e, window_name=arg1, index=self.monitor_button_index[4])
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # column_count += 1

        # if arg110 != None:
        # 	button = ttk.Label(
        # 		master 				= frame_label,
        # 		text 				= '시작',
        # 		anchor 				= tkinter.N,
        # 		justify 			= tkinter.CENTER,
        # 		style 				= 'mouse_up.TLabel',
        # 		cursor 				= 'hand2',
        # 		width 				= 5
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # 	# self.monitor_button_index[1] = column_count
        # 	# button.bind('<Button-1>', lambda event: self.callback_monitoring_execute_worker(event, window_name=arg1, index=self.monitor_button_index[1]))
        # # column_count += 1

        # if arg111 != None:
        # 	button = ttk.Label(
        # 		master 				= frame_label,
        # 		text 				= '멈춤',
        # 		anchor 				= tkinter.N,
        # 		justify 			= tkinter.CENTER,
        # 		style 				= 'mouse_up.TLabel',
        # 		cursor 				= 'hand2',
        # 		width 				= 5
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # self.monitor_button_index[2] = column_count
        # button.bind('<Button-1>', lambda event: self.callback_monitoring_execute_worker(event, window_name=arg1, index=self.monitor_button_index[2]))
        # column_count += 1

        # if arg112 != None:
        # 	button = ttk.Label(
        # 		master 				= frame_label,
        # 		text 				= '《',
        # 		anchor 				= tkinter.N,
        # 		justify 			= tkinter.CENTER,
        # 		style 				= 'mouse_up.TLabel',
        # 		cursor 				= 'hand2',
        # 		width 				= 5
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # 	self.monitor_button_index[3] = column_count
        # 	button.bind('<Button-1>', lambda event: self.callback_monitoring_execute_worker(event, window_name=arg1, index=self.monitor_button_index[3]))
        # column_count += 1

        # if arg113 != None:
        # 	button = ttk.Label(
        # 		master 				= frame_label,
        # 		text 				= '》',
        # 		anchor 				= tkinter.N,
        # 		justify 			= tkinter.CENTER,
        # 		style 				= 'mouse_up.TLabel',
        # 		cursor 				= 'hand2',
        # 		width 				= 5
        # 		)
        # 	button.pack(side=tkinter.LEFT)
        # 	self.monitor_button_index[4] = column_count
        # 	button.bind('<Button-1>', lambda event: self.callback_monitoring_execute_worker(event, window_name=arg1, index=self.monitor_button_index[4]))
        # column_count += 1

        frame_label.pack(anchor=tkinter.W, fill=tkinter.BOTH)

        return frame_label

    def adjust_monitor_name(self, name, adj_length=10):

        if name == None:
            return ''

        if len(name) > adj_length:
            return name[0:adj_length - 3] + '...' + name[-1]

        return name

    def callback_monitoring_title_button(self, event, window_name):
        self.callback_show_tumbnail(None, window_name)

    def callback_monitoring_subject_button(self, event, window_name):

        game_object = self.game_object[window_name]
        if game_object == None or game_object.main_scene == None:
            return

        button_label = self.option_dic[window_name + '_monitor'].winfo_children()[1]
        # self.logger.warn(game_object.getCurrentStatistic())
        button_label.configure(text=game_object.getCurrentStatistic())

        if game_object.statistics_iterator >= len(game_object.statistics) - 1:
            game_object.statistics_iterator = 0
        else:
            game_object.statistics_iterator += 1

    def callback_monitoring_execute_worker(self, event, window_name, index):

        stop_button_label = self.option_dic[window_name + '_monitor'].winfo_children()[index]
        # self.logger.warn(str(window_name) + ':' + str(index) + ':' + str(stop_button_label))

        # stop_button_label.configure(style='mouse_down.TLabel')
        self.master.after(100,
                          lambda: self.callback_monitoring_execute_worker_back(window_name=window_name, index=index))

    def callback_monitoring_execute_worker_back(self, window_name, index):
        # stop_button_label = self.option_dic[window_name + '_monitor'].winfo_children()[index]
        # stop_button_label.configure(style='mouse_up.TLabel')
        # self.logger.debug('window_name=['+window_name+']['+str(index)+']')

        if index == self.monitor_button_index[0]:
            self.callback_show_window(None, window_name)
        elif index == self.monitor_button_index[1]:
            self.terminate_each_worker(window_name)
        elif index == self.monitor_button_index[2]:
            self.pause_each_worker(window_name)
        elif index == self.monitor_button_index[3]:
            self.start_each_worker(window_name)
        # 	self.pause_each_worker(window_name)
        # elif index == self.monitor_button_index[3]:
        # 	self.backward_work_each_worker(window_name)
        # elif index == self.monitor_button_index[4]:
        # 	self.forward_work_each_worker(window_name)

    def backward_work_each_worker(self, window_name):

        game_object = self.game_object[window_name]
        if game_object == None or game_object.main_scene == None:
            return

        work_name = game_object.current_schedule_work
        if work_name != None:
            try:
                if not work_name in game_object.main_scene.move_status:
                    work_index = game_object.main_scene.last_status[work_name]
                else:
                    work_index = game_object.main_scene.move_status[work_name]
            except:
                work_index = game_object.main_scene.last_status[work_name]

        work_index -= 1

        self.move_to_work_index(window_name, work_index)

    def forward_work_each_worker(self, window_name):

        game_object = self.game_object[window_name]
        if game_object == None or game_object.main_scene == None:
            return

        work_name = game_object.current_schedule_work
        if work_name != None:
            try:
                if not work_name in game_object.main_scene.move_status:
                    work_index = game_object.main_scene.last_status[work_name]
                else:
                    work_index = game_object.main_scene.move_status[work_name]
            except:
                work_index = game_object.main_scene.last_status[work_name]

        work_index += 1

        self.move_to_work_index(window_name, work_index)

    def callback_select_wlist_stringvar(self, args, option_name):
        self.logger.debug('[MoveStatus] callback_select_wlist_stringvar: ' + option_name)
        self.logger.debug(str(self.wlist_stringvar_skip_dic))

        if len(option_name) < 1:
            return

        if not option_name in self.current_work_dic:
            return

        # self.logger.debug('[MoveStatus] CP1')
        if option_name in self.wlist_stringvar_skip_dic:
            if self.wlist_stringvar_skip_dic[option_name] == True:
                self.wlist_stringvar_skip_dic[option_name] = False
                self.logger.debug('[MoveStatus] ' + str(self.wlist_stringvar_skip_dic))
                return

        # self.logger.debug('[MoveStatus] CP2')
        if len(self.wlist_stringvar_dic[option_name].get()) < 1:
            return

        # self.logger.debug('[DEBUG MoveStatus] CP3')
        move_status = int(self.wlist_stringvar_dic[option_name].get().split('.')[0])
        self.logger.debug(
            '[DEBUG MoveStatus] moveStatus: ' + str(move_status) + ' current_work_name: ' + self.current_work_dic[
                option_name])

        game_object = self.game_object[option_name]
        if game_object == None or game_object.main_scene == None:
            return

        self.move_to_work_index(option_name, move_status)

    def move_to_work_index(self, window_name, index):
        if not window_name in self.game_object:
            return

        game_object = self.game_object[window_name]
        if game_object == None or game_object.main_scene == None:
            return

        max_len = len(game_object.main_scene.get_game_config('schedule_list'))
        if index >= max_len - 1:
            index = max_len - 1

        if index < 1:
            index = 1

        work_name = game_object.current_schedule_work
        if work_name != None:
            call_index = 0
            if len(game_object.main_scene.callstack) > 0:
                for each_call in game_object.main_scene.callstack:
                    iterator_key = game_object.build_iterator_key(call_index, each_call)
                    game_object.main_scene.set_option(iterator_key, None)
                    call_index += 1
                game_object.main_scene.callstack.clear()
            game_object.main_scene.callstack_status.clear()

            game_object.main_scene.set_option(work_name + '_end_flag', True)
            game_object.main_scene.move_status[work_name] = index

        move_work_name = str(index) + '. ' + game_object.main_scene.get_game_config('schedule_list')[index - 1]
        self.wlist_stringvar_dic[window_name].set(move_work_name)

    def tooltip(self, widget_name, text):
        tooltip = ToolTip(widget_name, text)
        tooltip.wraplength = 640

    def callback_telegram(self, event):
        # self.logging_message("SUCCESS", "현재 텔레그램 기능을 점검 중입니다.")
        # return

        if self.telegram_button_label.get() == '연동하기':

            if len(self.telegram_entry.get()) < 1:
                self.logging_message("NORMAL", "연동하기 버튼 위 입력란에 아무거나 입력하세요.")
                self.logging_message("NORMAL", "입력한 내용을 텔레그램 도그푸터 봇 대화창에 똑같이 입력하고 연동 버튼을 누르세요.")
                return
            rest = self.login()

            chat_id = rest.connect_telegram(self.telegram_entry.get(), adjust_time=int(self.configure.common_config[lybconstant.LYB_DO_STRING_PERIOD_TELEGRAM]))
            if chat_id != '' and chat_id != -1:
                error_message = rest.update_chat_id(chat_id)
                if error_message == '':
                    self.telegram_button_label.set('연동해제')
                    self.telegram_chat_id_label.set(chat_id)

                    self.logger.info('DEBUG1')

                    rest.send_telegram_message(chat_id,
                                               self.telegram_entry.get() + ' from DogFooter Macro ' + lybconstant.LYB_VERSION)

                    self.logger.info('DEBUG2')

                    self.logging_message("SUCCESS", "텔레그램 연동에 성공했습니다.")
                    self.logging_message("SUCCESS", "도그푸터 봇이 메세지를 전송했습니다.")
                    self.logging_message("SUCCESS", "텔레그램 알람이 온다면 텔레그램 연동에 성공한 것입니다.")
                    self.logging_message("SUCCESS", "연동해제 버튼을 눌러서 언제든지 해제 할 수 있습니다.")
                    self.telegram_entry.set('')

                    self.logger.info('DEBUG3')

                    chat_id = rest.get_chat_id()
                    self.logger.debug('update chatting id: ' + str(chat_id))
                    return
            self.logging_message("FAIL", "텔레그램 연동에 실패했습니다.")
            self.logging_message("FAIL", "[" + self.telegram_entry.get() + "]를 텔레그램 대화창에 제대로 입력했는지 확인하세요.")
        else:
            rest = self.login()

            error_message = rest.update_chat_id(0)
            if error_message == '':
                self.logging_message("SUCCESS", "텔레그램 연동을 해제했습니다.")
                self.telegram_button_label.set('연동하기')
                self.telegram_chat_id_label.set('')
                self.telegram_entry.set(self.generate_token())
                chat_id = rest.get_chat_id()

    def get_mb_point(self):
        if self.mb_point != None:
            return self.mb_point

        rest = self.login()
        error_message = rest.login()

        self.mb_point = rest.get_point()

        return self.mb_point

    # def get_mb_ip(self):
    # rest = self.login()
    # return rest.get_ip()

    def login(self):
        if self.rest is not None:
            return self.rest

        user_id = self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id']
        user_password = likeyoubot_license.LYBLicense().get_decrypt(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'])

        self.rest = likeyoubot_rest.LYBRest(self.configure.root_url, user_id, user_password)

        return self.rest

    def generate_token(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def send_screenshot_telegram(self):
        self.logger.debug('/SS')
        screenShot = ImageGrab.grab()
        png_name = self.save_image(screenShot, 'ss_command')
        rest = self.login()
        chat_id = rest.get_chat_id()
        self.rest.send_telegram_image(chat_id, png_name)

    def save_image(self, image, png_name):

        try:
            directory = resource_path('screenshot')
            if not os.path.exists(directory):
                os.makedirs(directory)

            now = datetime.datetime.now()
            now_time = now.strftime('%y%m%d_%H%M%S')
            png_name = directory + '\\' + png_name + '_' + str(now_time) + '.png'
            image.save(png_name)

            return png_name
        except:
            self.logger.error('스크린샷 저장 중 에러 발생')
            self.logger.error(traceback.format_exc())

            return None

    def callback_hide_window(self, e, window_name):
        self.configure.keyword = self.keyword_entry.get()
        self.master.focus()

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

        worker_thread = self.executeThread()
        if worker_thread == None:
            return

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('watchout', [self, 'hide', window_name]))

    def callback_show_window(self, e, window_name):
        self.configure.keyword = self.keyword_entry.get()
        self.master.focus()

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

        worker_thread = self.executeThread()
        if worker_thread == None:
            return

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('watchout', [self, 'show', window_name]))

    def callback_show_tumbnail(self, e, window_name):
        self.configure.keyword = self.keyword_entry.get()
        self.master.focus()

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

        worker_thread = self.executeThread()
        if worker_thread == None:
            return

        worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('thumbnail', [self, window_name]))
