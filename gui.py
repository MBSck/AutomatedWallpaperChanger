import PySimpleGUI as sg
import datetime
import time
import getpass
import os

from Linker import Linker

# It doenst work to only select one custom time


class InstallerGUI:
    """Sets up GUI that asks user at what time intervals he wants to change the desktop wallpaper"""

    def __init__(self):
        """Initializes the GUI"""
        # Sets the theme
        sg.theme("DarkAmber")

        # Sets the layout
        self.layout = [[sg.Text("Choose path of wallpaper folder:")],
                       [sg.In(), sg.FolderBrowse(key="Folder")],

                       [sg.Text("Time interval of wallpaper change:"),
                        sg.Combo(["1 Week", "1 Day", "12 Hours", "1 Hour", "30 Minutes", "15 Minutes", "5 Minutes"],
                                 default_value="1 Day", key="Time")],

                       [sg.Checkbox("Custom time interval (If toggled, numbers below will count):", change_submits=True,
                                    enable_events=True, default=False, key="CTimeBox")],

                       [sg.Text("Hours"), sg.Spin([i for i in range(0, 25)], initial_value=0, key="CHours"),
                        sg.Text("Minutes"), sg.Spin([i for i in range(0, 60)], initial_value=0, key="CMinutes"),
                        sg.Text("Seconds"), sg.Spin([i for i in range(0, 60)], initial_value=0, key="CSeconds")],

                       [sg.Button("Install"), sg.Button("Cancel")]]

        # Initializes the Window
        self.window = sg.Window("AWC - Config_Installer", self.layout, finalize=True)

        # Takes the shorter time frames and converts it into seconds for the time.sleep() function
        self.second_dictionary = {"1 Week": 604800, "1 Day": 86400, "12 Hours": 43200,
                                  "1 Hour": 3600, "30 Minutes": 1800, "15 Minutes": 300, "5 Minutes": 300}

        # Checks for errors
        self.error = False

        # Gets the autostart folder and makes it into path
        self.autostart_path = \
            f"C:\\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

        # Sets install path
        self.install_path = os.path.dirname(os.path.abspath(__file__))

        # Initializes linker
        self.linker = Linker

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
            f.write(f"Time_Since_Last_TimeStep = {round(time.time())}\n")

            if values["CTimeBox"]:
                f.write(f"Timestep_Selection = {int(values['CTime'])}\n")
            else:
                f.write(f"Timestep_Selection = {self.second_dictionary[values['Time']]}\n")

            f.write(f"Wallpaper_Path = {values['Folder']}\n")

    def create_install_folder(self, values):
        """Creates folder that contains config.cfg as well as the exe"""
        self.create_cfg_file(values)

    def install_checker(self, values):
        """Installs the program"""
        # Returns the custom time if it is selected
        if values["CTimeBox"]:
            # Yields error if custom time is set at 0
            if (int(values["CHours"]) and int(values["CMinutes"]) and int(values["CSeconds"])) == 0:
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
        if (not values["CTimeBox"]) and (values["Time"] == ""):
            self.error = True
            sg.PopupError("No time selected!\nChoose either from drop down or custom time!")

    def run(self):
        """Logs the data changes it into seconds"""
        while True:
            # Reads the values and events of the window
            event, values = self.window.read()

            # Checks if the window is closed
            if (event == sg.WIN_CLOSED) or (event == "Cancel"):
                break

            # Formats Install Path so that folder is created
            elif event == "InstallPath":
                print("Hey")

            # Formats Custom Time so everything is zero when pressed
            elif event == "CTimeBox":
                if values["CTimeBox"] is False:
                    self.window["CHours"].update("0")
                    self.window["CMinutes"].update("0")
                    self.window["CSeconds"].update("0")

                    values["CHours"] = values["CMinutes"] = values["CSeconds"] = "0"

            # Checks if the install button is pressed
            elif event == "Install":
                self.install_checker(values)

                # Checks if error occurred and send user back to installer, else exits
                if not self.error:
                    self.create_install_folder(values)
                    self.linker(self.install_path, self.autostart_path)
                    break

                else:
                    self.error = False

        self.window.Close()


class AWCGUI:
    """The Gui that gets minimized to tray as well as changes the config file if accessed"""

    def __init__(self):
        sg.theme("Dark Amber")

        self.layout = []

    def run(self):
        """Runs the gui interface"""
        while True:
            print("Yeah")


if __name__ == "__main__":
    gui = InstallerGUI()
    print(gui.run())
    gui.window.Close()

    with open("config.cfg", "r") as f:
        print(f.read())
