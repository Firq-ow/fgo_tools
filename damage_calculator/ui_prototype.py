"""
UI for damage Calculator
"""
import PySimpleGUI as psg


# Layout of main windows
layout_main = [
    [
        psg.Text("Enter Damage formular here:")
    ],
    [
        psg.In(size=(25, 1), enable_events=False, key="-DMG_Input-")
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

    # Close Application if window is closed
    if event == psg.WINDOW_CLOSED:
        main.close()
        break
