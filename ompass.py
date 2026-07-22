#!/usr/bin/python3


import sys
import termios
import time


def print_log(mode:str, *args, sep:str=" ", end:str"\n"):
    r"""Print a message to stderr with a preceding type specifier.
    
    All arguments other than `mode` mirror those of the `print()`
    builtin.
    
    mode:str: [DEIW] First character of message type
    """
    match mode:
        case "D": typestr:str = "36mDEBUG"
        case "E": typestr:str = "31mERROR"
        case "I": typestr:str = "32mINFO"
        case "W": typestr:str = "33mWARN"
        case _: typestr:str = "30m    "
    
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
