from constants import StringConstants as sC, PrintStrings as pS, LogStrings as lS
from util.LogHelper import LogHelper


class EndMatch:
    def __init__(self, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)

    def get_match_id(self, matches, user_input_helper, local_data_helper, config):
        """
        To get match id from the user

        :param config: Config Object
        :param local_data_helper: LocalDataHelper Object
        :param user_input_helper: UserInputHelper Object
        :param matches: Dict of matches
        :return: match Id
        """

        # Create Directories for Logs,Scores and HLTV
        local_data_helper.create_directory(config[sC.FOLDER_LOCATIONS][sC.FILES_HOME])
        local_data_helper.create_directory(config[sC.FOLDER_LOCATIONS][sC.LOGS_STARTING])
        local_data_helper.create_directory(config[sC.FOLDER_LOCATIONS][sC.SCORE_STARTING])
        local_data_helper.create_directory(config[sC.FOLDER_LOCATIONS][sC.HLTV_STARTING])

        # Check if any match is present in datastore
        if matches.__len__() == 0:
            self.logger.error(pS.NO_ACTIVE_MATCHES_FOUND_)
            print(pS.NO_ACTIVE_MATCHES_FOUND_)
            exit(1)

        # Get match id as input from user
        match_id_ = user_input_helper.get_match_id(matches)

        return match_id_

    def download_using_ftp(self, match_id, node_name, server_id, folder, cloud_server_helper, data_store_helper,
                           ftp_helper, hltv_node_name):
        """
        Download Logs, HLTV Demos from server

        :param hltv_node_name: HLTV node name
        :param ftp_helper: FTPHelper Object
        :param data_store_helper: DataStoreHelper Object
        :param cloud_server_helper: CloudServerHelper Object
        :param match_id: Id of the match
        :param node_name: Instance name
        :param server_id: Server Id
        :param folder: Destination folder
        """

        self.logger.info(lS.CONFIRMING_DATE)
        date = data_store_helper.confirm_start_date(match_id)

        self.logger.info(lS.VERIFY_SERVER_FOR_DATA_DOWNLOAD)
        node = cloud_server_helper.start_server(node_name, server_id, display_ip=False)
        self.logger.info(lS.SERVER_STARTED_FOR_DOWNLOAD)
        ftp_helper.get_logs_from_ftp(date, node, server_id, folder, cloud_server_helper)
        self.logger.info(lS.MATCH_DATA_DOWNLOADED_FROM_FTP)

        self.logger.info(lS.VERIFYING_AND_STARTING_HLTV)
        node = cloud_server_helper.start_hltv(server_id, hltv_node_name, display_ip=False)
        self.logger.info(lS.STARTING_HLTV_FOR_DOWNLOAD)
        ftp_helper.get_hltv_demos_from_ftp(date, node, server_id, folder, cloud_server_helper)
        self.logger.info(lS.MATCH_DEMOS_FROM_FTP)

    def stop_servers(self, server_id, cloud_server_helper):
        """
        Stop Match and HLTV Server

        :param cloud_server_helper: CloudServerHelper Object
        :param server_id: Server Id
        """

        self.logger.info(lS.STOPPING_MATCH_SERVER)
        cloud_server_helper.stop_server_with_confirmation(server_id)
        self.logger.info(lS.SERVER_SUCCESSFULLY)

        self.logger.info(lS.STOPPING_HLTV_SERVER)
        cloud_server_helper.stop_hltv_with_confirmation(server_id)
        self.logger.info(lS.HLTV_SERVER_SUCCESSFULLY)

    def add_to_data_store(self, match_id, matches, data_store_helper, local_data_helper):
        """
        Add player stats to DataStore

        :param local_data_helper: LocalDataHelper Object
        :param data_store_helper: DataStoreHelper Object
        :param match_id: Id of the match
        :param matches: Dict of matches
        """

        self.logger.info(lS.FETCHING_MATCH_DETAILS)
        match_name, team1, team2 = self.get_match_name(match_id, matches)
        self.logger.info(lS.MATCH_BETWEEN_AND_.format(team1, team2))

        self.logger.info(lS.FETCHING_DATA_FROM_LOGS)
        stats = local_data_helper.get_stats_from_logs(match_name)
        self.logger.info(lS.DATA_FETCHED_SUCCESSFULLY)

        key_value = pS.Z_MATCH__VS_.format(match_id, local_data_helper.get_og_team_name(team1),
                                           local_data_helper.get_og_team_name(team2))
        self.logger.info(lS.KEY_.format(key_value))

        self.logger.info(lS.SAVING_TO_DATASTORE)
        data_store_helper.save_to_data_store(stats, key_value)
        self.logger.info(lS.DATA_SAVED_SUCCESSFULLY)

    def get_match_name(self, match_id, matches):
        """
        Format and return the match name

        :param match_id: Id of the match
        :param matches: Dict of matches
        :return: Match name and team names
        """

        team1 = matches[match_id][sC.TERRORIST]
        team2 = matches[match_id][sC.COUNTER_TERRORIST]

        match_name = pS.MATCH__ + match_id + sC.SPACE + team1 + sC.SPACE + sC.VERSUS + sC.SPACE + team2
        self.logger.info(pS.MATCH_INFO_.format(match_id, team1, team2))

        return match_name, team1, team2

    def ip_parse(self, local_data_helper):
        """
        Parse IP of players from logs

        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(pS.LOADING_SAVED_DATA)
        steam_id = local_data_helper.get_ip_data()
        self.logger.info(lS.LOCAL_DATA_LOADED)

        self.logger.info(pS.NEW_DATA_FROM_LOGS)
        steam_id = local_data_helper.get_data_from_logs(steam_id)
        self.logger.info(lS.DATA_FROM_LOGS_LOADED)

        self.logger.info(pS.FETCHING_IP_DETAILS)
        steam_id = local_data_helper.get_ip_details(steam_id)
        self.logger.info(lS.IP_DETAILS_FETCHED)

        self.logger.info(pS.SAVING_DATA)
        local_data_helper.save_to_file(steam_id)
        self.logger.info(lS.IP_DATA_SAVED)

    def end_match(self, cloud_server_helper, data_store_helper, ftp_helper, local_data_helper, my_sql_helper,
                  user_input_helper, print_helper, config):
        """
        End the match and process its data

        :param config: Config object
        :param print_helper: PrintHelper Object
        :param user_input_helper: UserInputHelper Object
        :param my_sql_helper: MySQLHelper Object
        :param local_data_helper: LocalDataHelper Object
        :param ftp_helper: FTPHelper Object
        :param cloud_server_helper: CloudServerHelper Object
        :param data_store_helper: DataStoreHelper Object
        """

        self.logger.info(lS.FETCHING_ACTIVE_MATCHES)
        matches = data_store_helper.get_matches()
        self.logger.info(lS.LOADED_ACTIVE_MATCHES.format(matches.__len__()))

        match_id = self.get_match_id(matches, user_input_helper, local_data_helper, config)
        self.logger.info(lS.MATCH_ID_SELECTED.format(match_id))

        self.logger.info(lS.CREATING_DIR_SAVING_DATA)
        folder = local_data_helper.get_folder_name_create_dirs(match_id, matches)

        self.logger.info(pS.MATCH_SELECTED_ + sC.COLON + sC.SPACE + match_id + sC.SPACE +
                         matches[match_id][sC.TERRORIST] + sC.SPACE + sC.VERSUS + sC.SPACE +
                         matches[match_id][sC.COUNTER_TERRORIST])
        self.logger.info(pS.ASSOCIATED_SERVERS___)

        node_name, hltv_node_name, server = local_data_helper.get_node_name_and_server(matches, match_id)
        self.logger.info(lS.SERVER_ID_.format(server))
        self.logger.info(lS.INSTANCE_NAME_.format(node_name))
        self.logger.info(lS.HLTV_INSTANCE_NAME_.format(hltv_node_name))

        self.logger.info(lS.DOWNLOADING_MATCH_DATA)
        self.download_using_ftp(match_id, node_name, server, folder, cloud_server_helper, data_store_helper, ftp_helper,
                                hltv_node_name)
        self.logger.info(lS.DOWNLOAD_OF_MATCH_DATA_COMPLETE)

        self.logger.info(lS.STOPPING_SERVERS)
        self.stop_servers(server, cloud_server_helper)
        self.logger.info(lS.STOPPING_SERVERS_SUCCESSFUL)

        self.logger.info(lS.MATCH_IN_MY_SQL_DATABASE)
        my_sql_helper.end_match(match_id, matches)
        self.logger.info(lS.MATCH_END_IN_MY_SQL)

        self.logger.info(lS.SAVING_MATCH_SCORES)
        print(pS.SAVE_MAP_SCORES_MSG)
        data_store_helper.add_match_scores(match_id, matches, user_input_helper, print_helper)
        self.logger.info(lS.MATCH_SCORES_SAVED_SUCCESSFULLY)

        self.logger.info(lS.SAVING_PLAYER_SCORES)
        print(pS.SAVE_PLAYER_SCORES_MSG)
        self.add_to_data_store(match_id, matches, data_store_helper, local_data_helper)
        self.logger.info(lS.PLAYER_SCORES_SAVED_SUCCESSFULLY)

        self.logger.info(lS.PARSING_IP_LOGS)
        print(pS.PARSING_LOGS_MSG)
        local_data_helper.save_logs(match_id, matches)
        self.ip_parse(local_data_helper)
        self.logger.info(lS.LOGS_PARSED_SUCCESSFULLY)
