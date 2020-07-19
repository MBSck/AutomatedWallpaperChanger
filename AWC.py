from gui import InstallerGUI, AWCGUI
from runtime import AWC
import os

__author__ = "Marten Scheuck"

"""This runs the install process."""

# Make from current time or day start time function
# Make file go into sidetray when executed
# Make days start from this day at midnight

# Make next and previous desktop available

if __name__ == "__main__":
    gui_install = AWCGUI
    awc = AWC

    if not os.path.isfile("config.cfg"):
        gui_install().run()
        awc()
    else:
        awc()

