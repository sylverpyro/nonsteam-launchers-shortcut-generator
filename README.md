# nonSteam-launchers-shortcut-generatorn (nssg)
Project to create links in Steam for all non-Steam storefront games that are installed.  Primary target is Linux/SteamOS/SteamDeck.

This is mainly a personal project, but I imagine that this would be useful for other SD and SteamOS users, so I'm going to try to make it flexible

## Current Tool State
A BASH version of the tool that scans known major Non-Steam storefronts and outputs (stdout) the data to manually create Steam shortcuts for each [is complete](nssg.sh).  However I realized that trying to write a VDF serializer in BASH was a complete fools errand.

So: I am working on porting the tool to Python which has at least one known good VDF serialization library.  It also has at least one known good SteamGridDB wrapper, so once I get to the point of searching/setting artwork that will be much easier.

## Why
Personal experience: Directly installing the non-Steam storefronts has proven to be the most reliable way to play non-Steam games on SteamOS (Heroic and Lutris frequently have problems installing or launching games, vs the native storefronts which - unless the storefront is broken fundamentally in Proton - always tend to work as expected)

### But why not just use NonSteamLaunchers-On-Steam-Deck?
Moraroy's project NonSteamLaunchers On Steam Deck (NSLOSD) for automatically installing all major native game storefronts/launchers on the Steamdeck is fantastic.  I use it to install the storefronts myself.  It got even better in 3.x when it added a python script to scan and add games from those storefronts directly to your Steamdeck library as a Linux Service.

In a lot of ways, that script has scooped part of the intent of this project.  Just use NonSteamLaunchers-On-Steam-Deck's python script and you're all set.

However: 
* The tool in NSLOSD is directly targeted at the paths that NSLOSD creates and manages
  * Meaning: if you don't use NSLOSD to install your storefronts, the tool will not work for you
* NSLOSD is targeted directly at the SteamDeck/SteamOS
  * Chances of it supporting any other OS in the future are very slim to be sure

### What about other existing projects?
#### Steam Shortcut Manager
* https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager
* Written in Python 2.7 (needs modernizing)
* Is really a front end to writing out changes to shortcuts.vdf
* Doesn't set Proton, Artwork, ect.
* Can't be used to remove an existing shortcut if needed
* May be a path way to for, updating it to 3.x, and extending it to have the additional features...

#### BOILR
* https://github.com/PhilipK/BoilR
* Written in RUST so nice an modern (and memory safe)
* Currently works best and most consistently on Windows
* SteamOS/Linux: Lacks the ability to configure/point the application at the install prefix
  * There is an open issue for this however

#### All the above and others I have looked at

All the existing projects lack a few key items that bother me a LOT
- Cutomizing the collections in Steam that are created for each storefront
  - e.g. Call the collection for games from EGS `NSL: EGS` (or something else wild)
- Lack of management of existing shortcuts created by the tool
  - e.g. I change my mind and want the tool to use `Non-Steam games: EGS` and have the tool move them automatically
- Lack of pruning/removed game management
  - e.g. I uninstall Hadies from EGS, the tool should detect this and remove the Hades EGS shortcut (but leave, for example, the GOG shortcut alone)

## Research and references
Accumulated research of where various storefronts store data about games they have installed and extracting the necessary data to create a Steam shortcut

See [per-storefront shortcut formatting and installed games locations](docs/non-Steam-shortcuts.md)

## External Libs
Full credit to https://github.com/moraroy for fidning all of these first for the https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck project

### VDF Serialization
* vdf serialization lib: https://github.com/ValvePython/vdf

### SteamGridDB Support
* python wrapper for Steamgrid: https://github.com/ZebcoWeb/python-Steamgriddb
* urllib3:  https://github.com/urllib3/urllib3
* requests: https://github.com/psf/requests


## Status
### [Pre-0.1 BASH Script](nssg.sh)
This was a proof of concept to show that shortcut data could be extracted and generated from on-disk information for each major storefront.
It does not add anything to Steam, but does output all the information necessary to add each detected game to Steam by hand
#### Working:
* Generate text help for creating shortcuts for all installed EGL, GOG, EA, Ubisoft, and Amazon
* Works on SteamDeck with stock installs from NonSteamLaunchers project
* Works on non-SteamDeck Linux as long as Steam folder is symlink'd to ~/.local/shared/Steam

#### Not Working:
- Detection of games that were installed but are now uninstalled is spotty (EA at least is fixed)
  - Does not (currently) advise that a game was uninstalled so the shortcut should be removed (roadmap)
- Battle.net and any other platform not listed in 'working'

Other functionality is listed in Roadmap

## 1.0 Roadmap

### 0.1 - Basic functionality
- Detect games installed from EGL
- Output human readable shortcut generation data from EGL
- Add shortcut data to Steam shortcuts.vdf
- Add shutcuts to custom collection based on storefront
- Identify and list out shutcuts managed by nssg
- Insert missing games into Steam shortcuts.vdf
- Identify shortcuts under managment vs shortcuts added by user or other tools
  - Probably: Add to custom hidden collection
- Optionally relaunch Steam to force reload of shortcuts.vdf

### 0.2 - Proton config fuctionality
- Set Proton-Experimental for shortcuts when added

### 0.3 - Removal functionality
- Remove shortcuts when game from EGL is removed
- Remove associated proton config

### 0.4 - Additional Major Stores, Duplicates, and Store Images
Storefronts
- Support for GOG
- Support for EA
- Support for Ubisoft
- Support for Battle.net

Storefront image data
- If a store provides game ico, hero, logo, ect. link imges to shortcuts.vdf as well

Duplicate support
- Handle multiple storefronts providing the same game

### 0.5 - Customization
- Config file support for storefronts
  - Windows: Specify location of storefront install paths
  - Linux/SteamOS: Specify location of storefront install PFX
- Specify per-storefront game defaults
  - Proton version to use
  - Library collection to use
- Specify per-storefront launcher details
  - Specify proton version to use with each storefront

### 0.6 - Auto-Detection
- Linux/SteamOS: Auto search and detect compdata/pfx folders for storefronts
- Windows: Auto search/detect install location of storefronts

### 0.7 - Decky Integration
- Figure out how to use Decky to launch tool for updates
  - Probably just with the Decky BASH exec plugin
- Document, --decky flag for headless running

### 0.8 - Minor and Indy storefronts
- Support for Amazon
- Support for itch.io

### 0.9 - Improved Proton/Wine/Proton-GE support
- Detection for nonSteam Proton/Wine versions
- Allow selection of non-Steam Proton/Wine for storefronts

### 1.0 - Main Release Goal
- All previuos milestones complete

## 1.x - Wishlist
SteamGrid Support
- Auto search and fetch SteamGrid icon, hero, logo, ect.
- Configuration support for auto-selection behaviour

More Storefront Support
- Xbox (PC) / Windows Store
- ...

## 2.x - Wishlist
Universal Steam-As-Universal-Library
- i.e. what GOG promised with Galaxy 2.0 but then left the plugin community out in the cold
- SteamDeck/SteamOS users: now you don't have to launch each storefront to insall a game, you can just click on the game shortcut and it will launch the correct storefront for you
- Create shortcuts for NON-INSTALLED games from storefronts
  - non-installed game shortcuts launch game installer from storefront
- Find a way to indicate installed vs. non-installed as Steam doesn't natively reflect this for non-Steam shortcuts

## Not on roadmap / may not address
- Support for game-per-compatdata/prefix with seperate storefront prefix
  - Both detecting these and generating the proper links likely a nightmare
  - I don't even know if this is a thing/would be possible (at least with todays Proton)
- Support for Heroic or Lutris installed games
  - Both of these have built-in Steam shortcut generation already
  - Would be a pain as Heroic and Lutris expect the game they install to be launched though them, so it would be setting a Steam shortcut to launch Heroic or Lutris (which they do already)
- Roms
  - There's tons of great tool for this already (Steam Rom Manager)
- OSX Support
  - I'm not an OSX user
  - I don't know THAT many OSX users playing games though Steam AND alternative storefronts
