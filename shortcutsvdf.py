#!/usr/bin/python3

# Attribution: Cribbing occuring from https://github.com/chyyran/SteamShortcutManager/blob/master/steam_shortcut_manager.py
# This will encumbers this program with the MIT license

# Reference: Steam developer documentation on the non-steam game shortcut file format: https://developer.valvesoftware.com/wiki/Add_Non-Steam_Game

# Needed to open, read, and write files
import sys

# Needed to normalize filesystem paths
# https://docs.python.org/3/library/os.html#module-os
import os

# Needed to leverage Regex searches of the shortcut file
import re

# Define some short-hand for the binary speerators used in the VDF format
#  https://developer.valvesoftware.com/wiki/Add_Non-Steam_Game
# Null (NUL)
nul = b'\x00'
# Start of Heading (SOH)
soh = b'\x01'
# Backspace (BS)
bs = b'\x08'
# Line Feed (LF)
lf = b'\x0a'
# Start of Text (STX)
stx = b'\x02'

class NonSteamShortcut:
  def __init__(self, displayName, targetExe, startIn='', launchOptions=''):
    pass

class shortcutsVDF:
  def __init__(self):
    self.shortcutsPath = "/home/sylverpyro/example-shortcuts.vdf"
    print("shortcut file init: {}".format(self.shortcutsPath))

  def readShortcuts(self):
    # https://docs.python.org/3/library/functions.html#open
    # NOTE: a VDF file MUST be opened in 'binary' mode in order to
    #       properly handle the binary sequences that valve uses to
    #       seperate fields
    #       We just need to remember to do 'b' (binary) searches from now on
    # This worked different in Python 2 which most python VDF readers were
    # based on - namely python 2 didn't differentiate between binary and
    # character strings
    contents = open(self.shortcutsPath, "rb").read()

    # Example of compiling binary regex seraches and dicts
    # https://code.activestate.com/recipes/181065-parsing-binary-files-with-regular-expressions/
    nullterms = re.compile(b"(.*?)\x00",re.DOTALL)
    nullsplits = nullterms.findall(contents)
    for entry in nullsplits:
      print("Entry: {}".format(entry))

    # Regex to find the shortcuts by 'section number' (shortcut number)
    re_shortcuts = re.compile(b"\x00([0-9*])\x00",re.DOTALL)
    shortcuts = re_shortcuts.findall(contents)
    for entry in shortcuts:
      print ("shortcut: {}".format(entry))

    # Binary streams have no close function
    #contents.close()

def main():
  print("starting main")
  nonsteamShotcutsFile = shortcutsVDF()
  nonsteamShotcutsFile.readShortcuts()

if __name__ == '__main__':
  main()