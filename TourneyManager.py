import time

from constants import StringConstants as sC, PrintStrings as pS, LogStrings
from functions import *
from util import *


class TourneyManager:

    def __init__(self):
        self.helpers = {
            sC.CLOUD_SERVER_HELPER: CloudServerHelper.CloudServerHelper,
            sC.DATA_STORE_HELPER: DataStoreHelper.DataStoreHelper,
            sC.FTP_HELPER: FTPHelper.FTPHelper,
            sC.LOCAL_DATA_HELPER: LocalDataHelper.LocalDataHelper,
            sC.SQL_HELPER: MySQLHelper.MySQLHelper,
            sC.PRINT_HELPER: PrintHelper.PrintHelper,
            sC.USER_INPUT_HELPER: UserInputHelper.UserInputHelper,
            sC.WORKBOOK_HELPER: WorkbookHelper.WorkbookHelper,
            sC.CONFIG_HELPER: ConfigHelper.ConfigHelper(),
            sC.CERTIFICATE_HELPER: CertificateHelper.CertificateHelper,
        }
        self.helpers[sC.LOG_HELPER] = LogHelper.LogHelper(self.helpers[sC.CONFIG_HELPER])

        self.config = self.helpers[sC.CONFIG_HELPER].get_config()
        self.logger = self.helpers[sC.LOG_HELPER].get_logger(self.__class__.__name__)
        self.logger.info(LogStrings.HELPER_CLASSES)

        if self.config.getboolean(section=sC.TOURNEY_MANAGER, option=sC.INITIAL_SETUP):
            self.logger.info(LogStrings.INITIAL_SETUP)
            self.helpers[sC.SQL_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]).initial_setup()
            self.logger.info(LogStrings.INITIAL_SETUP_COMPLETED)
        else:
            self.logger.info(LogStrings.ENABLE_INIT)

        self.logger.info(LogStrings.POSSIBLE_OPERATIONS)
        self.operations = {
            sC.ONE: lambda: CreateNewMatch.CreateNewMatch(self.helpers[sC.LOG_HELPER]).create_new_match(
                self.helpers[sC.DATA_STORE_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.USER_INPUT_HELPER](self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.LOCAL_DATA_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.SQL_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.PRINT_HELPER]()
            ),
            sC.TWO: lambda: StartMatch.StartMatch(self.helpers[sC.LOG_HELPER]).start_match(
                self.helpers[sC.DATA_STORE_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.CLOUD_SERVER_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.USER_INPUT_HELPER](self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.LOCAL_DATA_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER])
            ),
            sC.THREE: lambda: EndMatch.EndMatch(self.helpers[sC.LOG_HELPER]).end_match(
                self.helpers[sC.CLOUD_SERVER_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.DATA_STORE_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.FTP_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.LOCAL_DATA_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.SQL_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.USER_INPUT_HELPER](self.helpers[sC.LOG_HELPER]), self.helpers[sC.PRINT_HELPER](),
                self.helpers[sC.CONFIG_HELPER].get_config()
            ),
            sC.FOUR: lambda: GetMatchData.GetMatchData(
                self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]).get_match_data(
                self.helpers[sC.DATA_STORE_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.PRINT_HELPER](),
                self.helpers[sC.LOCAL_DATA_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]),
                self.helpers[sC.WORKBOOK_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER])
            ),
            sC.FIVE: LoadSteamIDs.LoadSteamIDs(self.helpers[sC.CONFIG_HELPER],
                                               self.helpers[sC.LOG_HELPER]).get_player_list,
            sC.SIX: LoadSteamIDs.LoadSteamIDs(self.helpers[sC.CONFIG_HELPER],
                                              self.helpers[sC.LOG_HELPER]).get_team_list,
            sC.SEVEN: lambda: self.helpers[sC.SQL_HELPER](
                self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER]).add_steam_ids_to_db(
                self.helpers[sC.LOCAL_DATA_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER])),
            sC.EIGHT: lambda: self.helpers[sC.CERTIFICATE_HELPER](self.helpers[sC.CONFIG_HELPER],
                                                                  self.helpers[sC.LOG_HELPER]).create_certificates(
                self.helpers[sC.LOCAL_DATA_HELPER](self.helpers[sC.CONFIG_HELPER], self.helpers[sC.LOG_HELPER])
            ),
            sC.NINE: LoadSteamIDs.LoadSteamIDs(self.helpers[sC.CONFIG_HELPER],
                                               self.helpers[sC.LOG_HELPER]).convert_steam_id,
            sC.TEN: LoadSteamIDs.LoadSteamIDs(self.helpers[sC.CONFIG_HELPER],
                                              self.helpers[sC.LOG_HELPER]).get_access_data_for_captains,
        }

    def tourney_manager(self):
        print(pS.WELCOME_MSG)

        while 1:
            print(pS.TOURNEY_MANAGER_MSG)
            inp = input(pS.ENTER_YOUR_CHOICE_)

            self.operations[inp]() if inp in self.operations else exit(sC.BYE)
            self.logger.info(LogStrings.ACTION_COMPLETED)
            self.logger.info(LogStrings.LOADING_OPERATIONS)
            time.sleep(5)


if __name__ == '__main__':
    TourneyManager().tourney_manager()
