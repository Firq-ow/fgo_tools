"""
UI for damage Calculator
"""
import PySimpleGUI as psg
from calc_dmg import CalculateDamage
from get_atlas_json import AtlasFunctions
from get_atlas_json import DateError, HashError


# Layout of main windows
layout_main = [
    [
        psg.Text("Enter Damage formular here:")
    ],
    [
        psg.In(size=(25, 1),
               enable_events=False,
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
                  )

# Event Loop
while True:
    # Read Events
    event, values = main.read()

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
