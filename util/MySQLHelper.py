import datetime

import mysql.connector
from mysql.connector import ProgrammingError

from constants import Config as cF, StringConstants as sC, PrintStrings as pS, TeamDetails as tD, \
    PlayerDetails as pD, LogStrings as lS
from util import LogHelper


class MySQLHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        config = config_helper.get_config()
        self.MY_SQL_DATABASE_ = config[sC.MY_SQL][sC.DATABASE]
        self.MY_SQL_HOSTNAME_ = config[sC.MY_SQL][sC.HOSTNAME]
        self.MY_SQL_PASSWORD_ = config[sC.MY_SQL][sC.PASS_WORD]
        self.MY_SQL_USERNAME_ = config[sC.MY_SQL][sC.USER_NAME]
        self.MAX_PLAYERS_ = config[sC.PROJECT_DETAILS][sC.MAX_PLAYERS]

    def get_connection(self):
        """
        Get MySQL DB connection

        :return: Connection variable for MySQL
        """
        cnx = None
        try:
            cnx = mysql.connector.connect(user=self.MY_SQL_USERNAME_,
                                          password=self.MY_SQL_PASSWORD_,
                                          host=self.MY_SQL_HOSTNAME_,
                                          database=self.MY_SQL_DATABASE_)
        except ProgrammingError:
            self.logger.error(lS.CONNECTION_ERROR)
            exit(-1)
        return cnx

    def execute_query(self, cursor, query):
        try:
            cursor.execute(query)
        except ProgrammingError:
            self.logger.error(lS.QUERY_FAILED_.format(query))

    def initial_setup(self):
        create_db_query = sC.CREATE_DATABASE.format(self.MY_SQL_DATABASE_)
        self.create_database(create_db_query)
        create_table_matches = sC.TABLE_MATCHES.format(sC.MATCHES)
        self.create_table(create_table_matches)
        create_table_teams = sC.TABLE_TEAMS.format(sC.TEAMS)
        for i in range(1, int(self.MAX_PLAYERS_)):
            create_table_teams += sC.TABLE_TEAMS_PL1.format(i)
        create_table_teams += sC.TABLE_TEAMS_PL2.format(self.MAX_PLAYERS_)
        self.create_table(create_table_teams)

    def create_table(self, create_table_matches):
        cnx = self.get_connection()
        cursor = cnx.cursor()
        self.execute_query(cursor, create_table_matches)
        cnx.commit()
        cursor.close()
        self.close_connection(cnx)

    def create_database(self, create_db_query):
        cnx = None
        try:
            cnx = mysql.connector.connect(user=self.MY_SQL_USERNAME_,
                                          password=self.MY_SQL_PASSWORD_,
                                          host=self.MY_SQL_HOSTNAME_)
        except ProgrammingError:
            self.logger.error(lS.CONNECTION_ERROR)
            exit(-1)
        cursor = cnx.cursor()
        self.execute_query(cursor, create_db_query)
        cnx.commit()
        cursor.close()
        self.close_connection(cnx)

    def create_db_query(self, cnx, ip, match_id, team1, team2, team_tag2, team_tag1, team1_id, team2_id):
        """
        Create a query to add match data to MySQL DB

        :param cnx: Connection variable for MySQL
        :param match_id: Id of the match
        :param team1: Name of team 1
        :param team2: Name of team 2
        :param team_tag1: Tag of team 1
        :param team_tag2: Tag of team 2
        :param ip: Ip of the server on which match will be player
        :param team1_id: Email of team 1 captain
        :param team2_id: Email of team 2 captain
        :return: SQL query as a string
        """

        cursor_select = cnx.cursor()
        query_select = sC.SELECT_MATCHES_WHERE_IP_.format(ip)
        self.execute_query(cursor_select, query_select)

        for result in cursor_select:

            if result:
                print(pS.MATCH_ALREADY_SET_FOR_.format(ip, result[0], result[1], result[cF.PADDING]))
                remove_previous = input(pS.REMOVE_THE_PREVIOUS_MATCH_Y_N_)

                if remove_previous == sC.N:
                    print(sC.DISCARDED)
                    exit(0)
                else:
                    cursor_update = cnx.cursor()
                    update_query = sC.UPDATE_DONE_WHERE_MATCHES_ID_.format(ip, result[0])
                    print(update_query)
                    self.execute_query(cursor_update, update_query)
                    cnx.commit()
                    cursor_update.close()

        cursor_select.close()

        query_insert = sC.INSERT_MATCHES_VALUES_.format(int(match_id),
                                                        team1[:cF.MAX_CHARACTERS_SQL],
                                                        team2[:cF.MAX_CHARACTERS_SQL],
                                                        team_tag1[:cF.MAX_CHARACTERS_SQL],
                                                        team_tag2[:cF.MAX_CHARACTERS_SQL],
                                                        ip,
                                                        team1_id,
                                                        team2_id,
                                                        datetime.datetime.now())

        return query_insert

    def add_match(self, match_id, team1, team2, team_tag1, team_tag2, ip, team1_id, team2_id):
        """
        Add a new match to MySQL DB

        :param match_id: Id of the match
        :param team1: Name of team 1
        :param team2: Name of team 2
        :param team_tag1: Tag of team 1
        :param team_tag2: Tag of team 2
        :param ip: Ip of the server on which match will be player
        :param team1_id: Email of team 1 captain
        :param team2_id: Email of team 2 captain
        """
        self.logger.info(lS.MY_SQL_CONNECTION)
        cnx = self.get_connection()

        query = self.create_db_query(cnx, ip, match_id, team1, team2, team_tag2, team_tag1, team1_id, team2_id)
        self.logger.info(lS.EXECUTING_QUERY_.format(query))
        cursor = cnx.cursor()
        self.logger.info(lS.SET_WITH_MATCH_ID_.format(match_id))

        try:
            cursor.execute(query)
        except mysql.connector.errors.IntegrityError:
            self.logger.info(lS.MATCH_WITH_ID_EXISTS.format(match_id))
            print(sC.SPACE + sC.STAR + pS.MATCH_ID_ALREADY_EXISTS.format(match_id))
            cursor.close()
            delete = input(pS.PREVIOUS_MATCH_Y_N_)
            if delete == sC.Y:
                self.logger.info(lS.DELETING_OLD_MATCH_DATA)
                cursor = cnx.cursor()
                delete_query = sC.DELETE_FROM_MATCHES_WHERE_ID_.format(match_id)
                self.execute_query(cursor, delete_query)
                cnx.commit()
                cursor.close()
                cursor = cnx.cursor()
                self.execute_query(cursor, query)
                self.logger.info(lS.ADDED_SUCCESSFULLY)
            self.logger.info(lS.MATCH_DATA_DISCARDED)

        cnx.commit()
        cursor.close()
        self.close_connection(cnx)

    def add_steam_ids_to_db(self, local_data_helper):
        """
        Add players in teams to MySQL DB

        :param local_data_helper: local_data_helper Object
        """
        # MySQL
        self.logger.info(lS.MY_SQL_CONNECTION)
        cnx = self.get_connection()

        self.logger.info(lS.PREVIOUS_PLAYER_DATA)
        cursor = cnx.cursor()
        query = sC.TRUNCATE_TABLE_.format(sC.TEAMS)
        self.logger.info(lS.EXECUTING_QUERY_.format(query))
        self.execute_query(cursor, query)
        cnx.commit()
        cursor.close()
        self.logger.info(lS.CURRENT_PLAYER_DATA)

        for team in tD.TeamList:
            self.logger.info(lS.TEAM_ID_PLAYERS_
                             .format(team, len(pD.PlayerList[tD.TeamList[team][sC.TEAM_NAME_OG]])))

            query = sC.INSERT_INTO_TEAMS_VALUES_.format(team)
            for i in range(1, int(self.MAX_PLAYERS_) + 1):
                query += sC.INSERT_VALUE_.format(local_data_helper.get_steam_id(i, tD.TeamList[team][sC.TEAM_NAME_OG]))
            query = query[:-2] + sC.CLOSE_CIRCULAR_BRACE_

            cursor = cnx.cursor()
            self.logger.info(lS.EXECUTING_QUERY_.format(query))
            self.execute_query(cursor, query)
            cnx.commit()
            cursor.close()

        self.logger.info(lS.SQL_CONNECTION)
        self.close_connection(cnx)

    def end_match(self, match_id, matches):
        """
        Set match as ended in MySQL DB

        """
        self.logger.info(lS.MY_SQL_CONNECTION)
        cnx = self.get_connection()
        cursor = cnx.cursor()
        c_query = sC.UPDATE_DONE_WHERE_MATCHES_ID_.format(matches[match_id][sC.IP], int(match_id))
        self.logger.info(lS.EXECUTING_QUERY_.format(c_query))
        self.execute_query(cursor, c_query)
        cnx.commit()
        self.logger.info(lS.QUERY_RAN_SUCCESSFULLY)
        cursor.close()
        self.close_connection(cnx)

    @staticmethod
    def close_connection(cnx):
        """
        Close the DB connection

        :param cnx: Connection instance
        """

        cnx.close()
