"""
UI for damage Calculator
"""
import json
import re
from slugify import slugify

import PySimpleGUI as psg
from calc_dmg import CalculateDamage
from get_atlas_json import AtlasFunctions
from get_atlas_json import DateError, HashError


# Layout of main windows
layout_main = [
    [
      psg.Text("Enter Servant Name or ID:"),
      psg.In(enable_events=False,
             key="-Servant_Input-"),
      psg.Button(button_text="Submit",
                 key="-Servant_Input_BT-")
    ],
    [
        psg.Text(key="-Sout-")
    ],
    [
        psg.Text("Enter Damage formular here:")
    ],
    [
        psg.In(enable_events=False,
               key="-DMG_Input-"
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
                  margins=(100, 50)
                  )

# Event Loop
while True:
    # Read Events
    event, values = main.read()

    if event == "-Servant_Input_BT-":
        name = values["-Servant_Input-"]
        pattern = re.compile("^[0-9]*$")
        SERVANT_NAMES = ''

        with open('nice_servant.json') as f:
            data = json.load(f)

        if pattern.match(name):
            for keyval in data:
                if keyval['collectionNo'] == int(name):
                    SERVANT_NAMES = [keyval['name'], keyval['className'], keyval['id']]
                    print(keyval)
        else:
            names = []
            for keyval in data:
                serv_id = []
                keyval_slug = slugify(keyval['name'])
                name_slug = slugify(name)
                if name_slug in keyval_slug:
                    names.append([keyval['name'], keyval['className'], keyval['id']])
                    print(names)

            if len(names) > 0:
                print(names)
                for x in names:
                    SERVANT_NAMES += f"{''.join(str(x))}\n"

        main["-Sout-"].update(f"{SERVANT_NAMES}")

    if event == "-Calculate-":
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
