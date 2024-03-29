import os
import PySimpleGUI as sg
import psutil


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


def launcher():
    """Launches the AWC.exe and/or if it is already running"""

    # Gets process list
    process_list = get_all_process()

    # Set process running
    awc_running = False

    # Cycles through active processes and compares by name
    try:
        for proc in process_list:
            try:
                # Tries to launch either the update or the exe itself
                if proc["name"] == "AWC.exe":
                    awc_running = True
                    os.system("Updater.exe")
                    break

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if awc_running is False:
            os.system("AWC.exe")

    # Logs all errors
    except Exception as e:
        sg.PopupError("An Error has occurred! Could not start Program!")
        if os.path.isfile("error.log"):
            with open("error.log", "a") as f:
                f.write("AWC_Launcher.exe - ERROR: " + str(e) + '\n')
        else:
            with open("error.log", "w") as f:
                f.write("AWC_Launcher.exe - ERROR: " + str(e) + '\n')


if __name__ == "__main__":
    launcher()
