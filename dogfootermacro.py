import threading
import time
import collections
import sys
import os
import likeyoubot_logger
import likeyoubot_win
import likeyoubot_configure
import likeyoubot_worker
import likeyoubot_message
import likeyoubot_rest
import webbrowser
import signal
from PIL import ImageGrab
import cv2
import numpy as np
import pickle
import queue
import traceback
import copy


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

signal.signal(signal.SIGINT, signal.SIG_DFL)
global dogfootermacro_logger
global dogfootermacro_games

form_class = uic.loadUiType('dogfootermacro.ui')[0]
dogfootermacro_title = 'DogFooter Macro'
dogfootermacro_games = []

def resource_path(relative):
	return os.path.join(
	os.environ.get(
	    "_MEIPASS2",
	    os.path.abspath(".")
	),
	relative
	)

class PlayThread(QThread):
	def __init__(self, ui):
		QThread.__init__(self)
		self.ui = ui
		self.hwnd = self.ui.hwnd_dic[self.ui.appPlayer_comboBox.currentText()]
		self.win = self.ui.win

	def __del__(self):
		self.wait()

	def run(self):

		while True:
			try:

				dogfootermacro_logger.debug('1. ' + str(self.ui.configure.common_config['wakeup_period_entry']))

				response_message = self.ui.worker_thread.response_queue.get()
				if response_message == None:
					continue

				if response_message.type == 'game_object':
					game_object = response_message.message
					if game_object != None:
						if game_object.current_schedule_work != None and game_object.main_scene != None:
							if self.ui.schedule_comboBox.currentText() != game_object.current_schedule_work and len(game_object.main_scene.move_status) < 1:
								self.ui.skip_signal_schedule_comboBox = True
								# self.ui.schedule_comboBox.setCurrentIndex( self.ui.configure.window_config['custom_config_dic'][self.ui.config_comboBox.currentText()]['schedule_list'].index(game_object.current_schedule_work))
								try:
									if game_object.main_scene.last_status[game_object.main_scene.current_work] > 0:
										# dogfootermacro_logger.debug('last_status =====> ' + str(game_object.main_scene.last_status))
										# dogfootermacro_logger.debug('callstack =====> ' + str(game_object.main_scene.callstack))
										# dogfootermacro_logger.debug('callstack_status =====> ' + str(game_object.main_scene.callstack_status))
										if len(game_object.main_scene.callstack) < 1:
											self.ui.schedule_comboBox.setCurrentIndex(game_object.main_scene.last_status[game_object.main_scene.current_work] - 1)
										else:
											self.ui.schedule_comboBox.setCurrentIndex(game_object.main_scene.callstack_status[0] - 1)												
									else:
										self.ui.schedule_comboBox.setCurrentIndex(0)
								except:
									self.ui.schedule_comboBox.setCurrentIndex(0)

						self.ui.game_object = game_object
				elif response_message.type == 'end':
					break


				self.ui.worker_thread.response_queue.task_done()

			except queue.Empty:
				dogfootermacro_logger.debug('empty')
			except:
				dogfootermacro_logger.error(traceback.format_exc())
				break
		
		return

		# (anchor_x, anchor_y, end_x, end_y) = self.win.get_window_location(self.hwnd)
		# adj_x, adj_y = self.win.get_player_adjust(self.hwnd)
		# while(True):
		# 	# img = ImageGrab.grab(bbox=(anchor_x - adj_x, anchor_y - adj_y, end_x, end_y))
		# 	img = self.win.get_window_screenshot(self.hwnd, 2)
		# 	# img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height)
		# 	img_np = np.array(img)
		# 	# img_np = cv2.resize(img_np, (width, height), interpolation = cv2.INTER_AREA)
			
		# 	r = int(self.ui.lower_r_slider.value())
		# 	g = int(self.ui.lower_g_slider.value())
		# 	b = int(self.ui.lower_b_slider.value())

		# 	# lowerBound = np.array((r, g, b), dtype=np.uint8, ndmin=1)
		# 	# upperBound = np.array((255, 255, 255), dtype=np.uint8, ndmin=1)
		# 	lowerBound = (r, g, b)
			
		# 	r = int(self.ui.upper_r_slider.value())
		# 	g = int(self.ui.upper_g_slider.value())
		# 	b = int(self.ui.upper_b_slider.value())

		# 	upperBound = (r, g, b)

		# 	anchor_x = int(self.ui.view_anchor_x_spinBox.value())
		# 	anchor_y = int(self.ui.view_anchor_y_spinBox.value())

		# 	width = int(self.ui.view_width_spinBox.value())
		# 	height = int(self.ui.view_height_spinBox.value())

		# 	if width < anchor_x + 120:
		# 		width = anchor_x + 120

		# 	if height < anchor_y + 120:
		# 		height = anchor_y + 120



		# 	img_np = cv2.inRange(img_np, lowerBound, upperBound)
		# 	img_np = img_np[anchor_y:height, anchor_x:width]
		# 	# tgt = img_np.copy()
		# 	# for row in range(img.height):
		# 	# 	for col in range(img.width):
		# 	# 		img_np[row][col][0] = 255 - img_np[row][col][0] 
		# 	# 		img_np[row][col][1] = 255 - img_np[row][col][1] 
		# 	# 		img_np[row][col][2] = 255 - img_np[row][col][2] 

		# 	# frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
		# 	title = "Press ESC or Q " + str(self.hwnd)

		# 	cv2.imshow(title, img_np)
		# 	wait_key = cv2.waitKey(25)

		# 	if wait_key & 0xFF == ord('q'):
		# 		break
		# 	elif wait_key == 27:
		# 		break

		# 	if cv2.getWindowProperty(title, 0) == -1:
		# 		break

		# cv2.destroyAllWindows()	


class MainWindow(QMainWindow, form_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle(dogfootermacro_title)
		self.refresh_pushButton.clicked.connect(self.callback_refresh_pushButton_clicked)
		self.start_pushButton.clicked.connect(self.callback_start_pushButton_clicked)
		self.stop_pushButton.clicked.connect(self.callback_stop_pushButton_clicked)
		self.pause_pushButton.clicked.connect(self.callback_pause_pushButton_clicked)
		self.hide_pushButton.clicked.connect(self.callback_hide_pushButton_clicked)
		self.show_pushButton.clicked.connect(self.callback_show_pushButton_clicked)
		self.homepage_pushButton.clicked.connect(self.callback_homepage_pushButton_clicked)

		self.appPlayer_comboBox.currentIndexChanged.connect(self.callback_appPlayer_comboBox_currentIndexChanged)
		self.game_comboBox.currentIndexChanged.connect(self.callback_game_comboBox_currentIndexChanged)
		self.config_comboBox.currentIndexChanged.connect(self.callback_config_comboBox_currentIndexChanged)
		self.schedule_comboBox.currentIndexChanged.connect(self.callback_schedule_comboBox_currentIndexChanged)
		self.skip_signal_schedule_comboBox = False
		self.configure = None
		self.worker_thread = None
		self.play_thread = None
		self.game_object = None
		# self.search_comboBox.currentIndexChanged.connect(self.callback_search_comboBox_currentIndexChanged)
		# self.play_button.clicked.connect(self.callback_play_button_clicked)

		# self.upper_r_slider.valueChanged.connect(self.callback_upper_r_slider_changed)
		# self.upper_r_spinBox.valueChanged.connect(self.callback_upper_r_spinBox_changed)
		# self.upper_g_slider.valueChanged.connect(self.callback_upper_g_slider_changed)
		# self.upper_g_spinBox.valueChanged.connect(self.callback_upper_g_spinBox_changed)
		# self.upper_b_slider.valueChanged.connect(self.callback_upper_b_slider_changed)
		# self.upper_b_spinBox.valueChanged.connect(self.callback_upper_b_spinBox_changed)


		# self.lower_r_slider.valueChanged.connect(self.callback_lower_r_slider_changed)
		# self.lower_r_spinBox.valueChanged.connect(self.callback_lower_r_spinBox_changed)
		# self.lower_g_slider.valueChanged.connect(self.callback_lower_g_slider_changed)
		# self.lower_g_spinBox.valueChanged.connect(self.callback_lower_g_spinBox_changed)
		# self.lower_b_slider.valueChanged.connect(self.callback_lower_b_slider_changed)
		# self.lower_b_spinBox.valueChanged.connect(self.callback_lower_b_spinBox_changed)


		self.win = likeyoubot_win.LYBWin(dogfootermacro_title)
		self.hwnd_dic = {}

	def callback_refresh_pushButton_clicked(self):
		try:
			with open(resource_path('lyb.cfg'), 'rb') as dat_file:
				self.configure = pickle.load(dat_file)

			self.configure.path = resource_path('lyb.cfg')
			dogfootermacro_logger.debug('configure.path [' + self.configure.path + ']')

		except FileNotFoundError:       
			exitMessage = QMessageBox.warning(self, ' ', resource_path('lyb2.cfg') + ' 파일이 없습니다.')
			sys.exit(1)

		self.appPlayer_comboBox.clear()
		try:
			self.win.find_window_wildcard('')
			for each_hwnd in self.win.handle_list:
				dogfootermacro_logger.debug(str(each_hwnd) + ' ' + self.win.get_title(each_hwnd))
				if each_hwnd in self.win.parent_handle_dic:
					title = self.win.get_title(self.win.parent_handle_dic[each_hwnd])
				else:
					title = self.win.get_title(each_hwnd)

				self.appPlayer_comboBox.addItem(title)
				self.hwnd_dic[title] = each_hwnd

			dogfootermacro_logger.debug(self.appPlayer_comboBox.count())
			if self.appPlayer_comboBox.count() > 0:
				self.setEnabledAllButton(True)
			else:
				self.setEnabledAllButton(False)

			self.callback_appPlayer_comboBox_currentIndexChanged()

		except:
			self.win = likeyoubot_win.LYBWin(dogfootermacro_title)
			self.hwnd_dic = {}
			dogfootermacro_logger.error(traceback.format_exc())

	def setEnabledAllButton(self, isEnabled):
		self.start_pushButton.setEnabled(isEnabled)
		# self.stop_pushButton.setEnabled(isEnabled)
		#self.pause_pushButton.setEnabled(isEnabled)
		self.hide_pushButton.setEnabled(isEnabled)
		self.show_pushButton.setEnabled(isEnabled)

	def setEnabledStartButton(self, isEnabled):
		self.start_pushButton.setEnabled(isEnabled)	
		self.stop_pushButton.setEnabled(not isEnabled)
		self.pause_pushButton.setEnabled(not isEnabled)
		self.refresh_pushButton.setEnabled(isEnabled)
		self.appPlayer_comboBox.setEnabled(isEnabled)
		self.game_comboBox.setEnabled(isEnabled)
		self.config_comboBox.setEnabled(isEnabled)

	def callback_start_pushButton_clicked(self):
		self.setEnabledStartButton(False)
		pass_config = copy.deepcopy(self.configure)

		pass_config.window_config[self.appPlayer_comboBox.currentText()][self.game_comboBox.currentText()]['schedule_list'] = \
			copy.deepcopy(pass_config.window_config['custom_config_dic'][self.config_comboBox.currentText()]['schedule_list'])

		dogfootermacro_logger.debug(pass_config.window_config[self.appPlayer_comboBox.currentText()][self.game_comboBox.currentText()]['schedule_list'])

		self.worker_thread = likeyoubot_worker.LYBWorker('Worker', pass_config, queue.Queue(), queue.Queue())
		self.worker_thread.daemon = True
		self.worker_thread.start()

		hwnd = self.hwnd_dic[self.appPlayer_comboBox.currentText()]

		side_hwnd = None
		if hwnd in self.win.side_window_dic:
			side_hwnd = self.win.side_window_dic[hwnd]

		parent_hwnd = None
		if hwnd in self.win.parent_handle_dic:
			parent_hwnd = self.win.parent_handle_dic[hwnd]

		started_window_name = self.appPlayer_comboBox.currentText()
		started_game_name = self.game_comboBox.currentText()

		if started_game_name in pass_config.window_config[started_window_name]:
			started_option			= pass_config.get_window_config(started_window_name, started_game_name)
		else:
			started_option			= pass_config.common_config[started_game_name]

		for key, value in pass_config.common_config[started_game_name].items():
			dogfootermacro_logger.debug(key)

		self.worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('start', 
			[
				self.schedule_comboBox.currentIndex() + 1, 
				hwnd, 
				self.appPlayer_comboBox.currentText(),
				self.game_comboBox.currentText(),
				started_option,
				pass_config,
				pass_config.window_config[self.appPlayer_comboBox.currentText()],
				side_hwnd,
				parent_hwnd,
				self.win.multi_window_handle_dic,
				None,
				]					
			)
		)

		self.setWindowTitle(dogfootermacro_title + ' - ' + self.appPlayer_comboBox.currentText() + ' : ' + self.game_comboBox.currentText())

		self.play_thread =  PlayThread(self)
		self.play_thread.start()

	def callback_stop_pushButton_clicked(self):
		self.setEnabledStartButton(True)
		self.setWindowTitle(dogfootermacro_title)
		self.worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('end', None))

	def callback_pause_pushButton_clicked(self):
		self.worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('pause', None))
		if '일시' in self.pause_pushButton.text():
			self.pause_pushButton.setText('재시작')
		else:
			self.pause_pushButton.setText('일시 정지')


	def callback_show_pushButton_clicked(self):
		worker_thread = likeyoubot_worker.LYBWorker('Worker', self.configure, queue.Queue(), queue.Queue())
		worker_thread.daemon = True
		worker_thread.start()

		worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('watchout2', [self.configure, 'show', self.appPlayer_comboBox.currentText(), self.win, self.hwnd_dic]))

	def callback_hide_pushButton_clicked(self):
		worker_thread = likeyoubot_worker.LYBWorker('Worker', self.configure, queue.Queue(), queue.Queue())
		worker_thread.daemon = True
		worker_thread.start()
		worker_thread.command_queue.put_nowait(likeyoubot_message.LYBMessage('watchout2', [self.configure, 'hide', self.appPlayer_comboBox.currentText(), self.win, self.hwnd_dic]))

	def callback_homepage_pushButton_clicked(self):
		return
		# webbrowser.open_new(likeyoubot_rest.LYBHttp.getMacroBaseUrl())

	def callback_appPlayer_comboBox_currentIndexChanged(self):
		dogfootermacro_logger.debug('callback_appPlayer_comboBox_currentIndexChanged called()')
		appPlayer_name = self.appPlayer_comboBox.currentText()
		dogfootermacro_logger.debug('appPlayer_name: ' + appPlayer_name)
		if len(appPlayer_name) < 1:
			return

		if not appPlayer_name in self.configure.window_config:
			exitMessage = QMessageBox.warning(self, ' ', '앱플레이어[' + str(appPlayer_name) + '] 설정 정보가 없습니다.')
		else:

			game_name = self.configure.window_config[appPlayer_name]['games']
			self.game_comboBox.clear()
			for each_game in dogfootermacro_games:
				self.game_comboBox.addItem(each_game)
			self.game_comboBox.setCurrentIndex(dogfootermacro_games.index(game_name))
			# self.callback_game_comboBox_currentIndexChanged()

	def callback_game_comboBox_currentIndexChanged(self):
		dogfootermacro_logger.debug('callback_game_comboBox_currentIndexChanged')
		if len(self.game_comboBox.currentText()) < 1:
			return

		last_config_name = self.game_comboBox.currentText() + '_last'
		self.config_comboBox.clear()
		# dogfootermacro_logger.debug(last_config_name)
		temp_list = []
		for each_config, each_config_value in self.configure.window_config['custom_config_dic'].items():
			# dogfootermacro_logger.debug(self.game_comboBox.currentText())
			if self.game_comboBox.currentText() in each_config:
				if each_config == self.game_comboBox.currentText():
					pass
				else:
					temp_list.append(each_config)
					self.config_comboBox.addItem(each_config)

		dogfootermacro_logger.debug(last_config_name)
		if last_config_name in self.configure.window_config[self.appPlayer_comboBox.currentText()]:
			self.config_comboBox.setCurrentIndex(temp_list.index(self.configure.window_config[self.appPlayer_comboBox.currentText()][last_config_name]))
		else:
			self.config_comboBox.setCurrentIndex(0)

	def callback_config_comboBox_currentIndexChanged(self):
		dogfootermacro_logger.debug('callback_config_comboBox_currentIndexChanged')
		if len(self.config_comboBox.currentText()) < 1:
			return

		self.schedule_comboBox.clear()
		for each_work in self.configure.window_config['custom_config_dic'][self.config_comboBox.currentText()]['schedule_list']:
			if len(each_work) > 0:
				self.schedule_comboBox.addItem(each_work)

		self.schedule_comboBox.setCurrentIndex(0)

	def callback_schedule_comboBox_currentIndexChanged(self):
		dogfootermacro_logger.debug('callback_schedule_comboBox_currentIndexChanged')
		if len(self.schedule_comboBox.currentText()) < 1:
			return


		if self.skip_signal_schedule_comboBox == True:
			self.skip_signal_schedule_comboBox = False
			return

		dogfootermacro_logger.debug(self.skip_signal_schedule_comboBox)

		if self.game_object != None and self.game_object.main_scene != None:
			game_object = self.game_object
			index = self.schedule_comboBox.currentIndex()

			max_len = len(game_object.main_scene.get_game_config('schedule_list'))
			if  index >= max_len - 1:
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
				game_object.main_scene.move_status[work_name] = index + 1

	# def callback_search_comboBox_currentIndexChanged(self):
	# 	dogfootermacro_logger.debug('callback_search_comboBox_currentIndexChanged called()')

	# def callback_play_button_clicked(self):
	# 	dogfootermacro_logger.debug('callback_play_button_clicked called()')	
	# 	self.play_thread =  PlayThread(self)
	# 	self.play_thread.start()

	# def callback_upper_r_slider_changed(self):
	# 	self.upper_r_spinBox.setValue(self.upper_r_slider.value())

	# def callback_upper_r_spinBox_changed(self):
	# 	self.upper_r_slider.setValue(self.upper_r_spinBox.value())

	# def callback_upper_g_slider_changed(self):
	# 	self.upper_g_spinBox.setValue(self.upper_g_slider.value())

	# def callback_upper_g_spinBox_changed(self):
	# 	self.upper_g_slider.setValue(self.upper_g_spinBox.value())

	# def callback_upper_b_slider_changed(self):
	# 	self.upper_b_spinBox.setValue(self.upper_b_slider.value())

	# def callback_upper_b_spinBox_changed(self):
	# 	self.upper_b_slider.setValue(self.upper_b_spinBox.value())

	# def callback_lower_r_slider_changed(self):
	# 	self.lower_r_spinBox.setValue(self.lower_r_slider.value())

	# def callback_lower_r_spinBox_changed(self):
	# 	self.lower_r_slider.setValue(self.lower_r_spinBox.value())

	# def callback_lower_g_slider_changed(self):
	# 	self.lower_g_spinBox.setValue(self.lower_g_slider.value())

	# def callback_lower_g_spinBox_changed(self):
	# 	self.lower_g_slider.setValue(self.lower_g_spinBox.value())

	# def callback_lower_b_slider_changed(self):
	# 	self.lower_b_spinBox.setValue(self.lower_b_slider.value())

	# def callback_lower_b_spinBox_changed(self):
	# 	self.lower_b_slider.setValue(self.lower_b_spinBox.value())	

if __name__ == '__main__':

	if len(sys.argv) < 3:
		sys.exit()

	if sys.argv[1] != 'dogfooter':
		sys.exit(1)

	for i in range(len(sys.argv)):
		if i < 2:
			continue
		else:
			dogfootermacro_games.append(sys.argv[i])

	try:
		dogfootermacro_logger = likeyoubot_logger.LYBLogger.getLogger()
		likeyoubot_logger.LYBLogger.setLevel('C')

		app = QApplication(sys.argv)
		app.setWindowIcon(QIcon(resource_path('image/dogfootermacro_icon.png')))

		mainWindow = MainWindow()
		mainWindow.show()
		mainWindow.callback_refresh_pushButton_clicked()
		app.exec_()
	except:
		print('create logger fail: ' +str(sys.exc_info()[0]) + '(' +str(sys.exc_info()[1]) + ')')
		sys.exit(1) 
