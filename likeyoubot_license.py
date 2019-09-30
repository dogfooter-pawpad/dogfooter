from cryptography.fernet import Fernet
import pickle
import os
import time
import likeyoubot_logger
import traceback
from datetime import datetime

def resource_path(relative):
	return os.path.join(
	os.environ.get(
	    "_MEIPASS2",
	    os.path.abspath(".")
	),
	relative
	)

class LYBLicense():
	def __init__(self):
		self.key = None
		self.logger = likeyoubot_logger.LYBLogger.getLogger()


	def generate_license(self, limit_time, lic_key_file='license_key.dat', lic_dat_file='license.dat'):
		license_info = 'lybheader:' + str(limit_time)
		self.key = Fernet.generate_key()

		f = Fernet(self.key)
		license_dat = f.encrypt(license_info.encode())

		try:
			with open(resource_path(lic_key_file), 'wb') as dat_file:
				pickle.dump(self.key, dat_file)
		except:
			self.logger.error(traceback.format_exc())
			return

		try:
			with open(resource_path(lic_dat_file), 'wb') as dat_file:
				pickle.dump(license_dat, dat_file)
		except:
			self.logger.error(traceback.format_exc())

	def read_license(self):
		if self.key == None:
			try:
				with open(resource_path('license_key.dat'), 'rb') as dat_file:
					self.key = pickle.load(dat_file)
			except:
				self.logger.error(traceback.format_exc())
				return

		try:
			with open(resource_path('license.dat'), 'rb') as dat_file:
				license_dat = pickle.load(dat_file)
		except:
			self.logger.error(traceback.format_exc())

		f = Fernet(self.key)
		license_info = f.decrypt(license_dat).decode()
		if 'lybheader' in license_info:
			license_due_date = float(license_info.replace('lybheader:', '', 1))
		else:
			license_due_date = 0

		remain_time = license_due_date - time.time()

		return remain_time

	def get_encrypt(self, data):
		if len(data) < 1:
			return ''

		is_there = os.path.exists(resource_path('account_key.dat'))
		if is_there == False:
			self.generate_license(0, lic_key_file='account_key.dat', lic_dat_file='account.dat')

		if self.key == None:
			try:
				with open(resource_path('account_key.dat'), 'rb') as dat_file:
					self.key = pickle.load(dat_file)
			except:
				self.logger.error(traceback.format_exc())
				return
		f = Fernet(self.key)

		try:
			to_data = f.encrypt(data.encode())
		except:
			to_data = ''

		return to_data

	def get_decrypt(self, data):
		if len(data) < 1:
			return ''

		is_there = os.path.exists(resource_path('account_key.dat'))
		if is_there == False:
			self.generate_license(0, lic_key_file='account_key.dat', lic_dat_file='account.dat')

		if self.key == None:
			try:
				with open(resource_path('account_key.dat'), 'rb') as dat_file:
					self.key = pickle.load(dat_file)
			except:
				self.logger.error(traceback.format_exc())
				return
		f = Fernet(self.key)

		try:
			to_data = f.decrypt(data).decode()
		except:
			to_data = ''
			
		return to_data

	def update_ads_info(self):
		ads_dat = self.get_encrypt(str(datetime.today().day))

		try:
			with open(resource_path('lybads.info'), 'wb') as dat_file:
				pickle.dump(ads_dat, dat_file)
		except:
			self.logger.error(traceback.format_exc())

	def is_done_ads_info(self):

		try:
			with open(resource_path('lybads.info'), 'rb') as dat_file:
				ads_dat = pickle.load(dat_file)
		except:
			return False

		today = int(self.get_decrypt(ads_dat))
		if today == datetime.today().day:
			return True

		return False
