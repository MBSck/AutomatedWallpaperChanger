import PySimpleGUI as sg
import configparser
import shutil
import os

# Buttons do not cause uninstall yet


class Uninstaller:
    """Removes all files that are connected to AWC"""
    def __init__(self):
        """Gets the data and location of files"""
        sg.theme("Dark Amber")

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Sets the paths
        self.paths = []
        self.install_path = ""
        self.autostart_path = ""

        # Gets the data from the cfg file
        self.cfg_path = os.path.abspath("config.cfg")
        self.get_data()

        # Runs the popup
        self.window = ""
        self.popup = ""
        self.run_popup()

    def run_popup(self):
        """Shows and runs the popup"""
        self.popup = sg.PopupYesNo("Uninstall AWC Tool?")

        if self.popup == "Yes":
            print("hello")
            # Uninstalls all files
            self.uninstall()

        elif (self.popup == "No") or (self.popup == sg.WIN_CLOSED):
            print("bye")

    def get_data(self):
        """Gets the data of all files"""
        self.cfg_parser.read(self.cfg_path)
        self.install_path = self.cfg_parser.get("Install-Config", "Install_Path")
        self.autostart_path = self.cfg_parser.get("Install-Config", "Autostart_Path")

    def uninstall(self):
        """Uninstalls all files"""
        sg.Popup("All Files Removed!")

        # Terminates the process
        os.system("taskkill /F /IM AWC.exe")

        # Removes all files
        os.remove(self.autostart_path)
        shutil.rmtree(self.install_path)


if __name__ == "__main__":
    uninst = Uninstaller
    uninst()

