# Game Closer

# Description
**Game Closer** is a game auto-closing script for Windows. It's designed for people who spend too much time on games and want to stop but have difficulty doing so. Basically, it closes your game after a period of time, so you don't have to force yourself to click on the red cross.

## How it works
1. The script searches for the name of the process you specified and kills it.
2. If it doesn't find the process, it searches for a window with the process name and closes it.

# Prerequisites
You must have [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/cli/pip_download/) installed on your computer to run the script.

# Installation
## 1. Code downloading
In order to use the script, you have to run the `git` command:
```
git clone https://github.com/Sheep-s4n/Game-Closer
```
Or, you can download it manually:


[![download github code example](https://img.shields.io/badge/%20-Download-03c2fc?logo=github&style=for-the-badge&labelColor=333)](https://github.com/Sheep-s4n/Game-Closer/archive/refs/heads/main.zip)


## 2. Dependencies downloading
Run this `pip` command in the directory containing the code so as to install all required dependencies:
```
pip install -r requirements.txt
```
# Usage
## 1. Arguments

You can change default arguments in the script by changing the variables at the top of the script.  

There are 3 arguments that you can provide for running the script:

- **Process name** *(name in script: `process_name`)* - *(default: "")* 
 
  - The process/game name should be the **name of the executable** file that makes the game process, not the game name itself (often they are the same).
  
  - You can also use the **title of the window** created by the process in order to close the game.
  
  - The process/game name isn't case-sensitive, and you can enter only a part of the process name.
    - For instance, if the process name is `ARandomGame.exe`. You could set the process name to `arandomegame.exe`, `arandomegame` or even `randomGame`.
    - ⚠️ **Be careful when shortening process names because it may close unwanted processes** ⚠️

- **Time to wait** *(name in script: `time_to_wait`)* - *(default: 30)*

  - The time to wait for the script to close the game is in **minutes**.

- **Optional end message** *(name in script: `optional_end_message`)* - *(default: "Go to work you slacker!")*
  - A message that will be printed when the script ends. It can be used for example to display a motivational message to do something other than gaming.

## 2. Running the script
To run the `python` script, open a terminal emulator and run the following command:
```
python main.py
```
The variable `ask_on_run` is a boolean that indicates wheter the script should be executed with command line arguments or not.
You can set the `ask_on_run` variable at the top of the script to `False` if you want to run the script with command line arguments.

In order to display the available command line options(arguments) usages and positions, you can run: 
```
python main.py --help
```