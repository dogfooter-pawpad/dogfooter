import threading
import queue
import time
import win32api
import likeyoubot_message
import likeyoubot_win
from PIL import ImageGrab
import cv2
import numpy as np
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_v4
import likeyoubot_logger
import traceback
import pyautogui


class LYBWorker(threading.Thread):
    def __init__(self, name, configure, cmd_queue, res_queue):
        super().__init__()
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.command_queue = cmd_queue
        self.response_queue = res_queue
        self.name = name
        self.keyword = ""
        self.start_action = False
        self.start_flag = 0
        self.ui = None
        self.hwnd = 0
        self.side_hwnd = 0
        self.parent_hwnd = 0
        self.multi_hwnd = 0
        self.multi_handle_dic = {}
        self.game = None
        self.game_tab = None
        self.game_name = None
        self.game_option = None
        self.win = None
        self.window_title = ''
        self.configure = configure
        self.config = None
        self.common_config = None
        self.window_config = None
        self.pause_flag = False
        self.app_player_type = 'nox'

    def run(self):
        threading.currentThread().setName('워커쓰레드')
        recv_msg = None
        # logger.debug('['+self.name+']'+' start:'+str(threading.currentThread()))
        while True:
            try:
                if self.pause_flag:
                    if self.game is not None:
                        self.game.interval = 9999999
                    recv_msg = self.command_queue.get()
                else:
                    recv_msg = self.command_queue.get_nowait()

                if recv_msg.type == 'end':
                    self.response_queue.put_nowait(likeyoubot_message.LYBMessage('end_return', str(self.window_title)))
                    self.response_queue.join()
                    break
                elif recv_msg.type == 'start_app_player':
                    self.logger.warn('WORKER: start_app_player')
                    player_type = recv_msg.message[0]
                    multi_hwnd_dic = recv_msg.message[1]
                    window_title = recv_msg.message[2]
                    configure = recv_msg.message[3]
                    window_config = configure.window_config[window_title]
                    window = likeyoubot_win.LYBWin(configure.window_title, configure)

                    if player_type == 'nox':
                        if lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX in multi_hwnd_dic:
                            mHwnd = multi_hwnd_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_NOX]
                            app_player_index = int(
                                window_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number']) - 1
                            self.logger.debug('app_player_index: ' + str(app_player_index))

                            window.mouse_click(mHwnd, 523, 116 + (57 * app_player_index))
                    elif player_type == 'momo':
                        if lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO in multi_hwnd_dic:
                            mHwnd = multi_hwnd_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO]
                            app_player_index = int(
                                window_config[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'number']) - 1
                            self.logger.debug('app_player_index: ' + str(app_player_index))

                            window.mouse_click(mHwnd, 387, 116 + (50 * app_player_index))

                    self.response_queue.put_nowait(
                        likeyoubot_message.LYBMessage('end_start_app_player', str(self.window_title)))
                    self.response_queue.join()
                    break
                elif recv_msg.type == 'GetWindowLocation':
                    self.ui = recv_msg.message
                    (handle_list, side_handle_dic, parent_handle_dic, multi_handle_dic) = self.findWindows()
                    for h in handle_list:
                        (anchor_x, anchor_y, end_x, end_y) = self.win.get_window_location(h)
                        if h in parent_handle_dic:
                            window_title = self.win.get_title(parent_handle_dic[h])
                        else:
                            window_title = self.win.get_title(h)

                        self.logger.info(
                            '창 [' + str(window_title) + '] 위치 정보 현재 위치로 업데이트: ' + str((anchor_x, anchor_y)))
                        if window_title == str(self.ui.app_player_process.get()):
                            self.ui.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'].set(anchor_x)
                            self.ui.gui_config_dic[lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'].set(anchor_y)

                        self.ui.configure.window_config[window_title][
                            lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x'] = anchor_x
                        self.ui.configure.window_config[window_title][
                            lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y'] = anchor_y

                    # self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_hwnd_return', rhwnds_dic))
                    # self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_side_hwnd_return', side_handle_dic))
                    # self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_parent_hwnd_return', parent_handle_dic))
                    # self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_multi_hwnd_return', multi_handle_dic))
                    # self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_title_return', window_list))

                    # self.response_queue.join()
                    break

                elif recv_msg.type == 'search':
                    window_config = recv_msg.message
                    (handle_list, side_handle_dic, parent_handle_dic, multi_handle_dic) = self.findWindows()
                    self.logger.debug(handle_list)
                    self.logger.debug(parent_handle_dic)

                    window_list, rhwnds_dic = self.set_location(window_config, handle_list, side_handle_dic,
                                                                parent_handle_dic)

                    self.logger.debug('search window handle list: ' + str(window_list))
                    self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_hwnd_return', rhwnds_dic))
                    self.response_queue.put_nowait(
                        likeyoubot_message.LYBMessage('search_side_hwnd_return', side_handle_dic))
                    self.response_queue.put_nowait(
                        likeyoubot_message.LYBMessage('search_parent_hwnd_return', parent_handle_dic))
                    self.response_queue.put_nowait(
                        likeyoubot_message.LYBMessage('search_multi_hwnd_return', multi_handle_dic))
                    self.response_queue.put_nowait(likeyoubot_message.LYBMessage('search_title_return', window_list))

                    self.response_queue.join()
                    break
                # elif recv_msg.type =='hide':
                # 	self.ui = recv_msg.message
                # 	self.logger.warn('창 숨기기')
                # 	self.win = likeyoubot_win.LYBWin(self.ui.configure.window_title, self.ui.configure)

                # 	if len(self.ui.parent_hwnds) > 0:
                # 		hwnds = self.ui.parent_hwnds
                # 	else:
                # 		hwnds = self.ui.hwnds

                # 	# (handle_list, side_handle_dic, parent_handle_dic, multi_handle_dic) = self.findWindows()
                # 	handle_list = []
                # 	for key, each_handle in self.ui.hwnds.items():
                # 		handle_list.append(each_handle)

                # 	self.logger.warn(handle_list)
                # 	parent_handle_dic = self.ui.parent_hwnds
                # 	side_handle_dic = self.ui.side_hwnds

                # 	window_list, rhwnds_dic = self.set_location(
                # 								self.ui.configure.window_config,
                # 								handle_list,
                # 								side_handle_dic,
                # 								parent_handle_dic,
                # 								custom_loc_x=self.ui.master.winfo_screenwidth(),
                # 								custom_loc_y=self.ui.master.winfo_screenheight() )

                # 	for key, each_hwnd in hwnds.items():
                # 		self.win.set_invisible(int(each_hwnd))

                # 	self.response_queue.join()
                # 	break
                elif recv_msg.type == 'watchout' or recv_msg.type == 'watchout2':
                    if recv_msg.type == 'watchout':
                        self.ui = recv_msg.message[0]
                        configure = self.ui.configure
                        resolution_w = self.ui.master.winfo_screenwidth()
                        resolution_h = self.ui.master.winfo_screenheight()
                        hwnds = self.ui.hwnds
                        parent_hwnds = self.ui.parent_hwnds
                        side_hwnds = self.ui.side_hwnds
                    else:
                        configure = recv_msg.message[0]
                        win = recv_msg.message[3]
                        resolution_w = win32api.GetSystemMetrics(0)
                        resolution_h = win32api.GetSystemMetrics(1)
                        hwnds = recv_msg.message[4]
                        parent_hwnds = win.parent_handle_dic
                        side_hwnds = win.side_window_dic

                    cmd = recv_msg.message[1]
                    window_name = recv_msg.message[2]

                    self.win = likeyoubot_win.LYBWin(configure.window_title, configure)

                    if cmd == 'show':
                        self.logger.warn('창 보이기')
                        custom_loc_x = 0
                        custom_loc_y = 0
                    else:
                        self.logger.warn('창 숨기기' + ' ' + str(resolution_w) + ', ' + str(resolution_h))
                        custom_loc_x = resolution_w
                        custom_loc_y = resolution_h

                    if window_name == None:
                        # if len(self.ui.parent_hwnds) > 0:
                        # 	hwnds = self.ui.parent_hwnds
                        # else:
                        # 	hwnds = self.ui.hwnds

                        # self.ui.searchWindow(None)
                        handle_list = []
                        for key, each_handle in hwnds.items():
                            handle_list.append(each_handle)

                        parent_handle_dic = parent_hwnds
                        side_handle_dic = side_hwnds
                    else:
                        win_hwnds = hwnds[window_name]
                        handle_list = [win_hwnds]

                        parent_handle_dic = {}
                        try:
                            parent_handle_dic[win_hwnds] = parent_hwnds[win_hwnds]
                        except:
                            pass

                        side_handle_dic = {}
                        try:
                            side_handle_dic[win_hwnds] = side_hwnds[win_hwnds]
                        except:
                            pass

                    window_list, rhwnds_dic = self.set_location(
                        configure.window_config,
                        handle_list,
                        side_handle_dic,
                        parent_handle_dic,
                        custom_loc_x=custom_loc_x,
                        custom_loc_y=custom_loc_y)

                    if cmd == 'show':
                        for each_hwnd in handle_list:
                            if each_hwnd in parent_hwnds:
                                self.win.set_visible(parent_hwnds[each_hwnd])
                            else:
                                self.win.set_visible(each_hwnd)
                    else:
                        for each_hwnd in handle_list:
                            if each_hwnd in parent_hwnds:
                                self.win.set_invisible(parent_hwnds[each_hwnd])
                            else:
                                self.win.set_invisible(each_hwnd)

                    self.response_queue.join()
                    break
                elif recv_msg.type == 'websocket':
                    self.ui = recv_msg.message
                    threading.currentThread().setName('websocket_worker')
                    # websocket.enableTrace(True)
                    # ws = websocket.WebSocketApp("ws://localhost:18091",
                    #                             on_message=self.on_message,
                    #                             on_error=self.on_error,
                    #                             on_close=self.on_close)
                    # ws.on_open = self.on_open
                    if self.ui.ws is not None:
                        self.ui.ws.run_forever()
                elif recv_msg.type == 'long_polling':
                    self.ui = recv_msg.message
                    threading.currentThread().setName('long_polling_worker')
                    # self.logger.debug('long_polling_worker started')
                    if self.win is None:
                        self.win = likeyoubot_win.LYBWin(self.ui.configure.window_title, self.ui.configure)
                elif recv_msg.type == 'thumbnail':
                    self.ui = recv_msg.message[0]
                    window_name = recv_msg.message[1]
                    # img = self.win.get_window_screenshot(self.multi_hwnd, 2)
                    # img_np = np.array(img)
                    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                    # cv2.imshow("test", frame)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()

                    win_hwnds = self.ui.hwnds[window_name]
                    self.win = likeyoubot_win.LYBWin(self.ui.configure.window_title, self.ui.configure)
                    (anchor_x, anchor_y, end_x, end_y) = self.win.get_window_location(win_hwnds)
                    adj_x, adj_y = self.win.get_player_adjust(win_hwnds)
                    width = int(self.ui.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'width'])
                    height = int(self.ui.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'height'])
                    is_shortcut = self.ui.configure.common_config[lybconstant.LYB_DO_STRING_THUMBNAIL_SIZE + 'shortcut']
                    while (True):

                        win_hwnds = self.ui.hwnds[window_name]
                        # img = ImageGrab.grab(bbox=(anchor_x - adj_x, anchor_y - adj_y, end_x, end_y))
                        try:
                            img = self.win.get_window_screenshot(win_hwnds, 2)
                        # img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height)
                        except:
                            # self.logger.error(traceback.format_exc())
                            pass

                        img_np = np.array(img)
                        img_np = cv2.resize(img_np, (width, height), interpolation=cv2.INTER_AREA)
                        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                        if is_shortcut == True:
                            title = "Press ESC or Q " + str(win_hwnds)
                        else:
                            title = "DogFooter " + str(win_hwnds)
                        cv2.imshow(title, frame)
                        wait_key = cv2.waitKey(25)

                        if is_shortcut == True:
                            if wait_key & 0xFF == ord('q'):
                                break
                            elif wait_key == 27:
                                break

                        if cv2.getWindowProperty(title, 0) == -1:
                            break

                    cv2.destroyAllWindows()
                    break
                elif recv_msg.type == 'start':
                    self.start_action = True
                    self.start_flag = recv_msg.message[0]
                    self.hwnd = recv_msg.message[1]
                    self.window_title = recv_msg.message[2]
                    self.game_name = recv_msg.message[3]
                    self.game_option = recv_msg.message[4]
                    self.config = recv_msg.message[5]
                    self.common_config = self.config.common_config
                    self.window_config = recv_msg.message[6]
                    self.side_hwnd = recv_msg.message[7]
                    self.parent_hwnd = recv_msg.message[8]
                    self.multi_handle_dic = recv_msg.message[9]
                    self.game_tab = recv_msg.message[10]

                    threading.currentThread().setName(self.window_title)

                    if self.win == None:
                        self.win = likeyoubot_win.LYBWin(self.configure.window_title, self.configure)
                    if self.window_config[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE] == False:
                        self.win.set_foreground(self.hwnd)

                    # 무슨 게임이냐에 따라서
                    try:

                        if self.game_name == lybconstant.LYB_GAME_V4:
                            self.game = likeyoubot_v4.LYBV4(None, None, self.win)
                        # elif self.game_name == lybconstant.LYB_GAME_HUNDREDSOUL:
                        # 	self.game = likeyoubot_hundredsoul.LYBHundredSoul(None, None, self.win)

                        # elif self.game_name == lybconstant.LYB_GAME_BLACKDESERT:
                        # 	self.game = likeyoubot_blackdesert.LYBBlackDesert(None, None, self.win)
                        # elif self.game_name == lybconstant.LYB_GAME_BLADE2:
                        # 	self.game = likeyoubot_blade2.LYBBlade2(None, None, self.win)
                        # elif self.game_name == lybconstant.LYB_GAME_ICARUS:
                        # 	self.game = likeyoubot_icarus.LYBIcarus(None, None, self.win)
                        # elif self.game_name == lybconstant.LYB_GAME_TALION:
                        # 	self.game = likeyoubot_talion.LYBTalion(None, None, self.win)

                        self.game.setGameTab(self.game_tab)
                        self.game.setLoggingQueue(self.response_queue)
                        self.game.setCommonConfig(self.config)
                        self.game.setWindowConfig(self.window_config)
                        self.game.setWindowHandle(self.hwnd, self.side_hwnd, self.parent_hwnd, self.multi_handle_dic)
                        self.game.setStartFlag(self.start_flag)

                    except:
                        self.logger.error(traceback.format_exc())
                        # self.response_queue.put_nowait(likeyoubot_message.LYBMessage('log', 'Thread Game Init Exception:' +  str(sys.exc_info()[0]) + '(' +str(sys.exc_info()[1]) + ')'))
                        self.response_queue.put_nowait(
                            likeyoubot_message.LYBMessage('end_return', 'Fail to initialize'))
                        self.response_queue.join()
                        break

                    self.logger.info('[' + self.window_title + '] 창, [' + self.game_name + '] 게임 작업 시작')
                    # self.response_queue.put_nowait(
                    # 	likeyoubot_message.LYBMessage('log',
                    # 		'[' + self.window_title + '] 창에서 [' + self.game_name + '] 게임에 대해 작업을 시작합니다')
                    # 	)

                    self.app_player_type, resolution = self.win.get_player(self.hwnd)
                    win_width, win_height = self.win.get_player_size(self.hwnd)

                    # print(win_width, win_height)
                    if (self.app_player_type == 'momo' or
                            self.app_player_type == 'memu'
                    ):

                        self.response_queue.put_nowait(
                            likeyoubot_message.LYBMessage('log',
                                                          '[' + self.window_title + '] 창 크기: ' + str(
                                                              (win_width, win_height)) + ', 플레이어 종류: ' + '모모/미뮤')
                        )
                        if (self.window_config[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG] == '윈7' or
                                self.window_config[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE] == False):
                            self.logger.warn('앱 플레이어 재시작 기능은 Windows 10 비활성 모드 필수')
                        else:
                            if lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO in self.multi_handle_dic:
                                self.multi_hwnd = self.multi_handle_dic[lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO]
                                self.logger.critical(str(lybconstant.LYB_MULTI_APP_PLAYER_NAME_MOMO) + '(' + str(
                                    self.multi_hwnd) + ') 검색됨')
                                self.logger.critical('앱 플레이어 재시작 기능 사용 가능')

                        # img = self.win.get_window_screenshot(self.multi_hwnd, 2)
                        # img_np = np.array(img)
                        # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                        # cv2.imshow("test", frame)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()

                        # (anchor_x, anchor_y, end_x, end_y) = self.win.get_window_location(self.hwnd)
                        # adj_x, adj_y = self.win.get_player_adjust(self.hwnd)
                        # self.logger.warn('CP1')
                        # while(True):
                        # 	# img = ImageGrab.grab(bbox=(anchor_x - adj_x, anchor_y - adj_y, end_x, end_y))
                        # 	img = self.win.get_window_screenshot(self.hwnd, 2)
                        # 	# img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height)

                        # 	img_np = np.array(img)
                        # 	img_np = cv2.resize(img_np, (64, 36), interpolation = cv2.INTER_AREA)
                        # 	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                        # 	cv2.imshow("test", frame)
                        # 	if cv2.waitKey(25) & 0xFF == ord('q'):
                        # 		break

                        # cv2.destroyAllWindows()
                        # self.logger.warn('CP2')

                    elif self.app_player_type == 'nox':

                        self.response_queue.put_nowait(
                            likeyoubot_message.LYBMessage('log',
                                                          '[' + self.window_title + '] 창 크기: ' + str(
                                                              (win_width, win_height)) + ', 플레이어 종류: ' + '녹스')
                        )

                    else:
                        self.response_queue.put_nowait(
                            likeyoubot_message.LYBMessage('log',
                                                          '[' + self.window_title + '] 창 크기: ' + str(
                                                              (win_width, win_height)) + ' - (' + str(likeyoubot_win.LYBWin.WIDTH) + 'x' + str(likeyoubot_win.LYBWin.HEIGHT) + ') 불일치')
                        )
                        self.response_queue.put_nowait(
                            likeyoubot_message.LYBMessage('end_return', 'Fail to initialize'))
                        self.response_queue.join()
                        break

                    self.game.setAppPlayer(self.app_player_type)

                elif recv_msg.type == 'pause':
                    if self.pause_flag == True:
                        if self.game != None:
                            self.game.interval = None
                        self.logger.warn("Resume")
                        self.pause_flag = False
                    else:
                        self.logger.warn("Paused")
                        self.pause_flag = True

            except queue.Empty:
                pass
            except:
                self.logger.error(traceback.format_exc())
                self.response_queue.put_nowait(likeyoubot_message.LYBMessage('end_return', str(traceback.format_exc())))
                self.response_queue.join()
                break

            try:
                if self.start_action:
                    s = time.time()
                    rc = self.letsgetit()
                    if rc < 0:
                        self.response_queue.put_nowait(
                            likeyoubot_message.LYBMessage('end_return', self.window_title + ' 비정상'))
                        break
                    elif rc == 7000051:
                        self.logger.warn('DEBUG CP - 1')
                        self.response_queue.put_nowait(likeyoubot_message.LYBMessage('stop_app', self.game))
                        self.response_queue.join()
                        self.game.interval = int(
                            self.common_config[lybconstant.LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER + 'delay']) - 1
                    else:
                        self.response_queue.put_nowait(likeyoubot_message.LYBMessage('game_object', self.game))
                    e = time.time()
                # print('[DEBUG] Process Game:', round(e-s, 2))
                else:
                    if recv_msg is not None and recv_msg.type == 'long_polling':
                        if self.ui is not None:
                            # self.logger.info('long_polling start')
                            rc = self.long_polling()
                            if rc < 0:
                                self.logger.error('long_polling_worker is terminated abnormally.')
                                break
            except:
                self.logger.error(traceback.format_exc())
                # self.logger.error(str(sys.exc_info()[0]) + '(' +str(sys.exc_info()[1]) + ')')
                self.response_queue.put_nowait(likeyoubot_message.LYBMessage('end_return', str(traceback.format_exc())))
                self.response_queue.join()
                break

            if self.game != None and self.game.interval != None:
                # print('[GAME INTERVAL]:', self.game.interval)
                if self.game.interval > 0:
                    time.sleep(self.game.interval)
                self.game.interval = None
            else:
                if self.common_config == None:
                    time.sleep(1)
                else:
                    # print('[INTERVAL]:', float(self.common_config['wakeup_period_entry']))
                    time.sleep(float(self.common_config['wakeup_period_entry']))

    # logger.debug('['+self.name+']'+' end:'+str(threading.currentThread()))

    def findWindows(self):

        self.win = likeyoubot_win.LYBWin(self.configure.window_title, self.configure)

        wildcard = ".*" + self.configure.keyword + ".*"
        # wildcard = '.*'
        # print('DEBUG 1003:', wildcard)

        self.win.find_window_wildcard(wildcard)

        # print('DEBUG 1004:', self.win.handle_list)

        for each_hwnd in self.win.handle_list:
            # self.win.set_foreground(each_hwnd)
            time.sleep(0.1)
        time.sleep(0.1)
        # self.win.set_foreground(self.win.my_handle)

        return (
        self.win.handle_list, self.win.side_window_dic, self.win.parent_handle_dic, self.win.multi_window_handle_dic)

    # return (self.win.handle_list, {})

    def letsgetit(self):
        logging = '';

        (anchor_x, anchor_y, end_x, end_y) = self.win.get_window_location(self.hwnd)
        adj_x, adj_y = self.win.get_player_adjust_capture(self.hwnd)
        cur_x, cur_y = pyautogui.position()

        self.game.cursor_loc = (cur_x - anchor_x + adj_x, cur_y - anchor_y + adj_x)
        self.game.statistics['마우스 포인터 위치'] = (cur_x - anchor_x + adj_x, cur_y - anchor_y + adj_x)

        # print('inactive mode flag =', self.window_config[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG])
        if self.window_config[lybconstant.LYB_DO_STRING_INACTIVE_MODE_FLAG] == '윈7':
            inactive_flag = 1
        else:
            inactive_flag = 2

        # print( self.app_player_type, (anchor_x, anchor_y, end_x, end_y) )
        # print('START GRAB', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        # s = time.time()
        try:
            if self.window_config[lybconstant.LYB_DO_BOOLEAN_USE_INACTIVE_MODE] is False:
                current_window_image_grab = ImageGrab.grab(bbox=(anchor_x - adj_x, anchor_y - adj_y, end_x, end_y))
            else:
                current_window_image_grab = self.win.get_window_screenshot(self.hwnd, inactive_flag)
        except:
           # self.logger.error(traceback.format_exc())
            return 0
        # e = time.time()
        # print('[DEBUG] Grab Screenshot:', round(e-s,2))
        # print('END GRAB', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        # current_window_image_grab.save("test.png")

        # time.sleep(2)
        # sys.exit()

        return self.game.process(current_window_image_grab)

    # self.resource_manager.pixel_box_dic.debug()
    # print(self.resource_manager.pixel_box_dic['lineage_revolution_icon'][0])
    # ((loc_x, loc_y), (pixel_R, pixel_G, pixel_B)) = self.resource_manager.pixel_box_dic['lineage_revolution_icon'][0]
    # self.win.mouse_click(self.hwnd, int(loc_x), int(loc_y))
    # logging = 'Click (' + str(loc_x) + ', ' + str(loc_y) + '):'
    # self.win.mouse_drag(self.hwnd, 400, 180, 450, 180)

    def long_polling(self):
        try:
            self.ui.update_telegram()
        # self.ui.check_ip()

        # f2 = win32api.GetAsyncKeyState(win32con.VK_F2)
        # shift = win32api.GetAsyncKeyState(win32con.VK_SHIFT)
        # e = win32api.GetAsyncKeyState(ord('E'))

        # if len(self.ui.parent_hwnds) > 0:
        # 	hwnds = self.ui.parent_hwnds
        # else:
        # 	hwnds = self.ui.hwnds

        # # if f2 != 0 and shift != 0:
        # if self.ui.show_window == True:
        # 	self.logger.warn('창 보이기')
        # 	self.ui.searchWindow(None)
        # 	for key, each_hwnd in hwnds.items():
        # 		self.win.set_visible(each_hwnd)
        # 	self.ui.show_window = False

        # # elif f2 != 0:
        # elif self.ui.hide_window == True:
        # 	self.logger.warn('창 숨기기')

        # 	(handle_list, side_handle_dic, parent_handle_dic, multi_handle_dic) = self.findWindows()
        # 	window_list, rhwnds_dic = self.set_location(
        # 								self.ui.configure.window_config,
        # 								handle_list,
        # 								side_handle_dic,
        # 								parent_handle_dic,
        # 								custom_loc_x=self.ui.master.winfo_screenwidth(),
        # 								custom_loc_y=self.ui.master.winfo_screenheight() )
        # 	for key, each_hwnd in hwnds.items():
        # 		self.win.set_invisible(int(each_hwnd))

        # 	self.ui.hide_window = False
        except:
            # self.ui.show_window = False
            # self.ui.hide_window = False
            self.logger.error(traceback.format_exc())

        return 0

    def set_location(self, window_config, handle_list, side_handle_dic, parent_handle_dic, custom_loc_x=0,
                     custom_loc_y=0):

        rhwnds_dic = {}
        window_list = []

        iterator = 0
        for h in handle_list:
            if h in parent_handle_dic:
                win_title = self.win.get_title(parent_handle_dic[h])
                self.logger.warn('ldplayer ' + str((custom_loc_x, custom_loc_y)) + ' ' + str(win_title))
                try:
                    if window_config[win_title][lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'] == True:
                        try:
                            win_loc_x = int(window_config[win_title][
                                                lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x']) + custom_loc_x
                            win_loc_y = int(window_config[win_title][
                                                lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y']) + custom_loc_y
                        except:
                            win_loc_x = custom_loc_x
                            win_loc_y = custom_loc_y

                        self.win.set_window_pos(parent_handle_dic[h], win_loc_x, win_loc_y)
                except:
                    pass
            else:
                win_title = self.win.get_title(h)
                self.logger.warn('nox ' + str((custom_loc_x, custom_loc_y)) + ' ' + str(win_title))
                try:
                    if window_config[win_title][lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'] == True:
                        try:
                            win_loc_x = int(window_config[win_title][
                                                lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x']) + custom_loc_x
                            win_loc_y = int(window_config[win_title][
                                                lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y']) + custom_loc_y
                        except:
                            win_loc_x = custom_loc_x
                            win_loc_y = custom_loc_y

                        self.win.set_window_pos(h, win_loc_x, win_loc_y)
                except:
                    pass

            if h in side_handle_dic:
                win_title = self.win.get_title(h)
                # self.logger.info('----------------------->' + win_title)
                # adjust_x = 4
                # adjust_y = 30
                # 20190807 Nox 사이드바 변경됨('Form')
                adjust_x = 0
                adjust_y = 0
                try:
                    if window_config[win_title][lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'boolean'] == True:
                        win_width, win_height = self.win.get_player_size(h)
                        try:
                            win_loc_x = int(window_config[win_title][
                                                lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'x']) + win_width + adjust_x + custom_loc_x
                            win_loc_y = int(window_config[win_title][
                                                lybconstant.LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION + 'y']) + adjust_y + custom_loc_y
                        except:
                            win_loc_x = win_width + adjust_x + custom_loc_x
                            win_loc_y = adjust_y + custom_loc_y

                        self.win.set_window_pos(side_handle_dic[h], win_loc_x, win_loc_y)
                except:
                    pass

            window_list.append(win_title)
            rhwnds_dic[win_title] = h

            win_width, win_height = self.win.get_player_size(h)
            iterator += 1
        # time.sleep(1)

        return window_list, rhwnds_dic

    # @staticmethod
    # def on_message(ws, message):
    #     print(message)
    #
    # @staticmethod
    # def on_error(ws, error):
    #     print(error)
    #
    # @staticmethod
    # def on_close(ws):
    #     print("### closed ###")
    #
    # @staticmethod
    # def on_open(ws):
    #     print('onopen')
    #     ws.send("%s connected" % threading.currentThread().getName())
    #     time.sleep(1)
    #     # ws.close()
    #     # print("thread terminating...")
