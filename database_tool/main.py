# Imports
import json
import urllib.request

with urllib.request.urlopen("https://api.atlasacademy.io/export/NA/nice_servant.json") as url:
    data = json.loads(url.read().decode())

with open("servant_data_nice.json", "w") as write_file:
    json.dump(data, write_file)
