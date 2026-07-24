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

import optparse
import sys
import termios
import time


def print_log(mode:str, *args, sep:str=" ", end:str="\n"):
    r"""Print a message to stderr with a preceding type specifier.
    
    All arguments other than `mode` mirror those of the `print()`
    builtin.
    
    mode:str: [DEIW] First character of message type
    """
    if (mode == "D" and not config.debug): return
    
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


def print_usage(short:bool=False, file=sys.stdout):
    r"""Print a usage message to `file` including all arguments.
    
    If `short` is True, then only the first line ('usage: *') will be
    printed.
    """
    print(f"usage: {MYNAME} [options]", file=file)
    if (short): return
    
    print("options:",
          "  -h --help           print this help message and exit",
          "  -l --location FILE  specify the location of your password file",
          "  -v --version        print version information and exit",
          "  --debug             print debug messages",
          sep="\n", file=file)


def parse_cmdline_args(args):
    r"""Parse the arguments with which the program was invoked.
    
    The return value is a tuple as returned from
    `optparse.OptionParser.parse_args()`.
    """
    parser = optparse.OptionParser(
        prog=MYNAME,
        usage=optparse.SUPPRESS_USAGE,
        add_help_option=False)
    
    def err(*args):
        print_log("E", *args)
        sys.exit(2)
    parser.error = err
    
    parser.add_option("-h","--help", dest="help",
                      action="store_true", default=False)
    parser.add_option("-l","--location", dest="location",
                      action="store", default=None)
    parser.add_option("-v","--version", dest="version",
                      action="store_true", default=False)
    parser.add_option("--debug", dest="debug",
                      action="store_true", default=False)
    
    return parser.parse_args(args)


## VARIABLES
MYVER:str = "0.0.1"
MYNAME:str = "ompass"
config, posargs = parse_cmdline_args(sys.argv[1:])

print_log("D", "config =", config)
print_log("D", "posargs =", posargs)


if (config.help is True):
    print_usage()
    sys.exit(0)
if (config.version is True):
    print(f"{MYNAME} v{MYVER}")
    sys.exit(0)
