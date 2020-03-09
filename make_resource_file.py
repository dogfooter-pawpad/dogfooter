import pyautogui
import pickle
import time
import os
import win32api
import win32gui
import sys
import likeyoubot_resource as lybresource
import likeyoubot_win as lybwin
import likeyoubot_configure as lybconfigure
from PIL import ImageGrab

class LYBMakeResource():
	def __init__(self):
		self.filename = None
		self.window_title = None
		self.resource_manager = None
		self.anchor_x = -1
		self.anchor_y = -1
		self.bx = -1
		self.by = -1
		self.current_grab_window = None
		self.epb = None

	def resource_path(self, relative):
		return os.path.join(
			os.environ.get(
				"_MEIPASS2",
				os.path.abspath(".")
				),
			relative
			)

	def mouseMove(self, str, x, y):
		pyautogui.moveTo( x, y )

	def execute(self):

		print(sys.argv)

		game_name_list = []
		for k, v in lybconfigure.LYBConstant.LYB_GAMES.items():
			game_name_list.append(k)

		if len(game_name_list) > 1:
			if len(sys.argv) > 1:
				game_number = int(sys.argv[1])
			else:
				print('----------------------')
				for game_name in game_name_list:
					print(game_name_list.index(game_name) + 1, game_name)

				print('----------------------')
				print("Select Game: ", end='')
				game_number = input()
		else:
			game_number = 0

		if len(str(game_number)) == 0:
			game_number = 0

		self.filename = lybconfigure.LYBConstant.LYB_GAMES[game_name_list[int(game_number) - 1]] + '.lyb'
		print("filename: ", self.filename)

		if len(sys.argv) > 2:
			self.window_title = ".*" + str(sys.argv[2]) + ".*"
		else:
			self.window_title = ".*"+".*"
			# self.window_title = ".*"+'녹스'+".*"
			# self.window_title = ".*"+'모모 5'+".*"
			# self.window_title = '.*' + 'NoxPlayer' + '.*'

		try:
			with open(self.resource_path(self.filename), 'rb') as resource_file:
				self.resource_manager = pickle.load(resource_file)
		except:
			self.resource_manager = lybresource.LYBResourceManager(lybresource.LYBPixelBoxDic(), lybresource.LYBResourceDic())

		# self.resource_manager.debug()

		window = lybwin.LYBWin('.*cmd\.exe - python.*make_resource_file.py.*')
		window.find_window_wildcard(self.window_title)
		if len(window.handle_list) < 1:
			print('Not found window:', self.window_title)
			sys.exit()

		print(window.my_handle)

		print("'E' : New resource data")
		print("'G' : Pick 7x7 pixels")
		print("'A' : Pick 15x15 pixels")
		print("'S' : Pick 31x31 pixels")
		print("'D' : Pick 63x63 pixels")
		print("'F' : Remove resource data")
		print("'Z' : Search resource data")
		print("'W' : Confirm")
		print("'R' : Redraw")
		print("'T' : Delete all pixel box not in resource")
		print("'Q' : Save & Quit")

		window.set_foreground_console(window.handle_list[0])
		print(window.get_player(window.handle_list[0]), game_name_list[int(game_number) - 1])
		adj_x, adj_y = window.get_player_adjust(window.handle_list[0])
		self.anchor_x, self.anchor_y, self.bx, self.by = win32gui.GetWindowRect(window.handle_list[0])
		self.anchor_x += adj_x
		self.anchor_y += adj_y
		pass_count_for_name = 10
		pixel_box = None
		resource_pixel_box_list = []
		resource_name = ''
		parent_resource_name = ''
		current_resource = None
		resource_type = 'etc'
		is_working = False
		is_done = False
		is_ready = False

		while True:
			x, y = pyautogui.position()
			positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + \
				' ' + str(pyautogui.pixel(x, y)).rjust(16) + \
				'      ' + 'R-X: ' + str(x - self.anchor_x).rjust(4) + ' R-Y: ' + str(y - self.anchor_y).rjust(4)
			print(positionStr, end='')
			print('\b' * len(positionStr), end='', flush=True)

			e = win32api.GetAsyncKeyState(ord('E'))
			a = win32api.GetAsyncKeyState(ord('A'))
			g = win32api.GetAsyncKeyState(ord('G'))
			s = win32api.GetAsyncKeyState(ord('S'))
			d = win32api.GetAsyncKeyState(ord('D'))
			w = win32api.GetAsyncKeyState(ord('W'))
			c = win32api.GetAsyncKeyState(ord('C'))
			f = win32api.GetAsyncKeyState(ord('F'))
			z = win32api.GetAsyncKeyState(ord('Z'))
			r = win32api.GetAsyncKeyState(ord('R'))
			q = win32api.GetAsyncKeyState(ord('Q'))
			t = win32api.GetAsyncKeyState(ord('T'))
			h = win32api.GetAsyncKeyState(ord('H'))

			if pass_count_for_name > 0:
				pass_count_for_name -= 1
				continue

			if e != 0:
				print('\nEnter resource_name: ', end='')
				resource_name = input()
				if len(resource_name) < 1:
					continue
				try:
					current_resource = self.resource_manager.resource_dic[resource_name]
				except:
					if 'loc' == resource_name.split('_')[-1]:
						resource_type = 'location'
					elif 'scene' == resource_name.split('_')[-1]:
						resource_type = 'scene'
					elif 'icon' == resource_name.split('_')[-1]:
						resource_type = 'icon'
					elif 'event' == resource_name.split('_')[-1]:
						resource_type = 'event'
					else:
						resource_type = 'etc'

					print('\n', resource_type, '\n')
					current_resource = lybresource.LYBResource(resource_name, resource_type)

				pass_count_for_name = len(resource_name)

				print('\n')
				# for each_resource_name, each_resource in self.resource_manager.resource_dic.items():
				# 	print(each_resource_name, ':', each_resource.resource_type)

				print('Enter parent resource_name: ', end='')
				parent_resource_name = input()

				if len(parent_resource_name) > 0:
					try:
						parent_rsc = self.resource_manager.resource_dic[parent_resource_name]
						if parent_rsc.pixel_box_count > 0:
							for each_pixel_box_name in parent_rsc:
								current_resource.append(each_pixel_box_name)
					except:
						print('Not found parent resource: ', parent_resource_name)

				pass_count_for_name += len(parent_resource_name)

				# for each_name, each_resource in self.resource_manager.pixel_box_dic.items():
				# 	print(each_name)

				print('Enter pixel_box_name to add: ', end='')
				pixel_box_name = input()

				plist = pixel_box_name.split(',')
				for pname in plist:
					if len(pname) > 0:
						if not pname in self.resource_manager.pixel_box_dic:
							print('Not found pixel_box_name: ', pname)
						else:
							current_resource.append(pname)

				pass_count_for_name += len(pixel_box_name)

				pixel_box = None
				resource_pixel_box_list = []
				is_working = True
				is_done = False
			
			elif f != 0 and is_working == False:
				print('\n')
				# for each_resource_name, each_resource in self.resource_manager.resource_dic.items():
				# 	print(each_resource_name, ':', each_resource.resource_type)

				# for each_pixel_box_name, each_resource in self.resource_manager.pixel_box_dic.items():
				# 	print(each_pixel_box_name, ':', each_resource.height, each_resource.width)

				print('\nEnter resource_name to delete: ', end='')
				resource_name = input()
				if len(resource_name) < 1:
					continue

				if resource_name in self.resource_manager.resource_dic:
					self.resource_manager.resource_dic.pop(resource_name)
					print('\ndeleted resource: ', resource_name)
				else:
					if resource_name in self.resource_manager.pixel_box_dic:
						self.resource_manager.pixel_box_dic.pop(resource_name)
						print('\ndeleted pixel box: ', resource_name)
						
					for each_resource_name, each_pixel_box in self.resource_manager.resource_dic.items():
						for each_pb_name in self.resource_manager.resource_dic[each_resource_name]:
							if each_pb_name == resource_name:
								self.resource_manager.resource_dic[each_resource_name].remove(resource_name)
								print('\ndeleted pixel box name in', each_resource_name)

					if len(self.resource_manager.resource_dic[each_resource_name]) == 0:
						self.resource_manager.resource_dic.pop(each_resource_name)

				pass_count_for_name = len(resource_name)

			elif z != 0 and is_working == False:
				print('\nEnter resource_name to search: ', end='')
				resource_name = input()
				if len(resource_name) < 1:
					continue

				print('\n')
				for each_resource_name, each_resource in self.resource_manager.resource_dic.items():
					if resource_name in each_resource_name:
						print(each_resource_name, ':', each_resource.resource_type)

				for each_pixel_box_name, each_resource in self.resource_manager.pixel_box_dic.items():
					if resource_name in each_pixel_box_name:
						print(each_pixel_box_name, ':', each_resource.height, each_resource.width)

				pass_count_for_name = len(resource_name)

			elif t != 0 and is_working == False:
				print('\nEnter to confirm: ', end='')
				resource_name = input()
				if len(resource_name) < 1:
					continue

				new_pixel_box_dic = lybresource.LYBPixelBoxDic()
				for each_pixel_box_name, each_pixel_box in self.resource_manager.pixel_box_dic.items():
					if not resource_name in each_pixel_box_name:
						continue
					for each_resource_name, each_resource in self.resource_manager.resource_dic.items():
						if each_pixel_box in each_resource:
							new_pixel_box_dic[each_pixel_box_name] = each_pixel_box
							break

				self.resource_manager.pixel_box_dic = new_pixel_box_dic
				pass_count_for_name = len(resource_name)

			elif a != 0 or s != 0 or d != 0 or g != 0 or h != 0 and is_ready == True:
				if h != 0 :
					size = 4
				elif g != 0:
					size = 8
				elif a != 0:
					size = 16
				elif s != 0:
					size = 32
				elif d != 0:
					size = 64

				if self.current_grab_window == None or self.epb == None:
					print('======================DEBUG1')
					self.current_grab_window = ImageGrab.grab(bbox=(self.anchor_x, self.anchor_y, self.bx, self.by))
					# grabbed_image.save('test_grab.png')
					self.epb =  lybresource.LYBExtractPixelBox(self.anchor_x, self.anchor_y, self.current_grab_window.load())

				pixel_box = self.epb.extract_pixel_box(x, y, None, size)
				if pixel_box != None:
					print('\nEnter pixel box name: ', end='')
					pixel_box_name = input()	
					pixel_box.pixel_box_name = pixel_box_name
					resource_pixel_box_list.append(pixel_box)
					current_resource.append(pixel_box_name)
					pass_count_for_name = len(pixel_box_name)
				is_ready = False
			elif w != 0:
				if current_resource != None and len(current_resource) > 0:
					if len(resource_pixel_box_list) > 0:
						for each_pixel_box in resource_pixel_box_list:
							self.resource_manager.pixel_box_dic[each_pixel_box.pixel_box_name] = each_pixel_box

					self.resource_manager.resource_dic[resource_name] = current_resource

					print('\n\n---------------------------------')
					print('resource name  : ', resource_name)
					if len(parent_resource_name) > 0 :
						print('parent name    : ', parent_resource_name)
					print('pixel box name : ')

					for each_pixel_box_name in current_resource:
						print('                 ', each_pixel_box_name)

					print('\nsuccessfully extracted')	
					print('---------------------------------')				
					self.current_grab_window = None
				else:
					print('Not found pixel box information')
				# is_working = False
				# is_done = True
			elif r != 0 and is_working == True:
				index = 0
				print('\n')
				for each_pixel_box_name in self.resource_manager.resource_dic[resource_name]:
					each_pixel_box = self.resource_manager.pixel_box_dic[each_pixel_box_name]
					print('\n', index, '-----------------------------')
					print(each_pixel_box_name, each_pixel_box[0][0][0], each_pixel_box[0][0][1])
					self.mouseMove(each_pixel_box_name, each_pixel_box[0][0][0] + self.anchor_x, each_pixel_box[0][0][1] + self.anchor_y)
					index+=1
				print('\n')
			elif q != 0:
				with open(self.resource_path(self.filename), 'wb') as resource_file:
					pickle.dump(self.resource_manager, resource_file)
				sys.exit()
			else:
				if is_working == True and is_ready == False:								
					print('\n\n---------------------------------')
					print('resource name  : ', resource_name)
					if len(parent_resource_name) > 0 :
						print('parent name    : ', parent_resource_name)
					if len(current_resource) > 0:
						print('pixel box name : ')

						for each_pixel_box_name in current_resource:
							print('                 ', each_pixel_box_name)
					print('\npick location')
					print('---------------------------------')
					is_ready = True


			time.sleep(0.5)


LYBMakeResource().execute()
