import os
import time
import copy
import sys
import pickle
import likeyoubot_logger


class LYBConfigure():
    def __init__(self, x, y, w, h, keyword, path):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.keyword = keyword
        self.path = path
        self.common_config = {}
        self.window_config = {}
        self.game_config = {}
        self.window_title = 'DogFooter'
        self.version = '1.3.5'
        self.root_url = ''

    def merge(self):
        merge_file = 'lyb.cfg.merge'
        try:
            with open(LYBConfigure.resource_path(merge_file), 'rb') as dat_file:
                merge_configure = pickle.load(dat_file)

            if 'custom_config_dic' in merge_configure.window_config:
                for each_custom in merge_configure.window_config['custom_config_dic']:
                    if not 'custom_config_dic' in self.window_config:
                        self.window_config['custom_config_dic'] = {}

                    if not each_custom in self.window_config['custom_config_dic']:
                        self.window_config['custom_config_dic'][each_custom] = \
                            copy.deepcopy(merge_configure.window_config['custom_config_dic'][each_custom])
        except FileNotFoundError:
            likeyoubot_logger.LYBLogger.getLogger().info(merge_file + ' is not found')
        except:
            likeyoubot_logger.LYBLogger.getLogger().error('Merge Exception: ' + sys.exc_info()[0])

    def getGeometry(self):
        return (self.w, self.h, self.x, self.y)

    def getGeometryLogin(self):
        if not 'login_geometry' in self.common_config:
            return None
        else:
            return self.common_config['login_geometry']

    def setGeometry(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def setGeometryLogin(self, w, h, x, y):
        self.common_config['login_geometry'] = (w, h, x, y)

    def set_window_config(self, window_title, key, value):
        if not window_title in self.window_config:
            self.window_config[window_title] = copy.deepcopy(self.common_config)

        self.window_config[window_title][key] = value

    def get_window_config(self, window_title, key):
        if not window_title in self.window_config:
            self.window_config[window_title] = {}
        if not key in self.window_config[window_title]:
            self.window_config[window_title][key] = self.common_config[key]

        return self.window_config[window_title][key]

    @classmethod
    def resource_path(self, relative):
        return os.path.join(
            os.environ.get(
                "_MEIPASS2",
                os.path.abspath(".")
            ),
            relative
        )

    @classmethod
    def get_version(self, version_string):
        version_list = version_string.replace('v', '', 1).split()
        major_number = version_list[0].replace('.', '', 3)
        if len(version_list) > 1:
            fix_number = version_list[1].split('#')[1]
        else:
            fix_number = '0'

        return int(major_number) * 100 + int(fix_number)


class LYBConstant():
    LYB_USAGE = '. 홈페이지 주소는 www.dogfooter.com 입니다.                          \n' \
                '. DogFooter 프로그램은 무료입니다.                                   \n' \
                '. DogFooter 프로그램은 현재 녹스, 모모 앱플레이어를 지원합니다.      \n' \
                '. 제작자 여건 상 녹스만 피드백받습니다.                              \n' \
                '. 모모는 피드백 안받습니다. 문제 생기면 녹스로 하세요.               \n' \
                '. 앱플레이어 창 사이즈를 가로x세로(960 x 540)으로 설정해야 인식됩니다. \n' \
                '. DPI는 120으로 설정해야 합니다.                                     \n' \
                '. 앱플레이어 창 이름을 확인하시고 검색창에 입력하세요.               \n' \
                '. 창 이름 검색 단어로는 일부 단어만 입력해도 검색이 됩니다.          \n' \
                '. 앱플레이어 바탕화면에 게임 아이콘이 있어야 자동으로 시작됩니다.    \n' \
                '. 단, 스케쥴에 [게임 시작] 작업이 있어야 합니다.                     \n' \
                '. [게임 시작]은 게임 아이콘을 인식해서 작업합니다.                   \n' \
                '. [게임 시작]은 정상 동작하지 않는다면,                              \n' \
                '. 유사한 아이콘들을 치워주세요.                                      \n' \
                '. 게임별 설정을 각 게임 탭에서 할 수 있습니다.                       \n' \
                '. 스케쥴링 목록에 설정된 작업들을 순차적으로 실행합니다.             \n' \
                '. 게임 안의 다양한 상황에 대한 설정을 각각 할 수 있습니다.           \n' \
                '. 기존 설정을 [복사]해서 새로운 스케쥴을 만들어서 [저장]하세요.      \n' \
                '. 작업을 실행할 창, 게임을 선택 후 "시작" 버튼을 눌러주세요.         \n' \
                '. 매칭 확률을 높이면 이미지 인식이 잘 안됩니다.                      \n' \
                '. RGB 값을 낮추면 이미지 인식이 잘 안됩니다.                         \n' \
                '. 비활성 모드는 두 가지가 있습니다.                                  \n' \
                '. 윈도우 버전마다 동작이 다르니 정상 동작하는 걸로 설정하세요.       \n' \
                '. 만약 두 가지 모드 다 정상동작하지 않는다면,                        \n' \
                '. 비활성 모드를 사용할 수 없습니다.                                  \n' \
                '. DogFooter 프로그램은 100% Python 으로 작성되었습니다.              \n' \
                '. DogFooter 프로그램 소스는 모두에게 공개되어 있습니다.              \n' \
                '. 허접하지만 도움이 된다면 마음대로 사용하세요.                      \n' \
                '. 어차피 저도 오픈소스 도움으로 만든겁니다.                          \n' \
                '. 소스 위치 - https://bitbucket.org/dogfooter/dogfooter/src          \n'

    LYB_VERSION = 'v3.0.0'

    # LYB_SECURITY_CODE = '72830158'		# 1.3.5.fix4
    # LYB_SECURITY_CODE = '25218203'		# 1.3.6.fix1
    LYB_SECURITY_CODE = '82391347'  # 1.3.6.fix2

    LYB_LICENSE_LIMIT = time.mktime((2017, 12, 30, 0, 0, 0, 0, 0, 0))

    LYB_GAME_V4 = 'V4'
    LYB_GAME_DATA_V4 = 'v4'

    LYB_GAMES = {
        LYB_GAME_V4: LYB_GAME_DATA_V4,
    }

    LYB_MULTI_APP_PLAYER_NAME_MOMO = '[MOMO]멀티플레이어'
    LYB_MULTI_APP_PLAYER_NAME_NOX = '멀티 앱플레이어'
    LYB_MULTI_APP_PLAYER_NAME_MEMU = 'MEmuConsole'

    LYB_LABEL_SELECT_WINDOW_TEXT = '오른쪽 창을 선택해주세요'
    LYB_LABEL_SELECTED_ALL = '전체 창 선택됨'
    LYB_LABEL_AVAILABLE_WORK_LIST = '내 작업 목록'
    LYB_LABEL_SCHEDULE_WORK_LIST = '실행 스케쥴'
    LYB_LABEL_WORK_LIST = '전체 작업 목록'
    LYB_PADDING = 2
    LYB_WAKEUP_PERIOD = 100

    LYB_LABEL_WIDTH = 80
    LYB_LABEL_HEIGHT = 24

    LYB_BUTTON_WIDTH = 40
    LYB_BUTTON_HEIGHT = 24

    LYB_OPTION_WIDTH = 30
    LYB_BD_OPTION_WIDTH = 30

    LYB_FONT_FAMILY = '굴림체'
    LYB_FONT_SIZE = 9
    LYB_FONT = (LYB_FONT_FAMILY, LYB_FONT_SIZE)

    LYB_DO_PREFIX = 'do_'
    LYB_V4_PREFIX = 'v4_'

    LYB_STATISTIC_0 = '스케쥴 완료 횟수'
    LYB_STATISTIC_1 = '플레이 시간'

    LYB_TOOLTIP_WINDOW_LIST = '\n' \
                              '게임 실행 윈도우 목록\n\n' \
                              '검색 버튼을 누르면 앱플레이어가 검색됩니다.\n' \
                              '검색된 앱플레이어에 실행할 게임을 선택하면 이 목록에 나타납니다.\n' \
                              '선택한 게임과 같은 이름의 탭 목록 정보에서만 확인할 수 있습니다.\n'

    LYB_TOOLTIP_CUSTOM_CONFIG = '\n' \
                                '사용자 설정\n\n' \
                                '사용자가 지정한 설정 값들을 저장할 수 있습니다.\n\n' \
                                '1. 설정 이름을 수정한 후 [복사] 버튼을 눌러 새로운 설정을 만든다.\n' \
                                '2. 스케쥴을 수정하고 설정값도 이거저거 만져본다.\n' \
                                '3. 새로운 설정 수정이 끝났으면 [저장] 버튼을 누른다.\n' \
                                '4. 설정들 중 마음에 안드는 것이 있다면 설정 선택 후 [삭제] 버튼을 누른다.\n' \
                                '5. 설정 이름을 변경하고 싶다면 설정 선택 후 이름을 변경하고 [변경] 버튼을 누른다.\n\n' \
                                '모든 사용자 설정은 그 자체로 스케쥴 작업이 될 수 있습니다.\n' \
                                '이 기능이 도그푸터 매크로의 특징이자 장점입니다.\n'

    LYB_TOOLTIP_MY_WLIST = '\n' \
                           '내 작업 목록\n\n' \
                           '[고급 설정]에서 [내 작업 목록]을 편집할 수 있습니다.\n' \
                           '[전체 작업 목록]에서 자주 쓰는 작업을 상단으로 옮기거나 필요없는 작업들을 [내 작업 목록]에서 삭제하세요.\n' \
                           '언제든지 초기화(I) 버튼을 눌러 [전체 작업 목록]과 동일하게 되돌릴 수 있습니다.\n' \
                           '변경된 사항은 [시작] 또는 [저장] 버튼을 누르기 전까지는 반영되지 않습니다.\n'

    LYB_TOOLTIP_SCHEDULE_LOCK_BUTTON = '\n' \
                                       'U(nlocked)\n\n' \
                                       '실행 스케쥴 목록에서 작업을 클릭할 경우 목록에서 삭제됩니다.\n\n' \
                                       'L(ocked)\n\n' \
                                       '실행 스케쥴 목록에서 작업을 클릭할 경우 작업이 선택되며 편집 기능을 사용할 수 있습니다.\n'

    LYB_TOOLTIP_SCHEDULE = '\n' \
                           '실행 스케쥴\n\n' \
                           '매크로를 시작하면 "실행 스케쥴"에 등록된 작업이 순차적으로 실행됩니다.\n\n' \
                           '※ 중요 작업에 대한 설명\n\n' \
                           '[작업 예약]\n' \
                           '스케쥴을 순차적으로 진행하다가 정해진 시간에 [작업 예약]으로 건너뜁니다.\n' \
                           '정해진 시간이 되지 않아도 스케쥴 순서가 되면 실행됩니다.\n\n' \
                           '[반복 시작][반복 종료]\n' \
                           '스케쥴 순서가 [반복 시작] 작업 차례가 되면 일단 다음 작업들을 순차적으로 실행합니다.\n' \
                           '이후 [반복 종료] 작업을 만나거나 스케쥴 작업이 더 이상 없으면 다시 [반복 시작]으로 돌아가서 작업을 수행합니다.\n' \
                           '반복 작업은 설정한 횟수만큼 수행합니다.\n'

    LYB_TOOLTIP_COPY = '\n' \
                       'C(opy)\n\n' \
                       '실행 스케쥴에서 선택된 작업을 복사해서 추가합니다.\n' \
                       '이 버튼은 잠금(L) 상태에서만 동작합니다.\n'

    LYB_TOOLTIP_DELETE = '\n' \
                         'D(elete)\n\n' \
                         '실행 스케쥴에서 선택된 작업을 삭제합니다.\n' \
                         '이 버튼은 잠금(L) 상태에서만 동작합니다.\n'

    LYB_TOOLTIP_TERA_PARTY_MEMBER_MODE = '\n' \
                                         '파티원 모드\n\n' \
                                         '던전 작업 진행 시 "파티 매칭" 버튼을 누르지 않습니다.\n'

    LYB_TOOLTIP_MONSTER_DOGAM = '\n' \
                                '몬스터 도감\n\n' \
                                '게임 내 몬스터 도감 화면을 인식하고 몬스터 리스트 중 최상단 [추적] 또는 [받기] 버튼을 누릅니다.\n' \
                                '또한, [활성]버튼이 인식되면 누릅니다.\n\n' \
                                '[몬스터 도감]은 [지역 이동] 작업과 함께 스케쥴될 때 여러 지역으로 이동하면서 작업합니다.\n' \
                                '그렇지 않을 경우 현재 지역에서만 [몬스터 도감]작업을 합니다.\n\n' \
                                '지역을 이동하면서 [몬스터 도감]작업을 하고 싶을 경우에는 아래와 같이 스케쥴하시면 됩니다.\n\n' \
                                '[지역 이동] -> [몬스터 도감] -> [지역 이동] -> [몬스터 도감] -> ...\n'

    LYB_TOOLTIP_APP_TITLE = '\n' \
                            '앱 플레이어 창 이름\n\n' \
                            '녹스 또는 모모같은 프로그램을 앱플레이어라고 합니다.\n\n' \
                            '앱플레이어를 실행한 후 앱플레이어의 좌측 상단에 표시되는 이름을 검색란에 입력하면 됩니다.\n' \
                            '창 이름에 속하는 단어만 입력해도 됩니다.\n\n' \
                            '예를 들어 창 이름이 "녹스 플레이어 1"이라고 하면 "녹스"라고 단어의 일부만 검색란에 입력해도 검색이 됩니다.\n\n' \
                            '두 개 이상의 앱플레이어를 검색하고 싶을 때는 검색 단어 중간에 "|" 문자를 넣으면 됩니다.\n' \
                            '예를 들어 검색하려는 창 이름이 "녹스 플레이어 1", "모모 플레이어1" 이라고 하면, \n' \
                            '"녹스|모모" 라고 입력하면 됩니다.\n'

    LYB_TOOLTIP_TELEGRAM = '\n' \
                           '텔레그램 봇 연동\n\n' \
                           '도그푸터 텔레그램 봇이 발급한 고유 번호(chat id)를 보여줍니다.\n' \
                           '매크로 실행 중 특정 이벤트가 발생하면 텔레그램 메신저로 알림을 보내줍니다.\n\n' \
                           '텔레그램 연동 방법:\n\n' \
                           '0. 아래 입력칸에 아무거나 입력하세요. 이왕이면 본인만 알 수 있는 거로 입력하세요.\n' \
                           '1. 텔레그램에 가입하세요. -> https://www.telegram.org\n' \
                           '2. 텔레그램 대화 상대에서 "@DogFooterBot 를 검색하세요.\n' \
                           '3. 텔레그램 도그푸터 봇과 대화를 시작하세요.\n' \
                           '4. 도그푸터 봇 대화창에 0번에서 입력한 것을 대화창에 쓰세요.\n' \
                           '5. "연동하기" 버튼을 클릭하세요. \n' \
                           '6. 고유 변호가 표시되면 성공적으로 연동된 것입니다.\n'

    LYB_WAIT_ATTACK = '\n' \
                      '공격 스킬 사용 대기 시간\n\n' \
                      '메인퀘스트 클릭 후 이동 중에 스킬 버튼을 누르지 않도록 대기 시간을 설정한다.\n' \
                      '대기 시간이 지나면 스킬 버튼을 순차적으로 누른다. 단, 자동 사냥 중이라면 누르지 않는다.\n'

    LYB_TOOLTIP_COMBAT_BOX_RANGE = '\n' \
                                   '전투의 흔적 인식 범위\n\n' \
                                   '드랍된 전투의 흔적 아이콘을 인식합니다. 수행 시간이 차이 납니다.\n\n' \
                                   '좁게: 0.2초 반응 속도 \n' \
                                   '중간: 0.5초 반응 속도\n'

    LYB_TOOLTIP_GABANG_FULL = '\n' \
                              '가방 경고 클릭\n\n' \
                              '가방 차고 있다는 경고를 인식한 후 몇 초를 대기한 후 클릭할 지를 설정합니다.\n' \
                              '0 초로 설정하면 바로 클릭합니다.\n'

    LYB_TOOTLIP_POTION_SHOP = '\n' \
                              '뭉약 상점 인식 지연 시간\n\n' \
                              '뭉략 상점 아이콘이 인식되면 클릭해서 상점에 잡템을 팔고 물약을 구매합니다.\n' \
                              '물약 상점 아이콘을 인식할 때마다 상점을 열게 되면 다른 작업이 진행이 안되므로 \n' \
                              '다음 인식까지 지연 시간을 둡니다.\n'

    LYB_DO_BOOLEAN_BUY_HP_POTION = LYB_DO_PREFIX + 'hp_potion_buy_booleanvar'
    LYB_DO_STRING_NUMBER_HP_POTION = LYB_DO_PREFIX + 'hp_potion_number_stringvar'
    LYB_DO_BOOLEAN_BUY_MP_POTION = LYB_DO_PREFIX + 'mp_potion_buy_booleanvar'
    LYB_DO_STRING_NUMBER_MP_POTION = LYB_DO_PREFIX + 'mp_potion_number_stringvar'
    LYB_DO_STRING_DURATION_MAIN_QUEST = LYB_DO_PREFIX + 'main_quest_duration_stringvar'
    LYB_DO_STRING_DURATION_MAIN_QUEST_EACH = LYB_DO_PREFIX + 'main_quest_each_duration_stringvar'
    LYB_DO_STRING_DURATION_WEEKLY_QUEST = LYB_DO_PREFIX + 'weekly_quest_duration_stringvar'
    LYB_DO_STRING_DURATION_WEEKLY_QUEST_EACH = LYB_DO_PREFIX + 'weekly_quest_each_duration_stringvar'
    LYB_DO_STRING_DURATION_DUNGEON = LYB_DO_PREFIX + 'daily_dungeon_duration_stringvar'
    LYB_DO_STRING_CHECK_HP = LYB_DO_PREFIX + 'hp_check_stringvar'
    LYB_DO_STRING_MODE_COMBAT = LYB_DO_PREFIX + 'combat_mode_stringvar'
    LYB_DO_BOOLEAN_0_COMBAT_SKILL = LYB_DO_PREFIX + 'combat_skill_0_booleanvar'
    LYB_DO_BOOLEAN_1_COMBAT_SKILL = LYB_DO_PREFIX + 'combat_skill_1_booleanvar'
    LYB_DO_BOOLEAN_2_COMBAT_SKILL = LYB_DO_PREFIX + 'combat_skill_2_booleanvar'
    LYB_DO_BOOLEAN_3_COMBAT_SKILL = LYB_DO_PREFIX + 'combat_skill_3_booleanvar'
    LYB_DO_BOOLEAN_4_COMBAT_SKILL = LYB_DO_PREFIX + 'combat_skill_4_booleanvar'
    LYB_DO_BOOLEAN_BONUS_DAILY_WONBO = LYB_DO_PREFIX + 'bonus_daily_wonbo_booleanvar'
    LYB_DO_BOOLEAN_BONUS_DAILY_REWARD = LYB_DO_PREFIX + 'bonus_daily_reward_booleanvar'
    LYB_DO_BOOLEAN_BONUS_GOLD_TREE = LYB_DO_PREFIX + 'bonus_gold_tree_booleanvar'
    LYB_DO_BOOLEAN_BONUS_OFFEXP = LYB_DO_PREFIX + 'bonus_offexp_booleanvar'
    LYB_DO_BOOLEAN_BONUS_IMMEDIATE = LYB_DO_PREFIX + 'bonus_immediate_booleanvar'
    LYB_DO_STRING_DURATION_EVENT = LYB_DO_PREFIX + 'event_search_duration_stringvar'
    LYB_DO_BOOLEAN_CLAN_DONATE_ADENA = LYB_DO_PREFIX + 'clan_donate_adena_booleanvar'
    LYB_DO_STRING_CLAN_DONATE_ADENA = LYB_DO_PREFIX + 'clan_donate_adena_stringvar'
    LYB_DO_BOOLEAN_CLAN_DONATE_BLOOD = LYB_DO_PREFIX + 'clan_donate_blood_booleanvar'
    LYB_DO_STRING_CLAN_DONATE_BLOOD = LYB_DO_PREFIX + 'clan_donate_blood_stringvar'
    LYB_DO_BOOLEAN_CLAN_DONATE_RED = LYB_DO_PREFIX + 'clan_donate_red_booleanvar'
    LYB_DO_STRING_CLAN_DONATE_RED = LYB_DO_PREFIX + 'clan_donate_red_stringvar'
    LYB_DO_STRING_DAILY_REWARD = LYB_DO_PREFIX + 'daily_reward_stringvar'
    LYB_DO_BOOLEAN_STOP_WORKING = LYB_DO_PREFIX + 'stop_wokring_booleanvar'
    LYB_DO_STRING_DURATION_MONSTER_DOGAM = LYB_DO_PREFIX + 'monster_dogam_stringvar'
    LYB_DO_STRING_DURATION_DOGAM_CHECK = LYB_DO_PREFIX + 'monster_dogam_check_stringvar'
    LYB_DO_STRING_NORMAL_DUNGEON = LYB_DO_PREFIX + 'normal_dungeon_stringvar'
    LYB_DO_STRING_DURATION_NORMAL_DUNGEON = LYB_DO_PREFIX + 'normal_dungeon_duration_stringvar'
    LYB_DO_STRING_NORMAL_TOBUL = LYB_DO_PREFIX + 'normal_tobul_stringvar'
    LYB_DO_STRING_DURATION_NORMAL_TOBUL = LYB_DO_PREFIX + 'normal_tobul_duration_stringvar'
    LYB_DO_STRING_WAIT_MATCHING = LYB_DO_PREFIX + 'wait_matching_stringvar'
    LYB_DO_STRING_SKIP_LEVEL_ADJUST = LYB_DO_PREFIX + 'skip_level_adjust_stringvar'
    LYB_DO_STRING_MODE_DIFFICULTY = LYB_DO_PREFIX + 'difficulty_challenge_stringvar_'
    LYB_DO_STRING_DOGAM_AREA = LYB_DO_PREFIX + 'area_dogam_stringvar'
    LYB_DO_STRING_DOGAM_THRESHOLD = LYB_DO_PREFIX + 'dogam_threshold_stringvar'
    LYB_DO_STRING_SKIP_THRESHOLD = LYB_DO_PREFIX + 'skip_threshold_stringvar'
    LYB_DO_STRING_HERO_TALENT_LEVEL = LYB_DO_PREFIX + 'hero_talent_level_stringvar_'
    LYB_DO_BOOLEAN_HERO_SKILL = LYB_DO_PREFIX + 'hero_skill_booleanvar_'
    LYB_DO_BOOLEAN_RANDOM_SKILL = LYB_DO_PREFIX + 'random_skill_booleanvar'
    LYB_DO_STRING_RANDOM_SKILL_RATE = LYB_DO_PREFIX + 'random_skill_rate_booleanvar'
    LYB_DO_BOOLEAN_RANDOM_SKILL_1 = LYB_DO_PREFIX + 'random_skill_1_booleanvar'
    LYB_DO_STRING_RANDOM_SKILL_RATE_1 = LYB_DO_PREFIX + 'random_skill_rate_1_booleanvar'
    LYB_DO_BOOLEAN_RANDOM_SKILL_2 = LYB_DO_PREFIX + 'random_skill_2_booleanvar'
    LYB_DO_STRING_RANDOM_SKILL_RATE_2 = LYB_DO_PREFIX + 'random_skill_rate_2_booleanvar'
    LYB_DO_STRING_LIMIT_DUNGEON = LYB_DO_PREFIX + 'limit_dungeon_stringvar'
    LYB_DO_STRING_LIMIT_DUNGEON_ENTER = LYB_DO_PREFIX + 'limit_dungeon_enter_stringvar'
    LYB_DO_BOOLEAN_CHINMILDO_NPC_GIFT = LYB_DO_PREFIX + 'chinmildo_npc_gift_booleanvar_'
    LYB_DO_BOOLEAN_RESTART_GAME = LYB_DO_PREFIX + 'restart_game_booleanvar'
    LYB_DO_STRING_PERIOD_RESTART_GAME = LYB_DO_PREFIX + 'period_restart_game_stringvar'
    LYB_DO_STRING_CHINMILDO_ITEM_RANK = LYB_DO_PREFIX + 'chinmildo_item_rank_stringvar'
    LYB_DO_STRING_DURATION_DUNGEON_EACH = LYB_DO_PREFIX + 'duration_dungeon_each_stringvar'
    LYB_DO_STRING_LIMIT_COUNT_DUNGEON = LYB_DO_PREFIX + 'limit_count_dungeon_stringvar_'
    LYB_DO_STRING_LIMIT_COUNT_TOBUL = LYB_DO_PREFIX + 'limit_count_tobul_stringvar_'
    LYB_DO_BOOLEAN_DEBUG_CHINMILDO = LYB_DO_PREFIX + 'chinmildo_debug_booleanvar'
    LYB_DO_STRING_CHINMILDO_THRESHOLD = LYB_DO_PREFIX + 'chinmildo_threshold_stringvar'
    LYB_DO_STRING_DURATION_BATTLE = LYB_DO_PREFIX + 'duration_battle_stringvar'
    LYB_DO_STRING_DOGAM_STANCE = LYB_DO_PREFIX + 'stance_dogam_stringvar'
    LYB_DO_STRING_DOGAM_INTERVAL = LYB_DO_PREFIX + 'interval_dogam_stringvar'
    LYB_DO_STRING_TYPE_ENTER_DUNGEON = LYB_DO_PREFIX + 'type_enter_dungeon_stringvar_'
    LYB_DO_STRING_TYPE_ENTER_TOBUL = LYB_DO_PREFIX + 'type_enter_tobul_stringvar_'
    LYB_DO_BOOLEAN_MUHANTAP_SOTANG = LYB_DO_PREFIX + 'muhantap_sotang_booleanvar'
    LYB_DO_STRING_COUNT_CHINMILDO_DRAG = LYB_DO_PREFIX + 'chinmildo_drag_count_booleanvar'
    LYB_DO_STRING_TIARAN_GIVE = LYB_DO_PREFIX + 'tiaran_give_stringvar'
    LYB_DO_STRING_GUILD_DONATE = LYB_DO_PREFIX + 'donate_guild_stringvar'
    LYB_DO_STRING_PERIOD_REST = LYB_DO_PREFIX + 'period_rest_stringvar'
    LYB_DO_STRING_WAIT_TIME_SCENE_CHANGE = LYB_DO_PREFIX + 'wait_time_scene_change_stringvar'
    LYB_DO_STRING_AREA_THRESHOLD = LYB_DO_PREFIX + 'area_theshold_stringvar'
    LYB_DO_BOOLEAN_STOP_INVENTORY_FULL = LYB_DO_PREFIX + 'stop_inventory_full_booleanvar'
    LYB_DO_BOOLEAN_LEVELUP_ITEM_OPTION = LYB_DO_PREFIX + 'levelup_item_option_booleanvar_'
    LYB_DO_BOOLEAN_LEVELUP_ITEM_RANK = LYB_DO_PREFIX + 'levelup_item_rank_booleanvar_'
    LYB_DO_BOOLEAN_USE_INACTIVE_MODE = LYB_DO_PREFIX + 'use_inactive_mode_booleanavr'
    LYB_DO_BOOLEAN_USE_RESTART_APP_PLAYER = LYB_DO_PREFIX + 'user_restart_app_player_booleanvar'
    LYB_DO_BOOLEAN_FIX_WINDOW_LOCATION = LYB_DO_PREFIX + 'fix_window_location_stringvar_'
    LYB_DO_STRING_INACTIVE_MODE_FLAG = LYB_DO_PREFIX + 'inactive_mode_flag_stringvar'
    LYB_DO_STRING_WAITING_DUNGEON_START = LYB_DO_PREFIX + 'waiting_dungeon_start_stringvar'
    LYB_DO_STRING_EQUIP_SET = LYB_DO_PREFIX + 'equip_set_stringvar'
    LYB_DO_STRING_LEVELUP_EQUIP_SET = LYB_DO_PREFIX + 'levelup_equip_set_stringvar'
    LYB_DO_STRING_COUNT_LOOP = LYB_DO_PREFIX + 'count_loop_stringvar'
    LYB_DO_STRING_LOG_FILTER = LYB_DO_PREFIX + 'log_filter_stringvar'
    LYB_DO_BOOLEAN_LOCK_SCHEDULE = LYB_DO_PREFIX + 'lock_schedule_booleanvar'
    LYB_DO_BOOLEAN_LOCK_MY_WLIST = LYB_DO_PREFIX + 'lock_my_wlist_booleanvar'
    LYB_DO_STRING_PERIOD_BOT_DUNGEON = LYB_DO_PREFIX + 'period_bot_dungeon_stringvar'
    LYB_DO_BOOLEAN_RAID_MATCH_HERO = LYB_DO_PREFIX + 'raid_match_hero_booleanvar'
    LYB_DO_STRING_MATCH_HERO_THRESHOLD = LYB_DO_PREFIX + 'raid_match_hero_threshold_stringvar'
    LYB_DO_BOOLEAN_FULL_PARTY_CANCEL = LYB_DO_PREFIX + 'full_party_cancel_booleanvar'
    LYB_DO_STRING_THRESHOLD_BOSS_WARNING = LYB_DO_PREFIX + 'threshold_boss_warning_stringvar'
    LYB_DO_STRING_MATCH_HERO_OPERATION = LYB_DO_PREFIX + 'match_hero_operation_stringvar'
    LYB_DO_STRING_COUNT_DUNGEON_DEATH = LYB_DO_PREFIX + 'count_dungeon_death_stringvar'
    LYB_DO_STRING_DURATION_DUNGEON_DEATH = LYB_DO_PREFIX + 'duration_dungeon_death_stringvar'
    LYB_DO_BOOLEAN_USE_BOSS_WARNING_SKILL = LYB_DO_PREFIX + 'use_boss_warning_skill_booleanvar'
    LYB_DO_STRING_MAINSCENE_QUEST_THRESHOLD = LYB_DO_PREFIX + 'mainscene_quest_threshold_stringvar'
    LYB_DO_BOOLEAN_ELIMINATE_BUHYU = LYB_DO_PREFIX + 'eliminate_buhyu_booleanvar'
    LYB_DO_STRING_PERIOD_UPDATE_UI = LYB_DO_PREFIX + 'period_update_ui_stringvar'
    LYB_DO_BOOLEAN_USE_MONITORING = LYB_DO_PREFIX + 'use_monitoring_booleanvaar'
    LYB_DO_STRING_THRESHOLD_HERO_HP = LYB_DO_PREFIX + 'threshold_hero_hp_stringvar'
    LYB_DO_STRING_THRESHOLD_HERO_HP_2 = LYB_DO_PREFIX + 'threshold_hero_hp_2_stringvar'
    LYB_DO_STRING_THRESHOLD_HERO_HP_3 = LYB_DO_PREFIX + 'threshold_hero_hp_3_stringvar'
    LYB_DO_STRING_THRESHOLD_PARTY_HP = LYB_DO_PREFIX + 'threshold_party_hp_stringvar_'
    LYB_DO_STRING_THRESHOLD_PARTY_HP_2 = LYB_DO_PREFIX + 'threshold_party_hp_2_stringvar_'
    LYB_DO_BOOLEAN_USE_BOSS_WARNING_SKILL_EVADE = LYB_DO_PREFIX + 'use_boss_warning_skill_evade_booleanvar'
    LYB_DO_STRING_PERIOD_BOSS_SKILL = LYB_DO_PREFIX + 'period_boss_skill_stringvar'
    LYB_DO_STRING_PERIOD_BOSS_SKILL_1 = LYB_DO_PREFIX + 'period_boss_skill_1_stringvar'
    LYB_DO_STRING_PERIOD_BOSS_SKILL_2 = LYB_DO_PREFIX + 'period_boss_skill_2_stringvar'
    LYB_DO_STRING_GLOBAL_COOL_SKILL = LYB_DO_PREFIX + 'global_cool_skill_stringvar'
    LYB_DO_STRING_AFTER_BOSS_SKILL_2 = LYB_DO_PREFIX + 'after_boss_skill_stringvar'
    LYB_DO_STRING_DURATION_BOSS_QUEST = LYB_DO_PREFIX + 'duration_boss_quest_stringvar'
    LYB_DO_STRING_SUB_AREA = LYB_DO_PREFIX + 'sub_area_stringvar'
    LYB_DO_STRING_LIMIT_MOVE_AREA = LYB_DO_PREFIX + 'limit_move_area_stringvar'
    LYB_DO_STRING_DELAY_DUPLICATE_CONFIRM = LYB_DO_PREFIX + 'delay_duplicate_confirm_stringvar'
    LYB_DO_STRING_DURATION_MONSTER_CHASE = LYB_DO_PREFIX + 'duration_monster_chase_stringvar'
    LYB_DO_STRING_RESERVED_HOUR = LYB_DO_PREFIX + 'reserved_hour_stringvar'
    LYB_DO_STRING_RESERVED_MINUTE = LYB_DO_PREFIX + 'reserved_minute_stringvar'
    LYB_DO_STRING_RESERVED_SECOND = LYB_DO_PREFIX + 'reserved_second_stringvar'
    LYB_DO_STRING_PERIOD_TRACKING = LYB_DO_PREFIX + 'period_tracking_stringvar'
    LYB_DO_STRING_GUILD_EXP_POTION = LYB_DO_PREFIX + 'guild_exp_potion_stringvar'
    LYB_DO_STRING_RECOVERY_COUNT = LYB_DO_PREFIX + 'recovery_count_stringvar'
    LYB_DO_STRING_CLOSE_APP_COUNT = LYB_DO_PREFIX + 'close_app_count_stringvar'
    LYB_DO_STRING_SKIP_PERIOD = LYB_DO_PREFIX + 'skip_period_stringvar'
    LYB_DO_STRING_SKIP_THRESHOLD_2 = LYB_DO_PREFIX + 'skip_threshold_2_stringvar'
    LYB_DO_STRING_CHANNEL_FAVORITE = LYB_DO_PREFIX + 'channel_favorite_stringvar'
    LYB_DO_STRING_THRESHOLD_TARGET_HP = LYB_DO_PREFIX + 'threshold_target_hp_stringvar'
    LYB_DO_STRING_THRESHOLD_TARGET_HP_2 = LYB_DO_PREFIX + 'threshold_target_hp_2_stringvar'
    LYB_DO_STRING_THRESHOLD_TARGET_HP_3 = LYB_DO_PREFIX + 'threshold_target_hp_3_stringvar'
    LYB_DO_BOOLEAN_GUILD_SKILL_0 = LYB_DO_PREFIX + 'guild_skill_0_booleanvar'
    LYB_DO_BOOLEAN_GUILD_SKILL_1 = LYB_DO_PREFIX + 'guild_skill_1_booleanvar'
    LYB_DO_BOOLEAN_GUILD_SKILL_2 = LYB_DO_PREFIX + 'guild_skill_2_booleanvar'
    LYB_DO_BOOLEAN_GUILD_SKILL_3 = LYB_DO_PREFIX + 'guild_skill_3_booleanvar'
    LYB_DO_STRING_RETRY_CHANNEL = LYB_DO_PREFIX + 'retry_channel_stringvar'
    LYB_DO_STRING_DURATION_LAST_BOSS = LYB_DO_PREFIX + 'duration_last_boss_stringvar'
    LYB_DO_BOOLEAN_SHOP_EXP_BOOSTER_1 = LYB_DO_PREFIX + 'shop_exp_booster_1_stringvar'
    LYB_DO_BOOLEAN_SHOP_EXP_BOOSTER_2 = LYB_DO_PREFIX + 'shop_exp_booster_2_stringvar'
    LYB_DO_BOOLEAN_SHOP_EXP_BOOSTER_5 = LYB_DO_PREFIX + 'shop_exp_booster_5_stringvar'
    LYB_DO_BOOLEAN_SHOP_GOLD_BOOSTER_1 = LYB_DO_PREFIX + 'shop_gold_booster_1_stringvar'
    LYB_DO_BOOLEAN_SHOP_GOLD_BOOSTER_2 = LYB_DO_PREFIX + 'shop_gold_booster_2_stringvar'
    LYB_DO_BOOLEAN_SHOP_GOLD_BOOSTER_5 = LYB_DO_PREFIX + 'shop_gold_booster_5_stringvar'
    LYB_DO_STRING_EXP_DRAG_COUNT = LYB_DO_PREFIX + 'exp_drag_count_stringvar'
    LYB_DO_STRING_COOL_NORMAL_SKILL = LYB_DO_PREFIX + 'cool_normal_skill_stringvar_'
    LYB_DO_STRING_DEJANGGAN_LEVELUP_RANK = LYB_DO_PREFIX + 'dejangan_levelup_rank_stringvar'
    LYB_DO_STRING_SMITHY_LIMIT_DRAG = LYB_DO_PREFIX + 'smithy_limit_drag_stringvar'
    LYB_DO_BOOLEAN_SCREENSHOT_BOSS_KILL = LYB_DO_PREFIX + 'screenshot_boss_kill_booleanvar'
    LYB_DO_STRING_GAME_CONFIG_INVITE_PARTY = LYB_DO_PREFIX + 'game_config_invite_party_stringvar'
    LYB_DO_STRING_PARTY_LOC = LYB_DO_PREFIX + 'party_loc_stringvar'
    LYB_DO_BOOLEAN_PARTY_MEMBER_MODE = LYB_DO_PREFIX + 'party_member_mode_booleanvar'
    LYB_DO_BOOLEAN_SAVE_LOGIN_ACCOUNT = LYB_DO_PREFIX + 'save_login_account_booleanvar'
    LYB_DO_STRING_LOGIN_MESSAGE = LYB_DO_PREFIX + 'login_message_stringvar'
    LYB_DO_BOOLEAN_TELEGRAM_NOTIFY = LYB_DO_PREFIX + 'telegram_notify_booleanvar_'
    LYB_DO_STRING_TELEGRAM_ENTRY = LYB_DO_PREFIX + 'telegram_entry_booleanvar_'
    LYB_DO_BOOLEAN_AUTO_UPDATE = LYB_DO_PREFIX + 'auto_update_booleanvar'
    LYB_DO_BOOLEAN_TELEGRAM_IMAGE = LYB_DO_PREFIX + 'telegram_image_booleanvar_'
    LYB_DO_BOOLEAN_COMMON_TELEGRAM_NOTIFY = LYB_DO_PREFIX + 'common_telegram_notify_booleanvar_'
    LYB_DO_BOOLEAN_LOG_LEVEL = LYB_DO_PREFIX + 'log_level_booleanvar_'
    LYB_DO_STRING_NOTIFY_MESSAGE = LYB_DO_PREFIX + 'notify_message_stringvar'
    LYB_DO_STRING_PERIOD_TELEGRAM = LYB_DO_PREFIX + 'period_telegram_stringvar'
    LYB_DO_STRING_WAIT_FOR_NEXT = LYB_DO_PREFIX + 'wait_for_next_stringvar'
    LYB_DO_BOOLEAN_MOUSE_POINTER = LYB_DO_PREFIX + 'mouse_pointer_booleanvar'

    LYB_DO_BOOLEAN_RANDOM_CLICK = LYB_DO_PREFIX + 'random_click_booleanvar'
    LYB_DO_STRING_RANDOM_CLICK_DELAY = LYB_DO_PREFIX + 'random_delay'
    LYB_DO_STRING_THUMBNAIL_SIZE = LYB_DO_PREFIX + 'thumbnail_size_stringvar'
    LYB_DO_STRING_CLOSE_APP_NOX_NEW = LYB_DO_PREFIX + 'close_app_nox_new_boolenvar'
    LYB_DO_STRING_TERA_ETC = LYB_DO_PREFIX + 'tera_etc_stringvar_'

    LYB_DO_STRING_V4_WORK = LYB_DO_PREFIX + LYB_V4_PREFIX + 'work_'
    LYB_DO_STRING_V4_NOTIFY = LYB_DO_PREFIX + LYB_V4_PREFIX + 'notify_'
    LYB_DO_STRING_V4_ETC = LYB_DO_PREFIX + LYB_V4_PREFIX + 'etc_'

    def __init__(self):
        pass
