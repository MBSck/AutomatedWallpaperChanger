from gui import AWCGUI
from runtime import AWC

import psutil
import os
import PySimpleGUI as sg

__author__ = "Marten Scheuck"

"""This runs the install process."""

# Make next and previous desktop wallpaper available
# Log when desktop wallpaper is change


def get_all_process():
    """Cycles through all active processes and lists them"""
    proc_list = list()

    for proc in psutil.process_iter():
        try:
            proc_dict = proc.as_dict(attrs=["pid", "name", "cpu_percent"])

            proc_list.append(proc_dict)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return proc_list


def main():
    """This function runs the program"""
    gui_install_update = AWCGUI
    awc = AWC

    # Process not running at start
    process_running = False

    # Gets process list
    process_list = get_all_process()

    """
    # Cycles through active processes and compares by name
    for proc in process_list:
        if proc["name"] == "AWC.exe":
            process_running = True
            break
    """

    # Checks if process is running
    if process_running:
        # Checks if config file, if not runs installer
        gui_install_update().run()

    else:
        try:
            if not os.path.isfile("config.cfg"):
                gui_install_update().run()
                awc()
            elif os.path.isfile("config.cfg"):
                awc()

        # Logs all errors
        except Exception as e:
            sg.PopupError("An Error has occurred! Program shutting down!")
            if os.path.isfile("error.log"):
                with open("error.log", "a") as f:
                    f.write(str(e) + '\n')
            else:
                with open("error.log", "w") as f:
                    f.write(str(e) + '\n')


if __name__ == "__main__":
    main()

