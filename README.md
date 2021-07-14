[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# AutomatedWallpaperChanger (AWC)
> The AWC program serves as a testrun for how to program on different OS.
> Changes the desktop wallpaper with some widgets.

## Project Status
_Is not currently being worked on_

## Table of contents
* [Features](#Features)
* [Screenshot](#Screenshot)
* [GIFs](#GIFs)
* [Windows-Version](#Windows-Version)
* [Linux-Version](#Linux-Version)
* [Contact](#Contact)

## Features
* Automatically changes the Wallpaper from a previously set folder
* Time spacings can be set and are completely variable
* Runs in the background with very low CPU consumption ~0.%
* Skip function to get next background is available

## Screenshot
GUI-Interface:

![AWC_GUI](./img/AWC_gui.png)

## GIFs
This GIF shows how the updating process works and the wallpapers change:

<img src="./img/UpdatingAWC.gif" width="800">
In this GIF the manual switching mechanic is shown:

<img src="./img/SwitchingWallpaper.gif" width="800">

## Windows-Version

### Installation
The program for the windows version can either be run as a ".py" or a ".exe".
If it is run as an ".exe" then only the compiled installer has to be run.

>The code has been compiled via _pyinstaller_

The code can also be run in python3, however, one needs to fulfill the following dependencies:

* PySimpleGui
* PySimpleGuiQt
* winshell and pywin32 (includes win32con)

Additionally all references to the "AWC.exe" have to be changed to "../AWC.py" as well some other
direct references to ".exe" related files.

## Linux-Version
>Disclaimer the code for this version has not been completed yet.

### Setup
Coming soon

## Contact
Created by Marten B. Scheuck - feel free to contact me
