import winshell
import os
from pathlib import Path


class Linker:
    """Creates the shortcuts for the Desktop as well as the Autostart"""
    def __init__(self, install_path, autostart_path):
        # Gets the paths
        self.install_path = install_path
        self.autostart_path = autostart_path

        # Gets desktop path
        self.desktop_path = Path(winshell.desktop())

        # Creates shortcut for autostart
        self.create_shortcut(self.autostart_path)

        # Creates shortcut for desktop
        self.create_shortcut(self.desktop_path)

    def create_shortcut(self, path):
        """Makes a shortcut of the .exe in the specified folder"""
        with winshell.shortcut(os.path.join(path, "AWC.lnk")) as link:
            link.path = os.path.join(self.install_path, "AWC.exe")
            link.working_directory = self.install_path


if __name__ == "__main__":
    ...
