from configparser import ConfigParser, ExtendedInterpolation
from constants import StringConstants as sC


class ConfigHelper:
    def __init__(self):
        self.config = ConfigParser(allow_no_value=True, inline_comment_prefixes=('#',),
                                   interpolation=ExtendedInterpolation())
        self.config_conf = None
        self.get_config_file()

    def get_config_file(self):
        print("Config File is not set. Copy its FULL path default in resources/config.conf")
        self.config_conf = input("Enter config file path: ")
        try:
            self.config.read(self.config_conf)
            _ = self.config[sC.FILE_LOCATIONS][sC.LOGGING_CONF]
            _ = self.config[sC.MY_SQL][sC.USER_NAME]
            _ = self.config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_EMAIL]
            _ = self.config[sC.TOURNEY_MANAGER][sC.INITIAL_SETUP]
        except KeyError:
            print('Enter valid config file path')
            return self.get_config_file()
        self.write_config_py()
        print('Config set successfully')
        print('Restart the application to continue')
        exit(0)

    def write_config_py(self):
        file = open('util/ConfigHelper.py', 'w+')
        file.write("""from configparser import ConfigParser, ExtendedInterpolation


class ConfigHelper:
    def __init__(self):
        self.config = ConfigParser(allow_no_value=True, inline_comment_prefixes=('#', ),
                                   interpolation=ExtendedInterpolation())
        self.config_conf = r'{}'""".format(self.config_conf) + """
        self.config.read(self.config_conf)
        self.validate_config()

    def get_config(self):
        return self.config

    def validate_config(self):
        config = self.get_config()
        for section in config.sections():
            for key, value in config[section].items():
                if value is None:
                    exit('[{}] {} is not set\\nSet Value in {} to continue'.format(section, key.upper(),
                                                                                  self.config_conf))
"""
                   )
