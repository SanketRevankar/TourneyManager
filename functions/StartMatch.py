from constants import LogStrings as lS
from util.LogHelper import LogHelper


class StartMatch:
    def __init__(self, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)

    def start_match(self, data_store_helper, cloud_server_helper, user_input_helper, local_data_helper):
        """
        Starts a match

        :param local_data_helper: LocalDataHelper Object
        :param user_input_helper: UserInputHelper Object
        :param data_store_helper: DataStoreHelper Object
        :param cloud_server_helper: CloudServerHelper Object
        """
        self.logger.info(lS.FETCHING_CREATED_MATCHES)
        matches = data_store_helper.get_created_matches()
        self.logger.info(lS.LOADED___MATCHES.format(matches.__len__()))

        match_id = user_input_helper.get_match_id(matches)
        self.logger.info(lS.MATCH_ID_SELECTED.format(match_id))

        node_name, hltv_node_name, server = local_data_helper.get_node_name_and_server(matches, match_id)
        self.logger.info(lS.SERVER_ID_.format(server))
        self.logger.info(lS.INSTANCE_NAME_.format(node_name))
        self.logger.info(lS.HLTV_INSTANCE_NAME_.format(hltv_node_name))

        cloud_server_helper.start_server(node_name, server)
        self.logger.info(lS.SERVER_STARTED_SUCCESSFULLY.format(node_name))

        cloud_server_helper.start_hltv(server, hltv_node_name)
        self.logger.info(lS.SERVER_STARTED_SUCCESSFULLY.format(hltv_node_name))

        data_store_helper.start_match(match_id)
        self.logger.info(lS.MATCH_STARTED_SUCCESSFULLY.format(match_id))
