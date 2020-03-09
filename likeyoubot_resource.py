import operator
import pyautogui

class LYBExtractPixelBox():
	def __init__(self, anchor_x, anchor_y, grabbed_image):
		self.anchor_x = anchor_x
		self.anchor_y = anchor_y
		self.grabbed_image = grabbed_image

	def extract_pixel_box(self, x, y, resource_name, size):
		start = int((size - 1) / 2 * -1)
		end = int((size - 1) / 2)

		rc_list = LYBPixelBox(resource_name)
		rc_list.height = size - 2
		rc_list.width = size - 2

		for width in range(start, end):
			for height in range(start, end):
				adj_x = x + width
				adj_y = y + height

				if adj_x < 0 or adj_y < 0:
					print('Out of range:', adj_x, adj_y)
					return None

				# ((loc_x, loc_y), (r,g,b)) = ((adj_x-self.anchor_x, adj_y-self.anchor_y), pyautogui.pixel(adj_x, adj_y))
				
				(loc_x, loc_y) = (adj_x-self.anchor_x, adj_y-self.anchor_y)
				(r,g,b) = self.grabbed_image[loc_x, loc_y]

				rc_list.append(((loc_x, loc_y), (r,g,b)))

		rc_list.debug()
		return rc_list

class LYBPixelBoxDic(dict):
	def __init__(self):
		dict.__init__({})

	def sortedList(self):
		return sorted(self.values(), key=operator.attrgetter('pixel_box_name'), reverse=True)

	def debug(self):
		for pixel_box in self.sortedList():
			pixel_box.debug()

class LYBPixelBox(list):
	def __init__(self, pixel_box_name):
		list.__init__([])
		self.pixel_box_name = pixel_box_name

	def debug(self):
		print(self.pixel_box_name)
		for i in range(len(self)):
			print(self[i])

class LYBResourceDic(dict):
	def __init__(self):
		dict.__init__({})

	def sortedResourceListByCount(self):
		return sorted(self.values(), key=operator.attrgetter('pixel_box_count'), reverse=True)

	def sortedResourceListByName(self):
		return sorted(self.values(), key=operator.attrgetter('resource_name'), reverse=False)

	def debug(self):
		for resource in self.sortedResourceListByCount():
			resource.debug()


class LYBResource(list):
	def __init__(self, resource_name, resource_type):
		list.__init__([])
		self.resource_name = resource_name
		self.resource_type = resource_type
		self.pixel_box_count = 0

	def append(self, item):
		super(LYBResource, self).append(item)
		self.pixel_box_count = len(self)

	def debug(self):
		print(self.resource_name)
		for i in range(len(self)):
			print(self[i])

class LYBResourceManager():
	def __init__(self, pbdic, rdic):
		self.pixel_box_dic = pbdic
		self.resource_dic = rdic

	def debug(self):
		self.pixel_box_dic.debug()
		self.resource_dic.debug()