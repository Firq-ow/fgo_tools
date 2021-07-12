# Imports
import os
import json
import urllib.request

with urllib.request.urlopen("https://api.atlasacademy.io/export/NA/nice_servant.json") as url:
    data = json.loads(url.read().decode())
    print(data)
