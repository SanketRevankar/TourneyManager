import re

from PIL import Image, ImageDraw, ImageFont

from constants import StringConstants as sC, Config as cF, PlayerDetails as pD, LogStrings
from util.LogHelper import LogHelper


class CertificateHelper:
    def __init__(self, config_helper, log_helper: LogHelper):
        self.log_helper = log_helper
        self.logger = log_helper.get_logger(self.__class__.__name__)
        self.config = config_helper.get_config()
        self.files_home_ = self.config[sC.FOLDER_LOCATIONS][sC.FILES_HOME]
        self.locations_certificates_ = self.config[sC.FOLDER_LOCATIONS][sC.CERTIFICATES]
        self.cert_img_path_ = self.config[sC.FILE_LOCATIONS][sC.CERT_IMG_PATH]
        self.locations_font_path_ = self.config[sC.FILE_LOCATIONS][sC.FONT_PATH]

    def print_name(self, c_name, team):
        """
        Prints the name on the certificate using position defined in Config file

        :param team: Team of the player
        :param c_name: Name of the player
        """

        image = Image.open(self.cert_img_path_)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.locations_font_path_, size=cF.FONT_SIZE)

        (x, y) = (cF.START_IF_LONG_NAME, cF.END_POS_CERT_NAME) if c_name.__len__() > cF.LONG_NAME_LEN else \
            (cF.START_IF_SHORT_NAME, cF.END_POS_CERT_NAME)
        message = c_name.center(cF.WIDTH_CERT_NAME)
        color = cF.CERT_TEXT_FONT_COLOR

        draw.text((x, y), message, fill=color, font=font, align=cF.ALIGNMENT)
        image.save(self.files_home_ + sC.SEPARATOR + self.locations_certificates_ + sC.SEPARATOR +
                   re.sub(cF.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING, team)[:cF.MAX_CHARACTERS_SQL] +
                   sC.SEPARATOR + c_name + sC.JPG)

    def create_certificates(self, local_data_helper):
        """
        Create participation certificates for all players in tournament

        :param local_data_helper: LocalDataHelper Object
        """

        self.logger.info(LogStrings.STORE_CERTIFICATES)
        local_data_helper.create_directory(self.files_home_ + sC.SEPARATOR + self.locations_certificates_)

        for team in pD.PlayerList:
            self.logger.info(LogStrings.CERTIFICATES_FOR_.format(team))
            local_data_helper.create_directory(
                self.files_home_ + sC.SEPARATOR + self.locations_certificates_ + sC.SEPARATOR +
                re.sub(cF.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING, team)[:cF.MAX_CHARACTERS_SQL]
            )

            for player in pD.PlayerList[team]:
                name = str(pD.PlayerList[team][player][sC.NAME_])
                self.print_name(name, team)

        self.logger.info(LogStrings.CERTIFICATES_CREATED)
