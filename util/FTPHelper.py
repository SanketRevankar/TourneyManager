import datetime
import os
import win32file
from ftplib import FTP

import pywintypes
import win32con

from constants import StringConstants as sC, PrintStrings as pS, Config as cF, MatchServers as mS, \
    LogStrings as lS
from util.LogHelper import LogHelper


class FTPHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.logger = log_helper.get_logger(self.__class__.__name__)
        config = config_helper.get_config()
        self.locations_hltv_starting_ = config[sC.FOLDER_LOCATIONS][sC.HLTV_STARTING]
        self.results_ = config[sC.FOLDER_LOCATIONS][sC.CONFIGS_RESULTS]
        self.score_starting_ = config[sC.FOLDER_LOCATIONS][sC.SCORE_STARTING]
        self.amxmodx_logs_ = config[sC.FOLDER_LOCATIONS][sC.ADDONS_AMXMODX_LOGS]
        self.logs_starting_ = config[sC.FOLDER_LOCATIONS][sC.LOGS_STARTING]
        self.cstrike_logs_ = config[sC.FOLDER_LOCATIONS][sC.CSTRIKE_LOGS]

        _old_makepasv = FTP.makepasv

        def _new_makepasv(self_):
            """
            To use passive mode for FTP

            :param self_: current reference
            :return: host and port
            """
            host, port = _old_makepasv(self_)
            host = self_.sock.getpeername()[0]
            print(host, port)
            return host, port

        FTP.makepasv = _new_makepasv

    def download(self, ftp, src, des, time):
        """
        Download file from FTP to local

        :param ftp: FTP connection var
        :param src: Source path - Cloud
        :param des: Destination path - local
        :param time: Time of modification
        """

        f = open(des, sC.WB_MODE)
        ftp.retrbinary(sC.RETR_ + src, f.write)
        f.close()
        self.logger.info(sC.STAR + sC.SPACE + pS.ADDED_ + sC.COLON + sC.SPACE + des)
        win_file = win32file.CreateFile(
            des, win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None, win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL, None)
        # noinspection PyUnresolvedReferences
        win_time = pywintypes.Time(time)
        win32file.SetFileTime(win_file, win_time, None, None)
        win32file.CloseHandle(win_file)
        os.utime(des, (time, time))

    def get_hltv_demos_from_ftp(self, date, node, server_id, folder, cloud_server_helper):
        """
        Download Match HLTV demos from instance

        :param date: date for which the demos will be downloaded
        :param node: Instance from which the Demos should be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        :param cloud_server_helper: CloudServerHelper Object
        """
        ftp = FTP()
        ftp.connect(cloud_server_helper.ip(node), 21)
        ftp.login(mS.ServerList[server_id][sC.HLTV_USERNAME], mS.ServerList[server_id][sC.HLTV_PASSWORD])
        ftp.set_pasv(False)
        print(sC.STAR + pS.DOWNLOADING_HLTV_DEMOS)
        for file in ftp.mlsd(sC.CSTRIKE):
            if file[1][sC.TYPE] == sC.DIR or sC.DEMO_FORMAT not in file[0]:
                continue
            date_file = datetime.datetime.strptime(file[1][sC.MODIFY], cF.DATETIME_FORMAT)

            if date_file.date() >= date:
                source = sC.CSTRIKE + sC.SEPARATOR + file[0]
                destination = self.locations_hltv_starting_ + folder + sC.SEPARATOR + file[0]
                self.download(ftp, source, destination, date_file.timestamp())
        ftp.close()

    def get_logs_from_ftp(self, date, node, server_id, folder, cloud_server_helper):
        """
        Get log data from instance

        :param date: date for which the logs will be downloaded
        :param node: Instance from which the logs should be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        :param cloud_server_helper: CloudServerHelper Object
        """

        self.logger.info(lS.FTP_CONNECTION)
        ftp = FTP()

        ip = cloud_server_helper.ip(node)
        self.logger.info(lS.CONNECTING_TO_.format(ip))
        ftp.connect(ip, 21)

        self.logger.info(lS.USERNAME_AND_PASSWORD_.format(
            mS.ServerList[server_id][sC.USERNAME], mS.ServerList[server_id][sC.PASSWORD]))
        ftp.login(mS.ServerList[server_id][sC.USERNAME], mS.ServerList[server_id][sC.PASSWORD])

        self.logger.info(lS.PASSIVE_MODE_FOR_FTP)
        ftp.set_pasv(False)

        self.logger.info(lS.FOR_FTP_TRANSFER_)
        folders = [
            [self.results_, self.score_starting_ + folder],
            [self.amxmodx_logs_, self.logs_starting_ + folder],
            [self.cstrike_logs_, self.logs_starting_ + folder],
        ]

        self.logger.info(lS.DOWNLOADING_DATA)
        for c_folder in folders:
            self.logger.info(lS.CURRENT_FOLDER_.format(c_folder))
            for file in ftp.mlsd(c_folder[0]):
                if file[1][sC.TYPE] == sC.DIR or (sC.LOG not in file[0] and sC.TXT not in file[0]):
                    continue
                date_file = datetime.datetime.strptime(file[1][sC.MODIFY], cF.DATETIME_FORMAT)

                if date_file.date() >= date:
                    source = c_folder[0] + sC.SEPARATOR + file[0]
                    destination = c_folder[1] + sC.SEPARATOR + file[0]
                    self.download(ftp, source, destination, date_file.timestamp())
        ftp.close()
