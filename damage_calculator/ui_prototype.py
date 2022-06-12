"""
UI for damage Calculator
"""
import json
import re
from slugify import slugify
import requests

import PySimpleGUI as psg
from calc_dmg import CalculateDamage
from get_atlas_json import AtlasFunctions
from get_atlas_json import DateError, HashError


def get_web_image(img_url : str):
    url = img_url
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    return response.raw.read()

# Setting theme and Font
psg.theme("DarkBlue3")
psg.set_options(font=("Courier New", 12))

# Search layout
layout_searchinput = [
    [
        psg.Text("Enter Servant Name or ID:")
    ],
    [
        psg.In(enable_events=False,
               key="-Servant_Input-"),
        psg.Button(button_text="Submit",
                   key="-Servant_Input_BT-")
    ],
    [
        psg.Listbox(values=[],
                    enable_events=True,
                    size=(52, 10),
                    key="-Servants_Listbox-")
    ]
]

# Data Output Layout
layout_dataoutput = [
    [
        psg.Image(key="-IMAGE_SERVANT-")
    ],
    [
        psg.Text(key="-ServantInfoText-")
    ]
]


# Layout of main windows
layout_main = [
    layout_searchinput,
    layout_dataoutput,
    [
        psg.Text("Enter Damage formular here:")
    ],
    [
        psg.In(enable_events=False,
               key="-DMG_Input-",
               size=42
               )
    ],
    [
        psg.Button(key="-Calculate-",
                   button_text="Calculate"
                   )
    ],
    [
        psg.Text(key="-Tout-")
    ]
]

# Create Application window
main = psg.Window(title="Damage Calculator Window",
                  layout=layout_main,
                  margins=(100, 50),
                  finalize=True
                  )

# Pressing Enter event
main['-Servant_Input-'].bind("<Return>", "_Enter")
main['-DMG_Input-'].bind("<Return>", "_Enter")

with open('nice_servant.json') as f:
    _DATA = json.load(f)

_CURRENT_KEYVALS = []

# Event Loop
while True:
    # Read Events
    event, values = main.read()

    if event == "-Servant_Input_BT-" or event == "-Servant_Input-" + "_Enter":
        name = values["-Servant_Input-"]
        pattern = re.compile("^[0-9]+$")
        SERVANT_NAMES = []
        matches = ["best girl", "waifu"]

        if pattern.match(name):
            _CURRENT_KEYVALS = []
            for keyval in _DATA:
                if keyval['collectionNo'] == int(name) and not "beast" in keyval['className']:
                    _CURRENT_KEYVALS.append(keyval)
                    servant_name = [f"[{keyval['collectionNo']}] - {keyval['name']}, Class: {keyval['className'].capitalize()}"]
                    SERVANT_NAMES = servant_name
        elif any(x in name for x in matches):
            for keyval in _DATA:
                if keyval['collectionNo'] == 70:
                    _CURRENT_KEYVALS.append(keyval)
                    servant_name = [f"[{keyval['collectionNo']}] - {keyval['name']}, Class: {keyval['className'].capitalize()}"]
                    SERVANT_NAMES = servant_name
        else:
            _CURRENT_KEYVALS = []
            servant_name = []
            for keyval in _DATA:
                keyval_slug = slugify(keyval['name'])
                name_slug = slugify(name)
                if name_slug in keyval_slug and not any(x in keyval['className'] for x in ["beast", "grandCaster"]) and not keyval_slug == slugify("Solomon"):
                    _CURRENT_KEYVALS.append(keyval)
                    servant_name.append(f"[{keyval['collectionNo']}] - {keyval['name']}, Class: {keyval['className'].capitalize()}")
            SERVANT_NAMES = servant_name

        if len(SERVANT_NAMES) == 0:
            SERVANT_NAMES = ["No Servant found."]

        main["-IMAGE_SERVANT-"].update()
        main["-Servants_Listbox-"].update(SERVANT_NAMES)

    if event == "-Servants_Listbox-":
        value = values["-Servants_Listbox-"][0]
        if value != "No Servant found.":
            id = int(re.findall(r'\[(.*?)\]', value)[0])
            json_keyvals = json.dumps(_CURRENT_KEYVALS)
            data = json.loads(json_keyvals)
            hit_keyval = []
            for keyval in data:
                if keyval['collectionNo'] == id:
                    hit_keyval =keyval

            img_url = hit_keyval['extraAssets']['faces']['ascension']['1']
            name_servant = hit_keyval['name']
            img_data = get_web_image(img_url)

            main["-IMAGE_SERVANT-"].update(data=img_data)
            main["-ServantInfoText-"].update(f"{name_servant}")
        else:
            main["-IMAGE_SERVANT-"].update()
            main["-ServantInfoText-"].update("")

    if event == "-Calculate-" or event == "-DMG_Input-" + "_Enter":
        formular = values["-DMG_Input-"]
        calc = CalculateDamage()
        try:
            calc.parse_values(formular)
        except (ValueError, NameError):
            print("Could not parse input string")

        dmg = calc.calculate()

        main["-Tout-"].update(f"Calculated Damage:\nAvg: {dmg[0]}\nMin: {dmg[1]}\nMax: {dmg[2]}")

    # Close Application if window is closed
    if event == psg.WINDOW_CLOSED:
        main.close()
        break
