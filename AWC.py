from gui import AWCGUI
from runtime import AWC
import os

__author__ = "Marten Scheuck"

"""This runs the install process."""

# Fix linker
# Make next and previous desktop wallpaper available

if __name__ == "__main__":
    gui_install_update = AWCGUI
    awc = AWC

    if not os.path.isfile("config.cfg"):
        gui_install_update().run()
        awc()
    else:
        awc()

