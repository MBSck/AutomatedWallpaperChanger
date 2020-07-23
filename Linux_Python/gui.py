import PySimpleGUI as sg
import datetime
import time
import getpass
import os
import configparser
import sys

from Linux_Python.Linker import Linker


class AWCGUI:
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

                       [sg.Button("Install"), sg.Button("Open Readme"), sg.Button("Switch"), sg.Button("Cancel")]]

        # Initializes the Window
        self.window = sg.Window("AWC - Config_Installer", self.layout, finalize=True)

        # Takes the shorter time frames and converts it into seconds for the time.sleep() function
        self.timestep_second_dictionary = {"1 Day": "1-Day", "12 Hours": 43200,
                                  "1 Hour": 3600, "30 Minutes": 1800, "15 Minutes": 300, "5 Minutes": 300}

        # Checks for errors
        self.error = False

        # Gets the autostart folder and makes it into path
        self.autostart_path = f"/home/{getpass.getuser()}/"

        # For python file
        self.install_path = os.path.dirname(os.path.abspath("AWC.py"))

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Values to update
        self.time_since_last_timestep = 0
        self.timestep_selection = 0
        self.wallpaper_path = ""

        # Initializes linker
        self.linker = Linker

        # Runs the GUI
        self.run()

    def create_cfg_file(self, values):
        """Creates the config.cfg file"""
        # Writes down the install data into file
        with open("config.cfg", "w") as f:
            # Install config
            f.write("[Install-Config]\n")
            f.write(f"Install_Date = {datetime.datetime.now()}\n")
            f.write(f"Install_Path = {self.install_path}\n")
            f.write(f"Autostart_Path = {self.autostart_path}\n")

            f.write('\n')

            # Runtime config
            f.write("[Runtime-Config]\n")
            f.write(f"Date = {datetime.date.today()}\n")
            f.write(f"Time_Since_Last_TimeStep = {round(time.time())}\n")

            if values["CTimeBox"]:
                f.write(f"Timestep_Selection = {int(values['CTime'])}\n")
            else:
                f.write(f"Timestep_Selection = {self.timestep_second_dictionary[values['Time']]}\n")

            f.write(f"Wallpaper_Path = {values['Folder']}\n")

    def install_checker(self, values):
        """Installs the program"""
        # Returns the custom time if it is selected
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

        # Warns user if folder not selected
        if values["Folder"] == "":
            self.error = True
            sg.PopupError("Please select folder!")

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
                if os.path.isfile("config.cfg"):
                    break

                # If it is the update window close window only
                else:
                    sys.exit()

            if event == "Open Readme":
                if os.path.isfile("../Linux/README.txt"):
                    os.startfile(os.path.abspath("../Linux/README.txt"))

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
                # Writes config.cfg if it doesn't exist
                if not os.path.isfile("config.cfg"):
                    self.install_checker(values)

                    # Checks if error occurred and send user back to installer, else exits
                    if not self.error:
                        self.create_cfg_file(values)
                        self.linker(self.install_path, self.autostart_path)
                        sg.Popup("Configuration Installed!")
                        break

                    else:
                        self.error = False

                else:
                    sg.PopupError("Already installed!")
                    break

        self.window.Close()


if __name__ == "__main__":
    gui = AWCGUI
    gui()

