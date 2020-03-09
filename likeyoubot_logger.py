import os
import sys
import datetime
import logging
import likeyoubot_configure
import traceback

class LYBLogger:

	dogfooter_logger = None
	logPath = ''

	@classmethod
	def getLogger(self, refresh=False):

		if LYBLogger.dogfooter_logger != None and refresh is False:
			return LYBLogger.dogfooter_logger

		formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname).1s %(threadName)s: %(message)s FileInfo: %(module)s:%(lineno)d', '%H:%M:%S')
		LYBLogger.dogfooter_logger = logging.getLogger('DogFooter')

		postfix = 'dogfooter'
		log_path = ''
		try:
			now = datetime.datetime.now()
			today = now.strftime('%Y%m%d')
			now_time = now.strftime('%Y%m%d_%H%M%S')
			log_path = likeyoubot_configure.LYBConfigure.resource_path('log/' + today)
			if not os.path.exists(log_path):
				os.makedirs(log_path)
			log_path += '/'+postfix+'_'+str(now_time)+'.log'
		except:
			print(str(sys.exc_info()[0]) + '(' +str(sys.exc_info()[1]) + ')')
			raise ValueError

		clog_fh = logging.FileHandler(log_path)
		clog_fh.setFormatter(formatter)

		# clog_ch = logging.StreamHandler()
		# clog_ch.setFormatter(formatter)

		log_fd = open(log_path, "a")
		# sys.stdout = log_fd
		# sys.stderr = log_fd

		LYBLogger.dogfooter_logger.addHandler(clog_fh)
		# LYBLogger.dogfooter_logger.addHandler(clog_ch)

		LYBLogger.dogfooter_logger.setLevel(logging.DEBUG)
		LYBLogger.logPath = log_path

		return LYBLogger.dogfooter_logger

	@classmethod
	def setLevel(self, log_level):
		if log_level == 'D':
			LYBLogger.dogfooter_logger.setLevel(logging.DEBUG)
		elif log_level == 'I':
			LYBLogger.dogfooter_logger.setLevel(logging.INFO)
		elif log_level == 'E':
			LYBLogger.dogfooter_logger.setLevel(logging.ERROR)
		elif log_level == 'C':
			LYBLogger.dogfooter_logger.setLevel(logging.CRITICAL)
		elif log_level == 'W':
			LYBLogger.dogfooter_logger.setLevel(logging.WARN)
		else:
			LYBLogger.dogfooter_logger.setLevel(logging.INFO)			


	@classmethod
	def removeLog(self):
		day = str(datetime.datetime.today()).split()[0].replace('-','',3)

		try:
			log_path = likeyoubot_configure.LYBConfigure.resource_path('log')
			for root, dirs, files in os.walk(log_path):  
				for filename in files:
					if not day in filename:
						try:
							os.remove(os.path.join(root, filename))
						except:
							pass

			for root, dirs, files in os.walk(log_path):  
				for d in dirs:
					if not day in d:
						try:
							os.rmdir(os.path.join(root, d))
						except:
							continue
		except:
			print(str(sys.exc_info()[0]) + '(' +str(sys.exc_info()[1]) + ')')
			raise ValueError
		
		now = datetime.datetime.now()
		now_time = now.strftime('%y%m%d')

		try:
			screenshot_path = likeyoubot_configure.LYBConfigure.resource_path('screenshot')
			for root, dirs, files in os.walk(screenshot_path):  
				for filename in files:
					if not now_time in filename:
						try:
							os.remove(os.path.join(root, filename))
						except:
							pass
		except:
			print(str(sys.exc_info()[0]) + '(' +str(sys.exc_info()[1]) + ')')
			raise ValueError

