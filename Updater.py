import os
import configparser
import time
import PySimpleGUI as sg


class Updater:
    """Sets up GUI that asks user at what time intervals he wants to change the desktop wallpaper"""
    def __init__(self):
        """In itializes the GUI"""
        # Sets the theme
        sg.theme("DarkAmber")

        # Sets the layout
        self.layout = [[sg.Text("Choose path of wallpaper folder:")],
                       [sg.In(key="Path"), sg.FolderBrowse(key="Folder")],

                       [sg.Text("Time interval of wallpaper change:"),
                        sg.Combo(["1 Day", "12 Hours", "1 Hour", "30 Minutes", "15 Minutes", "5 Minutes"],
                                 default_value="1 Day", key="Time")],

                       [sg.Checkbox("Custom time interval (If toggled, numbers below will count):", change_submits=True,
                                    enable_events=True, default=False, key="CTimeBox")],

                       [sg.Text("Hours"), sg.Spin([i for i in range(0, 25)], initial_value=0, key="CHours"),
                        sg.Text("Minutes"), sg.Spin([i for i in range(0, 60)], initial_value=0, key="CMinutes"),
                        sg.Text("Seconds"), sg.Spin([i for i in range(0, 60)], initial_value=0, key="CSeconds")],

                       [sg.Button("Install"), sg.Button("Open Readme"),
                        sg.Button("Cancel"), sg.Button("Exit Program", button_color=("black", "red"))]]

        # Initializes the Window
        self.window = sg.Window("AWC - Config_Installer", self.layout, finalize=True)

        # Takes the shorter time frames and converts it into seconds for the time.sleep() function
        self.timestep_second_dictionary = {"1 Day": "1-Day", "12 Hours": 43200,
                                  "1 Hour": 3600, "30 Minutes": 1800, "15 Minutes": 300, "5 Minutes": 300}

        # Checks for errors
        self.error = False

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Values to update
        self.time_since_last_timestep = 0
        self.timestep_selection = 0
        self.wallpaper_path = ""

        # Runs the GUI
        self.run()

    def update_config_file(self, values):
        """Updates the config file"""
        self.cfg_parser.read(os.path.abspath("config.cfg"))

        update_object = self.cfg_parser["Runtime-Config"]

        self.time_since_last_timestep = round(time.time())
        update_object["Time_Since_Last_TimeStep"] = str(self.time_since_last_timestep)

        # Updates the path to the wallpaper folder
        if values["Path"] != "":
            update_object["Wallpaper_Path"] = values["Path"]

        # Updates time step selection
        if values["CTimeBox"]:
            update_object["Timestep_Selection"] = values["CTime"]

        else:
            update_object["Timestep_Selection"] = str(self.timestep_second_dictionary[values['Time']])

        with open(os.path.abspath("config.cfg"), "w") as f:
            self.cfg_parser.write(f)

    def update_checker(self, values):
        """Checks if values are too much"""
        if values["CTimeBox"]:
            # Yields error if custom time is set at 0
            if (int(values["CHours"] == 0)) and (int(values["CMinutes"]) == 0) and (int(values["CSeconds"]) == 0):
                self.error = True
                sg.PopupError("Input custom time or uncheck custom time box!")

            else:
                # Warns that if time is selected as well the custom time will override it
                sg.Popup("Custom time will override drop down selection!", keep_on_top=True)

                values["CTime"] = str(int(values["CHours"]) * 3600 + \
                                  int(values["CMinutes"]) * 60 + int(values["CSeconds"]))

        # Warns if neither time nor Custom time is selected
        if (values["CTimeBox"] is False) and (values["Time"] == ""):
            self.error = True
            sg.PopupError("No time selected!\nChoose either from drop down or custom time!")

    def run(self):
        """Logs the data changes it into seconds"""
        while True:
            # Reads the values and events of the window
            event, values = self.window.read()

            # Checks if the window is closed
            if (event == sg.WIN_CLOSED) or (event == "Cancel"):
                # If the config is not yet created close program
                quit()

            # Kills the task of the AWC.exe if terminated
            elif event == "Exit Program":
                try:
                    os.system("taskkill /F /IM AWC.exe")
                    sg.Popup("Program Terminated!")
                    quit()

                except Exception:
                    pass

            if event == "Open Readme":
                if os.path.isfile("README.txt"):
                    os.startfile(os.path.abspath("README.txt"))

                else:
                    sg.PopupError("No Readme.txt found!")

            # Formats Custom Time so everything is zero when pressed
            elif event == "CTimeBox":
                if values["CTimeBox"] is False:
                    self.window["CHours"].update("0")
                    self.window["CMinutes"].update("0")
                    self.window["CSeconds"].update("0")

                    values["CHours"] = values["CMinutes"] = values["CSeconds"] = "0"

            # Checks if the install button is pressed
            elif event == "Install":
                # Gives error if config doesn't exist
                if not os.path.isfile("config.cfg"):
                    sg.PopupError("No Configuration File Found!")

                # Overwrites data contained in config.cfg if it exists
                else:
                    self.update_checker(values)

                    # Checks if error occurred and send user back to installer, else exits and updates
                    if not self.error:
                        self.update_config_file(values)
                        sg.Popup("Configuration Updated!")
                        break

                    else:
                        self.error = False

        self.window.Close()


if __name__ == "__main__":
    up = Updater
    up().run()
