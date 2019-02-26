import re

from google.cloud import datastore

from constants import StringConstants as sC, Config as cF, PrintStrings as pS, PlayerDetails as pD, \
    TeamDetails as tD, LogStrings as lS
from util.LogHelper import LogHelper


class LoadSteamIDs:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        config = config_helper.get_config()
        account_key_path_ = config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_KEY_PATH]
        self.project_id_ = config[sC.PROJECT_DETAILS][sC.PROJECT_ID]
        self.id_list_txt_ = config[sC.FILE_LOCATIONS][sC.STEAM_ID_LIST_TXT]
        self.player_details = config[sC.FILE_LOCATIONS][sC.PLAYER_DETAILS]
        self.team_details = config[sC.FILE_LOCATIONS][sC.TEAM_DETAILS]
        self.client = datastore.Client.from_service_account_json(account_key_path_)

    def get_player_list(self):
        """
        Save Player List as Python Dict to a file

        """

        # noinspection PyTypeChecker
        self.logger.info(lS.TEAMS_FROM_DATASTORE)
        emails = self.team_list()

        player_details_py = self.player_details
        self.logger.info(lS.WRITING_PLAYER_DATA_TO_.format(player_details_py))
        file = open(player_details_py, sC.W_PLUS_MODE)
        file.write(pS.PLAYER_LIST_ + sC.NEW_LINE)
        for team in emails:
            self.logger.info(lS.FETCHING_PLAYERS_IN_TEAM_.format(team))
            # noinspection PyTypeChecker
            team_key = datastore.key.Key(sC.TEAM_LIST, team, project=self.project_id_)
            team_entity = self.client.get(team_key)

            # noinspection PyTypeChecker
            query = self.client.query(kind=sC.USERS)
            query.add_filter(sC.TEAM, sC.EQUALS, team)
            file.write(sC.TAB + pS.FORMAT_BRACES.format(sC.DOUBLE_QUOTE + team_entity[sC.TEAM_NAME]) + sC.DOUBLE_QUOTE +
                       sC.COLON + sC.SPACE + sC.OPEN_CURL_BRACE + sC.NEW_LINE)

            index = 0

            for entity in query.fetch():
                index += 1

                file.write(sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + pS.FORMAT_BRACES.format(index) + sC.DOUBLE_QUOTE +
                           sC.COLON + sC.SPACE + sC.OPEN_CURL_BRACE + sC.NEW_LINE)
                file.write(sC.TAB + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.STEAM_ID + sC.DOUBLE_QUOTE + sC.COLON +
                           sC.SPACE + sC.DOUBLE_QUOTE + pS.FORMAT_BRACES.format(entity[sC.S_STEAM_ID]) +
                           sC.DOUBLE_QUOTE + sC.COMMA + sC.NEW_LINE)
                file.write(
                    sC.TAB + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.NAME_ + sC.DOUBLE_QUOTE + sC.COLON + sC.SPACE +
                    sC.DOUBLE_QUOTE + pS.FORMAT_BRACES.format(entity[sC.NAME]) + sC.DOUBLE_QUOTE + sC.COMMA +
                    sC.NEW_LINE)
                file.write(
                    sC.TAB + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.NICK_ + sC.DOUBLE_QUOTE + sC.COLON + sC.SPACE +
                    "r" + sC.DOUBLE_QUOTE + pS.FORMAT_BRACES.format(entity[sC.STEAM_NICK]) + sC.DOUBLE_QUOTE +
                    sC.COMMA + sC.NEW_LINE)
                file.write(
                    sC.TAB + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.EMAIL + sC.DOUBLE_QUOTE + sC.COLON + sC.SPACE +
                    sC.DOUBLE_QUOTE + pS.FORMAT_BRACES.format(entity.key.name) + sC.DOUBLE_QUOTE + sC.COMMA +
                    sC.NEW_LINE)
                file.write(sC.TAB + sC.TAB + sC.CLOSE_CURL_BRACE + sC.COMMA + sC.NEW_LINE)

            file.write(sC.TAB + sC.CLOSE_CURL_BRACE + sC.COMMA + sC.NEW_LINE)

        file.write(sC.CLOSE_CURL_BRACE + sC.NEW_LINE)
        self.logger.info(lS.PLAYER_DATA_SUCCESSFULLY_WRITTEN_TO_.format(player_details_py))

    def convert_steam_id(self):
        """
        Convert Steam IDs to Community Ids

        """

        self.logger.info(lS.STEAM_ID_TO_COMMUNITY_ID)
        steam_id_list_txt_ = self.id_list_txt_
        self.logger.info(lS.WRITING_CONVERTED_IDS_TO_.format(steam_id_list_txt_))
        file = open(steam_id_list_txt_, sC.WRITE_MODE)

        for c_team in pD.PlayerList:
            for player in pD.PlayerList[c_team]:
                id_change_value = 76561197960265728
                id32 = pD.PlayerList[c_team][player][sC.STEAM_ID]
                y = id32[8:9]
                z = id32[10:]
                steam_id32_conv = int(z) * int(2) + int(y)
                steam_id_64_conv = int(steam_id32_conv) + int(id_change_value)
                file.write(str(steam_id_64_conv) + '\n')

        self.logger.info(lS.CONVERT_IDS_SUCCESSFULLY)

    def get_team_list(self):
        """
        Save Team List as Python Dict to a file

        """

        self.logger.info(lS.FETCHING_TEAM_LIST)
        emails = self.team_list()

        team_details_py = self.team_details
        self.logger.info(lS.WRITING_TEAM_DATA_TO_ + team_details_py)
        file = open(team_details_py, sC.W_PLUS_MODE)
        file.write(pS.TEAM_LIST_ + sC.NEW_LINE)

        i = 1

        for team in emails:
            self.logger.info(lS.FETCHING_DATA_FOR_TEAM_.format(team))
            # noinspection PyTypeChecker
            task_key = datastore.key.Key(sC.USERS, team, project=self.project_id_)
            # noinspection PyTypeChecker
            team_key = datastore.key.Key(sC.TEAM_LIST, team, project=self.project_id_)

            entity = self.client.get(task_key)
            team_entity = self.client.get(team_key)

            file.write(
                sC.TAB + sC.DOUBLE_QUOTE + pS.FORMAT_BRACES.format(str(i)) + sC.DOUBLE_QUOTE + sC.COLON + sC.SPACE +
                sC.OPEN_CURL_BRACE + sC.NEW_LINE + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.TEAM_NAME_ + sC.DOUBLE_QUOTE +
                sC.COLON + sC.SPACE + pS.FORMAT_BRACES.format(
                    sC.DOUBLE_QUOTE + re.sub(cF.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING,
                                             str(team_entity[sC.TEAM_NAME])) + sC.DOUBLE_QUOTE + sC.COMMA) +
                sC.NEW_LINE + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.TEAM_NAME_OG + sC.DOUBLE_QUOTE + sC.COLON +
                sC.SPACE +
                pS.FORMAT_BRACES.format(sC.DOUBLE_QUOTE + str(team_entity[sC.TEAM_NAME]) + sC.DOUBLE_QUOTE + sC.COMMA) +
                sC.NEW_LINE + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.TEAM_TAG_ + sC.DOUBLE_QUOTE + sC.COLON + sC.SPACE +
                pS.FORMAT_BRACES.format(sC.DOUBLE_QUOTE + str(team_entity[sC.TEAM_TAG]) + sC.DOUBLE_QUOTE + sC.COMMA) +
                sC.NEW_LINE + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.EMAIL + sC.DOUBLE_QUOTE + sC.COLON + sC.SPACE +
                pS.FORMAT_BRACES.format(sC.DOUBLE_QUOTE + str(team_entity.key.name) + sC.DOUBLE_QUOTE + sC.COMMA) +
                sC.NEW_LINE + sC.TAB + sC.TAB + sC.DOUBLE_QUOTE + sC.CAPTAINS_NAME + sC.DOUBLE_QUOTE + sC.COLON +
                sC.SPACE + pS.FORMAT_BRACES.format(
                    sC.DOUBLE_QUOTE + str(entity[sC.NAME]) + sC.DOUBLE_QUOTE + sC.COMMA) +
                sC.NEW_LINE + sC.TAB + sC.CLOSE_CURL_BRACE + sC.COMMA + sC.NEW_LINE
            )

            i += 1

        file.write(sC.CLOSE_CURL_BRACE + sC.NEW_LINE)
        self.logger.info(lS.TEAM_DATA_WRITTEN_TO_ + team_details_py)

    def team_list(self):
        """
        Fetch team list from datastore

        :return: List of teams
        """

        emails = []
        # noinspection PyTypeChecker
        query = self.client.query(kind=sC.TEAM_LIST)
        for entity in query.fetch():
            emails.append(entity.key.name)
        return emails

    def get_access_data_for_captains(self):
        """
        Print access strings for all captains

        """
        self.logger.info(lS.ACCESS_FOR_ALL_CAPTAINS)
        self.logger.info(lS.MANUALLY_TO_TEAM_LIST)
        self.logger.info(lS.CAPTAIN_DETAILS_FORMAT)
        for team in tD.TeamList:
            print('\n; {} - {}'.format(tD.TeamList[team][sC.TEAM_NAME_OG], tD.TeamList[team][sC.CAPTAINS_NAME]))
            try:
                print('\"{}\" \"\" \"m\" \"ce\" ; {}'.format(tD.TeamList[team][sC.CAPTAIN_1],
                                                             tD.TeamList[team][sC.CAPTAIN_NAME_1]))
                print('\"{}\" \"\" \"m\" \"ce\" ; {}'.format(tD.TeamList[team][sC.CAPTAIN_2],
                                                             tD.TeamList[team][sC.CAPTAIN_NAME_2]))
            except KeyError:
                continue
