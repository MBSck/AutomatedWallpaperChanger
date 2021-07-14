import os
import subprocess
import time
import random
import configparser
import datetime


class DesktopChanger:
    """The Automated Wallpaper Changer Mainframe"""
    def __init__(self):
        """Initializes the dataset"""
        # sets the Paths
        # self.wallpaper_path = input("Enter the path for the wallpaper folder: ")

        self.wallpaper_path = "/home/marten/Pictures/Wallpapers"
        self.time_since_last_timestep = 0
        self.timestep = int(input("Enter the time when the Desktop should be changed.\n"
                                  "In seconds: "))
        self.date = ""
        self.wallpaper_name = ""

        # Takes the shorter time frames and converts it into seconds for the time.sleep() function
        self.timestep_second_dictionary = {"1 Day": "1-Day", "12 Hours": 43200,
                                  "1 Hour": 3600, "30 Minutes": 1800, "15 Minutes": 300, "5 Minutes": 300}

        # Defines the parser for the cfg files
        self.cfg_parser = configparser.RawConfigParser()

        # Gets the data from the cfg file
        self.cfg_path = os.path.abspath("config.cfg")

        # Creates file and writes first run
        self.create_cfg_file()
        self.first_run = False

        # Gets data
        self.get_data()

        # Executes the wallpaper changing loop
        self.main_loop(self.wallpaper_path)

    def create_cfg_file(self):
        """Creates the config.cfg file"""
        # Writes down the install data into file
        with open("config.cfg", "w") as f:
            # Install config
            f.write("[Install-Config]\n")
            f.write(f"Install_Date = {datetime.datetime.now()}\n")
            f.write(f"Install = True\n")
            f.write('\n')

            # Runtime config
            f.write("[Runtime-Config]\n")
            f.write(f"Date = {datetime.date.today()}\n")
            f.write(f"Time_Since_Last_TimeStep = {round(time.time())}\n")
            f.write(f"Timestep_Selection = {self.timestep}\n")
            f.write(f"Wallpaper_Path = {self.wallpaper_path}\n")

    def get_data(self):
        """Gets the data from the config file"""
        self.cfg_parser.read(self.cfg_path)
        self.first_run = self.cfg_parser.get("Install-Config", "Install")

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

    def get_wallpaper(self, wallpaper_folder_path):
        file = random.choice(os.listdir(wallpaper_folder_path))
        cond = True

        while cond:
            if file == self.wallpaper_name:
                file = random.choice(os.listdir(wallpaper_folder_path))

            if file != self.wallpaper_name:
                self.wallpaper_name
                break

        return os.path.join(wallpaper_folder_path, file)

    def desktop_changer(self, wallpaper_folder_path):
        if self.first_run:
            args0 = [f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path"
                     f" -n -t string -s {self.get_wallpaper(wallpaper_folder_path)}"]
            args1 = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-style", "-s", "3"]
            args2 = ["xfconf-query", "--create","-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]

            try:
                subprocess.Popen(args0)
            except Exception:
                pass

            subprocess.Popen(args1)
            subprocess.Popen(args2)

        args = ["xfdesktop", "--reload"]
        subprocess.Popen(args)

    def main_loop(self, wallpaper_folder):
        while True:
            time.sleep(1)
            self.get_data()
            self.desktop_changer(wallpaper_folder)



if __name__ == "__main__":
    desktopchanger = DesktopChanger
    desktopchanger().main_loop()
