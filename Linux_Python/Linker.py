import os
import getpass


class Linker:
    """Creates the shortcuts for the Desktop as well as the Autostart"""
    def __init__(self, install_path, autostart_path):
        # Gets the paths
        self.install_path = install_path
        self.autostart_path = autostart_path

        # Gets desktop path
        self.desktop_path = f"/home/{getpass.getuser()}/Desktop"

        # Creates shortcut for desktop
        self.create_shortcut(install_path, self.desktop_path)

    def create_shortcut(self, source_path, destination_path):
        """Makes a shortcut of the .exe in the specified folder"""
        source_path = os.path.join(source_path, "Launcher.py")
        os.symlink(source_path, destination_path)


if __name__ == "__main__":
    ...
