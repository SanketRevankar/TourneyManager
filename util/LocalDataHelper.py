import json
import os
from time import sleep

import requests

from constants import StringConstants as sC, PrintStrings as pS, Config as cF, PlayerDetails as pD, \
    MatchServers as mS, TeamDetails as tD, MatchServers, LogStrings as lS
from util.LogHelper import LogHelper


class LocalDataHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        config = config_helper.get_config()
        self.ip_log_starting_ = config[sC.FOLDER_LOCATIONS][sC.IP_LOG_STARTING]
        self.hltv_starting_ = config[sC.FOLDER_LOCATIONS][sC.HLTV_STARTING]
        self.score_starting_ = config[sC.FOLDER_LOCATIONS][sC.SCORE_STARTING]
        self.logs_starting_ = config[sC.FOLDER_LOCATIONS][sC.LOGS_STARTING]
        self.steam_api_key = config[sC.PROJECT_DETAILS][sC.STEAM_API_KEY]
        self.steam_user_api_ = config[sC.PROJECT_DETAILS][sC.STEAM_USER_API]
        self.banned_users_file_ = config[sC.FILE_LOCATIONS][sC.BANNED_USERS_FILE]

    @staticmethod
    def get_server_ip_from_server_id(server_id):
        """
        Returns Server Ip of server with given Id

        :param server_id: Id of given server
        :return: Ip of the server
        """

        return mS.ServerList[server_id][sC.SERVER_IP]

    @staticmethod
    def get_team_details_from_id(team_id):
        """
        Returns Team name, Team tag and Captain id from Team Id

        :param team_id: Id of the team
        :return: Team name, Team tag and Captain id from Team Id
        """

        return tD.TeamList[team_id][sC.TEAM_NAME_], tD.TeamList[team_id][sC.TEAM_TAG_], tD.TeamList[team_id][sC.EMAIL]

    @staticmethod
    def get_details_by_id(steam_id):
        """
        Get nick, name of a player by steam id

        :param steam_id: Steam id of the player
        :return: Nick, Name
        """

        for team_name in pD.PlayerList:
            for player in pD.PlayerList[team_name]:
                if pD.PlayerList[team_name][player][sC.STEAM_ID] == steam_id:
                    return team_name, pD.PlayerList[team_name][player][sC.NICK_], pD.PlayerList[team_name][player][
                        sC.NAME_]

    @staticmethod
    def get_og_team_name(team_name):
        """
        Get original team name from team name

        :param team_name: Team name without special chars
        :return: Original team name
        """

        for zTeamName in tD.TeamList:
            if tD.TeamList[zTeamName][sC.TEAM_NAME_] == team_name:
                return tD.TeamList[zTeamName][sC.TEAM_NAME_OG]

    @staticmethod
    def get_nick_name(name):
        """
        Get details of player by player's name

        :param name: Name of the player
        :return: Player nick, Player name
        """

        for team_name in pD.PlayerList:
            for player in pD.PlayerList[team_name]:
                if pD.PlayerList[team_name][player][sC.NAME_] == name:
                    return pD.PlayerList[team_name][player][sC.NICK_], pD.PlayerList[team_name][player][sC.NAME_]

    @staticmethod
    def get_name_nick_team(steam):
        """
        Get details of a player

        :param steam: Steam ID of the Player
        :return: Name, Nick and team of the Player
        """

        for team in pD.PlayerList:
            for player in pD.PlayerList[team]:
                if pD.PlayerList[team][player][sC.STEAM_ID] == steam:
                    return pD.PlayerList[team][player][sC.NAME_], pD.PlayerList[team][player][sC.NICK_], team

    def get_captain_nick_name(self, team):
        """
        Returns the name of captain if team with given Id exists.

        :param team: Id of the team
        :return: Captains name
        """

        try:
            return self.get_nick_name(tD.TeamList[team][sC.CAPTAINS_NAME])
        except TypeError:
            return ''

    @staticmethod
    def count_wins(i, scores):
        print(pS.MATCH_ + sC.COLON, i)
        print(sC.TAB, scores[i][sC.TEAM_1_], sC.VERSUS,
              scores[i][sC.TEAM_2_])

        win = 0
        for m in range(0, 5):
            try:
                score = scores[i][pS.MAP__SCORE.format(m + 1)]
                print(sC.TAB + sC.TAB + sC.STAR,
                      scores[i][pS.MAP_.format(m + 1)].ljust(10), score.rjust(cF.PADDING))
                score_split = score.split(sC.DASH)
                if int(score_split[0].strip()) < int(score_split[1].strip()):
                    win += 1
                else:
                    win -= 1
            except KeyError:
                break
        return win

    @staticmethod
    def add_team_count(count_matches, file_split):
        """
        Count matches played by teams from logs

        :param count_matches: Dict to store matches played by teams
        :param file_split: File name as split to get team names
        """

        if file_split[1] not in count_matches:
            count_matches[file_split[1]] = 0
        count_matches[file_split[1]] += 1
        if file_split[3] not in count_matches:
            count_matches[file_split[3]] = 0
        count_matches[file_split[3]] += 1

    @staticmethod
    def get_steam_id(index, current_team):
        """
        Get steam id of a player with given index belonging to a team if exists

        :param index: Index of the player
        :param current_team: Name of the team
        :return: Steam ID of the player
        """

        try:
            return pD.PlayerList[current_team][str(index)][sC.STEAM_ID]
        except KeyError:
            return sC.NO_PLAYER

    def get_folder_name_create_dirs(self, match_id, matches):
        """
        Generate Folder name and create directories to store Logs,Scores and HLTV

        :param match_id: Id of the match
        :param matches: Dict of all matches
        :return: Name of the folder created
        """

        folder = pS.MATCH_VS_.format(match_id, matches[match_id][sC.TERRORIST], matches[match_id][sC.COUNTER_TERRORIST])
        self.logger.info(lS.FOLDER_NAME_.format(folder))

        self.create_directory(self.logs_starting_ + folder)
        self.create_directory(self.score_starting_ + folder)
        self.create_directory(self.hltv_starting_ + folder)

        return folder

    @staticmethod
    def get_team(steam):
        """
        Find team of a given player

        :param steam: Steam ID of the player
        :return: Team name of the player
        """

        for team_name in pD.PlayerList:
            for player in pD.PlayerList[team_name]:
                if pD.PlayerList[team_name][player][sC.STEAM_ID] == steam:
                    return team_name

    @staticmethod
    def get_nick(steam):
        """
        Find nick of a given player

        :param steam: Steam ID of the player
        :return: Nick of the player
        """

        for team_name in pD.PlayerList:
            for player in pD.PlayerList[team_name]:
                if pD.PlayerList[team_name][player][sC.STEAM_ID] == steam:
                    return pD.PlayerList[team_name][player][sC.NICK_]

    def get_ip_data(self):
        """
        Load previous IP Data from local system

        :return: Dict of IP Data
        """

        steam_id = {}

        self.logger.info(lS.THE_DATA_IS_STORED)
        files = self.get_files_to_save_logs()

        c_steam = sC.UNKNOWN
        c_ip = sC.UNKNOWN

        for file in files:
            self.logger.info(lS.LOADING_DATA_FOR_.format(file))
            for line in files[file]:
                if line[0] == sC.HASH:
                    steam_id_ = line[line.index(sC.STEAM):].strip()
                    c_steam = steam_id_

                if sC.SEMI_COLON in line and line[0] != sC.HASH:
                    line_split = line.split(sC.SEMI_COLON)
                    c_ip = line_split[0].strip()
                    details = line_split[1].split(sC.TAB)

                    if c_steam not in steam_id:
                        steam_id[c_steam] = {}
                    steam_id[c_steam][c_ip] = {
                        sC.REGION_NAME: details[0].strip(),
                        sC.CITY: details[1].strip(),
                        sC.ISP: details[2].strip(),
                        sC.ORG: details[3].strip()
                    }

                if sC.DATE in line:
                    line_split = line.split()
                    c = 0
                    date = sC.UNKNOWN

                    for line_c in line_split:
                        if c == 0:
                            c += 1
                            steam_id[c_steam][c_ip][line_c] = []
                            date = line_c
                        else:
                            steam_id[c_steam][c_ip][date] \
                                .append(line_c.replace(sC.SINGLE_QUOTE, sC.EMPTY_STRING)
                                        .replace(sC.OPEN_SQ_BRACE, sC.EMPTY_STRING)
                                        .replace(sC.CLOSE_SQ_BRACE, sC.EMPTY_STRING)
                                        .replace(sC.COMMA, sC.EMPTY_STRING))

        return steam_id

    def load_stats_from_logs(self, stats):
        """
        Load stats from logs stored locally

        :param stats: Dict of stats for all players
        """

        starting_ = self.score_starting_
        self.logger.info(lS.LOADING_MATCHES_FROM_.format(starting_))

        for file in os.listdir(starting_):
            self.logger.info(lS.LOADING_STATS_FOR_.format(starting_ + file))
            temp_ids = []

            for file_ip in os.listdir(starting_ + file):
                if sC.TEXT not in file_ip:
                    continue

                with open(starting_ + file + sC.SEPARATOR + file_ip) as f:
                    for line in f:
                        stat = line.strip().split()
                        team, nick, name = self.get_details_by_id(stat[0])

                        if stat[0] not in temp_ids:
                            temp_ids.append(stat[0])
                            stats[team][stat[0]][sC.MATCHES] += 1
                        stats[team][stat[0]][stat[1]] += 1

    def get_files_to_save_logs(self):
        """
        Get list of files to store IP data

        :return: Dict of files
        """

        files = {}
        for team in pD.PlayerList:
            if os.path.exists(self.ip_log_starting_ + team.replace(sC.PIPE, sC.EMPTY_STRING) + sC.TXT):
                files[team] = open(self.ip_log_starting_ +
                                   team.replace(sC.PIPE, sC.EMPTY_STRING) + sC.TXT, sC.READ_MODE, encoding=cF.ENCODING)
        return files

    def get_data_from_logs(self, steam_id):
        """
        Get IP Data from logs of current match

        :param steam_id: List of all steam IDs
        """

        self.logger.info(lS.IP_DATA_FROM_MATCH_LOGS)
        for file_a in os.listdir(self.logs_starting_):
            for file in os.listdir(self.logs_starting_ + file_a):
                if pS.IP_ + sC.UNDERSCORE in file:
                    date = file.strip().replace(pS.IP_ + sC.UNDERSCORE, sC.EMPTY_STRING).replace(
                        sC.TXT, sC.EMPTY_STRING)
                    with open(self.logs_starting_ + sC.UNIX_SEPARATOR + file_a +
                              sC.UNIX_SEPARATOR + file, encoding=cF.ENCODING) as f:
                        for line in f:
                            log = line.strip().split(sC.TAB_)

                            try:
                                _, _, _ = self.get_name_nick_team(log[2])
                            except TypeError:
                                continue

                            if log[2] not in steam_id:
                                steam_id[log[2]] = {}

                            if log[3] not in steam_id[log[2]]:
                                steam_id[log[2]][log[3]] = {}

                            if sC.DATE_ + date not in steam_id[log[2]][log[3]]:
                                steam_id[log[2]][log[3]][sC.DATE_ + date] = []

                            steam_id[log[2]][log[3]][sC.DATE_ + date].append(log[0])

        return steam_id

    def get_connections(self, file, match, steam):
        """
        Returns connection to server by players

        :param file: Name of the file to open
        :param match: Name of the match folder
        :param steam: steam Id of the player
        """

        self.logger.info(lS.LOADING_CONNECTIONS_OF_.format(steam))
        count = 0
        with open(self.logs_starting_ + match + sC.SEPARATOR + file,
                  encoding=cF.ENCODING) as f:
            for line in f:
                line_split = line.split(sC.DOUBLE_QUOTE)

                if pS.CONNECTED in line or pS.WAS_KICKED_BY_CONSOLE_ in line or pS.ENTERED_THE_GAME in line:
                    try:
                        pos_steam = line_split[1].index(sC.STEAM)
                    except ValueError:
                        continue
                    steam_id = line_split[1][pos_steam:line_split[1].index(sC.GREATER_THAN, pos_steam)]
                    if steam_id == steam:
                        print(sC.TAB, line.strip())
                        count += 1
        if count == 0:
            self.logger.info(lS.NO_CONNECTIONS_FOUND)
        else:
            self.logger.info(lS.FOUND_CONNECTIONS.format(count))

    @staticmethod
    def get_info(community_id):
        """
        Get player information

        :param community_id: Community id of the player
        """

        authserver = (int(community_id) - 76561197960265728) & 1
        authid = (int(community_id) - 76561197960265728 - authserver) / 2
        steamid = cF.STEAM_ID_FORMAT.format(authserver, int(authid))

        for team in pD.PlayerList:
            for player in pD.PlayerList[team]:
                if pD.PlayerList[team][player][sC.STEAM_ID] == steamid:
                    print(team)
                    print(sC.TAB + sC.STEAM_ID + sC.COLON + sC.SPACE + steamid)
                    print(sC.TAB + sC.NAME_ + sC.COLON + sC.SPACE + pD.PlayerList[team][player][sC.NAME_])
                    print(sC.TAB + sC.NICK_ + sC.COLON + sC.SPACE + pD.PlayerList[team][player][sC.NICK_])

    def get_data(self, ac):
        """
        Fetch data from Steam API

        :return: 0 for failure
        """

        url_final = self.steam_user_api_ + self.steam_api_key + cF.STEAM_API_ADDRESS + ac.read(1800)
        data_from_site = requests.get(url_final)

        file = open(self.banned_users_file_, sC.WRITE_MODE)
        file.write(str(data_from_site.text))
        file.close()

        if str(data_from_site)[11:14] != cF.MAX_USERS_TO_CHECK_FOR_BANS:
            print(pS.DOWNLOAD_ERROR_N_CODE_ + str(data_from_site))
            return 0

    def get_ip_details(self, steam_id):
        """
        Fetch details of IP from APIs

        :param steam_id: List of all steam IDs
        """

        url = cF.IP_API_URL
        self.logger.info(lS.IP_DETAILS_FROM_.format(url))

        for steam in steam_id:
            for c_ip in steam_id[steam]:
                try:
                    _ = steam_id[steam][c_ip][sC.REGION_NAME]
                    continue
                except KeyError:
                    pass

                url_c = url + c_ip
                self.logger.info(pS.FETCHING_DETAILS_OF_ + sC.COLON + sC.SPACE + c_ip)
                response = requests.get(url_c)
                resp = json.loads(response.text)
                steam_id[steam][c_ip][sC.REGION_NAME] = resp[sC.REGION_NAME]
                steam_id[steam][c_ip][sC.CITY] = resp[sC.CITY]
                steam_id[steam][c_ip][sC.ISP] = resp[sC.ISP]
                steam_id[steam][c_ip][sC.ORG] = resp[sC.ORG]
                sleep(cF.SLEEP_TIME)

        return steam_id

    def get_max(self, stat_current, ids, stats, count_matches):
        """
        Get player data with highest given stat

        :param count_matches: Dict containing matches played by teams
        :param stats: Dict containing stats for all players
        :param stat_current: Stat to find highest for
        :param ids: List of IDs not to check
        :return: Data of player with highest stat
        """

        max_stat = {stat_current: 0}

        for steam_id in stats:
            if steam_id not in ids:
                if stats[steam_id][stat_current] > max_stat[stat_current]:
                    max_stat[stat_current] = stats[steam_id][stat_current]
                    max_stat[sC.S_STEAM_ID] = steam_id

        try:
            team_name, nick_name, name_this = self.get_details_by_id(max_stat[sC.S_STEAM_ID])
        except KeyError:
            return

        return max_stat[sC.S_STEAM_ID], sC.PIPE + sC.SPACE + \
               str(max_stat[sC.S_STEAM_ID]).ljust(25) + sC.PIPE + \
               str(max_stat[stat_current]).center(7) + sC.PIPE + sC.SPACE + \
               name_this.ljust(30) + sC.PIPE + sC.SPACE + \
               str(count_matches[self.remove_spl_chars(team_name)]) + sC.SPACE + sC.SPACE + \
               sC.PIPE + sC.SPACE + team_name.ljust(37) + sC.PIPE + \
               sC.SPACE + nick_name.ljust(40) + sC.PIPE

    def load_stats_from_local(self, matches):
        """
        Get stats from Logs stored locally

        :param matches: Dict containing all the matches played
        :return: Dict containing stats of all players
        """

        stats = {}
        for match in matches:
            for file in os.listdir(self.score_starting_ + sC.UNIX_SEPARATOR +
                                   matches[match][sC.NAME_]):

                if sC.TXT not in file:
                    continue

                with open(sC.EMPTY_RAW_STRING + self.score_starting_ + sC.UNIX_SEPARATOR +
                          matches[match][sC.NAME_] + sC.UNIX_SEPARATOR + file) as f:
                    for line in f:
                        stat = line.strip().split()

                        if stat[0] not in stats:
                            team, nick, name = self.get_details_by_id(stat[0])
                            stats[stat[0]] = {
                                sC.KILLS: 0,
                                sC.DEATHS: 0,
                                sC.GRENADE: 0,
                                sC.HEADSHOT: 0,
                                sC.SUICIDE: 0,
                                sC.BOMB_PLANT: 0,
                                sC.BOMB_DEFUSE: 0,
                                sC.KNIFE: 0,
                                sC.NAME_SMALL: name,
                                sC.NICK_SMALL: nick,
                            }

                        stats[stat[0]][stat[1]] += 1
        return stats

    def load_match(self, file, file_split, matches):
        """
        Add match with given Id to Dict of matches

        :param file: Folder for the match
        :param file_split: File split for team names
        :param matches: Dict of matches
        """

        # noinspection PyTypeChecker
        match_id = file_split[0].split(sC.DASH)[1]
        matches[match_id] = {
            sC.NAME_: file,
            sC.TEAM_1_: file_split[1],
            sC.TEAM_2_: file_split[3],
        }

        self.logger.info(pS.LOADED_ + sC.SPACE + matches[match_id][sC.NAME_])

    @staticmethod
    def load_time_from_data(steam_id_):
        """
        Get Time of first and last login

        :param steam_id_: Steam Id of the player
        :return: Dict of Ips of players
        """

        ips = {}
        for steam_id in steam_id_:
            for ip in steam_id_[steam_id]:
                if ip not in ips:
                    ips[ip] = {}
                if steam_id not in ips[ip]:
                    ips[ip][steam_id] = {
                        sC.START_TIME: steam_id_[steam_id][ip][sC.START_TIME],
                        sC.END_TIME: steam_id_[steam_id][ip][sC.END_TIME],
                    }
        return ips

    def get_top_n(self, stat_current, number, stats, count_matches):
        """
        Get top players for each stat

        :param stats:
        :param count_matches:
        :param stat_current: Name of the stat
        :param number: Number of players to print
        """

        line_separator = sC.PLUS + sC.DASH * 26 + sC.PLUS + \
                         sC.DASH * 7 + sC.PLUS + sC.DASH * 31 + \
                         sC.PLUS + sC.DASH * 5 + sC.PLUS + \
                         sC.DASH * 38 + sC.PLUS + sC.DASH * 41 + \
                         sC.PLUS

        stats_header = sC.PIPE + sC.SPACE + sC.STEAM_ID.center(24) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.STATS.center(5) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.NAME_.center(29) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.M.center(3) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.T_TEAM.center(36) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.NICK_.center(39) + \
                       sC.SPACE + sC.PIPE

        print(line_separator)
        print(stats_header)
        print(line_separator)

        c_stat = []
        for i in range(number):
            try:
                steam_id, to_print = self.get_max(stat_current, c_stat, stats, count_matches)
            except TypeError:
                continue

            c_stat.append(steam_id)
            print(to_print)

        print(line_separator)

    def get_ip_data_from_logs(self):
        """
        Get player login from logs

        """

        steam_id = {}

        for file_ac in os.listdir(self.logs_starting_):
            self.logger.info(lS.LOADING_IP_DATA_OF_.format(file_ac))
            for file_c in os.listdir(self.logs_starting_ + file_ac):
                if pS.IP_ + sC.UNDERSCORE in file_c:
                    date_c = file_c.strip().replace(pS.IP_ + sC.UNDERSCORE, sC.EMPTY_STRING) \
                        .replace(sC.TXT, sC.EMPTY_STRING)

                    with open(self.logs_starting_ + sC.UNIX_SEPARATOR + file_ac +
                              sC.UNIX_SEPARATOR + file_c, encoding=cF.ENCODING) as f_c:
                        for line_c in f_c:
                            log_c = line_c.strip().split(sC.TAB_)

                            try:
                                _, _, _ = self.get_name_nick_team(log_c[2])
                            except TypeError:
                                continue

                            if log_c[2] not in steam_id:
                                steam_id[log_c[2]] = {}

                            if log_c[3] not in steam_id[log_c[2]]:
                                steam_id[log_c[2]][log_c[3]] = {}
                                steam_id[log_c[2]][log_c[3]][sC.START_TIME] = date_c + sC.SPACE + log_c[0]
                                steam_id[log_c[2]][log_c[3]][sC.END_TIME] = date_c + sC.SPACE + log_c[0]
                            else:
                                steam_id[log_c[2]][log_c[3]][sC.END_TIME] = date_c + sC.SPACE + log_c[0]
            return steam_id

    def get_stats_from_logs(self, match_name):
        """
        Get stats from Logs stored locally

        :param match_name: Name of the match folder
        :return: Dict of stats of given match
        """

        self.logger.info(lS.INITIALIZING_STATS)
        stats = {}
        starting_match_name = self.score_starting_ + match_name
        self.logger.info(lS.LOADING_STATS_FROM_.format(starting_match_name))
        for file_ip in os.listdir(starting_match_name):
            with open(starting_match_name + sC.SEPARATOR + file_ip) as f:
                for line in f:
                    stat = line.strip().split()

                    try:
                        team, nick, name = self.get_details_by_id(stat[0])
                    except TypeError:
                        self.logger.exception(lS.NOT_FOUND_.format(stat[0]))
                        continue

                    if team not in stats:
                        stats[team] = {}

                    if stat[0] not in stats[team]:
                        stats[team][stat[0]] = {
                            sC.KILLS: 0,
                            sC.DEATHS: 0,
                            sC.GRENADE: 0,
                            sC.HEADSHOT: 0,
                            sC.SUICIDE: 0,
                            sC.BOMB_PLANT: 0,
                            sC.BOMB_DEFUSE: 0,
                            sC.KNIFE: 0,
                            sC.NS_NAME: name,
                            sC.NICK_SMALL: nick,
                        }

                    stats[team][stat[0]][stat[1]] += 1

        self.logger.info(lS.LOADING_STATS_COMPLETED)
        return stats

    def create_directory(self, directory_path):
        """
        Create a directory if it doesn't exists

        :param directory_path: Path where the directory should be created
        """

        if not os.path.exists(directory_path):
            self.logger.info(pS.CREATING_FOLDER_ + sC.COLON + sC.SPACE + directory_path)
            os.mkdir(directory_path)

    def save_logs(self, match_id, matches):
        """
        Parse various logs of the match

        :param match_id: Id of the match
        :param matches: Dict of match details
        """

        self.logger.info(lS.SAVING_LOGS_FOR_MATCH_.format(match_id))
        file = pS.MATCH__ + match_id.zfill(2) + sC.SPACE + matches[match_id][sC.TERRORIST] + sC.SPACE + sC.VERSUS + \
               sC.SPACE + matches[match_id][sC.COUNTER_TERRORIST]
        self.logger.info(lS.FILE_.format(file))

        file_split = file.split()
        team_len = max(file_split[1].__len__(), file_split[3].__len__()) + 2

        say_logs_txt = self.logs_starting_ + file + sC.UNIX_SEPARATOR + sC.SAY_LOGS_TXT
        self.logger.info(lS.FILE_FOR_SAY_LOGS_.format(say_logs_txt))
        write_file = open(say_logs_txt, sC.W_PLUS_MODE, encoding=cF.ENCODING)

        say_team_logs_txt = self.logs_starting_ + file + sC.UNIX_SEPARATOR + \
                            sC.SAY_TEAM_LOGS_TXT
        self.logger.info(lS.FOR_TEAM_SAY_LOGS)
        write_file_team = open(say_team_logs_txt, sC.W_PLUS_MODE, encoding=cF.ENCODING)

        for c_file in os.listdir(self.logs_starting_ + file):
            if sC.LOG not in c_file:
                continue

            if sC.L_ in c_file:
                continue

            write_file.write(sC.STAR + sC.SPACE + c_file + sC.NEW_LINE)
            write_file_team.write(sC.STAR + sC.SPACE + c_file + sC.NEW_LINE)

            with open(self.logs_starting_ + file + sC.UNIX_SEPARATOR + c_file,
                      encoding=cF.ENCODING) as f:
                for line in f:
                    if sC.SAY in line and sC.TSAY not in line:
                        line_split = line.split(sC.DOUBLE_QUOTE)

                        try:
                            pos_steam = line_split[1].index(sC.STEAM)
                        except ValueError:
                            self.logger.exception(lS.VALUE_ERROR_.format(line_split[1]))
                            continue

                        steam_id = line_split[1][pos_steam:line_split[1].index(sC.GREATER_THAN, pos_steam)]

                        try:
                            nick = self.get_nick(steam_id)
                        except AttributeError:
                            self.logger.exception(lS.ATTRIBUTE_ERROR_.split(steam_id))
                            nick = steam_id

                        try:
                            team = self.get_team(steam_id)
                        except AttributeError:
                            self.logger.exception(lS.ATTRIBUTE_ERROR_.split(steam_id))
                            team = steam_id

                        if sC.SAY_TEAM not in line:
                            write_file.write(sC.TAB + str(team).ljust(team_len) + str(nick).ljust(38) + sC.COLON +
                                             sC.SPACE + line_split[3] + sC.NEW_LINE)
                        else:
                            write_file_team.write(sC.TAB + str(team).ljust(team_len) + str(nick).ljust(38) + sC.COLON +
                                                  sC.SPACE + line_split[3] + sC.NEW_LINE)

        self.logger.info(lS.WRITTEN_SUCCESSFULLY)

    def save_to_file(self, steam_id):
        """
        Save the current IP data

        :param steam_id: Steam id of the player
        """

        ip_log_starting_ = self.ip_log_starting_
        self.logger.info(lS.SAVING_IP_DATA_TO_.format(ip_log_starting_))
        self.create_directory(ip_log_starting_)

        files = {}

        self.logger.info(lS.CLEARING_PREVIOUS_DATA)
        for team in pD.PlayerList:
            files[team] = open(ip_log_starting_ + team.replace(sC.PIPE, sC.EMPTY_STRING) + sC.TXT,
                               sC.W_PLUS_MODE, encoding=cF.ENCODING)

        for steam in steam_id:
            try:
                name, nick, team = self.get_name_nick_team(steam)
            except TypeError:
                self.logger.exception(lS.STEAM_ID_NOT_FOUND_.format(steam))
                continue

            files[team].write((sC.NEW_LINE + pS.PRINT_PLAYER_INFO + sC.NEW_LINE).format(name, nick, steam.strip()))

            for c_ip in steam_id[steam]:
                files[team].write(sC.TAB + str(c_ip).ljust(15) + sC.SPACE + sC.SEMI_COLON +
                                  steam_id[steam][c_ip][sC.REGION_NAME] + sC.TAB + steam_id[steam][c_ip][sC.CITY] +
                                  sC.TAB + steam_id[steam][c_ip][sC.ISP] + sC.TAB + steam_id[steam][c_ip][sC.ORG] +
                                  sC.NEW_LINE)

                for date in steam_id[steam][c_ip]:
                    if sC.DATE in date:
                        files[team].write(sC.TAB + sC.TAB + date + sC.SPACE + str(steam_id[steam][c_ip][date]) +
                                          sC.NEW_LINE)

    def init_stats(self):
        """
        Initial stats values to 0

        :return: Dict of stats
        """

        stats = {}

        for team in pD.PlayerList:
            for player in pD.PlayerList[team]:
                if team not in stats:
                    stats[team] = {}
                if pD.PlayerList[team][player][sC.STEAM_ID] not in stats[team]:
                    stats[team][pD.PlayerList[team][player][sC.STEAM_ID]] = {
                        sC.KILLS: 0,
                        sC.DEATHS: 0,
                        sC.GRENADE: 0,
                        sC.HEADSHOT: 0,
                        sC.SUICIDE: 0,
                        sC.BOMB_PLANT: 0,
                        sC.BOMB_DEFUSE: 0,
                        sC.KNIFE: 0,
                        sC.MATCHES: 0,
                        sC.NAME_SMALL: pD.PlayerList[team][player][sC.NAME_],
                        sC.NICK_SMALL: pD.PlayerList[team][player][sC.NICK_],
                    }

        self.logger.info(lS.WITH_FOR_EACH_PLAYER)
        return stats

    @staticmethod
    def remove_spl_chars(team_name):
        """
        Remove special characters from team name

        :param team_name: Name of the team
        :return: Team name with removed special characters
        """

        for team_c in tD.TeamList:
            if tD.TeamList[team_c][sC.TEAM_NAME_OG] == team_name:
                return tD.TeamList[team_c][sC.TEAM_NAME_]

    def average_stats(self, count_matches, stats):
        """
        Average all player stats by number of matches played

        :param count_matches: Number of matches played
        :param stats: Dict of stats
        """

        for steam in stats:
            for stat in stats[steam]:
                if stat == sC.NAME_SMALL or stat == sC.NICK_SMALL:
                    continue

                team, _, _ = self.get_details_by_id(steam)
                stats[steam][stat] = round(stats[steam][stat] / count_matches[self.remove_spl_chars(team)], 1)

    def print_ip_matches(self, ips):
        """
        Print Ip which match with some player

        :param ips: Dict of IPs
        """

        count = 0
        for ip in ips:
            if ips[ip].__len__() > 1:
                print(ip)
                count += 1

                for steam in ips[ip]:
                    name, nick, team = self.get_name_nick_team(steam)
                    print(sC.TAB + sC.STAR + team[:cF.TEAM_PRINT_PADDING].ljust(cF.TEAM_PRINT_PADDING),
                          name[:cF.NAME_PRINT_PADDING].ljust(cF.NAME_PRINT_PADDING),
                          nick[:cF.NICK_PRINT_PADDING].ljust(cF.NICK_PRINT_PADDING),
                          ips[ip][steam][sC.START_TIME], ips[ip][steam][sC.END_TIME], sC.TAB, steam)

        if count > 0:
            self.logger.info(lS.PRINTED_IP_MATCHES)
        else:
            self.logger.info(lS.NO_IP_MATCHES_FOUND)

    def get_node_name_and_server(self, matches, match_id):
        """
        Get the node name of the instance and server details using match id

        :param matches: Dict of all matches
        :param match_id: Id of the match
        :return: Instance and hltv name and server Id
        """
        for server in MatchServers.ServerList:
            if MatchServers.ServerList[server][sC.SERVER_IP] == matches[match_id][sC.IP]:
                self.logger.info(pS.SERVER_FOUND_ + sC.COLON + sC.SPACE +
                                 MatchServers.ServerList[server][sC.SERVER_NAME])
                self.logger.info(pS.HLTV_ + sC.SPACE + MatchServers.ServerList[server][sC.SERVER_NAME]
                                 .replace(sC.MATCH_SERVER, sC.HLTV))
                return MatchServers.ServerList[server][sC.INSTANCE_NAME], \
                       MatchServers.ServerList[server][sC.HLTV_NAME], server
