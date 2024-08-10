#!/usr/bin/python3
# This is simply a POC of reading and writing data from/to a Valve VDF
# file using one of the community python libraries

# python.exe .\Experiments\vdf_read_and_write.py

# Insert the path to our local Modules folder at the head of the path list
import sys
import os


# Search for our module folder
# This must be done from the top level as imports are scoped per-function
# Depending on if this is run from the parent folder or not changes the path
if os.path.exists("./modules") :
  # This is pre 3.4 compatible
  ex_mods = os.path.abspath('./modules')
elif os.path.exists('../modules') : 
  ex_mods = os.path.abspath('../modules')
else :
  sys.exit('Error: could not find the modules directory at ./modules. Are you running this from the top level of the project?')

# Add it to the sys path so it can be imported
# Should always insert at '1' not '0'
# https://stackoverflow.com/questions/10095037/why-use-sys-path-appendpath-instead-of-sys-path-insert1-path
sys.path.insert(1,ex_mods)
#print(sys.path)

# Load the VDF module
import vdf

def open_and_show_shortcuts():
  import vdf
  # Load the shortcuts file
  shortcuts = vdf.parse(open("./examples/shortcuts_vdf/shortcuts.vdf"))

  # Dump the loaded shortcuts to plain text
  shortcuts_txt = vdf.dumps(shortcuts, pretty=True)

def main():
  print("starting main")
  open_and_show_shortcuts()

if __name__ == "__main__":
  main()