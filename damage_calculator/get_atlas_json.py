import datetime
import urllib.request
import json
import data_config
import os

atlas_url = "https://api.atlasacademy.io/export/NA/nice_servant.json"
filename = "nice_servant.json"
atlas_info = "https://api.atlasacademy.io/info"

HASH = ""
DATE = ""


class HashError(Exception):
    pass


class DateError(Exception):
    pass


def check_hash():
    global HASH
    with urllib.request.urlopen(atlas_info) as url:
        HASH = json.loads(url.read().decode())["NA"]["hash"]

    if not str(HASH) == data_config.atlas_NA_hash:
        return True
    return False


def check_date():
    global DATE
    DATE = datetime.date.today().strftime("%Y.%m.%d")

    if not DATE == data_config.atlas_NA_date:
        return True
    return False


def get_data():
    checks = False

    if not os.path.isfile(filename):
        checks = True
    elif not check_date():
        raise DateError(f"The current date matches the date of the last request ({DATE}).")
    elif not check_hash():
        raise HashError(f"The current hash matches the most recent hash ({HASH}).")
    else:
        checks = True

    if checks:
        with open(filename, 'w') as outfile:
            with urllib.request.urlopen(atlas_url) as url:
                data = json.loads(url.read().decode())
                json.dump(data, outfile)

        with open("data_config.py", "w") as configfile:
            configfile.write(f'atlas_NA_hash = "{HASH}"\natlas_NA_date = "{DATE}"')

    return True
