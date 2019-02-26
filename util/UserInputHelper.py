import re

from constants import Config as cF, StringConstants as sC, PrintStrings as pS, LogStrings as lS
from util.LogHelper import LogHelper


class UserInputHelper:
    def __init__(self, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)

    @staticmethod
    def get_server_id_from_user(print_helper):
        """
        Ask user for Server Id

        :param print_helper: PrintHelper Object
        :return: Server Id
        """

        print_helper.print_server_list()
        return input(pS.ENTER_ID_OF_THE_SERVER_ + sC.COLON + sC.SPACE)

    @staticmethod
    def get_team_id_from_user(team, print_helper):
        """
        Ask user for Team Id

        :param team: Team 1/2
        :param print_helper: PrintHelper Object
        :return: Team Id
        """

        print_helper.print_team_list()
        return input(team + sC.COLON + sC.SPACE)

    @staticmethod
    def get_no_of_maps():
        """
        Ask user for Number of maps

        :return: Number of maps
        """

        return input(pS.ENTER_NO_OF_MAPS_ + sC.COLON + sC.SPACE)

    def get_match_score(self, map_count):
        score = input(pS.ENTER_MAP_SCORE_.format(map_count + 1) + sC.COLON + sC.SPACE)
        if re.fullmatch(cF.SCORE_REGEX, score):
            return score
        else:
            self.logger.error(lS.SCORE_FORMAT_MISMATCH.format(score))
            self.logger.info(lS.SCORE_FORMAT)
            return self.get_match_score(map_count)

    def get_match_id(self, matches):
        """
        Ask user for Match Id

        :return: Match Id
        """

        match_id = input(pS.ENTER_MATCH_ID_TO_START_).zfill(2)

        if matches is not None:
            if match_id not in matches:
                print(pS.MATCH_ID_FROM_GIVEN_LIST)
                self.logger.error(lS.INVALID_INPUT.format(match_id))
                self.logger.info(lS.VALID_INPUTS_.format(list(matches.keys())))
                return self.get_match_id(matches)

            self.logger.info(sC.NEW_LINE + pS.MATCH_SELECTED_ + sC.COLON + sC.SPACE + match_id + sC.SPACE +
                             matches[match_id][sC.TERRORIST] + sC.SPACE + sC.VERSUS + sC.SPACE +
                             matches[match_id][sC.COUNTER_TERRORIST])
            self.logger.info(pS.ASSOCIATED_SERVERS___)

        return match_id
