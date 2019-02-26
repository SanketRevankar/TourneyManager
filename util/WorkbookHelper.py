import re

from constants import StringConstants as sC, PrintStrings as pS, Config as cF, \
    PlayerDetails as pD, LogStrings as lS
from util.LogHelper import LogHelper


class WorkbookHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        config = config_helper.get_config()
        self.STATS_FILE_ = config[sC.FILE_LOCATIONS][sC.STATS_FILE]
        self.FILES_HOME_ = config[sC.FOLDER_LOCATIONS][sC.FILES_HOME]

    @staticmethod
    def workbook_write_stat(cell_format, index, nick, steam, team, worksheet, stats):
        """
        Write given stat to workbook

        :param cell_format: Cell formatting to be used for this cell
        :param index: Row index to write in cell
        :param nick: Nick of the player
        :param steam: Steam id of the player
        :param team: Team which the player belongs to
        :param worksheet: Worksheet variable to write stat
        :param stats: Dict containing all stats
        """

        worksheet.write(sC.C + str(index), nick, cell_format)
        worksheet.write(sC.D + str(index), stats[team][steam][sC.MATCHES], cell_format)
        worksheet.write(sC.E + str(index), stats[team][steam][sC.KILLS], cell_format)
        worksheet.write(sC.F + str(index), stats[team][steam][sC.DEATHS], cell_format)
        worksheet.write(sC.G + str(index), stats[team][steam][sC.HEADSHOT], cell_format)
        worksheet.write(sC.H + str(index), stats[team][steam][sC.KNIFE], cell_format)
        worksheet.write(sC.I_ + str(index), stats[team][steam][sC.GRENADE], cell_format)
        worksheet.write(sC.J + str(index), stats[team][steam][sC.SUICIDE], cell_format)
        worksheet.write(sC.K + str(index), stats[team][steam][sC.BOMB_PLANT], cell_format)
        cell_format.set_right(2)
        worksheet.write(sC.L + str(index), stats[team][steam][sC.BOMB_DEFUSE], cell_format)

    @staticmethod
    def write_footer(cell_format, no_of_rows, worksheet):
        """
        Write footer to worksheet

        :param cell_format: Cell formatting to be used for this cell
        :param no_of_rows: Number of rows
        :param worksheet: Worksheet variable to write stat
        """

        worksheet.write(sC.B + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.C + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.D + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.E + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.F + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.G + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.H + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.I_ + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.J + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.K + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)
        worksheet.write(sC.L + str(no_of_rows + 3), sC.EMPTY_STRING, cell_format)

    @staticmethod
    def write_header(cell_format, worksheet):
        """
        Write header to worksheet

        :param cell_format: Cell formatting to be used for this cell
        :param worksheet: Worksheet variable to write stat
        """

        worksheet.write(sC.B + sC.TWO, sC.NAME_, cell_format)
        worksheet.write(sC.C + sC.TWO, sC.NICK_, cell_format)
        worksheet.write(sC.D + sC.TWO, pS.P_MATCHES, cell_format)
        worksheet.write(sC.E + sC.TWO, pS.P_KILLS, cell_format)
        worksheet.write(sC.F + sC.TWO, pS.P_DEATHS, cell_format)
        worksheet.write(sC.G + sC.TWO, pS.HS, cell_format)
        worksheet.write(sC.H + sC.TWO, pS.KNIFES, cell_format)
        worksheet.write(sC.I_ + sC.TWO, pS.P_GRENADE, cell_format)
        worksheet.write(sC.J + sC.TWO, pS.P_SUICIDE, cell_format)
        worksheet.write(sC.K + sC.TWO, pS.PLANTS, cell_format)
        worksheet.write(sC.L + sC.TWO, pS.DEFUSES, cell_format)

    @staticmethod
    def format_workbook(workbook):
        """
        Create the cell format for the workbook

        :param workbook: Workbook variable
        :return: Cell formatting to be used for this cell
        """

        cell_format = workbook.add_format()
        cell_format.set_font_color(cF.FONT_COLOR)
        cell_format.set_pattern(1)
        cell_format.set_bg_color(cF.BG_COLOR)
        cell_format.set_text_wrap()
        cell_format.set_align(cF.ALIGNMENT)
        cell_format.set_align(cF.VJUSTIFY)
        cell_format.set_bold()
        cell_format.set_border(cF.PADDING)
        return cell_format

    @staticmethod
    def workbook_blank_line(worksheet):
        """
        Add blank line to worksheet

        :param worksheet: Worksheet variable to write stat
        """

        worksheet.write(sC.B + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.C + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.D + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.E + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.F + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.G + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.H + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.I_ + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.J + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.K + sC.ONE, sC.EMPTY_STRING)
        worksheet.write(sC.L + sC.ONE, sC.EMPTY_STRING)

    def add_max_stat(self, index, steam, team, worksheet, workbook, stats, print_helper):
        """
        Add max stat to the provided worksheet

        :param print_helper: PrintHelper Object
        :param index: Row index to write in cell
        :param steam: Steam id of the player
        :param team: Team which the player belongs to
        :param worksheet: Worksheet variable to write stat
        :param workbook: Workbook variable
        :param stats: Dict containing all stats
        """

        cell_format_c = workbook.add_format()
        cell_format_c.set_left(2)
        cell_format_c.set_bg_color(cF.BORDER_BG_COLOR if index % 2 == 0 else cF.CELL_BG_COLOR)
        worksheet.write(sC.B + str(index), stats[team][steam][sC.NAME_SMALL], cell_format_c)
        nick_c = stats[team][steam][sC.NICK_SMALL]
        if nick_c[0] == sC.EQUALS:
            nick_c = sC.DOT + nick_c
        self.workbook_write_stat(cell_format_c, index, nick_c, steam, team, worksheet, stats)
        print_helper.print_stat(steam, stats, team)

    def get_max(self, stat_current, ids, team, index, worksheet, stats, workbook, local_data_helper, print_helper):
        """
        Get max stat from the ids not in list and save top in worksheet

        :param print_helper: PrintHelper Object
        :param local_data_helper: LocalDataHelper Object
        :param workbook: Workbook variable to write into
        :param stats: stats variable containing stats of every player
        :param stat_current: Current Stat
        :param ids: IDs already in worksheet
        :param team: Name of the team
        :param index: Column number
        :param worksheet: Worksheet object
        """

        max_stat = {
            stat_current: -1,
            sC.KILLS: -1,
        }

        for steam__id in stats[team]:
            if steam__id not in ids:
                if stats[team][steam__id][stat_current] > max_stat[stat_current]:
                    max_stat[stat_current] = stats[team][steam__id][stat_current]
                    max_stat[sC.KILLS] = stats[team][steam__id][sC.KILLS]
                    max_stat[sC.S_STEAM_ID] = steam__id

                if stats[team][steam__id][stat_current] >= max_stat[stat_current]:
                    if stats[team][steam__id][sC.KILLS] > max_stat[sC.KILLS]:
                        max_stat[stat_current] = stats[team][steam__id][stat_current]
                        max_stat[sC.KILLS] = stats[team][steam__id][sC.KILLS]
                        max_stat[sC.S_STEAM_ID] = steam__id

        try:
            _ = local_data_helper.get_details_by_id(max_stat[sC.S_STEAM_ID])
            steam = max_stat[sC.S_STEAM_ID]
        except KeyError:
            return

        self.add_max_stat(index, steam, team, worksheet, workbook, stats, print_helper)

        return steam

    def write_stats(self, stats, workbook, print_helper, local_data_helper):
        """
        Write stats to workbook

        :param local_data_helper: LocalDataHelper Object
        :param print_helper: PrintHelper Object
        :param workbook: Workbook variable
        :param stats: Dict containing all stats
        """

        for team in stats:
            self.logger.info(lS.WRITING_DATA_FOR_TEAM_.format(team))
            team_name = re.sub(cF.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING, team)[:31]
            worksheet = workbook.add_worksheet(team_name)
            worksheet.set_column(sC.B_C, cF.WIDTH_NAME_NICK)
            worksheet.set_column(sC.D_M, cF.WIDTH_STATS)

            self.workbook_blank_line(worksheet)

            cell_format = self.format_workbook(workbook)

            self.write_header(cell_format, worksheet)

            print(sC.NEW_LINE + sC.STAR, team)
            print(pS.STATS_PRINT_COVER_)
            print(pS.STATS_HEADER_)
            print(pS.STATS_PRINT_COVER_)

            c_stat = []
            end = 0

            for i in range(pD.PlayerList[team].__len__()):
                try:
                    steam_id = self.get_max(sC.MATCHES, c_stat, team, i + 3, worksheet, stats, workbook,
                                            local_data_helper, print_helper)
                    end = i
                except TypeError:
                    continue

                c_stat.append(steam_id)

            print(pS.STATS_PRINT_COVER_)

            cell_format = workbook.add_format()
            cell_format.set_top(2)

            self.write_footer(cell_format, end, worksheet)

        print(pS.FILE_SAVED_, self.FILES_HOME_ + sC.SEPARATOR +
              self.STATS_FILE_)
