from gui import InstallerGUI, AWCGUI
from runtime import AWC
import os

__author__ = "Marten Scheuck"

"""This runs the install process."""

# Make from current time or day start time function
# Make file go into sidetray when executed
# Make days start from this day at midnight

if __name__ == "__main__":
    gui_install = InstallerGUI
    gui_awc = AWCGUI
    awc = AWC

    if not os.path.isfile("config.cfg"):
        gui_install().run()
    else:
        gui_awc().run()

    awc()
