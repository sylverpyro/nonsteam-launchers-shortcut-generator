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
    #self.shortcutsPath = "/home/sylverpyro/prod-steam.vdf"
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
    #nullterms = re.compile(b"(.*?)\x00",re.DOTALL)
    #nullsplits = nullterms.findall(contents)
    #for entry in nullsplits:
    #  print("Entry: {}".format(entry))

    # Regex to find the shortcuts by shortcut number (NUL[0-9]*NUL ... BS BS)
    re_shortcuts = re.compile(b"(\x00[0-9*]\x00[^\x08]*[\x08]{2,})",re.DOTALL)
    shortcuts = re_shortcuts.findall(contents)
    #for entry in shortcuts:
    #  # We can directly decode byte objects on the fly
    #  # https://docs.python.org/3/library/stdtypes.html#bytes.decode
    #  print ("shortcut: {}".format(entry.decode(errors='replace')))
    #  print ("")

    # Now that we have each shortcut sectioned out, we need to parse out each shortcut entry into it's components
    # The easiest way, without using an regex itterator, is to grab ALL of the
    # fields with a single regex, with each field pulled out into a querryable
    # group
    # NOTE: We should have re.DOTALL AND re.VERBOSE in here, but I can't figure
    #       out how to pass two flags to 're.' at the same time, and VERBOSE is
    #       more imporant for readability as VDF files are not allowed to
    #       contain newline characters in the first place
    # Merging flags: x = re.findall(pattern=r'CAT.+?END', string='Cat \n eND', flags=re.I | re.DOTALL)
    re_fields = re.compile(b"""
      \x00(?P<entry_num>[0-9]*)\x00             # |NUL|number|NUL|
      \x02appid(?P<appid_data>[^\x01]*)         # |STX|appid|binarydata|
      \x01appname\x00(?P<app_name>[^\x00]*)\x00 # |SOH|appname|NUL|app name|NUL|
      (?P<remainder>.*)""", re.VERBOSE|re.DOTALL|re.IGNORECASE)
    for entry in shortcuts:
      print ("shortcut: {}".format(entry.decode(errors='replace')))
      fields = re_fields.search(entry)
      print (" Entry     : {}".format(fields.group('entry_num').decode(errors='backslashreplace')))
      print (" Appid Data: {}".format(fields.group('appid_data').decode(errors='backslashreplace')))
      print (" AppName : {}".format(fields.group('app_name').decode(errors='backslashreplace')))
      print (" Unparsed: {}".format(fields.group('remainder').decode(errors='backslashreplace')))
      print ('')

    #re_entrynum = re.compile(b"\x00([0-9]*)\x00",re.DOTALL)
    #re_appid = re.compile(b"\x02([^\x00]*)\x00{1,}")
    #for entry in shortcuts:
    #  entrynum = re_entrynum.search(entry)
    #  print (" Entry: {}".format(entrynum.group(1).decode(errors='ignore')))
    #  appid = re_appid.search(entry)
    #  print (" Appid: {}".format(appid))
    #  print (" Appid: {}".format(appid.group(1).decode(errors='ignore')))
    #  print ("")

    # Binary streams have no close function
    #contents.close()

def main():
  print("starting main")
  nonsteamShotcutsFile = shortcutsVDF()
  nonsteamShotcutsFile.readShortcuts()

if __name__ == '__main__':
  main()