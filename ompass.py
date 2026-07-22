#!/usr/bin/python3
#
# ompass -- local password management and storage
# Copyright (C) 2026 Speedy1894  (speedy1894 --at-- duck --dot-- com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import termios
import time


def print_log(mode:str, *args, sep:str=" ", end:str="\n"):
    r"""Print a message to stderr with a preceding type specifier.
    
    All arguments other than `mode` mirror those of the `print()`
    builtin.
    
    mode:str: [DEIW] First character of message type
    """
    if (mode == "D" and not config["debug"]): return
    
    match mode:
        case "D": typestr = "36mDEBUG"
        case "E": typestr = "31mERROR"
        case "I": typestr = "32mINFO"
        case "W": typestr = "33mWARN"
        case _: typestr = "30m    "
    
    print(f"[\x1b[{typestr}\x1b[39m]", *args,
          sep=sep, end=end, file=sys.stderr)


def safe_input(prompt:str=""):
    r"""Read from stdin with safety for KeyboardInterrupt and EoF.
    
    If either of the above exceptions are raised, they will be handled
    by running `sys.exit()` instead of printing a traceback.
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print(file=sys.stderr)  # Needed to proceed to next line
        sys.exit(130)


def input_pwd(prompt:str="Password (echo disabled):"):
    r"""Read from stdin with the ECHO property disabled."""
    oldattr = termios.tcgetattr(sys.stdin)
    newattr = oldattr.copy()
    newattr[3] &= ~termios.ECHO  # lflags
    
    try:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, newattr)
        out = safe_input(prompt)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldattr)
    
    print()  # Needs the trailing newline
    return out


## VARIABLES
MYVER:str = "0.0.1"
MYNAME:str = "ompass"
config:dict = {
    "location":None
    "debug":False
}
