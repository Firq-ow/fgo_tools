"""
UI for damage Calculator
"""
import json
import re
from slugify import slugify
import requests

import PySimpleGUI as psg
from calc_dmg import CalculateDamage


# from get_atlas_json import AtlasFunctions
# from get_atlas_json import DateError, HashError

def main():
    mainUi = UI()
    mainUi.eventLoop()


class UI:
    def __init__(self):
        # Load Atlas JSON
        with open('nice_servant.json') as json_file:
            self._DATA = json.load(json_file)

        # Set class vars
        self._CURRENT_KEYVALUES = []

        # Set PySimpleGui Standards
        psg.theme("DarkBlue3")
        psg.set_options(font=("Courier New", 12))

        # Set layouts
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

        self.mainWindow = psg.Window(title="Damage Calculator Window",
                                     layout=layout_main,
                                     margins=(100, 50),
                                     finalize=True
                                     )

        # Bind Enter Events
        self.mainWindow['-Servant_Input-'].bind("<Return>", "_Enter")
        self.mainWindow['-DMG_Input-'].bind("<Return>", "_Enter")

    @staticmethod
    def get_web_image(img_url: str):
        url = img_url
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        return response.raw.read()

    def eventLoop(self):
        while True:
            event, values = self.mainWindow.read()

            match event:
                case "-Servant_Input_BT-" | "-Servant_Input-_Enter":
                    servant_list = self.search_servant(values["-Servant_Input-"])
                    self.mainWindow["-IMAGE_SERVANT-"].update()
                    self.mainWindow["-Servants_Listbox-"].update(servant_list)
                case "-Servants_Listbox-":
                    value = values["-Servants_Listbox-"][0]
                    self.update_output_servant(value)
                case "-Calculate-" | "-DMG_Input-_Enter":
                    self.calculate_dmg(values["-DMG_Input-"])
                case psg.WINDOW_CLOSED:
                    self.mainWindow.close()
                    break

    def calculate_dmg(self, formular):
        calculator = CalculateDamage()

        try:
            calculator.parse_values(formular)
        except (ValueError, NameError):
            print("Could not parse input string")

        dmg = calculator.calculate()

        self.mainWindow["-Tout-"].update(f"Calculated Damage:\nAvg: {dmg[0]}\nMin: {dmg[1]}\nMax: {dmg[2]}")

    def update_output_servant(self, value):
        if value == "No Servant found.":
            self.mainWindow["-IMAGE_SERVANT-"].update()
            self.mainWindow["-ServantInfoText-"].update("")
            return

        listbox_id = int(re.findall(r'\[(.*?)]', value)[0])
        listbox_data = json.loads(json.dumps(self._CURRENT_KEYVALUES))
        result_key_value = []

        for key_value in listbox_data:
            if key_value['collectionNo'] == listbox_id:
                result_key_value = key_value

        image_url = result_key_value['extraAssets']['faces']['ascension']['1']
        servant_name = result_key_value['name']

        image_data = self.get_web_image(image_url)

        self.mainWindow["-IMAGE_SERVANT-"].update(data=image_data)
        self.mainWindow["-ServantInfoText-"].update(f"{servant_name}")

    def search_servant(self, name):
        id_pattern = re.compile("^[0-9]+$")
        matches = ["best girl", "waifu"]

        if id_pattern.match(name):
            return self.find_servant_by_id(int(name))

        if any(x in name for x in matches):
            return self.find_servant_by_id(70)

        return self.find_servant_by_name(name)

    def find_servant_by_id(self, servant_id):
        self._CURRENT_KEYVALUES = []

        for key_value in self._DATA:
            if key_value['collectionNo'] == int(servant_id) and "beast" not in key_value['className']:
                self._CURRENT_KEYVALUES.append(key_value)
                return [
                    f"[{key_value['collectionNo']}] - {key_value['name']}, Class: {key_value['className'].capitalize()}"]

        return ["No Servant found."]

    def find_servant_by_name(self, name):
        self._CURRENT_KEYVALUES = []

        servant_list = []
        for key_value in self._DATA:
            key_value_slug = slugify(key_value['name'])
            name_slug = slugify(name)
            if name_slug in key_value_slug and not any(
                    x in key_value['className'] for x in ["beast", "grandCaster"]) and not key_value_slug == slugify(
                    "Solomon"):
                self._CURRENT_KEYVALUES.append(key_value)
                servant_list.append(
                    f"[{key_value['collectionNo']}] - {key_value['name']}, Class: {key_value['className'].capitalize()}")

        if len(servant_list) == 0:
            return ["No Servant found."]

        return servant_list


if __name__ == '__main__':
    main()
