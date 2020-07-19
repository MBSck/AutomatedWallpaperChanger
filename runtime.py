import os
import random
import ctypes
import configparser
import time

# If time is bigger than 1 hour log it in file so python know what time it is
# Make config file that logs the timesteps and folder the user wants to use
# Log when desktop wallpaper is changed


class Singleton(type):
    """Creates a singleton ~ Global Class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class AWC(metaclass=Singleton):
    """The Automated Wallpaper Changer Mainframe"""
    def __init__(self):
        """Initializes the dataset"""
        # sets the Paths
        self.wallpaper_path = ""
        self.time_since_last_timestep = 0
        self.timestep = 0

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Gets the data from the cfg file
        self.cfg_path = os.path.abspath("config.cfg")

        # Initialized
        self.initialized = True
        self.get_data()

        # Executes the wallpaper changing loop
        self.automatic_loop(self.wallpaper_path)

    def get_data(self):
        """Gets the data from the config file"""
        self.cfg_parser.read(self.cfg_path)
        self.wallpaper_path = self.cfg_parser.get("Runtime-Config", "Wallpaper_Path")

        self.time_since_last_timestep = int(self.cfg_parser.get("Runtime-Config",
                                                                "Time_Since_Last_TimeStep"))

        self.timestep = int(self.cfg_parser.get("Runtime-Config", "Timestep_Selection"))

    def update_config_file(self):
        """Updates the config file"""
        self.time_since_last_timestep = round(time.time())
        update_object = self.cfg_parser["Runtime-Config"]

        update_object["Time_Since_Last_TimeStep"] = str(self.time_since_last_timestep)

        with open(self.cfg_path, "w") as f:
            self.cfg_parser.write(f)

    def get_desktop_background_file_path(self, wallpaper_folder_path):
        """Gets a file to change the wallpaper into from a specified folder"""
        file = random.choice(os.listdir(wallpaper_folder_path))
        return os.path.join(wallpaper_folder_path, file)

    def switch_background(self, wallpaper_folder_path):
        """Switches the background wallpaper"""
        ctypes.windll.user32.SystemParametersInfoW(
            20, 0, self.get_desktop_background_file_path(wallpaper_folder_path), 0)

    def automatic_loop(self, wallpaper_folder_path):
        """Runs the part of the program that changes the desktop wallpaper"""
        while True:
            # On first run get the data of the different actions
            if self.initialized:
                # On first activation set desktop the slow way
                if round(time.time()) >= (self.time_since_last_timestep + self.timestep):
                    self.update_config_file()

                    self.switch_background(wallpaper_folder_path)

                    self.initialized = False

            # Use sleep time for wait and update cfg
            else:
                time.sleep(self.timestep)
                self.update_config_file()

                self.switch_background(wallpaper_folder_path)


if __name__ == "__main__":
    cfg_parser = configparser.RawConfigParser()

    # Gets the data from the cfg file
    cfg_path = os.path.abspath("config.cfg")

    cfg_parser.read(cfg_path)
    wallpaper_path = cfg_parser.get("Automated-Wallpaper-Changer-Config", "Path")

    time_since_last_timestep = cfg_parser.get("Automated-Wallpaper-Changer-Config",
                                                        "Time_Since_Last_TimeStep")

    timestep = cfg_parser.get("Automated-Wallpaper-Changer-Config", "Timestep_Selection")

    print(wallpaper_path, timestep, time_since_last_timestep)
