from constants import PrintStrings as pS, LogStrings as lS
from util.LogHelper import LogHelper


class CreateNewMatch:
    def __init__(self, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)

    def create_new_match(self, data_store_helper, user_input_helper, local_data_helper, my_sql_helper, print_helper):
        """
        Used to create a new match

        :param data_store_helper DataStoreHelper Object
        :param user_input_helper: UserInputHelper Object
        :param local_data_helper: LocalDataHelper Object
        :param my_sql_helper: MySQLHelper Object
        :param print_helper: PrintHelper Object
        """
        # Get Match ID & Server ID from user
        match_id = user_input_helper.get_match_id(None)
        self.logger.info(lS.MATCH_ID_SELECTED.format(match_id))
        server_id = user_input_helper.get_server_id_from_user(print_helper)

        # Get IP of the server
        ip = local_data_helper.get_server_ip_from_server_id(server_id)
        self.logger.info(lS.IP_SELECTED.format(ip))

        # Get Match details
        team1_id = user_input_helper.get_team_id_from_user(pS.ENTER_ID_OF_TEAM_1_, print_helper)
        self.logger.info(lS.TEAM_WITH_ID_SELECTED.format(team1_id))
        team2_id = user_input_helper.get_team_id_from_user(pS.ENTER_ID_OF_TEAM_2_, print_helper)
        self.logger.info(lS.TEAM_WITH_ID_SELECTED.format(team2_id))
        team1, team_tag1, team1_email = local_data_helper.get_team_details_from_id(team1_id)
        team2, team_tag2, team2_email = local_data_helper.get_team_details_from_id(team2_id)
        self.logger.info(lS.MATCH_BTWN.format(team1, team_tag1, team2, team_tag2))

        # DataStore
        data_store_helper.add_match(match_id, team1, team2, team_tag1, team_tag2, ip, team1_email, team2_email)

        # MySQL
        my_sql_helper.add_match(match_id, team1, team2, team_tag1, team_tag2, ip, team1_id, team2_id)

        # Fetch Captain details
        nick_t1, name_t1 = local_data_helper.get_captain_nick_name(team1_id)
        nick_ct1, name_ct1 = local_data_helper.get_captain_nick_name(team2_id)

        # Print Info of created match
        print_helper.print_match_info(match_id, team1, team2, team_tag1, team_tag2, ip, name_t1, nick_t1, name_ct1,
                                      nick_ct1, server_id)

        self.logger.info(lS.MATCH_WITH_ID_SUCCESSFUL.format(match_id))
