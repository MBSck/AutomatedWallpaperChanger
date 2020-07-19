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

        # Defines the popup
        self.popup = ""

        # Popup Error Text
        self.popup_scroll_text = ""

        # Sets the paths
        self.paths = []
        self.install_path = ""
        self.autostart_path = ""
        self.autostart_file_path = ""

        # Gets the data from the cfg file
        if os.path.isfile("config.cfg"):
            self.cfg_path = os.path.abspath("config.cfg")
            self.get_data()

            # Runs the popup
            self.run_popup()

        else:
            sg.PopupError("No install config found!")

    def run_popup(self):
        """Shows and runs the popup"""
        self.popup = sg.PopupYesNo("Uninstall AWC Tool?")

        if self.popup == "Yes":
            # Uninstalls all files
            self.uninstall()

        elif (self.popup == "No") or (self.popup == sg.WIN_CLOSED):
            sg.Popup("Uninstall Canceled!")

    def get_data(self):
        """Gets the data of all files"""
        self.cfg_parser.read(self.cfg_path)
        self.install_path = self.cfg_parser.get("Install-Config", "Install_Path")
        self.autostart_path = self.cfg_parser.get("Install-Config", "Autostart_Path")

        self.autostart_file_path = os.path.join(self.autostart_path, "AWC.lnk")

    def uninstall(self):
        """Uninstalls all files"""
        # Terminates the process
        try:
            os.system("taskkill /F /IM AWC.exe")

        except Exception as e:
            pass

        # Removes all files
        if os.path.isfile(self.autostart_file_path):
            os.remove(self.autostart_file_path)

        else:
            self.popup_scroll_text += "AWC.exe.lnk not found in autostart folder.\n"
            sg.popup_scrolled(self.popup_scroll_text)
            sg.Popup("All Files Removed!")

        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path, ignore_errors=True)


if __name__ == "__main__":
    uninst = Uninstaller
    uninst()

