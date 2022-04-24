"""
Module to import data from atlas into a json.
 Also reducing the amount of requests by caching the previous hash and date
"""
import os
import datetime
import urllib.request
import json
import data_config


class HashError(Exception):
    """
    Exception if the Hash of the request and the cached Hash are equal.
    """


class DateError(Exception):
    """
    Exception if the current date and the cached date are equal
    """


class AtlasFunctions:
    """
    Class to get and verify the data from AtlasAcademy
    """
    def __init__(self,
                 filename="nice_servant.json",
                 url="https://api.atlasacademy.io/export/NA/nice_servant.json",
                 info_url="https://api.atlasacademy.io/info",
                 config="data_config.py", ):
        self._hash = ""
        self._date = ""
        self._atlasurl = url
        self._jsonfilename = filename
        self._atlasurlinfo = info_url
        self._configfile = config

    def _check_hash(self):
        """
        Checks if the hashes are equal
        :return: Result of checking hashes
        """

        with urllib.request.urlopen(self._atlasurlinfo) as url:
            self._hash = json.loads(url.read().decode())["NA"]["hash"]
        if str(self._hash) == data_config.atlas_na_hash:
            return True
        return False

    def _check_date(self):
        """
        Checks if the dates are equal
        :return:  Result of checking dates
        """
        self._date = datetime.date.today().strftime("%Y.%m.%d")

        if self._date == data_config.atlas_na_date:
            return True
        return False

    def force_update(self):
        """
        Forces an data update
        :param self:
        :return: None
        """
        with urllib.request.urlopen(self._atlasurlinfo) as url:
            self._hash = json.loads(url.read().decode())["NA"]["hash"]
        self._date = datetime.date.today().strftime("%Y.%m.%d")

        with open(self._jsonfilename, 'w') as outfile:
            with urllib.request.urlopen(self._atlasurl) as url:
                data = json.loads(url.read().decode())
                json.dump(data, outfile)

        with open(self._configfile, "w") as configfile:
            configfile.write(f'atlas_na_hash = "{self._hash}"\natlas_na_date = "{self._date}"\n')

        print(f"Data has been forcefully updated to hash version {self._hash} on {self._date}")

    def get_data(self):
        """
        gets data from atlas is hash and data are different or if the JSON doesn't exist
        :return: None
        """
        checks = False

        if not os.path.isfile(self._jsonfilename):
            checks = True
        elif self._check_date():
            raise DateError(f"The current date matches the date of the last request ({self._date}).")
        elif self._check_hash():
            raise HashError(f"The current hash matches the most recent hash ({self._hash}).")
        else:
            checks = True

        if checks:
            with open(self._jsonfilename, 'w') as outfile:
                with urllib.request.urlopen(self._atlasurl) as url:
                    data = json.loads(url.read().decode())
                    json.dump(data, outfile)

            with open(self._configfile, "w") as configfile:
                configfile.write(f'atlas_na_hash = "{self._hash}"\natlas_na_date = "{self._date}"\n')

            print(f"Data has been updated to hash version {self._hash} on {self._date}")
