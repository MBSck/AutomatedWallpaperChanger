import os
import PySimpleGUI as sg

from gui import AWCGUI
from runtime import AWC

__author__ = "Marten Scheuck"

"""This runs the install process."""

#TODO: Make next and previous desktop wallpaper available
#TODO: Log when desktop wallpaper is change


def main():
    """This function runs the program"""
    gui_install_update = AWCGUI
    awc = AWC

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
                f.write("AWC.exe - ERROR: " + str(e) + '\n')
        else:
            with open("error.log", "w") as f:
                f.write("AWC.exe - ERROR: " + str(e) + '\n')


if __name__ == "__main__":
    main()

