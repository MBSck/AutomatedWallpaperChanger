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
        sg.PopupYesNo("Uninstall AWC Tool?")

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Sets the paths
        self.paths = []
        self.install_path = ""
        self.autostart_path = ""

        # Gets the data from the cfg file
        self.cfg_path = os.path.abspath("config.cfg")
        self.get_data()

        # Uninstalls all files
        self.uninstall()

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
