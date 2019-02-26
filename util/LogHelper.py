import logging
import logging.config

from constants import StringConstants as sC


class LogHelper:
    def __init__(self, config_helper):
        self.config = config_helper.get_config()
        logging.config.fileConfig(self.config[sC.FILE_LOCATIONS][sC.LOGGING_CONF])

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        return logger
