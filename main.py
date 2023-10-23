import wmi
import time 
import sys 
from dragonfly import Window

# defaults
ask_on_run = True # if true process_name, time_to_wait and optional_end_message won't be used
process_name = ""
time_to_wait = 30 # in minute
optional_end_message = "Go to work you slacker!"

    # wont check the next condtition if there is less or 1 arg thanks to the 'and' operator 
if len(sys.argv) > 1 and sys.argv[1] == "--help":
    print("Usage: python main.py [process file name] [time to wait] [end message]")
    print("Note: if an arguments isn't provided, the default one will be used instead")
    sys.exit(1)

process_name = sys.argv[1]  if len(sys.argv) >= 2 else process_name
time_to_wait = int(sys.argv[2]  if len(sys.argv) >= 3 else time_to_wait)
optional_end_message = sys.argv[3]  if len(sys.argv) >= 4 else optional_end_message


if ask_on_run:
    process_name = input("Enter the process name: ")
    time_to_wait = int(input("Enter the time to wait for closing the process: ") or 0)
    optional_end_message = input("Enter the optional end message: ")
    print("\n-------------------\n")


SECONDS_IN_MINUTE = 60


def printInfo(info):
    print(f"\x1b[32mInfo: {info}\x1b[0m")

def printError(error):
    print(f"\x1b[31mError: {error}\x1b[0m")

def killProcess(p_name):
    printInfo(f"Searching for {p_name} process")

    found_process = False
    process_list = wmi.WMI()
    try:
        for process in process_list.Win32_Process():
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

    if process_name == "": 
        printError("Enter a process name")
        exit()
    else :
        print(f"name: {process_name}")

    print("\x1b[2J\x1b[H") # clear the screen and put cursor to beginning in order to remove the user input
    for i in range(time_to_wait):
        if i == 0: 
            print("\x1b[?25l") # for new line when moving cursor up + hide cursor
        time_unit = "minutes" if time_to_wait - i > 1  else "minute"
        # need to clear the previous line before writing !!!!!
        print(f"\x1b[1A\x1b[2K\x1b[33m #  Time: {time_to_wait - i} {time_unit} left until closing {process_name} process\x1b[0m") # \x1b[ = ANSI escape sequences |||| 1A move cursor up one time ||| 0m reset color ||| 2K = erase the entire line 
        time.sleep(SECONDS_IN_MINUTE)


    if time_to_wait > 0:
        print("\x1b[2J\x1b[H\x1b[?25h") # clear and make cursor visible again
    killProcess(process_name)
    if optional_end_message != "":
        print(f"\x1b[1;32m{optional_end_message}\x1b[0m")
    user_input = input("Press enter to exit...")
except:
    print("\x1b[?25h") # get back cursor when pressing ctrl+C for exiting
