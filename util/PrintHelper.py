from constants import StringConstants as sC, PrintStrings as pS, Config as cF, MatchServers as mS, \
    TeamDetails as tD


class PrintHelper:
    @staticmethod
    def print_server_list():
        """
        Print the list of servers available

        """

        for server in mS.ServerList:
            print(pS.PRINT_SERVER_DETAILS_.format(server, mS.ServerList[server][sC.SERVER_NAME],
                                                  mS.ServerList[server][sC.SERVER_IP]))

    @staticmethod
    def print_team_list():
        """
        Print list of teams registered

        """

        if tD.TeamList.__len__() == 0:
            print(pS.NO_TEAMS_FOUND)
            exit(1)
        for team in tD.TeamList:
            print(pS.PRINT_TEAM_DETAILS_.format(team.zfill(cF.PADDING), tD.TeamList[team][sC.TEAM_NAME_]))

    @staticmethod
    def print_match_info(match_id, team1, team2, team_tag1, team_tag2, ip, name_t1, nick_t1, name_ct1, nick_ct1,
                         server_id):
        """
        Print match information

        :param match_id: Id of the match
        :param team1: Name of team 1
        :param team2: Name of team 2
        :param team_tag1: Tag of team 1
        :param team_tag2: Tag of team 2
        :param ip: Ip of the server on which match will be player
        :param name_t1: Name of the captain of team 1
        :param nick_t1: Nick of the captain of team 1
        :param name_ct1: Name of the captain of team 2
        :param nick_ct1: Nick of the captain of team 2
        :param server_id: Id of the server
        """

        print(sC.NEW_LINE + pS.MATCH_SET_ + sC.COLON +
              sC.NEW_LINE + pS.COVER +
              sC.NEW_LINE + pS.MATCH_ID_.format(match_id) +
              sC.NEW_LINE + pS.TEAM_T_.format(team1, team_tag1) +
              sC.NEW_LINE + pS.T_CAPTAIN_.format(name_t1, nick_t1) +
              sC.NEW_LINE + pS.TEAM_CT_.format(team2, team_tag2) +
              sC.NEW_LINE + pS.CT_CAPTAIN_.format(name_ct1, nick_ct1) +
              sC.NEW_LINE + pS.SERVER_IP_.format(ip) +
              sC.NEW_LINE + pS.SERVER_NAME_.format(mS.ServerList[server_id][sC.SERVER_NAME]) +
              sC.NEW_LINE + pS.HLTV_IP_.format(mS.ServerList[server_id][sC.HLTV_IP]) +
              sC.NEW_LINE + pS.INSTANCE_NAME_.format(mS.ServerList[server_id][sC.INSTANCE_NAME]) +
              sC.NEW_LINE + pS.FOLDER_MATCH_VS_.format(match_id, team1, team2) +
              sC.NEW_LINE + pS.YOU_TUBE_MATCH_VS_.format(match_id, team1.replace(sC.UNDERSCORE, sC.SPACE),
                                                         team2.replace(sC.UNDERSCORE, sC.SPACE)) +
              sC.NEW_LINE + pS.COVER)

    @staticmethod
    def show_update(match_id_, task):
        """
        Shows current update to Match scores

        :param match_id_: Id of the match
        :param task: Updated entity to confirm
        :return: Nothing
        """

        print()
        print(pS.MATCH_ + sC.COLON, match_id_)
        print(sC.TAB, task[sC.TEAM_1_], sC.VERSUS, task[sC.TEAM_2_])

        win = 0
        for m in range(0, 5):
            try:
                score = task[pS.MAP__SCORE.format(m + 1)]
                print(sC.TAB + sC.TAB + sC.STAR, task[pS.MAP_.format(m + 1)].ljust(10), score.rjust(2))
                score_split = score.split(sC.DASH)

                if int(score_split[0].strip()) < int(score_split[1].strip()):
                    win += 1
                else:
                    win -= 1
            except KeyError:
                break

        if win > 0:
            print(sC.TAB + pS.WINNER_ + sC.COLON, task[sC.TEAM_2_])
        else:
            print(sC.TAB + pS.WINNER_ + sC.COLON, task[sC.TEAM_1_])

        return ''

    @staticmethod
    def print_stat(steam, stats, team):
        """
        Print stat of the given player

        :param steam: Steam ID of the player
        :param stats: Dict of stats of all players
        :param team: Team of the player
        """

        print(sC.PIPE, steam.ljust(20), sC.PIPE,
              str(stats[team][steam][sC.MATCHES]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.KILLS]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.DEATHS]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.GRENADE]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.HEADSHOT]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.SUICIDE]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.BOMB_PLANT]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.BOMB_DEFUSE]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.KNIFE]).center(cF.MED_PADDING), sC.PIPE,
              str(stats[team][steam][sC.NAME_SMALL]).ljust(cF.NAME_PADDING), sC.PIPE,
              str(stats[team][steam][sC.NICK_SMALL]).ljust(cF.NICK_PADDING), sC.PIPE)

    @staticmethod
    def print_top_stats(count_matches, stats, local_data_helper):
        """
        Print top performers in every stats

        :param local_data_helper: LocalDataHelper Object
        :param count_matches: Number of matches played by the player
        :param stats: Dict of stats of all players
        """

        start_shift = sC.NEW_LINE + sC.TAB + sC.TAB + sC.TAB + sC.TAB + sC.TAB + sC.TAB + sC.TAB + sC.TAB + sC.TAB
        print(start_shift + pS.MAX_KILLS_.ljust(19))
        local_data_helper.get_top_n(sC.KILLS, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_DEATHS_.ljust(19))
        local_data_helper.get_top_n(sC.DEATHS, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_HEADSHOT_.ljust(19))
        local_data_helper.get_top_n(sC.HEADSHOT, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_GRENADE_KILLS_.ljust(19))
        local_data_helper.get_top_n(sC.GRENADE, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_KNIFE_.ljust(19))
        local_data_helper.get_top_n(sC.KNIFE, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_SUICIDES_.ljust(19))
        local_data_helper.get_top_n(sC.SUICIDE, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_BOMB_PLANTS_.ljust(19))
        local_data_helper.get_top_n(sC.BOMB_PLANT, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)
        print(start_shift + pS.MAX_BOMB_DEFUSE_.ljust(19))
        local_data_helper.get_top_n(sC.BOMB_DEFUSE, cF.NUMBER_OF_TOP_PLAYERS, stats, count_matches)

    @staticmethod
    def print_winner(match_id, scores, win):
        """
        Print winner of the match

        :param match_id: Id of the match
        :param scores: Dict of all scores
        :param win: Difference of maps won by team 1 and team 2
        """

        if win > 0:
            print(sC.TAB + pS.WINNER_ + sC.COLON, scores[match_id][sC.TEAM_2_])
        elif win < 0:
            print(sC.TAB + pS.WINNER_ + sC.COLON, scores[match_id][sC.TEAM_1_])
        else:
            print(sC.TAB, pS.NO_SCORE_FOUND)
