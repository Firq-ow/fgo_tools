"""
Module to import data from atlas into a json.
 Also reducing the amount of requests by caching the previous hash and date
"""
import os
import datetime
import urllib.request
import json
import data_config


ATLAS_URL = "https://api.atlasacademy.io/export/NA/nice_servant.json"
FILENAME_JSON = "nice_servant.json"
ATLAS_URL_INFO = "https://api.atlasacademy.io/info"

HASH = ""
DATE = ""


class HashError(Exception):
    """
    Exception if the Hash of the request and the cached Hash are equal.
    """


class DateError(Exception):
    """
    Exception if the current date and the cached date are equal
    """


def check_hash():
    """
    Checks if the hashes are equal
    :return: Result of checking hashes
    """
    global HASH
    with urllib.request.urlopen(ATLAS_URL_INFO) as url:
        HASH = json.loads(url.read().decode())["NA"]["hash"]

    if str(HASH) == data_config.atlas_NA_hash:
        return True
    return False


def check_date():
    """
    Checks if the dates are equal
    :return:  Result of checking dates
    """
    global DATE
    DATE = datetime.date.today().strftime("%Y.%m.%d")

    if DATE == data_config.atlas_NA_date:
        return True
    return False


def get_data():
    """
    gets data from atlas is hash and data are different or if the JSON doesn't exist
    :return: None
    """
    checks = False

    if not os.path.isfile(FILENAME_JSON):
        checks = True
    elif check_date():
        raise DateError(f"The current date matches the date of the last request ({DATE}).")
    elif check_hash():
        raise HashError(f"The current hash matches the most recent hash ({HASH}).")
    else:
        checks = True

    if checks:
        with open(FILENAME_JSON, 'w') as outfile:
            with urllib.request.urlopen(ATLAS_URL) as url:
                data = json.loads(url.read().decode())
                json.dump(data, outfile)

        with open("data_config.py", "w") as configfile:
            configfile.write(f'atlas_NA_hash = "{HASH}"\natlas_NA_date = "{DATE}"')
