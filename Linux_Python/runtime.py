import os
import random
import subprocess
import configparser
import time

import datetime

from Linux_Python.gui import AWCGUITRAY


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
        self.date = ""
        self.wallpaper_name = ""

        # Initializes the gui tray
        self.gui_tray = AWCGUITRAY()

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Gets the data from the cfg file
        self.cfg_path = os.path.abspath("config.cfg")

        # Gets data
        self.get_data()

        # Executes the wallpaper changing loop
        self.automatic_loop(self.wallpaper_path)

    def get_data(self):
        """Gets the data from the config file"""
        self.cfg_parser.read(self.cfg_path)
        self.wallpaper_path = self.cfg_parser.get("Runtime-Config", "Wallpaper_Path")

        self.time_since_last_timestep = int(self.cfg_parser.get("Runtime-Config",
                                                                "Time_Since_Last_TimeStep"))

        self.timestep = self.cfg_parser.get("Runtime-Config", "Timestep_Selection")

        # brings data into the right format for datetime format
        date_temp = self.cfg_parser.get("Runtime-Config", "Date")
        date_temp = date_temp.split("-")
        if date_temp[1][0] == "0":
            date_temp[1] = date_temp[1][1:]

        for i, o in enumerate(date_temp):
            date_temp[i] = int(o)

        self.date = datetime.date(date_temp[0], date_temp[1], date_temp[2])

    def update_config_file(self, actual_time):
        """Updates the config file"""
        self.time_since_last_timestep = round(actual_time)
        update_object = self.cfg_parser["Runtime-Config"]

        update_object["Time_Since_Last_TimeStep"] = str(self.time_since_last_timestep)
        update_object["Date"] = str(datetime.date.today())

        with open(self.cfg_path, "w") as f:
            self.cfg_parser.write(f)

    def get_desktop_background_file_path(self, wallpaper_folder_path):
        """Gets a file to change the wallpaper into from a specified folder"""
        file = random.choice(os.listdir(wallpaper_folder_path))
        cond = True

        while cond:
            if file == self.wallpaper_name:
                file = random.choice(os.listdir(wallpaper_folder_path))

            if file != self.wallpaper_name:
                self.wallpaper_name = file
                break

        return os.path.join(wallpaper_folder_path, file)

    def switch_background(self, wallpaper_folder_path):
        """Switches the background wallpaper"""
        # Changes desktop background for linux xfce4
        args0 = ["xfconf-query", "-c", "xfce4-desktop",
             "-p", "/backdrop/screen0/monitor0/image-path", "-s", wallpaper_folder_path]
        args1 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-style", "-s", "3"]
        args2 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
        subprocess.Popen(args0)
        subprocess.Popen(args1)
        subprocess.Popen(args2)
        args = ["xfdesktop", "--reload"]

    def automatic_loop(self, wallpaper_folder_path):
        """Runs the part of the program that changes the desktop wallpaper"""
        while True:
            time.sleep(1)

            # Checks if any action for the gui tray is taken and returns true if config.cfg is changed
            try:
                if self.gui_tray.run():
                    self.get_data()

            except Exception as e:
                pass

            # Check if the timesteps are bigger than one day or not
            if self.timestep == "1-Day":
                if self.date < datetime.date.today():
                    actual_time = time.time()
                    self.update_config_file(actual_time)

                    self.switch_background(wallpaper_folder_path)

            else:
                # On first run get the data of the different actions
                actual_time = round(time.time())
                # On first activation set desktop the slow way
                if actual_time >= (self.time_since_last_timestep + int(self.timestep)):
                    self.update_config_file(actual_time)

                    self.switch_background(wallpaper_folder_path)


if __name__ == "__main__":
    help(random.sample)
