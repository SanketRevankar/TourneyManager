from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from constants import StringConstants as sC, PrintStrings as pS, MatchServers as mS, LogStrings as lS
from util.LogHelper import LogHelper


class CloudServerHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        self.config = config_helper.get_config()
        self.ComputeEngine = get_driver(Provider.GCE)
        self.gc = self.ComputeEngine(self.config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_EMAIL],
                                     self.config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_KEY_PATH],
                                     project=self.config[sC.PROJECT_DETAILS][sC.PROJECT_ID])

    @staticmethod
    def status(node):
        """
        Used to get Status a server.

        :param node: Node Object
        :return: Status of the server
        """
        return node.state

    def start(self, node):
        """
        Start a node. This is only possible if the node is stopped.

        :param node: Node Object
        :return: Server start success status
        """
        return self.gc.ex_start_node(node) if self.status(node) == sC.STOPPED else pS.ALREADY_RUNNING

    def stop(self, node):
        """
        Stop a node. This is only possible if the node is started.

        :param node: Node Object
        :return: Server stop success status
        """
        return self.gc.ex_stop_node(node) if self.status(node) == sC.RUNNING else pS.ALREADY_STOPPED

    def ip(self, node):
        """
        IP of a node. This is only possible if the node is started.

        :param node: Node Object
        :return: Server IP
        """
        return node.public_ips[0] if self.status(node) == sC.RUNNING else pS.SERVER_TO_GET_IP

    def stop_hltv_with_confirmation(self, server_id):
        """
        Used to stop a Compute Engine Instance after getting confirmation from user. If already stopped no action will
        be taken.

        :param server_id: Id of the server
        """

        node_name = mS.ServerList[server_id][sC.HLTV_NAME]
        node = self.gc.ex_get_node(node_name)
        server_status = self.status(node)
        self.logger.info(lS.SERVER_STATUS_.format(node_name, server_status))

        if server_status == sC.RUNNING:
            if sC.Y == input(pS.STOP_THE_SERVER_Y_N_ + sC.COLON + sC.SPACE):
                self.logger.info(pS.STOPPING_HLTV___)

                if self.stop(node) is True:
                    self.logger.info(pS.HLTV_STOPPED_ + sC.COLON + sC.SPACE +
                                     mS.ServerList[server_id][sC.HLTV_SERVER_NAME])
                else:
                    self.logger.error(pS.HLTV_NOT_STOPPED_)
                    exit(-1)
        elif server_status == sC.STOPPED:
            self.logger.info(pS.ALREADY_STOPPED)

    def stop_server_with_confirmation(self, server_id):
        """
        Used to stop a Compute Engine Instance after getting confirmation from user. If already stopped no action will
        be taken.

        :param server_id: Id of the server
        """

        node_name = mS.ServerList[server_id][sC.INSTANCE_NAME]
        node = self.gc.ex_get_node(node_name)
        server_status = self.status(node)
        self.logger.info(lS.SERVER_STATUS_.format(node_name, server_status))

        if server_status == sC.RUNNING:
            if sC.Y == input(pS.STOP_THE_SERVER_Y_N_ + sC.COLON + sC.SPACE):
                self.logger.info(pS.STOPPING_SERVER___)
                if self.stop(node) is True:
                    self.logger.info(pS.SERVER_STOPPED_ + sC.COLON + sC.SPACE +
                                     mS.ServerList[server_id][sC.SERVER_NAME])
                else:
                    self.logger.error(pS.NOT_STOP_SUCCESSFULLY_)
                    exit(-1)

        elif server_status == sC.STOPPED:
            self.logger.info(pS.ALREADY_STOPPED)

    def start_server(self, node_name, server_id, display_ip=True):
        """
        Used to start a Compute Engine Instance. If already running no action will be taken.

        :param display_ip: Whether to display IP after starting the server
        :param node_name: Name of the instance to start
        :param server_id: ID of the server
        :return: Instance variable which was started
        """

        node = self.gc.ex_get_node(node_name)
        server_status = self.status(node)
        self.logger.info(lS.SERVER_STATUS_.format(node_name, server_status))

        if server_status == sC.STOPPED:
            self.logger.info(lS.STARTING_SERVER_.format(node_name))

            if self.start(node):
                self.logger.info(pS.SERVER_STARTED_ + sC.COLON + sC.SPACE + mS.ServerList[server_id][sC.SERVER_NAME])
            else:
                self.logger.error(pS.NOT_START_SUCCESSFULLY_)
                exit(-1)

            node = self.gc.ex_get_node(node_name)
        elif server_status == sC.RUNNING:
            self.logger.info(pS.ALREADY_RUNNING)

        if display_ip:
            self.logger.info(lS.SERVER_IP_.format(
                node_name, self.ip(node) + sC.COLON + mS.ServerList[server_id][sC.PORT]))

        return node

    def start_hltv(self, server_id, node_name, display_ip=True):
        """
        Used to start a Compute Engine Instance for HLTV. If already running no action will be taken.

        :param display_ip: Whether to display IP after starting the server
        :param node_name: Name of the instance to start
        :param server_id: Id of the server to start
        """

        node = self.gc.ex_get_node(node_name)
        server_status = self.status(node)
        self.logger.info(lS.SERVER_STATUS_.format(node_name, server_status))

        self.logger.info(pS.HLTV_STATUS_ + sC.COLON + sC.SPACE + server_status)
        if server_status == sC.STOPPED:
            self.logger.info(lS.STARTING_SERVER_.format(node_name))

            if self.start(node):
                self.logger.info(pS.HLTV_STARTED_ + sC.COLON + sC.SPACE +
                                 mS.ServerList[server_id][sC.SERVER_NAME].replace(sC.MATCH_SERVER, sC.HLTV))
            else:
                self.logger.error(pS.HLTV_NOT_START_SUCCESSFULLY_)
                exit(-1)

            node = self.gc.ex_get_node(node_name)

        elif server_status == sC.RUNNING:
            self.logger.info(pS.ALREADY_RUNNING)

        if display_ip:
            self.logger.info(lS.SERVER_IP_.format(
                node_name, self.ip(node) + sC.COLON + mS.ServerList[server_id][sC.PORT]))

            print(pS.HLTV_IP_.format(self.ip(node) + sC.COLON + mS.ServerList[server_id][sC.PORT]))

        return node
