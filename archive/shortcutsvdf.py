#!/usr/bin/python3

# Attribution: Cribbing occuring from https://github.com/chyyran/SteamShortcutManager/blob/master/steam_shortcut_manager.py
# This will encumbers this program with the MIT license

# Reference: Steam developer documentation on the non-steam game shortcut file format: https://developer.valvesoftware.com/wiki/Add_Non-Steam_Game

# Needed to normalize filesystem paths
# https://docs.python.org/3/library/os.html#module-os
import os

# Needed to leverage Regex searches of the shortcut file
import re

# Needed to open, read, and write files
import sys

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
    # Originally the goal was to make one giant regex and extract the fields all at once.  However it turns out that some fields are optional and the fields are not required to be in a strict order.
    # So, we need to extract the fields one at a time unfortunately
    # Merging flags: x = re.findall(pattern=r'CAT.+?END', string='Cat \n eND', flags=re.I | re.DOTALL)
    # re.DOTALL     - Include NEWLINE characters in '.' globs
    # re.IGNORECASE - Make matches case-insensitive
    # re.VERBOSE    - Allow for multi-line regexes (no longer used)

    re_number  = re.compile(b"\x00(?P<entry_num>[0-9]*)\x00",re.DOTALL|re.IGNORECASE) # |NUL|number|NUL|
    re_appid   = re.compile(b"\x02appid(?P<appid_data>.{4})",re.DOTALL|re.IGNORECASE) # |STX|appid|<4 values>
    re_appname = re.compile(b"\x01appname\x00(?P<app_name>[^\x00]*)\x00",re.DOTALL|re.IGNORECASE) # |SOH|appname|NUL|Application Name|NUL|

    ## This method ultimately does not work as the fields are not in a fully predictable order
    ## AND they are not all present on all platforms. 
    #re_fields = re.compile(b"""
    #  \x00(?P<entry_num>[0-9]*)\x00             # |NUL|number|NUL|
    #  \x02appid(?P<appid_data>[^\x01]*)         # |STX|appid|data(4-chars)|
    #  \x01appname\x00(?P<app_name>[^\x00]*)\x00 # |SOH|appname|NUL|app name|NUL|
    #  (?P<remainder>.*)""", re.VERBOSE|re.DOTALL|re.IGNORECASE)

    # Print out each field we just extracted, making sure to replace binary data with backslash versions
    for entry in shortcuts:
      print ("shortcut: {}".format(entry.decode(errors='backslashreplace')))
      ## This is the OLD all-fields based method which ultimately does not work
      #fields = re_fields.search(entry)
      #print (" Entry     : {}".format(fields.group('entry_num').decode(errors='backslashreplace')))
      #print (" Appid Data: {}".format(fields.group('appid_data').decode(errors='backslashreplace')))
      #print (" AppName : {}".format(fields.group('app_name').decode(errors='backslashreplace')))
      #print (" Unparsed: {}".format(fields.group('remainder').decode(errors='backslashreplace')))

      number = re_number.search(entry)
      print (" Entry   : '{}'".format(number.group('entry_num').decode(errors='backslashreplace')))

      appid = re_appid.search(entry)
      print (" Appid   : '{}'".format(appid.group('appid_data').decode(errors='backslashreplace')))

      appname = re_appname.search(entry)
      print (" AppName : '{}'".format(appname.group('app_name').decode(errors='backslashreplace')))

      # Print a seperator to visually space out entries
      print ('')

    # Binary streams have no close function
    #contents.close()

def main():
  print("starting main")
  nonsteamShotcutsFile = shortcutsVDF()
  nonsteamShotcutsFile.readShortcuts()

if __name__ == '__main__':
  main()