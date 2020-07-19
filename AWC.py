from gui import AWCGUI
from runtime import AWC
import os

__author__ = "Marten Scheuck"

"""This runs the install process."""

# Make from current time or day start time function
# Make days start from this day at midnight
# Tray blocks function of program with while loop

# Make next and previous desktop wallpaper available

if __name__ == "__main__":
    gui_install_update = AWCGUI
    awc = AWC

    if not os.path.isfile("config.cfg"):
        gui_install_update().run()
        awc()
    else:
        awc()

