import http.cookiejar
import urllib
import ssl
import logging
import json
from bs4 import BeautifulSoup
import time
import datetime
import sys
import telegram
import requests
import likeyoubot_logger
import traceback
import requests


class LYBHttp:
    def __init__(self, user_id, password):
        self.mb_id = user_id
        self.mb_password = password
        self.logger = likeyoubot_logger.LYBLogger.getLogger()
        self.cj = http.cookiejar.CookieJar()
        self.https_sslv23_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv23))
        self.opener = urllib.request.build_opener(self.https_sslv23_handler,
                                                  urllib.request.HTTPCookieProcessor(self.cj))
        self.mb_point = 0
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept-Language', 'ko-KR')]
        self.json_obj = None
        self.dogphp = '/dogfooter_2.3.1.php'
        self.checkip = '/checkip.php'
        self.connectCount = '/getConnect.php'
        self.gameOnPlaying = '/checkgame.php'
        self.adjustTime = 0
        self.last_id = 0

        urllib.request.install_opener(self.opener)
        self.url = LYBHttp.getMacroBaseUrl()

        self.login_info = {
            'mb_id': '',
            'mb_password': '',
            'mb_1': '',
            'mb_2': '',
            'mb_3': '',
            'mb_6': '',
        }

    @classmethod
    def getMacroBaseUrl(self):

        try:
            req = urllib.request.Request('http://numaking.cafe24.com/superman.html')
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
        except:
            return ''

        macro_url = soup.find(id='url').text.strip()

        return macro_url

    def login(self, mb_3=None, mb_6=None):
        now = datetime.datetime.now()
        now_time = now.strftime('%y%m%d %H%M%S')

        self.login_info['mb_id'] = self.mb_id
        self.login_info['mb_password'] = self.mb_password
        self.login_info['mb_1'] = now_time
        if mb_3 is not None:
            self.login_info['mb_3'] = mb_3
        if mb_6 is not None:
            self.login_info['mb_6'] = mb_6

        try:
            login_request = urllib.parse.urlencode(self.login_info)

            req = urllib.request.Request(self.url + '/bbs/login_check.php', login_request.encode('UTF-8'))
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            # self.logger.debug(string)
            soup = BeautifulSoup(string, 'html.parser')
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return False

        error_dom = soup.find(id='validation_check')
        if error_dom == None:
            point = soup.find(id='ol_after_pt').text.strip()
            self.mb_point = point.split(' ')[-1].replace(',', '', 5)
            server_time = soup.find(id='server_time').text.strip()
            self.adjustTime = int(time.time()) - int(server_time)
            # self.logger.debug('adjustTime:'+str(self.adjustTime))
            return ''
        else:
            self.logger.debug(soup.findAll("p", {"class": "cbg"})[0].text.strip())
            return soup.findAll("p", {"class": "cbg"})[0].text.strip()

    def get_notice(self):

        now = datetime.datetime.now()
        now_time = now.strftime('%y%m%d %H%M%S')

        self.login_info['mb_id'] = self.mb_id
        self.login_info['mb_password'] = self.mb_password
        self.login_info['mb_1'] = now_time

        try:
            login_request = urllib.parse.urlencode(self.login_info)

            req = urllib.request.Request(self.url + '/bbs/board.php?bo_table=notice', login_request.encode('UTF-8'))
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            # self.logger.debug(string)
            soup = BeautifulSoup(string, 'html.parser')
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return {}

        r_dic = {}
        for each_notice in soup.find_all('td', {'class': 'td_subject'}):
            a = each_notice.find('a')

            key = a.text.strip()
            value = str(a['href'])
            r_dic[a.text.strip()] = str(a['href'])

        return r_dic

    def get_notice_content(self, custom_url):

        now = datetime.datetime.now()
        now_time = now.strftime('%y%m%d %H%M%S')

        self.login_info['mb_id'] = self.mb_id
        self.login_info['mb_password'] = self.mb_password
        self.login_info['mb_1'] = now_time

        try:
            login_request = urllib.parse.urlencode(self.login_info)

            req = urllib.request.Request(custom_url, login_request.encode('UTF-8'))
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            # self.logger.debug(string)
            soup = BeautifulSoup(string, 'html.parser')
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return 'empty'

        r_line = []
        for each_line in soup.find(id='bo_v_con').find_all('p'):
            r_line.append(each_line.text.strip())

        if len(r_line) == 0:
            for each_line in soup.find(id='bo_v_con').find_all('li'):
                r_line.append(each_line.text.strip())

        return r_line

    def getConnectCount(self):

        login_info = {}
        login_info['mb_id'] = self.mb_id
        login_info['mb_password'] = self.mb_password

        try:
            login_request = urllib.parse.urlencode(login_info)

            req = urllib.request.Request(self.url + self.connectCount, login_request.encode('UTF-8'))
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            # self.logger.debug(string)
            soup = BeautifulSoup(string, 'html.parser')
        except:
            return ""

        if soup.find(id='connect') == None:
            return ""

        connect_count = soup.find(id='connect').text.strip()

        return " - 현재 접속자: %d명" % int(connect_count)

    def getGameCountOnPlaying(self, game_name):

        login_info = {}
        login_info['mb_6'] = game_name

        try:
            login_request = urllib.parse.urlencode(login_info)

            req = urllib.request.Request(self.url + self.gameOnPlaying, login_request.encode('UTF-8'))
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            # self.logger.debug(string)
            soup = BeautifulSoup(string, 'html.parser')
        except:
            return 0

        if soup.find(id='game_on_playing') == None:
            return 0

        connect_count = soup.find(id='game_on_playing').text.strip()

        return int(connect_count)

    def is_ip_free(self):

        check_ip_info = {}
        check_ip_info['mb_id'] = self.mb_id
        check_ip_info['mb_password'] = self.mb_password

        try:
            login_request = urllib.parse.urlencode(check_ip_info)

            req = urllib.request.Request(self.url + self.checkip, login_request.encode('UTF-8'))
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            # self.logger.debug(string)
            soup = BeautifulSoup(string, 'html.parser')
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return True

        if soup.find(id='mb_5') == None or soup.find(id='remote_addr') == None:
            return True

        mb_login_ip = soup.find(id='mb_5').text.strip()
        remote_addr = soup.find(id='remote_addr').text.strip()

        if mb_login_ip == remote_addr:
            # self.logger.warn(str(mb_login_ip) + ':' + str(remote_addr))
            return True

        self.logger.error('로그온되어 있는 아이피 주소: ' + str(mb_login_ip))
        self.logger.error('현재 내 아이피 주소: ' + str(remote_addr))

        self.login()

        return False

    def get_ip(self):
        if self.json_obj != None:
            return self.json_obj[self.mb_id]['ip']

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            self.json_obj = json.loads(soup.prettify())
            self.logger.debug(str(self.json_obj[self.mb_id]['macro']))
            self.logger.debug(str(self.json_obj[self.mb_id]['ip']))
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return None

        return self.json_obj[self.mb_id]['ip']

    def get_elem(self, elem):
        if self.json_obj != None:
            if elem in self.json_obj:
                return self.json_obj[elem].replace(',', '', 5)
            else:
                return None

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            self.json_obj = json.loads(soup.prettify())
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return None

        if elem in self.json_obj:
            return self.json_obj[elem].replace(',', '', 5)
        else:
            return None

    def get_login_point(self):
        if self.json_obj != None:
            return self.json_obj['login_point'].replace(',', '', 5)

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            self.json_obj = json.loads(soup.prettify())
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return None

        return self.json_obj['login_point'].replace(',', '', 5)

    def get_chat_id(self, refresh=False):
        if self.json_obj != None:
            if refresh == False:
                return self.json_obj[self.mb_id]['chat_id']

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            self.json_obj = json.loads(soup.prettify())
        except:
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
            return None

        return self.json_obj[self.mb_id]['chat_id']

    def get_version(self):
        if self.json_obj != None:
            return self.json_obj['version']

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            self.json_obj = json.loads(soup.prettify())
        # print(soup.prettify())
        # print(json_obj)
        # print(json_obj['token'])
        except:
            self.logger.error(traceback.format_exc())
            return None

        return self.json_obj['version']

    def get_update_file(self):
        if self.json_obj != None:
            return self.json_obj['update_file']

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            self.json_obj = json.loads(soup.prettify())
        # print(soup.prettify())
        # print(json_obj)
        # print(json_obj['token'])
        except:
            self.logger.error(traceback.format_exc())
            return None

        return self.json_obj['update_file']

    def get_token(self):
        if self.json_obj != None:
            return self.json_obj['token']

        error_message = self.login()
        if error_message != '':
            self.logger.error('Login fail: ' + error_message)
            return None

        try:
            req = urllib.request.Request(self.url + self.dogphp, None)
            res = urllib.request.urlopen(req)

            string = res.read().decode('utf-8')
            soup = BeautifulSoup(string, 'html.parser')
            json_obj = json.loads(soup.prettify())
        # print(soup.prettify())
        # print(json_obj)
        # print(json_obj['token'])
        except:
            self.logger.error(traceback.format_exc())
            return None

        return json_obj['token']

    def connect_telegram(self, match_string):
        try:
            last_log = self.getTelegramUpdates(-1, match_string=match_string)
            if last_log != None:
                return str(last_log.message.chat_id)
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
        if chat_id == None or len(chat_id) < 1:
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
        if chat_id == None or len(chat_id) < 1:
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

            bot = telegram.Bot(token=m_token)
            lUpdateLog = bot.getUpdates(limit=99)
            # self.logger.debug(lUpdateLog)
            # self.logger.debug('-----------------' + str(len(lUpdateLog)))
            for eachLog in lUpdateLog:
                # self.logger.debug(eachLog)
                # 메세지가 입력된 시간이 10초가 경과한 것들은 다 제거한다.
                issue_time = int(time.mktime(eachLog.message.date.timetuple()))
                # self.logger.debug(str(int(time.time()) - issue_time - self.adjustTime))
                if int(time.time()) - issue_time - self.adjustTime > 10:
                    if update_id < eachLog.update_id:
                        update_id = int(eachLog.update_id)
                else:
                    if chat_id == -1:
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
            pass
        except telegram.error.NetworkError:
            pass
        except:
            # self.logger.error(traceback.format_exc())
            # self.logger.debug(traceback.format_exc())
            self.logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')

            return update

        return update
