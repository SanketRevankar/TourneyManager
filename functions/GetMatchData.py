import json
import os
import re

import pandas as pd
import xlsxwriter

from constants import StringConstants as sC, Config as cF, PrintStrings as pS, PlayerDetails as pD, \
    LogStrings as lS
from util.LogHelper import LogHelper


class GetMatchData:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        self.config = config_helper.get_config()
        self.ac = open(self.config[sC.FILE_LOCATIONS][sC.STEAM_ID_LIST_TXT], sC.READ_PLUS_MODE)

    """ ----------------------------------------------------------------------------------------------------------------
            # 1.  Save Team-wise Player Stats to Excel File.
    ---------------------------------------------------------------------------------------------------------------- """

    def save_stats_xls(self, local_data_helper, workbook_helper, print_helper):
        """
        Save Team-wise Player Stats to Excel File.

        :param print_helper: PrintHelper Object
        :param workbook_helper: WorkbookHelper Object
        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(lS.WORKBOOK_TO_SAVE_DATA)
        stats_file_ = self.config[sC.FOLDER_LOCATIONS][sC.FILES_HOME] + sC.SEPARATOR + \
                      self.config[sC.FILE_LOCATIONS][sC.STATS_FILE]
        workbook = xlsxwriter.Workbook(stats_file_)
        self.logger.info(lS.WORKBOOK_CREATED_AT_.format(stats_file_))

        self.logger.info(lS.INITIALIZING_STATS)
        stats = local_data_helper.init_stats()

        self.logger.info(lS.LOADING_STATS_FROM_LOGS)
        local_data_helper.load_stats_from_logs(stats)
        self.logger.info(lS.LOADED_STATS_FROM_LOGS)

        self.logger.info(lS.WRITING_STATS_TO_FILE_.format(stats_file_))
        workbook_helper.write_stats(stats, workbook, print_helper, local_data_helper)
        self.logger.info(lS.STATS_WRITTEN_TO_.format(stats_file_))

        workbook.close()
        self.logger.info(lS.WORKBOOK_CLOSED)

    """ ----------------------------------------------------------------------------------------------------------------
            # 2.  Get Players with Highest Stats.
    ---------------------------------------------------------------------------------------------------------------- """

    def get_top(self, local_data_helper, print_helper):
        """
        Get top players

        :param print_helper: PrintHelper Object
        :param local_data_helper: LocalDataHelper Object
        """

        matches = {}
        count_matches = {}
        self.logger.info(pS.LOADING_MATCHES_)

        for file in os.listdir(self.config[sC.FOLDER_LOCATIONS][sC.SCORE_STARTING]):
            file_split = file.split()

            local_data_helper.load_match(file, file_split, matches)
            local_data_helper.add_team_count(count_matches, file_split)

        stats = local_data_helper.load_stats_from_local(matches)

        if cF.AVERAGE_STATS_BY_MATCHES_PLAYED:
            self.logger.info(lS.AVG_STATS_ARE_CONFIGURED_)
            self.logger.info(lS.NUMBER_OF_MATCHES_PLAYED)
            local_data_helper.average_stats(count_matches, stats)

        self.logger.info(lS.PRINTING_TOP_STATS)
        print_helper.print_top_stats(count_matches, stats, local_data_helper)

    """ ----------------------------------------------------------------------------------------------------------------
            # 3.  Show Match Scores of all Matches.
    ---------------------------------------------------------------------------------------------------------------- """

    def show_scores(self, data_store_helper, local_data_helper, print_helper):
        """
        Print scores of matches

        :param data_store_helper: DataStoreHelper Object
        :param print_helper: PrintHelper Object
        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(lS.FETCHING_MATCH_SCORES)
        scores: dict = data_store_helper.fetch_scores(local_data_helper)
        self.logger.info(lS.MATCH_SCORES_LOADED)

        if scores.__len__() == 0:
            self.logger.error(pS.COMPLETED_YET_)

        self.logger.info(lS.PRINTING_MATCH_SCORES)
        for i in range(1, int(self.config[sC.PROJECT_DETAILS][sC.MAX_MATCHES])):
            try:
                _ = scores[i]
            except KeyError:
                continue

            win = local_data_helper.count_wins(i, scores)

            print_helper.print_winner(i, scores, win)
        self.logger.info(lS.MATCH_SCORES_ARE_PRINTED)

    """ ----------------------------------------------------------------------------------------------------------------
            # 4.  Get IP matches for every Player.
    ---------------------------------------------------------------------------------------------------------------- """

    def get_ip_matches(self, local_data_helper):
        """
        Find Players with same IP addresses

        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(lS.IP_DATA_FROM_LOGS)
        steam_id = local_data_helper.get_ip_data_from_logs()
        self.logger.info(lS.LOADED_IP_DATA)

        self.logger.info(lS.LOAD_TIME_FROM_IP_DATA)
        ips = local_data_helper.load_time_from_data(steam_id)
        self.logger.info(lS.LOADED_TIME_FROM_IP_DATA)

        self.logger.info(lS.PRINTING_IP_MATCHES)
        local_data_helper.print_ip_matches(ips)

    # Loads data from non-match server, local files
    """
        steamID = {}
        for file_a in os.listdir(cF.LOGS_STARTING):
            for file in os.listdir(cF.LOGS_STARTING + file_a):
                if pS.IP_ + sC.UNDERSCORE in file:
                    date = file.strip().replace(pS.IP_ + sC.UNDERSCORE, sC.EMPTY_STRING).replace(sC.TXT, 
                    sC.EMPTY_STRING)
                    
                    with open(cF.LOGS_STARTING + sC.UNIX_SEPARATOR + file_a + sC.UNIX_SEPARATOR + file, 
                              encoding=cF.ENCODING) as f:
                        for line in f:
                            log = line.strip().split(sC.TAB)
                            
                            try:
                                _, _, _ = get_name_nick_team(log[2])
                            except TypeError:
                                continue
                            
                            if log[2] not in steamID:
                                steamID[log[2]] = {}
                            
                            if log[3] not in steamID[log[2]]:
                                steamID[log[2]][log[3]] = []
                            
                            if date not in steamID[log[2]][log[3]]:
                                steamID[log[2]][log[3]].append(date)
        
        steam_ids = {}
        for folder in os.listdir(config.IP_LOG_STARTING):
            if '2018-06' not in folder and '2018-05' not in folder and '2018-07' not in folder:
                continue
            for file in os.listdir(Config.IP_LOG_STARTING + folder):
                with open(Config.IP_LOG_STARTING + folder + '/' + file, encoding='utf8') as f:
                    c_date = file.replace('IP_', StringConstants.EMPTY_STRING).replace('.txt', 
                    StringConstants.EMPTY_STRING)
                    for line in f:
                        line_split = line.split('\t')
                        try:
                            c_steam_id = line_split[2]
                            c_ip = line_split[3].strip()
                        except IndexError:
                            continue
                        if c_steam_id not in steam_ids:
                            steam_ids[c_steam_id] = {
                                StringConstants.IP: {},
                            }
                        if c_ip not in steam_ids[c_steam_id][StringConstants.IP]:
                            steam_ids[c_steam_id][StringConstants.IP][c_ip] = []
                        if c_date not in steam_ids[c_steam_id][StringConstants.IP][c_ip]:
                            steam_ids[c_steam_id][StringConstants.IP][c_ip].append(c_date)
    
        matches = {}
        for steam_id in steamID:
            name, nick, team = get_name_nick_team(steam_id)
            for ip in steamID[steam_id]:
                for c_steam_id in steam_ids:
                    for c_ip in steam_ids[c_steam_id][StringConstants.IP]:
                        if ip == c_ip and c_steam_id != steam_id:
                            if ip not in matches:
                                matches[ip] = {}
                                if c_steam_id not in matches[ip]:
                                    matches[ip][c_steam_id] = {
                                        'date': steam_ids[c_steam_id][StringConstants.IP][c_ip],
                                    }
                                if steam_id not in matches[ip]:
                                    matches[ip][steam_id] = {
                                        StringConstants.NICK_SMALL: name,
                                        StringConstants.NAME_SMALL: nick,
                                        'team': team,
                                        'date': steamID[steam_id][ip],
                                    }
    
        for ip in matches:
            temp = []
            for steam in matches[ip]:
                temp.append(steam)
            a = temp[0]
            b = temp[1]
            if a != '#' and b != '#':
                match = set(matches[ip][a]['date']) & set(matches[ip][b]['date'])
                if match.__len__() > 0:
                    print('\n', ip, StringConstants.DASH, match)
                    print('\t#', b, StringConstants.DASH, matches[ip][b][StringConstants.NAME_SMALL], '[' +
                     matches[ip][b][StringConstants.NICK_SMALL] + '] -',
                          matches[ip][b]['team'], '\n\t\t-', matches[ip][b]['date'])
                    print('\t*', a, matches[ip][a]['date'])
    """

    """ ----------------------------------------------------------------------------------------------------------------
            # 5.  Get Connections of a Player by his Steam ID.
    ---------------------------------------------------------------------------------------------------------------- """

    def get_player_connections(self, local_data_helper):
        """
        Get player connections and disconnections

        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(lS.CONNECTIONS_OF_A_USER)
        steam = input(sC.STEAM_ID + sC.COLON + sC.SPACE)
        self.logger.info(lS.STEAM_ID_.format(steam))

        for match in os.listdir(self.config[sC.FOLDER_LOCATIONS][sC.LOGS_STARTING]):
            for file in os.listdir(self.config[sC.FOLDER_LOCATIONS][sC.LOGS_STARTING] + match):
                if sC.LOG not in file:
                    continue
                if sC.L_ in file:
                    continue

                local_data_helper.get_connections(file, match, steam)

    """ ----------------------------------------------------------------------------------------------------------------
            # 6.  Save Team Details (Players in a team) to Excel File.
    ---------------------------------------------------------------------------------------------------------------- """

    def teams_to_xls(self):
        """
        Save players list as Excel file with team as sheets of workbook

        """

        self.logger.info(lS.INITIATING_EXCEL_WRITER)
        team_details_xlsx_ = self.config[sC.FOLDER_LOCATIONS][sC.FILES_HOME] + sC.SEPARATOR + \
                             self.config[sC.FILE_LOCATIONS][sC.TEAM_DETAILS_XLSX]
        writer = pd.ExcelWriter(team_details_xlsx_, engine=cF.XLSX_ENGINE)
        self.logger.info(lS.WRITING_TO_FILE_.format(team_details_xlsx_))

        for teams in pD.PlayerList:
            self.logger.info(lS.WRITING_TEAM_DETAILS_OF_.format(teams))
            team_name = re.sub(cF.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING, teams)[:31]
            players = pd.DataFrame.from_dict(pD.PlayerList[teams], orient=sC.ORIENT)
            players.to_excel(writer, sheet_name=team_name)

        self.logger.info(lS.SAVING_FILE_)
        writer.save()
        self.logger.info(lS.FILE_SAVED_.format(team_details_xlsx_))

    """ ----------------------------------------------------------------------------------------------------------------
            # 7.  Check VAC Bans of Players Registered.
    ---------------------------------------------------------------------------------------------------------------- """

    def acc_check_vac(self, local_data_helper):
        """
        VAC Ban checker for players

        :param local_data_helper: LocalDataHelper Object
        """

        def process_data_vac(local_data_helper_):
            """
            Process the data fetched from API

            :param local_data_helper_: LocalDataHelper Object
            """

            file_base = open(self.config[sC.FILE_LOCATIONS][sC.BANNED_USERS_FILE], sC.READ_PLUS_MODE)
            data = json.load(file_base)
            file_base.close()

            n = (len(data[sC.PLAYERS]))

            for n in range(0, n):
                if (data[sC.PLAYERS][n][sC.VAC_BANNED]) == bool(pS.TRUE):
                    print(data[sC.PLAYERS][n][sC.STEAM_ID_] + pS.VAC_BANNED_,
                          data[sC.PLAYERS][n][sC.NUMBER_OF_VAC_BANS],
                          pS.LAST_TIME_, data[sC.PLAYERS][n][sC.DAYS_SINCE_LAST_BAN], pS.DAYS_AGO)
                    local_data_helper_.get_info(data[sC.PLAYERS][n][sC.STEAM_ID_])

                if (data[sC.PLAYERS][n][sC.COMMUNITY_BANNED]) == bool(pS.TRUE):
                    print(data[sC.PLAYERS][n][sC.STEAM_ID_] + pS.P_COMMUNITY_BANNED)

                if (data[sC.PLAYERS][n][sC.ECONOMY_BAN]) == bool(pS.TRUE):
                    print(data[sC.PLAYERS][n][sC.STEAM_ID_] + pS.P_ECONOMY_BANN)

            if n != 0:
                self.acc_check_vac(local_data_helper_)

        self.logger.info(lS.STEAM_IDS_FOR_VAC_BANS)
        if local_data_helper.get_data(self.ac) != 0:
            process_data_vac(local_data_helper)

    def get_match_data(self, data_store_helper, print_helper, local_data_helper, workbook_helper):
        """
        Get locally stored match data

        :param workbook_helper: WorkbookHelper Object
        :param data_store_helper: DataStoreHelper Object
        :param print_helper: PrintHelper Object
        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(lS.ABOUT_MATCHES)

        print(pS.GET_MATCH_DATA_MSG)

        self.logger.info(lS.LOADING_OPERATIONS_)
        operations = {
            sC.ONE: lambda: self.save_stats_xls(local_data_helper, workbook_helper, print_helper),
            sC.TWO: lambda: self.get_top(local_data_helper, print_helper),
            sC.THREE: lambda: self.show_scores(data_store_helper, local_data_helper, print_helper),
            sC.FOUR: lambda: self.get_ip_matches(local_data_helper),
            sC.FIVE: lambda: self.get_player_connections(local_data_helper),
            sC.SIX: self.teams_to_xls,
            sC.SEVEN: lambda: self.acc_check_vac(local_data_helper),
        }

        inp = input(pS.ENTER_YOUR_CHOICE_)
        self.logger.info(lS.YOU_CHOSE_.format(inp))

        operations[inp]() if inp in operations else print(pS.INVALID_CHOICE)

        self.logger.info(lS.COMPLETED_SUCCESSFULLY)
