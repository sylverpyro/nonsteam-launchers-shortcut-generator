#!/usr/bin/python3

# Attribution: Cribbing occuring from https://github.com/chyyran/SteamShortcutManager/blob/master/steam_shortcut_manager.py
# This will encumbers this program with the MIT license

# Reference: Steam developer documentation on the non-steam game shortcut file format: https://developer.valvesoftware.com/wiki/Add_Non-Steam_Game

# Needed to open, read, and write files
import sys
# Needed to normalize filesystem paths
import os
# Needed to leverage Regex searches of the shortcut file
import re

# Define some short-hand for the binary speerators used in the VDF format
#  https://developer.valvesoftware.com/wiki/Add_Non-Steam_Game
# Null (NUL)
x00 = u'\x00'
# Start of Heading (SOH)
x01 = u'\x01'
# Backspace (BS)
x08 = u'\x08'
# Line Feed (LF)
x0a = u'\x0a'
# Start of Text (STX)
x02 = u'\x02'

class NonSteamShortcut:
  def __init__(self, displayName, targetExe, startIn='', launchOptions=''):
    pass

class shortcutsVDF:
  def __init__(self):
    self.shortcutsPath = "/home/sylverpyro/example-shortcuts.vdf"
    print("shortcut file init: {}".format(self.shortcutsPath))

  def readShortcuts(self):
    contents = open(self.shortcutsPath, "r").read()
    #contents = shortcutsFile.read()
    #shortcuts = re.search("\u0000[0-9]+\u0000", contents)
    shortcuts = re.search(r"\u0000shortcuts\u0000(.*)\u0008\u0008$", contents)
    for entry in shortcuts:
      print("Entry: {}".format(entry))
    shortcutsFile.close()

def main():
  print("starting main")
  nonsteamShotcutsFile = shortcutsVDF()
  nonsteamShotcutsFile.readShortcuts()

if __name__ == '__main__':
  main()