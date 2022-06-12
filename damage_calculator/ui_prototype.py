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
    """
    Main function
    :return: None
    """
    main_ui = UI()
    main_ui.event_loop()


class UI:
    """
    Class that houses the UI

    Call UI.eventLoop() to start UI event handling, otherwise it will be instantly closed
    """
    def __init__(self):
        """
        Init function:
        - creates JSON data constant
        - creates storage for current list elements
        - stes main window layout and design
        - creates main window
        - binds enter to specific text fields
        """
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

        self.main_window = psg.Window(title="Damage Calculator Window",
                                      layout=layout_main,
                                      margins=(100, 50),
                                      finalize=True
                                      )

        # Bind Enter Events
        self.main_window['-Servant_Input-'].bind("<Return>", "_Enter")
        self.main_window['-DMG_Input-'].bind("<Return>", "_Enter")

    @staticmethod
    def get_web_image(img_url: str):
        """
        Gets an image from a given URL
        :param img_url: url of the image
        :return: data of the image as raw data
        """
        url = img_url
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        return response.raw.read()

    def event_loop(self):
        """
        Main event loop, has to be called to handle all UI events
        :return: Nothing
        """
        while True:
            event, values = self.main_window.read()

            match event:
                case "-Servant_Input_BT-" | "-Servant_Input-_Enter":
                    servant_list = self.search_servant(values["-Servant_Input-"])
                    self.main_window["-IMAGE_SERVANT-"].update()
                    self.main_window["-Servants_Listbox-"].update(servant_list)
                case "-Servants_Listbox-":
                    value = values["-Servants_Listbox-"][0]
                    self.update_output_servant(value)
                case "-Calculate-" | "-DMG_Input-_Enter":
                    damage = self.calculate_dmg(values["-DMG_Input-"])
                    self.main_window["-Tout-"].update(f"Calculated Damage:\nAvg: {damage[0]}\nMin: {damage[1]}\nMax: {damage[2]}")
                case psg.WINDOW_CLOSED:
                    self.main_window.close()
                    break

    @staticmethod
    def calculate_dmg(formular):
        """
        Function to initiate the damage calculation
        :param formular: Damage formular
        :return: Nothing
        """
        calculator = CalculateDamage()

        try:
            calculator.parse_values(formular)
        except (ValueError, NameError):
            print("Could not parse input string")

        return calculator.calculate()


    def update_output_servant(self, value):
        """
        Updates the Image and name of the currently selected servant
        :param value: String returned by the ListBox event
        :return: Nothing
        """
        if value == "No Servant found.":
            self.main_window["-IMAGE_SERVANT-"].update()
            self.main_window["-ServantInfoText-"].update("")
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

        self.main_window["-IMAGE_SERVANT-"].update(data=image_data)
        self.main_window["-ServantInfoText-"].update(f"{servant_name}")

    def search_servant(self, name):
        """
        Selects the appropriate searching method for a given servant name or id
        :param name: Input from Listbox
        :return: Formatted List of servant strings
        """
        id_pattern = re.compile("^[0-9]+$")
        matches = ["best girl", "waifu"]

        if id_pattern.match(name):
            return self.find_servant_by_id(int(name))

        if any(x in name for x in matches):
            return self.find_servant_by_id(70)

        return self.find_servant_by_name(name)

    def find_servant_by_id(self, servant_id):
        """
        Searches a given servant by ID
        :param servant_id: ID of the servant
        :return: List with formatted servant data
        """
        self._CURRENT_KEYVALUES = []

        for key_value in self._DATA:
            if key_value['collectionNo'] == int(servant_id) and "beast" not in key_value['className']:
                self._CURRENT_KEYVALUES.append(key_value)
                return [
                    f"[{key_value['collectionNo']}] - {key_value['name']}, Class: {key_value['className'].capitalize()}"]

        return ["No Servant found."]

    def find_servant_by_name(self, name):
        """
        Searches a given servant by Name
        :param name: Name (or name fragment) of servant
        :return: List with formatted servant data
        """
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
