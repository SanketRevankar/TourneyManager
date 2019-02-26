""" --------------------------------------------------------------------------------------------------------------------
    Strings Used to print information
-------------------------------------------------------------------------------------------------------------------- """

""" --------------------------------------------------------------------------------------------------------------------
    Saving characters to print
-------------------------------------------------------------------------------------------------------------------- """
SPACE = " "
UNDERSCORE = "_"
DOT = "."
SEPARATOR = "/"
N = "n"
Y = "Y"
SINGLE_QUOTE = "'"
CLOSE_SQ_BRACE = "]"
OPEN_SQ_BRACE = "["
CLOSE_CIRCULAR_BRACE_ = ")"
COMMA = ","
COLON = ":"
DASH = "-"
PLUS = "+"
STAR = "*"
SEMI_COLON = ";"
HASH = "#"
EMPTY_STRING = ""
PIPE = "|"
EQUALS = "="
GREATER_THAN = ">"
DOUBLE_QUOTE = '"'
UNIX_SEPARATOR = "\\"
NEW_LINE = "\n"
TAB = "    "
TAB_ = "\t"
QUESTION_MARK = "?"
CLOSE_CURL_BRACE = r"}"
OPEN_CURL_BRACE = r"{"
BYE = 'Bye'

""" --------------------------------------------------------------------------------------------------------------------
    Stats
-------------------------------------------------------------------------------------------------------------------- """
KILLS = "kills"
DEATHS = "deaths"
GRENADE = "grenade"
HEADSHOT = "headshot"
SUICIDE = "suicide"
BOMB_PLANT = "bomb_plant"
BOMB_DEFUSE = "bomb_defuse"
KNIFE = "knife"
MATCHES = "matches"
NAME_SMALL = "name"
NICK_SMALL = "nick"
ONE = "1"
TWO = "2"
THREE = "3"
FOUR = "4"
FIVE = "5"
SIX = "6"
SEVEN = "7"
EIGHT = '8'
NINE = '9'
TEN = '10'
D_M = "D:M"
B_C = "B:C"
S_STEAM_ID = "steam_id"
M = "M"
L = "L"
K = "K"
J = "J"
I_ = "I"
H = "H"
G = "G"
F = "F"
E = "E"
D = "D"
C = "C"
B = "B"
ORIENT = 'index'

""" --------------------------------------------------------------------------------------------------------------------
    File Formats
-------------------------------------------------------------------------------------------------------------------- """
TXT = ".txt"
LOG = ".log"
DEMO_FORMAT = ".dem"
TEXT = "txt"
JPG = ".jpg"

""" --------------------------------------------------------------------------------------------------------------------
    Status for servers
-------------------------------------------------------------------------------------------------------------------- """
RUNNING = "running"
VERSUS = "vs"
DISCARDED = "Discarded"
ACTIVE = "Active"
STATUS = "status"
MATCH = "match"
IP = "ip"
CSTRIKE = "cstrike"
MODIFY = "modify"
DIR = "dir"
TYPE = "type"
STOPPED = "stopped"
HLTV = "HLTV"
START_TIME = "start_time"
END_TIME = "end_time"

""" --------------------------------------------------------------------------------------------------------------------
    Team constants
-------------------------------------------------------------------------------------------------------------------- """
TEAM_NAME_ = "Team Name"
TEAM_NAME = "team_name"
TEAM_TAG_ = "Team Tag"
TEAM_TAG = "team_tag"
TEAM_NAME_OG = "Team Name Og"
TEAM_2_ID = "team2_id"
TEAM_1_ID = "team1_id"
TEAM_TAG_2_ = "team_tag2"
TEAM_TAG_1_ = "team_tag1"
TEAM_2_ = "team2"
TEAM_1_ = "team1"
CAPTAINS_NAME = "Captains Name"
TEAMS = "teams"
CAPTAIN_NAME_2 = 'Captain 2 Name'
CAPTAIN_2 = 'Captain 2'
CAPTAIN_NAME_1 = 'Captain 1 Name'
CAPTAIN_1 = 'Captain 1'

""" --------------------------------------------------------------------------------------------------------------------
    Player constants
-------------------------------------------------------------------------------------------------------------------- """
EMAIL = "Email"
NO_PLAYER = "EMPTY_NO_PLAYER"
STEAM_ID = "Steam ID"
NICK_ = "Nick"
NAME_ = "Name"
NAME = "name"
STEAM_NICK = "steam_nick"
JOIN_TEAM = "join_team"
REG_TIME = "reg_time"
FB_LINK = "fb_link"

""" --------------------------------------------------------------------------------------------------------------------
    Queries
-------------------------------------------------------------------------------------------------------------------- """
DELETE_FROM_MATCHES_WHERE_ID_ = "DELETE FROM `matches` WHERE `id` = {}"
INSERT_MATCHES_VALUES_ = "INSERT INTO `matches` VALUES ({}, '{}', '{}', '{}', '{}', '{}', {}, {}, '{}')"
UPDATE_DONE_WHERE_MATCHES_ID_ = "UPDATE `matches` SET `ip` = '{}_done' WHERE `matches`.`id` = {}"
INSERT_VALUE_ = "'{}', "
INSERT_INTO_TEAMS_VALUES_ = "INSERT INTO `teams` VALUES('{}', "
SELECT_MATCHES_WHERE_IP_ = "SELECT * FROM `matches` WHERE `ip` = '{}'"
TRUNCATE_TABLE_ = "truncate table {}"
TABLE_TEAMS_PL2 = """
            player_{} varchar(35)
        );"""
TABLE_TEAMS_PL1 = """
            player_{} varchar(35),"""
TABLE_TEAMS = """
        create table if not exists {} (
            id int not null primary key,"""
TABLE_MATCHES = """
        create table if not exists `{}` (
            id int not null primary key,
            team1 varchar(35),
            team2 varchar(35),
            team_tag1 varchar(35),
            team_tag2 varchar(35),
            ip varchar(35),
            team1_id int,
            team2_id int,
            time timestamp
        );
        """
CREATE_DATABASE = "create database if not exists {}"

""" --------------------------------------------------------------------------------------------------------------------
    Server constants
-------------------------------------------------------------------------------------------------------------------- """
SERVER_NAME = "Server Name"
SERVER_IP = "Server IP"
HLTV_SERVER_NAME = "HLTV Server Name"
PORT = "Port"
HLTV_IP = "HLTV IP"
HLTV_PASSWORD = "HLTV_Password"
PASSWORD = "Password"
USERNAME = "Username"
HLTV_USERNAME = "HLTV_Username"
INSTANCE_NAME = "Instance Name"
HLTV_NAME = "HLTV Name"
MATCH_SERVER = "Match Server"

""" --------------------------------------------------------------------------------------------------------------------
    Team Names
-------------------------------------------------------------------------------------------------------------------- """
TERRORIST = "T"
COUNTER_TERRORIST = "CT"

""" --------------------------------------------------------------------------------------------------------------------
    Logging
-------------------------------------------------------------------------------------------------------------------- """
DATE = "date"
DATE_ = "date_"
ORG = "org"
ISP = "isp"
CITY = "city"
REGION_NAME = "regionName"
UNKNOWN = "Unknown"
SAY_TEAM = "say_team"
STEAM = "STEAM"
TSAY = "tsay"
SAY = "say"
SAY_TEAM_LOGS_TXT = "say_team_logs.txt"
SAY_LOGS_TXT = "say_logs.txt"
L_ = "L20"
NS_NAME = "name"
TEAM = "team"
RETR_ = "RETR "
D_M_Y = "%d-%m-%Y"

""" --------------------------------------------------------------------------------------------------------------------
    File modes
-------------------------------------------------------------------------------------------------------------------- """
READ_MODE = "r"
WB_MODE = "wb"
W_PLUS_MODE = "w+"
WRITE_MODE = "w"
READ_PLUS_MODE = "r+"

""" --------------------------------------------------------------------------------------------------------------------
    VAC Banned
-------------------------------------------------------------------------------------------------------------------- """
STEAM_ID_ = "SteamId"
T_TEAM = "Team"
ECONOMY_BAN = "EconomyBan"
COMMUNITY_BANNED = "CommunityBanned"
NUMBER_OF_VAC_BANS = "NumberOfVACBans"
DAYS_SINCE_LAST_BAN = "DaysSinceLastBan"
VAC_BANNED = "VACBanned"
STATS = "Stats"
PLAYERS = "players"
EMPTY_RAW_STRING = r""

""" --------------------------------------------------------------------------------------------------------------------
    Match constants
-------------------------------------------------------------------------------------------------------------------- """
TEAM_LIST = "team_list"
COUNT = "count"
USERS = "users"
CREATED = "Created"
COMPLETED = "Completed"

""" --------------------------------------------------------------------------------------------------------------------
    Helper constants
-------------------------------------------------------------------------------------------------------------------- """
WORKBOOK_HELPER = "workbook_helper"
USER_INPUT_HELPER = "user_input_helper"
PRINT_HELPER = "print_helper"
SQL_HELPER = "my_sql_helper"
LOCAL_DATA_HELPER = "local_data_helper"
FTP_HELPER = "ftp_helper"
DATA_STORE_HELPER = "data_store_helper"
CLOUD_SERVER_HELPER = "cloud_server_helper"
CONFIG_HELPER = 'config_helper'
CERTIFICATE_HELPER = 'certificate_helper'
LOG_HELPER = "log_helper"

""" --------------------------------------------------------------------------------------------------------------------
    Config Constants
-------------------------------------------------------------------------------------------------------------------- """
FOLDER_LOCATIONS = "Folder Locations"
FILE_LOCATIONS = "File Locations"
FONT_PATH = 'FONT_PATH'
CERT_IMG_PATH = 'CERT_IMG_PATH'
CERTIFICATES = 'CERTIFICATES'
FILES_HOME = 'FILES_HOME'
PROJECT_ID = 'PROJECT_ID'
SERVICE_ACCOUNT_KEY_PATH = 'SERVICE_ACCOUNT_KEY_PATH'
SERVICE_ACCOUNT_EMAIL = 'SERVICE_ACCOUNT_EMAIL'
PROJECT_DETAILS = 'Project Details'
STEAM_API_KEY = 'STEAM_API_KEY'
CSTRIKE_LOGS = 'CSTRIKE_LOGS'
LOGS_STARTING = 'LOGS_STARTING'
ADDONS_AMXMODX_LOGS = 'ADDONS_AMXMODX_LOGS'
SCORE_STARTING = 'SCORE_STARTING'
CONFIGS_RESULTS = 'CONFIGS_RESULTS'
HLTV_STARTING = 'HLTV_STARTING'
BANNED_USERS_FILE = 'STEAM_BANNED_USERS_FILE'
STEAM_USER_API = 'STEAM_USER_API'
IP_LOG_STARTING = 'IP_LOG_STARTING'
LOGGING_CONF = 'LOGGING_CONF'
MAX_PLAYERS = 'MAX_PLAYERS'
USER_NAME = 'USERNAME'
PASS_WORD = 'PASSWORD'
DATABASE = 'DATABASE'
HOSTNAME = 'HOSTNAME'
MY_SQL = 'MySQL'
STATS_FILE = 'STATS_FILE'
STEAM_ID_LIST_TXT = 'STEAM_ID_LIST_TXT'
TEAM_DETAILS = 'TEAM_DETAILS'
PLAYER_DETAILS = 'PLAYER_DETAILS'
MAX_MATCHES = 'MAX_MATCHES'
TEAM_DETAILS_XLSX = 'TEAM_DETAILS_XLSX'
INITIAL_SETUP = 'INITIAL_SETUP'
TOURNEY_MANAGER = 'Tourney Manager'
