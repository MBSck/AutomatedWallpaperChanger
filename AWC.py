from gui import AWCGUI
from runtime import AWC

import os
import PySimpleGUI as sg

__author__ = "Marten Scheuck"

"""This runs the install process."""

# Make next and previous desktop wallpaper available
# Log when desktop wallpaper is changed

if __name__ == "__main__":
    gui_install_update = AWCGUI
    awc = AWC

    try:
        if not os.path.isfile("config.cfg"):
            gui_install_update().run()
            awc()
        else:
            awc()

    except Exception as e:
        sg.PopupError("An Error has occurred and was logged! Program shutting down!")
        if os.path.isfile("error.log"):
            with open("error.log", "a") as f:
                f.write(str(e) + '\n')
        else:
            with open("error.log", "w") as f:
                f.write(str(e) + '\n')
