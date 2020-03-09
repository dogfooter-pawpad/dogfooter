import sys
import time

from simple_rest_client.api import API
import likeyoubot_logger
import traceback
import telegram
import json


class LYBRest:
    def __init__(self, root_url, email, password):
        self.account = email
        self.password = password
        self.access_token = ''
        self.login_point = -1
        self.point = -1
        self.chat_id = -1
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.token = ''
        self.last_id = -1
        self.rest = API(
            api_root_url=root_url,
            timeout=2000,
            json_encode_body=True,
        )
        self.rest.add_resource(resource_name='api')
        self.adjustTime = 0
        self.telegram_bot = None

    def login(self):
        payload = {
            'data': {
                'category': 'public',
                'service': 'Login',
                'account': self.account,
                'password': self.password,
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                self.access_token = data['access_token']
                return ''
            else:
                return json.loads(r)['err']
        except:
            return '로그인 에러'

    def get_public_elem(self, elem):
        payload = {
            'data': {
                'category': 'public',
                'service': 'GetElement',
                'element': elem,
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                return data['value']
            else:
                return json.loads(r)['err']
        except:
            return '에러'

    def update_chat_id(self, chat_id):
        payload = {
            'data': {
                'category': 'private',
                'service': 'UpdateChatId',
                'access_token': self.access_token,
                'chat_id': str(chat_id),
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                return ''
            else:
                return json.loads(r)['err']
        except:
            return '업데이트 에러'

    def get_login_point(self):
        if self.login_point >= 0:
            return self.login_point

        payload = {
            'data': {
                'category': 'private',
                'service': 'GetLoginPoint',
                'access_token': self.access_token
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                self.login_point = data['point']
                return self.login_point
            else:
                return json.loads(r)['err']
        except:
            self.logger.error(traceback.format_exc())

    def get_point(self):
        if self.point >= 0:
            return self.point

        payload = {
            'data': {
                'category': 'private',
                'service': 'GetPoint',
                'access_token': self.access_token
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                self.point = data['point']
                return self.point
            else:
                return json.loads(r)['err']
        except:
            self.logger.error(traceback.format_exc())

    def get_chat_id(self):
        if self.chat_id is not None and self.chat_id > 0:
            return self.chat_id

        payload = {
            'data': {
                'category': 'private',
                'service': 'GetChatId',
                'access_token': self.access_token
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                if 'chat_id' in data:
                    self.chat_id = int(data['chat_id'])
                    if self.chat_id > 0:
                        return self.chat_id
        except:
            return -1

        return -1

    def get_version(self):
        payload = {
            'data': {
                'category': 'private',
                'service': 'GetVersion',
                'access_token': self.access_token
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                return data['version']
            else:
                return json.loads(r)['err']
        except:
            self.logger.error(traceback.format_exc())

    def get_update_file(self):
        payload = {
            'data': {
                'category': 'private',
                'service': 'GetUpdateFileList',
                'access_token': self.access_token
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                return data['update_file_list']
            else:
                return json.loads(r)['err']
        except:
            self.logger.error(traceback.format_exc())

    def get_elem(self, elem):
        payload = {
            'data': {
                'category': 'private',
                'service': 'GetElement',
                'access_token': self.access_token,
                'element': elem,
            }
        }
        try:
            res = self.rest.api.create(body=payload)
            r = res.body
            if 'data' in r:
                data = r['data']
                return data['value']
            else:
                return json.loads(r)['err']
        except:
            self.logger.error(traceback.format_exc())

    def get_token(self):
        if len(self.token) == 0:
            self.token = self.get_elem('token')

        return self.token

    def getConnectCount(self):
        return ""

    def connect_telegram(self, match_string):
        try:
            last_log = self.getTelegramUpdates(-1, match_string=match_string)
            if last_log is not None:
                return str(last_log.message.chat.id)
        except:
            self.logger.error(traceback.format_exc())
            return ''

        return ''

    def long_pooling_telegram(self, chat_id):
        try:
            m_token = self.get_token()

            bot = telegram.Bot(token=m_token)
            # last_log = bot.getUpdates(-1)
            # self.logger.debug(last_log)
            # update_id = 284752270
            # last_log = bot.getUpdates(offset=update_id)
            last_log = bot.getUpdates()
            for each_log in last_log:
                self.logger.debug(each_log)

        except:
            self.logger.error(traceback.format_exc())
            return ''

        return ''

    def send_telegram_message(self, chat_id, message):
        if int(chat_id) <= 0:
            return

        try:
            m_token = self.get_token()

            bot = telegram.Bot(token=m_token)
            bot.sendMessage(chat_id=chat_id, text=message)
        except telegram.error.TimedOut:
            pass
        except telegram.error.NetworkError:
            pass
        except:
            self.logger.error(traceback.format_exc())
            return ''

    def send_telegram_image(self, chat_id, image_url):
        if chat_id <= 0:
            return
        try:
            m_token = self.get_token()
            bot = telegram.Bot(token=m_token)
            bot.sendPhoto(chat_id=chat_id, photo=open(image_url, 'rb'), timeout=60)
        except telegram.error.TimedOut:
            pass
        except telegram.error.NetworkError:
            pass
        except:
            self.logger.error(traceback.format_exc())

    def getTelegramUpdates(self, chat_id, match_string=None):
        update = None
        update_id = 0
        try:
            m_token = self.get_token()
            # self.logger.debug(m_token)
            if self.telegram_bot is None:
                self.telegram_bot = telegram.Bot(token=m_token)
            bot = self.telegram_bot
            lUpdateLog = bot.getUpdates(limit=99, timeout=99)
            self.logger.debug(lUpdateLog)
            self.logger.debug('-----------------' + str(len(lUpdateLog)))
            for eachLog in lUpdateLog:
                self.logger.debug(eachLog)
                # 메세지가 입력된 시간이 10초가 경과한 것들은 다 제거한다.
                issue_time = int(time.mktime(eachLog.message.date.timetuple()))
                self.logger.debug(str(int(time.time()) - issue_time - self.adjustTime))
                if int(time.time()) - issue_time - self.adjustTime > 10:
                    if update_id < eachLog.update_id:
                        update_id = int(eachLog.update_id)
                else:
                    if chat_id <= 0:
                        self.logger.debug('텔레그램 연동')
                        if str(eachLog.message.text) == match_string:
                            if self.last_id != eachLog.update_id:
                                self.last_id = eachLog.update_id
                                update = eachLog
                                break
                    else:
                        if str(eachLog.message.chat.id) == str(chat_id):
                            if self.last_id != eachLog.update_id:
                                self.last_id = eachLog.update_id
                                update = eachLog
                                break

            if update_id != 0:
                bot.getUpdates(offset=update_id + 1)
        except telegram.error.TimedOut:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            pass
        except telegram.error.NetworkError:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            pass
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            # self.logger.error(traceback.format_exc())
            # self.logger.debug(traceback.format_exc())
            # self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')

            return update

        return update

