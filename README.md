# nonsteam-launchers-shortcut-generatorn (nssg)
Project to create links in Steam for all non-steam storefront games that are installed.  Primary target is Linux/SteamOS/SteamDeck.

This is mainly a personal project, but I imagine that this would be useful for other SD and SteamOS users, so I'm going to try to make it flexible

## Current Tool State
A BASH version of the tool that scans known major Non-Steam storefronts and outputs (stdout) the data to manually create Steam shortcuts for each [is complete](nssg.sh).  However I realized that trying to write a VDF serializer in BASH was a complete fools errand.

So: I am working on porting the tool to Python which has at least one known good VDF serialization library.  It also has at least one known good SteamGridDB wrapper, so once I get to the point of searching/setting artwork that will be much easier.

## Why
Personal experience: Directly installing the non-steam storefronts has proven to be the most reliable way to play non-steam games on SteamOS (Heroic and Lutris frequently have problems installing or launching games, vs the native storefronts which - unless the storefront is broken fundamentally in Proton - always tend to work as expected)

### But why not just use NonSteamLaunchers-On-Steam-Deck?
Moraroy's project for automatically installing all major native game storefronts/launchers on the steamdeck is fantastic.  It got even better in 3.x when it added a python script to scan and add games from those storefronts directly to your steamdeck library as a Linux Service.

In a lot of whys, that has scooped the intent of this project.  Just use NonSteamLaunchers-On-Steam-Deck's python script and you're all set.

However: 
* The tool in NSLOSD is directly targeted at the paths that NSLOSD creates and manages
  * Meaning: if you don't use NSLOSD to install your storefronts, the tool will not work for you
* NSLOSD is targeted directly at the SteamDeck/SteamOS
  * Chances of it supporting any other OS in the future are very slim to be sure

### What about other existing projects?
Steam Shortcut Manager
* https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager
* Written in Python 2.7 (needs modernizing)
* Is really a front end to writing out changes to shortcuts.vdf
* Doesn't set Proton, Artwork, ect.
* Can't be used to remove an existing shortcut if needed
* May be a path way to for, updating it to 3.x, and extending it to have the additional features...

## Research and references
Accumulated research of where various storefronts store data about games they have installed and extracting the necessary data to create a steam shortcut

See [per-storefront shortcut formatting and installed games locations](docs/non-steam-shortcuts.md)

## External Libs
Full credit to https://github.com/moraroy for fidning all of these first for the https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck project

### VDF Serialization
* vdf serialization lib: https://github.com/ValvePython/vdf

### SteamGridDB Support
* python wrapper for steamgrid: https://github.com/ZebcoWeb/python-steamgriddb
* urllib3:  https://github.com/urllib3/urllib3
* requests: https://github.com/psf/requests


## Status and Roadmap
Pre-0.1 BASH Script

Working:
* Generate text help for creating shortcuts for all installed EGL, GOG, EA, Ubisoft, and Amazon
* Works on SteamDeck with stock installs from NonSteamLaunchers project
* Works on non-SteamDeck Linux as long as Steam folder is symlink'd to ~/.local/shared/Steam

Not Working:
- Detection of games that were installed but are now uninstalled is spotty (EA at least is fixed)
  - Does not (currently) advise that a game was uninstalled so the shortcut should be removed (roadmap)
- Battle.net and any other platform not listed in 'working'

Other functionality is listed in Roadmap

### Roadmap
0.1
- Re-write in Python
- Support for MAJOR storefronts
  - Starting with: EGL, GOG, EA, Ubisoft, Battle.net, Amazon
- Output accurate data for generating steam links for all installed games

 0.2
- Support for detecting proton and GE-Proton instances for generating steam VDF data
  - After some reasearch, this may require, or at lest necessitate, switching this to Python so I don't need to implement a bash-parser for the Valve DataFormat which exists in Python and Rust already
- Support for setting preferred Proton/GE-Proton version (default will likely be Ge-Proton-LATEST, then Proton-LATEST)

0.4
- Detect if a shortcut is already in shortcuts.vdf or not and add if missing

0.5
- Support for other storefronts: itch.io
- Support for detecting if a game has been uninstalled and remove shortcuts automatically from shortcuts

0.6
- Switchable compatdata folder paths
- config file support (stores paths compatdata folders)
- support for compatdata/storefront install folders on sdcard

0.7
- Auto Detect compatdata folders for all storefronts

0.8
- Windows Support ** (currently wishful thinking)

0.8
- Document how to run via the scripts shortcut in Decky so you can update the game library on the fly
- Support for re-starting Steam if the shortcuts.vdf file was updated

1.0
- All pre 1.0 features stable

1.1
- Support for bulk updating the Proton version on all shortcuts generated by this tool

1.2
- Generate Icon links for shortcuts if game comes with official icon(s)
  - Some stores provide these, some do not

1.3
- Auto-fetch image data from SteamGridDB

2.0
- All pre 2.0 features stable

3.0
- Create shortcuts for NON-INSTALLED games (i.e. library)
  - Set shortcuts to install & launch the game if selected

## Not on roadmap / may not address
- Support for game-per-compatdata/prefix
  - Both detecting these and generating the proper links likely a nightmare
  - If someone knows even how to generate the links for this (so they use one common instance of the storefront but launch out of individual prefixes let me know - I don't think this would work though)
- Support for Heroic or Lutris installed games
  - Both of these have built-in steam shortcut generation already
- Roms
  - There's tons of great tool for this already (Steam Rom Manager)
- Windows and OSX Support
  - There's not a lot of bulk import tools out there for either platform
  - Very well may some day make a python version that works on Windows
  - This is EXTREMELY low priority and likely will only occur after 2.0
