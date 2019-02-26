import datetime
from datetime import datetime

from google.cloud import datastore

from constants import StringConstants as sC, PrintStrings as pS, Config as cF, LogStrings as lS
from util.LogHelper import LogHelper


class DataStoreHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        config = config_helper.get_config()
        self.project_id_ = config[sC.PROJECT_DETAILS][sC.PROJECT_ID]
        self.client = datastore.Client.from_service_account_json(
            config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_KEY_PATH])

    def z_add_to_data_store(self, task_key, team1, team2, team_tag1, team_tag2, ip, team1_email, team2_email):
        """
        Add match data to DataStore

        :param task_key: Key of the entity to which the data will be stored
        :param team1: Name of team 1
        :param team2: Name of team 2
        :param team_tag1: Tag of team 1
        :param team_tag2: Tag of team 2
        :param ip: Ip of the server on which match will be player
        :param team1_email: Email of team 1 captain
        :param team2_email: Email of team 2 captain
        """

        task = datastore.Entity(key=task_key)
        task[sC.TEAM_1_] = team1
        task[sC.TEAM_2_] = team2
        task[sC.TEAM_TAG_1_] = team_tag1
        task[sC.TEAM_TAG_2_] = team_tag2
        task[sC.IP] = ip
        task[sC.TEAM_1_ID] = team1_email
        task[sC.TEAM_2_ID] = team2_email
        task[sC.STATUS] = sC.CREATED
        self.client.put(task)

    def fetch_scores(self, local_data_helper):
        """
        Fetch scores from Datastore

        :return: Dict of scores for all matches
        :param local_data_helper: LocalDataHelper Object
        """

        scores = {}
        # noinspection PyTypeChecker
        query = self.client.query(kind=sC.MATCH)
        query.add_filter(sC.STATUS, sC.EQUALS, sC.COMPLETED)
        self.logger.info(lS.COMPLETED_MATCHES)

        for match in query.fetch():
            scores[int(match.key.name)] = {
                sC.TEAM_1_: local_data_helper.get_og_team_name(match[sC.TEAM_1_]),
                sC.TEAM_2_: local_data_helper.get_og_team_name(match[sC.TEAM_2_]),
            }

            self.logger.info(lS.SCORES_FOR_MATCH_.format(match))
            for i in range(0, 5):
                try:
                    scores[int(match.key.name)][pS.MAP_.format(i + 1)] = match[pS.MAP_.format(i + 1)]
                    scores[int(match.key.name)][pS.MAP__SCORE.format(i + 1)] = match[pS.MAP__SCORE.format(i + 1)]
                except KeyError:
                    break
        return scores

    def add_match(self, match_id, team1, team2, team_tag1, team_tag2, ip, team1_email, team2_email):
        """
        Add a new match to datastore

        :param match_id: Id of the match
        :param team1: Name of team 1
        :param team2: Name of team 2
        :param team_tag1: Tag of team 1
        :param team_tag2: Tag of team 2
        :param ip: Ip of the server on which match will be player
        :param team1_email: Email of team 1 captain
        :param team2_email: Email of team 2 captain
        """

        # noinspection PyTypeChecker
        task_key = datastore.key.Key(sC.MATCH, match_id, project=self.project_id_)
        self.logger.info(lS.SET_WITH_MATCH_ID_.format(match_id))
        if self.client.get(key=task_key) is None:
            self.logger.info(lS.MATCH_IN_DATASTORE)
            self.z_add_to_data_store(task_key, team1, team2, team_tag1, team_tag2, ip, team1_email, team2_email)
            self.logger.info(lS.MATCH_ADDED_IN_DS)
        else:
            self.logger.info(lS.MATCH_WITH_ID_EXISTS.format(match_id))
            print(sC.SPACE + sC.STAR + pS.MATCH_ID_ALREADY_EXISTS.format(match_id))

            if input(pS.PREVIOUS_MATCH_Y_N_) == sC.Y:
                self.logger.info(lS.DELETING_OLD_MATCH_DATA)
                self.client.delete(task_key)
                self.z_add_to_data_store(task_key, team1, team2, team_tag1, team_tag2, ip, team1_email, team2_email)
                self.logger.info(lS.MATCH_ADDED_IN_DS)
            self.logger.info(lS.MATCH_DATA_DISCARDED)

    def get_matches(self):
        """
        Get all matches from datastore

        :return: Dict of all matches
        """
        matches = {}

        # noinspection PyTypeChecker
        query = self.client.query(kind=sC.MATCH)
        query.add_filter(sC.STATUS, sC.EQUALS, sC.ACTIVE)
        for entity in query.fetch():
            matches[entity.key.name] = {
                sC.TERRORIST: str(entity[sC.TEAM_1_]),
                sC.COUNTER_TERRORIST: str(entity[sC.TEAM_2_]), sC.IP: entity[sC.IP],
            }
            print(entity.key.name + sC.DOT + sC.SPACE + entity[sC.TEAM_1_], sC.VERSUS, entity[sC.TEAM_2_])

        return matches

    def confirm_start_date(self, match_id):
        """
        Reconfirm the match date from the user.

        :param match_id: Id of the match
        :return: Final date to consider
        """

        # noinspection PyTypeChecker
        task_key = datastore.key.Key(sC.MATCH, match_id, project=self.project_id_)
        task = self.client.get(key=task_key)
        self.logger.info(lS.DATE_FROM_DATASTORE)
        date = task[sC.START_TIME].date()
        self.logger.info(lS.DATE_SET_TO_.format(date))
        if sC.Y == input(pS.DATE_SET_TO_ + sC.COLON + sC.SPACE + str(date) + sC.NEW_LINE + pS.CHANGE_DATE_Y_N_ +
                         sC.COLON + sC.SPACE):
            date = datetime.datetime.strptime(input(pS.ENTER_DATE_DD_MM_YYYY_), sC.D_M_Y).date()
            self.logger.info(lS.DATE_CHANGED_TO_.format(date))
        return date

    def add_match_scores(self, match_id_, matches, user_input_helper, print_helper):
        """
        Add scores to DataStore

        :param print_helper: PrintHelper Object
        :param user_input_helper: UserInputHelper Object
        :param match_id_: Id of the match
        :param matches: Dict containing all matches
        """

        self.logger.info(lS.SCORES_TO_DATASTORE)
        n_maps = user_input_helper.get_no_of_maps()
        print(pS.SCORE_OF_.format(matches[match_id_][sC.TERRORIST], matches[match_id_][sC.COUNTER_TERRORIST]))

        # noinspection PyTypeChecker
        task_key = datastore.key.Key(sC.MATCH, match_id_, project=self.project_id_)
        task = self.client.get(key=task_key)

        self.logger.info(lS.MATCH_SCORES)
        map_count = 0
        while map_count < int(n_maps):
            maps = cF.MAPS

            for k, v in maps.items():
                print(lS.MAPS.format(k, v))
            map_c = input(pS.ENTER_MAP_NAME_.format(map_count + 1) + sC.COLON + sC.SPACE)

            if map_c not in maps:
                self.logger.error(lS.MAP_WITH_ID_NOT_FOUND.format(map_c))
                self.logger.info(lS.ENTER_VALID_IDS_FROM_.format(list(maps.keys())))
                continue

            c_map = maps[map_c]
            print(sC.STAR + sC.SPACE + pS.S_MAP_ + sC.COLON, c_map)
            task[pS.MAP_.format(map_count + 1)] = c_map
            task[pS.MAP__SCORE.format(map_count + 1)] = user_input_helper.get_match_score(map_count)
            map_count += 1

        if sC.Y in input(
                sC.NEW_LINE + pS.CONFIRM_UPDATE_Y_N_ + sC.COLON + sC.SPACE + print_helper.show_update(match_id_, task)):
            self.logger.info(lS.COMPLETED_IN_DATASTORE)
            task[sC.STATUS] = sC.COMPLETED
            self.client.put(task)
            self.logger.info(lS.DATASTORE_SUCCESSFULLY)
        else:
            self.logger.info(lS.DATA_DISCARDED_RETRYING)
            self.add_match_scores(match_id_, matches, user_input_helper, print_helper)

    def save_to_data_store(self, c_stats, c_key_value):
        """
        Upload stats to DataStore

        :param c_stats: Dict containing stats of the player
        :param c_key_value: Key of the player in DataStore
        """

        self.logger.info(lS.STATS_PER_TEAM_TO_LOAD)
        for teams in c_stats:
            for steam_id in c_stats[teams]:
                # noinspection PyTypeChecker
                task_key = datastore.key.Key(c_key_value, steam_id, project=self.project_id_)
                c_entity = self.client.get(task_key)

                if c_entity is None:
                    task = datastore.Entity(key=task_key)
                    task[sC.TEAM] = teams
                    task[sC.NS_NAME] = c_stats[teams][steam_id][sC.NS_NAME]
                    task[sC.NICK_SMALL] = c_stats[teams][steam_id][sC.NICK_SMALL]
                    task[sC.KILLS] = c_stats[teams][steam_id][sC.KILLS]
                    task[sC.DEATHS] = c_stats[teams][steam_id][sC.DEATHS]
                    task[sC.GRENADE] = c_stats[teams][steam_id][sC.GRENADE]
                    task[sC.KNIFE] = c_stats[teams][steam_id][sC.KNIFE]
                    task[sC.HEADSHOT] = c_stats[teams][steam_id][sC.HEADSHOT]
                    task[sC.SUICIDE] = c_stats[teams][steam_id][sC.SUICIDE]
                    task[sC.BOMB_PLANT] = c_stats[teams][steam_id][sC.BOMB_PLANT]
                    task[sC.BOMB_DEFUSE] = c_stats[teams][steam_id][sC.BOMB_DEFUSE]
                    self.client.put(task)
                else:
                    self.logger.info(pS.ALREADY_EXISTS + sC.COLON + sC.SPACE + str(task_key))

    def get_created_matches(self):
        """
        Get all matches from datastore whose current status is set to Created.

        :return: Dict of matches
        """

        self.logger.info(lS.FETCHING_CREATED_MATCHES)
        # noinspection PyTypeChecker
        query = self.client.query(kind=sC.MATCH)
        query.add_filter(sC.STATUS, sC.EQUALS, sC.CREATED)

        matches = {}
        for entity in query.fetch():
            matches[entity.key.name] = {
                sC.TERRORIST: str(entity[sC.TEAM_1_]).replace(sC.UNDERSCORE, sC.SPACE),
                sC.COUNTER_TERRORIST: str(entity[sC.TEAM_2_]).replace(sC.UNDERSCORE, sC.SPACE),
                sC.IP: entity[sC.IP],
            }

            print(entity.key.name + sC.DOT + sC.SPACE + entity[sC.TEAM_1_], sC.VERSUS, entity[sC.TEAM_2_])

        if matches.__len__() == 0:
            print(lS.NO_MATCHES_FOUND_)
            self.logger.error(lS.NO_MATCHES_FOUND_)
            exit(-1)

        return matches

    def start_match(self, match_id):
        """
        Start the match with given Id

        :param match_id: Id of the match to start
        """

        self.logger.info(lS.ACTIVE_IN_DATASTORE)
        # noinspection PyTypeChecker
        task_key = datastore.key.Key(sC.MATCH, match_id, project=self.project_id_)
        task = self.client.get(key=task_key)
        task[sC.STATUS] = sC.ACTIVE
        task[sC.START_TIME] = datetime.now()
        self.client.put(task)
