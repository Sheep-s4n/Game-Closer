import wmi
import time 
import sys 
from dragonfly import Window
import os
import json


# defaults
ask_on_run = True # if true processes, time_to_wait and optional_end_message won't be used
processes = [""]
time_to_wait = 30 # in minute
optional_end_message = "Go to work you slacker!"

# will not be asked on run
shutdown_pc = True
invisible_terminal = False





def printWarning(info):
    print(f"\x1b[33mWarning: {info}\x1b[0m")

if shutdown_pc:
    printWarning("The pc will be shuted down after the countdown")

    # wont check the next condtition if there is less or 1 arg thanks to the 'and' operator 
if len(sys.argv) > 1 and (sys.argv[1] in ["--help","-h"]):
    print("Usage: python main.py [processes files names (comma between each process)] [time to wait] [end message]")
    print("Example: python main.py \"genshin, minecraft\" 20 \"close genshin or/and minecraft after 20 min\"")
    print("Note: if an arguments isn't provided, the default one will be used instead")
    sys.exit(1)

processes = sys.argv[1].replace(" " , "").split(",")  if len(sys.argv) >= 2 else processes
time_to_wait = int(sys.argv[2]  if len(sys.argv) >= 3 else time_to_wait)
optional_end_message = sys.argv[3]  if len(sys.argv) >= 4 else optional_end_message


if ask_on_run:
    processes = input("Enter the processes names (comma between each process): ").replace(" " , "").split(",")
    time_to_wait = int(input("Enter the time to wait for closing the process: ") or 0)
    optional_end_message = input("Enter the optional end message: ")
    print("\n-------------------\n")

SECONDS_IN_MINUTE = 60

def printInfo(info):
    print(f"\x1b[32mInfo: {info}\x1b[0m")

def printError(error):
    print(f"\x1b[31mError: {error}\x1b[0m")

def killProcess(p_name ,process_array):
    printInfo(f"Searching for {p_name} process")

    found_process = False
    try:
        for process in process_array:
            if p_name.lower() in process.name.lower():
                printInfo(f"Found {p_name}({process.name}) process")
                process.Terminate()
                printInfo(f"Terminating {p_name} process...")
                found_process = True

        if not found_process:
            printError(f"Couldn't find {p_name} process")
            printInfo(f"Searching for {p_name} UWP app window instead")
            windows = Window.get_matching_windows(title=p_name)
            if (len(windows) != 0):
                printInfo(f"Closing {p_name} UWP app windows...")
                for window in windows:
                    Window.close(window)
            else :
                printError(f"Couldn't find {p_name} UWP app window")
    except:
        print("\x1b[?25h")  # get back cursor when pressing ctrl+C for exiting

# --------- Script ---------- #
try: 
    if not processes or processes[0] == "": 
        printError("Enter a process name")
        exit()
    print("\x1b[2J\x1b[H") # clear the screen and put cursor to beginning in order to remove the user input

    file = open("data.json" , "a+")
    if os.stat("data.json").st_size == 0: 
        file.write('{\n\t"spawn_process" : false\n}\n')
        file.close()
        file = open("data.json" , "a+")
    else : file = open("data.json" , "a+")
    data = json.load(file)
    print(data)
    if data.get("spawn_process") == None:
        printError("Something went wrong when fetching data (data.json)")
    else:
        json.dump({"spawn_process" : False}, file)

    for i in range(time_to_wait):
        if i == 0: 
            print("\x1b[?25l") # for new line when moving cursor up + hide cursor
        time_unit = "minutes" if time_to_wait - i > 1  else "minute"
        # need to clear the previous line before writing !!!!!
        if len(processes) < 1:
            print(f"\x1b[1A\x1b[2K\x1b[33m #  Time: {time_to_wait - i} {time_unit} left until closing {processes[0]} process\x1b[0m") # \x1b[ = ANSI escape sequences |||| 1A move cursor up one time ||| 0m reset color ||| 2K = erase the entire line 
        else:
            print(f"\x1b[1A\x1b[2K\x1b[33m #  Time: {time_to_wait - i} {time_unit} left until closing {', '.join(processes)} processes\x1b[0m")
        time.sleep(SECONDS_IN_MINUTE)


    if time_to_wait > 0:
        print("\x1b[2J\x1b[H\x1b[?25h") # clear and make cursor visible again
    # using one process list for all processes in order to increase execution speed
    printInfo(f"Fetching current runnning processes...")
    process_list = wmi.WMI()
    _process_array = process_list.Win32_Process()
    for process in processes:
        killProcess(process , _process_array)

    if shutdown_pc:
        os.system('shutdown -s')
    if optional_end_message != "":
        print(f"\x1b[1;32m{optional_end_message}\x1b[0m")
    user_input = input("Press enter to exit...")
except KeyboardInterrupt:
    print("\x1b[?25h") # get back cursor when pressing ctrl+C for exiting
except Exception as e:
    printError(f"python --> {e}")
    print("\x1b[?25h") # get back cursor
