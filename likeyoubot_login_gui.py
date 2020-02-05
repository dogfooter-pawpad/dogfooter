import tkinter
import webbrowser
from tkinter import ttk
from tkinter import font
import time
import collections
import pickle
import sys
import likeyoubot_gui
import os
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_configure
import likeyoubot_license
import likeyoubot_rest
import requests
import shutil
import likeyoubot_logger
import traceback
import threading
import queue


class LYBLoginGUI:

    def __init__(self, master, configure):
        self.master = master
        self.width = master.winfo_width()
        self.height = master.winfo_height()
        self.configure = configure
        self.master.title(self.configure.window_title + ' ' + str(lybconstant.LYB_VERSION))
        self.option_dic = {}
        self.gui_style = ttk.Style()
        self.shake_count = 0
        self.lyblicense = likeyoubot_license.LYBLicense()
        self.progress_bar = None
        self.num_of_file = 0
        self.rest = None
        self.worker_thread = None
        self.waiting_queue = None
        self.download_label = None
        self.download_file_label = None

        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.logger.debug(self.gui_style.theme_names())

        self.gui_style.theme_use('vista')
        self.gui_style.configure('.', font=lybconstant.LYB_FONT)
        self.gui_style.configure("Tab", focuscolor=self.gui_style.configure(".")["background"])
        self.gui_style.configure("TButton", focuscolor=self.gui_style.configure(".")["background"])
        self.gui_style.configure("TCheckbutton", focuscolor=self.gui_style.configure(".")["background"])

        self.main_frame = ttk.Frame(master)
        label_frame = ttk.LabelFrame(self.main_frame, text='로그인')
        frame_extra = ttk.Frame(label_frame)
        frame_extra.pack(pady=5)
        frame_top = ttk.Frame(label_frame)
        frame_left = ttk.Frame(frame_top)
        frame = ttk.Frame(frame_left)
        label = ttk.Label(
            master=frame,
            text="계정",
            justify=tkinter.LEFT,
            width=10
        )
        label.pack(side=tkinter.LEFT)

        if not lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT] = False

        if not self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT]:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'] = ''
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'] = ''

        self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'] = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'] = ''
        self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'])

        entry = ttk.Entry(
            master=frame,
            textvariable=self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'],
            width=24
        )
        entry.pack(side=tkinter.LEFT, padx=2)
        entry.focus()
        frame.pack()

        frame = ttk.Frame(frame_left)
        label = ttk.Label(
            master=frame,
            text="비밀번호",
            justify=tkinter.LEFT,
            width=10
        )
        label.pack(side=tkinter.LEFT)

        self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'] = tkinter.StringVar(frame)
        if not lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'] = ''
            self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'].set('')
        else:
            self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'].set(
                self.lyblicense.get_decrypt(
                    self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'])
            )

        entry = ttk.Entry(
            master=frame,
            textvariable=self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'],
            show="*",
            width=24
        )
        entry.pack(side=tkinter.LEFT, padx=2)
        frame.pack()
        frame_left.pack(anchor=tkinter.W, side=tkinter.LEFT)

        frame_extra = ttk.Frame(frame_top)
        frame_extra.pack(side=tkinter.LEFT, padx=1)

        frame_right = ttk.Frame(frame_top)

        button = ttk.Button(
            master=frame_right,
            text="로그인",
            command=lambda: self.callback_login_button(None)
        )
        button.pack(fill=tkinter.BOTH, expand=True)
        frame_right.pack(fill=tkinter.BOTH, expand=True)
        frame_top.pack()

        if not lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_chat_id' in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_chat_id'] = ''

        self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT] = tkinter.BooleanVar()
        self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT].trace(
            'w', lambda *args: self.callback_save_login_account_booleanvar(args,
                                                                           lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT)
        )
        self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT])

        frame_bottom = ttk.Frame(label_frame)
        frame = ttk.Frame(frame_bottom)
        check_box = ttk.Checkbutton(

            master=frame_bottom,
            text='아이디/비밀번호 기억하기',
            variable=self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT],
            onvalue=True,
            offvalue=False
        )

        check_box.pack(anchor=tkinter.E)
        frame.pack(anchor=tkinter.E)
        # frame = ttk.Frame(frame_bottom)

        if not lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE in self.configure.common_config:
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE] = False

        self.option_dic[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE] = tkinter.BooleanVar()
        self.option_dic[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE].trace(
            'w', lambda *args: self.callback_auto_update_booleanvar(args, lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE)
        )
        self.option_dic[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE].set(
            self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE])

        check_box = ttk.Checkbutton(
            master=frame_bottom,
            text='자동 업데이트',
            variable=self.option_dic[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE],
            onvalue=True,
            offvalue=False
        )

        # check_box.pack(anchor=tkinter.E)
        # frame.pack(anchor=tkinter.E)

        frame_extra = ttk.Frame(frame_bottom)
        frame_extra.pack(pady=1)
        s = ttk.Style()
        s.configure('label_link.TLabel', foreground='blue', font=('굴림체', 9, 'underline'))
        link_url = "회원가입"
        frame = ttk.Frame(frame_bottom)
        label = ttk.Label(
            master=frame,
            text=link_url,
            justify=tkinter.LEFT,
            style='label_link.TLabel',
            cursor='hand2'
        )
        label.pack(side=tkinter.LEFT)
        label.bind("<Button-1>", self.callback_register)
        frame.pack(anchor=tkinter.E)
        frame_bottom.pack(fill=tkinter.X, pady=5)
        label_frame.pack(padx=5, pady=10)

        frame_extra = ttk.Frame(frame_bottom)
        frame_extra.pack(pady=1)

        link_url = "아이디 비밀번호 찾기"
        frame = ttk.Frame(frame_bottom)
        label = ttk.Label(
            master=frame,
            text=link_url,
            justify=tkinter.LEFT,
            style='label_link.TLabel',
            cursor='hand2'
        )
        label.pack(side=tkinter.LEFT)
        label.bind("<Button-1>", self.callback_password_lost)
        frame.pack(anchor=tkinter.E)
        frame_bottom.pack(fill=tkinter.X, pady=5)
        label_frame.pack(padx=5, pady=10)

        frame_message = ttk.Frame(self.main_frame)

        s = ttk.Style()
        s.configure('label_error.TLabel', foreground='red', font=('굴림체', 9))
        frame = ttk.Frame(frame_message)
        self.option_dic[lybconstant.LYB_DO_STRING_LOGIN_MESSAGE] = tkinter.StringVar(frame)
        self.option_dic[lybconstant.LYB_DO_STRING_LOGIN_MESSAGE].set('')

        label = ttk.Label(
            master=frame,
            textvariable=self.option_dic[lybconstant.LYB_DO_STRING_LOGIN_MESSAGE],
            justify=tkinter.LEFT,
            wraplength=320,
            style='label_error.TLabel'
        )
        label.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)
        frame_message.pack(anchor=tkinter.W, padx=5, pady=5)
        self.main_frame.pack(fill=tkinter.BOTH, expand=True)

        self.master.bind('<Return>', self.callback_login_button)

    def callback_register(self, event):
        rest = likeyoubot_rest.LYBRest(self.configure.root_url, "", "")
        public_token = rest.get_public_elem("public_token")
        webbrowser.open_new(r"https://pawpad.kr/bbs/" + public_token + r"/register.php")

        return

    def callback_password_lost(self, event):
        rest = likeyoubot_rest.LYBRest(self.configure.root_url, "", "")
        public_token = rest.get_public_elem("public_token")
        webbrowser.open_new(r"https://pawpad.kr/bbs/" + public_token + r"/password_lost.php")

        return

    # webbrowser.open_new(likeyoubot_http.LYBHttp.getMacroBaseUrl() + '/bbs/register.php')

    def callback_close_button(self, event):
        self.logger.info('closed')
        sys.exit(0)

    def callback_login_button(self, event):
        self.callback_save_login_account_booleanvar(None, lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT)

        user_id = self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_id'].get()
        user_password = self.option_dic[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_passwd'].get()
        # self.lybhttp = likeyoubot_http.LYBHttp(user_id, user_password)
        self.rest = likeyoubot_rest.LYBRest(self.configure.root_url, user_id, user_password)
        self.rest.login()

        # error_message = self.lybhttp.login()
        error_message = self.rest.login()
        self.logger.info('로그인:' + str(error_message))
        if error_message == '':
            # login_point = self.lybhttp.get_login_point()
            # login_point = self.rest.get_login_point()
            # if int(self.lybhttp.mb_point) < int(login_point):
            # self.logger.info('DEBUG1')
            if self.rest.get_point() < self.rest.get_login_point():
                self.shake_frame()
                error_message = '포인트가 부족합니다.(현재: ' + str(self.rest.get_point()) + '점, 필요: ' + str(
                    self.rest.get_login_point()) + '점)'
                self.option_dic[lybconstant.LYB_DO_STRING_LOGIN_MESSAGE].set(error_message)
                return

            # self.logger.info('DEBUG3')
            self.main_frame.pack_forget()

            # chat_id = self.lybhttp.get_chat_id()
            chat_id = self.rest.get_chat_id()

            if chat_id != None:
                self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT + '_chat_id'] = chat_id

            if self.configure.common_config[lybconstant.LYB_DO_BOOLEAN_AUTO_UPDATE] == True:
                self.auto_update()
            else:
                try:
                    likeyoubot_gui.LYBGUI(self.master, self.configure, self.rest)
                except:
                    self.logger.error(traceback.format_exc())
        else:
            self.shake_frame()
            self.option_dic[lybconstant.LYB_DO_STRING_LOGIN_MESSAGE].set(error_message)

    def shake_frame(self):
        (w, h, x, y) = self.configure.getGeometryLogin()

        if self.shake_count % 2 == 0:
            self.master.geometry('%dx%d+%d+%d' % (w, h, x - 5, y))
        else:
            self.master.geometry('%dx%d+%d+%d' % (w, h, x + 5, y))

        self.shake_count += 1
        if self.shake_count > 10:
            self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
            self.shake_count = 0
        else:
            self.master.after(10, self.shake_frame)

    def callback_save_login_account_booleanvar(self, args, option_name):

        self.configure.common_config[option_name + '_id'] = self.option_dic[option_name + '_id'].get()
        self.configure.common_config[option_name + '_passwd'] = self.lyblicense.get_encrypt(
            self.option_dic[option_name + '_passwd'].get()
        )
        self.configure.common_config[option_name] = self.option_dic[option_name].get()

        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def callback_auto_update_booleanvar(self, args, option_name):

        self.configure.common_config[option_name] = self.option_dic[option_name].get()
        try:
            with open(self.configure.path, 'wb') as dat_file:
                pickle.dump(self.configure, dat_file)
        except:
            self.logger.error(traceback.format_exc())

    def auto_update(self):

        # last_version = self.lybhttp.get_version()
        # self.patch_urls = self.lybhttp.get_update_file()
        # self.logger.info('DEBUG-1')
        last_version = self.rest.get_version()
        # self.logger.info('DEBUG-2')
        self.logger.info(last_version)
        self.patch_urls = self.rest.get_update_file()
        # self.logger.info('DEBUG-3')

        self.logger.debug('last_version: ' + last_version + ', ' + lybconstant.LYB_VERSION)

        if (last_version == lybconstant.LYB_VERSION or
                len(self.patch_urls) < 1
        ):
            self.main_frame = ttk.Frame(self.master)
            frame = ttk.Frame(self.main_frame)
            s = ttk.Style(frame)
            s.configure('blue_label.TLabel', foreground='blue')
            label = ttk.Label(
                master=frame,
                text='업데이트 정보가 없습니다.',
                wraplength=320,
                style='blue_label.TLabel'
            )
            label.pack()
            frame.pack()
            self.main_frame.pack(expand=True)
            self.master.after(100, self.start_gui)
        else:

            self.main_frame = ttk.Frame(self.master)
            self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
            self.progress_bar.pack()

            self.download_label = tkinter.StringVar(self.main_frame)
            label = ttk.Label(
                master=self.main_frame,
                textvariable=self.download_label,
            )
            label.pack(expand=True)
            self.download_file_label = tkinter.StringVar(self.main_frame)
            label = ttk.Label(
                master=self.main_frame,
                textvariable=self.download_file_label,
            )
            label.pack(expand=True)
            self.main_frame.pack(expand=True)

            self.logger.debug('GoogleDrive file list: ' + str(self.patch_urls))

            self.waiting_queue = queue.Queue()
            self.worker_thread = LYBUpdateWorker('Update',
                                                 self.configure,
                                                 self.waiting_queue,
                                                 self.rest,
                                                 self.patch_urls,
                                                 self.progress_bar,
                                                 self.download_label,
                                                 self.download_file_label)
            self.worker_thread.daemon = True
            self.worker_thread.start()
            self.master.after(100, self.check_update)

    def check_update(self):
        message = ''

        try:
            message = self.waiting_queue.get_nowait()
        except queue.Empty:
            self.master.after(100, self.check_update)
            return

        if message == 'success':
            self.main_frame.pack_forget()

            self.main_frame = ttk.Frame(self.master)
            self.master.bind('<Return>', self.callback_close_button)
            frame = ttk.Frame(self.main_frame)
            s = ttk.Style(frame)
            s.configure('blue_label.TLabel', foreground='blue')
            label = ttk.Label(
                master=frame,
                text='업데이트가 완료되었습니다. 프로그램을 다시 실행해주세요.',
                wraplength=320,
                style='blue_label.TLabel'
            )
            label.pack()
            frame.pack()
            frame = ttk.Frame(self.main_frame)
            button = ttk.Button(
                master=frame,
                text="확인",
                command=lambda: self.callback_close_button(None)
            )
            button.pack(fill=tkinter.BOTH, expand=True)
            button.focus_set()
            frame.pack()

            self.main_frame.pack(expand=True)

        # cmd = [
        # 	likeyoubot_configure.LYBConfigure.resource_path('dogfooterbot.exe')
        # 	]
        # CREATE_NEW_PROCESS_GROUP = 0x00000200
        # DETACHED_PROCESS = 0x00000008

        # p = Popen(cmd)
        # sys.exit(1)
        # self.master.after(100, self.check_update)
        else:

            self.master.after(100, self.check_update)

    def start_gui(self):
        self.main_frame.pack_forget()
        likeyoubot_gui.LYBGUI(self.master, self.configure, self.rest)


class LYBUpdateWorker(threading.Thread):
    def __init__(self, name, configure, queue, pHttp, patch_urls, progress_bar, download_label, download_file_label):
        super().__init__()
        self.name = name
        self.rest = pHttp
        self.response_queue = queue
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.configure = configure
        self.patch_urls = patch_urls
        self.progress_bar = progress_bar
        self.download_label = download_label
        self.download_file_label = download_file_label
        self.dropbox_access_token = -1

    def run(self):
        threading.currentThread().setName(self.name)

        self.dropbox_access_token = self.rest.get_elem('dropbox_access_token')
        self.logger.debug('dropbox_access_token:' + str(self.dropbox_access_token))

        # patch_url_list = list(self.patch_urls)
        current_version = likeyoubot_configure.LYBConfigure.get_version(lybconstant.LYB_VERSION)
        patch_url_list = []
        for file_name, each_url in self.patch_urls.items():
            each_version = likeyoubot_configure.LYBConfigure.get_version(each_url[2])
            if current_version < each_version:
                patch_url_list.append(file_name)

        # self.logger.warn(patch_url_list)
        for file_name, each_url in self.patch_urls.items():
            # each_url = self.patch_urls[patch_url_list[patch_url_iter]]
            # h = requests.head(each_url, allow_redirects=True)
            # header = h.headers
            # content_length = header.get('content-length', None)
            self.logger.debug('GoogleDrive id: ' + str(each_url[0]))
            self.logger.debug('file name: ' + str(file_name))
            self.logger.debug('Each version: ' + str(each_url[2]))

            each_version = likeyoubot_configure.LYBConfigure.get_version(each_url[2])
            if current_version >= each_version:
                continue

            self.download_label.set(str(patch_url_list.index(file_name) + 1) + '/' + str(len(patch_url_list)) +
                                    ' 번째 파일 다운로드 중')
            self.download_file_label.set(file_name)

            # file_name = patch_url_list[self.patch_url_iter]
            try:
                os.remove(likeyoubot_configure.LYBConfigure.resource_path(file_name + '.bak'))
            except:
                self.logger.debug('This is exe file: skip')

            try:
                shutil.move(likeyoubot_configure.LYBConfigure.resource_path(file_name),
                            likeyoubot_configure.LYBConfigure.resource_path(file_name + '.bak'))
            except:
                self.logger.error(traceback.format_exc())
                self.logger.debug('New file: ' + file_name)

            self.logger.debug(file_name)

            self.logger.debug('TEST: ' + each_url[0])
            path = likeyoubot_configure.LYBConfigure.resource_path(file_name)
            self.progress_bar['value'] = 0
            self.progress_bar['maximum'] = int(each_url[1]) * 1024
            try:
                self.download(each_url[0], path)
            except:
                self.logger.error(traceback.format_exc())
                shutil.move(likeyoubot_configure.LYBConfigure.resource_path(file_name + '.bak'),
                            likeyoubot_configure.LYBConfigure.resource_path(file_name))
                self.response_queue.put_nowait('fail')
                return
            self.progress_bar['value'] = self.progress_bar['maximum']

            try:
                os.remove(likeyoubot_configure.LYBConfigure.resource_path(file_name + '.bak'))
            except:
                self.logger.debug('This is exe file: skip')

        self.response_queue.put_nowait('success')

    def download(self, share_id, destination):
        # URL = "https://docs.google.com/uc?export=download"

        # session = requests.Session()

        # response = session.get(URL, params = { 'id' : share_id }, stream = True)
        # token = self.get_confirm_token(response)

        # if token:
        # 	params = { 'id' : share_id, 'confirm' : token }
        # 	response = session.get(URL, params = params, stream = True)

        # url = 'https://www.dropbox.com/s/6opc0lpufkcs87e/dogfooterbot.exe?dl=0'
        # try:
        # 	self.logger.debug('destination: ' + str(destination))

        # 	dbx = dropbox.Dropbox(self.dropbox_access_token)
        # 	self.logger.debug(dbx.users_get_current_account())

        # 	with open(destination, "wb") as f:
        # 		metadata, response = dbx.files_download(path=share_id)
        # 	# 	f.write(response.content)
        # 		self.save_response_content(response, destination)
        # except:
        # 	self.logger.error(traceback.format_exc())

        url = share_id
        try:
            response = requests.get(url, allow_redirects=True)
            self.save_response_content(response, destination)
        except:
            self.logger.error(traceback.format_exc())

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 1024
        size = 0
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                self.progress_bar['value'] = size
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    size += CHUNK_SIZE

    # r = requests.get(each_url, stream=True)

    # h = requests.head(each_url, allow_redirects=True)
    # header = h.headers
    # content_length = header.get('content-length', None)

    # self.logger.debug('SIZE: ' + content_length)
    # path = likeyoubot_configure.LYBConfigure.resource_path(file_name)

    # try:
    # 	with open(path, 'wb') as f:
    # 		f.write(r.content)
    # except:
    # 	shutil.move(likeyoubot_configure.LYBConfigure.resource_path(file_name + '.bak'), likeyoubot_configure.LYBConfigure.resource_path(file_name))
    # 	return
    # try:
    # 	os.remove(likeyoubot_configure.LYBConfigure.resource_path(file_name + '.bak'))
    # except:
    # 	self.logger.debug('This is exe file: skip')

    # self.num_of_file += 1
    # self.progress_bar["value"] = self.num_of_file

    # self.patch_url_iter += 1
    # if self.patch_url_iter > len(self.patch_urls) - 1:
    # 	cmd = [
    # 		likeyoubot_configure.LYBConfigure.resource_path('dogfooterbot.exe')
    # 		]
    # 	CREATE_NEW_PROCESS_GROUP = 0x00000200
    # 	DETACHED_PROCESS = 0x00000008

    # 	p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    # 	sys.exit(1)
    # else:
    # 	self.master.after(100, self.read_file)
