# Goals
1. Document how to manually create shortcuts for Steam to launch games from all major non-steam storefronts using their native launcher for save support
   - Epic, GOG, Ubisoft, EA (App)
2. Script generation of shortcut fields
   - https://github.com/sylverpyro/steamdeck-setups/blob/main/nonsteam-game-shortcut-generator.sh
3. Script addition of shortcuts directly to Steam's shortcuts VDF file
4. Investiage other launchers/app stores
   - itch.io, Battle.net, Amazon Games

Per-Store Notes and Resources
* [Epic Games](#epic-games)
* [Uplay / Ubisoft Connect](#uplayubisoft-connect)
* [GOG](#gog)
* [EA App (formerly Origin)](#ea-app)
* [Amazon Games / Prime Gaming](#amazon-games)

Misc Resources
* [References](#references)

# Per-Store Resources
## Epic Games
NOTES

Even with properly created shortcuts, it's not possible to exit a game and have the EGL close automaticaly
  * To 'stop' the game in steam you'll need to manually close the EGL
  * This is actually a semi-good thing as if the game has cloud saves implemented though EGL, the EGL needs time post-shutdown to sync the new save files
  * It theoreticaly would be possible to launch the game via a script then close the EGL once the game exits

To improve Gamepad supprot it's a good idea to disable the EGL-Overlay by renaming it's binaries
  * See below for how to do that


## Shortcut Data from EGL
Windows link example: 
```
com.epicgames.launcher://apps/ff50f85ed609454e80ac46d9496da34d%3A9c7c10e8e1a648f8a9e35f28a1d45900%3Af7a0ebb44f93430fb1c4388a395eba96?action=launch&silent=true
```
Generic: 
```
com.epicgames.launcher://apps/NamespaceId%3AItemId%3AArtifactId?acton=launch&silent=true
Field Seperator = %3A
```
Loop Hero ID combination: 
```
ff50f85ed609454e80ac46d9496da34d %3A 9c7c10e8e1a648f8a9e35f28a1d45900 %3A f7a0ebb44f93430fb1c4388a395eba96
```
Hadies ID combination:  
```
min %3A fb39bac8278a4126989f0fe12e7353af %3A Min
```

## Game ID sources
All installed games list:  `C:\ProgramData\Epic\UnrealEngineLauncher\LauncherInstalled.dat`
   * InstallLocation == InstallLocation
   * NamespaceId == NamespaceId
   * ItemId == ItemId
   * ArtifactId == ArtifactId

Manifest file per installed game: `C:\programData\Epic\EpicGamesLauncher\Data\Manifests`
   * InstallLocation == InstallLocation 
   * CatalogNamespace == NamespaceID
   * CatalogItemId == ItemID
   * AppName == ArtifactID

Individual App IDs: `C:\Program Files\Epic Games\GAME_NAME\.egstore\*.mancpn`
  * CatalogNamespace == NamespaceID
  * CatalogItemId == ItemID
  * AppName == ArtifactID


## Disable Overlay
This only affects in-game notifications and chat.  It will not disable cloud services like cloud save.  It WILL interfeer with the Steam Overlay though so it's a good idea to disable this.
* Rename both:
   * `C:\Program Files (x86)\Epic Games\Launcher\Portal\Extras\Overlay\EOSOverlayRenderer-Win64-Shipping.exe`
   * `C:\Program Files (x86)\Epic Games\Launcher\Portal\Extras\Overlay\EOSOverlayRenderer-Win32-Shipping.exe`

## Creating Steam Shortcuts
Steam Shortcut (Windows) For Hades:
   * Target: `"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"`
   * Start In: `"C:\Program Files (x86)\Epic Games\"`
   * Launch Options: `%command% -com.epicgames.launcher://apps/min%3Afb39bac8278a4126989f0fe12e7353af%3AMin?action=launch&silent=true`

Steam Shortcut (SteamOS) For Hades:
   * Target: `"/home/deck/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"`
   * Start In:  `"/home/deck/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games"`
   * Launch Options: `STEAM_COMPAT_DATA_PATH="/home/deck/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/" %command% -com.epicgames.launcher://apps/min%3Afb39bac8278a4126989f0fe12e7353af%3AMin?action=launch&silent=true`

## Uplay/Ubisoft Connect
NOTES:
* The %command% to launch a game will exit immediately but will still launch the game
* Needs to be tested if it works as intended on SteamDeck
* Ubisot Connect will not work (or only work randomly) without OS settings to allow MTU probing 

MTU Probing Fix for Ubisoft Connect
```
sudo sysctl -w net.ipv4.tcp_mtu_probing=1
echo net.ipv4.tcp_mtu_probing=1 | sudo tee /etc/sysctl.d/zzz-custom-mtu-probing.conf
```

### Installed Game List
Installed List: `C:\Program Files (x86)\Ubisof\Ubisoft Game Launcher\data`
* NOTE: This just contains folders for each game ID but there's no way to correlate the entries to a game without RegEdit

### Application IDs
As of now, there's been no identified on-disk file to correlate the GameID to a game name

haoose@github has complied a list of game IDs here
* List of UPlay app IDs: https://github.com/Haoose/UPLAY_GAME_ID  

The only definitive way to match game names to game IDs on WINDOWS is via regedit.  However! Wine stores the registry data for the windows prefixes in plain text files at the root of the wine prefix path! 

From: https://wiki.winehq.org/Regedit
> Note: Although Wine stores the registry as text files (specifically $WINEPREFIX/*.reg), you should use the regedit tool for making changes to the registry, just like you would on Windows. This is because of, amongst other things, the special encoding used to store keys.

Because all we want to do is READ registry data, on Linux we can use any text processort to read back the contents and find the keys we want:

#### Linux SteamOS searching Wine-Windows registries
```
prefix="/home/deck/links/compatdata/UplayLauncher/pfx"
reg_file="$prefix/system.reg"

# NOTE: the registry structure for this key is pretty well
#       defined so we can return ALL data for the key by
#       using grep -A 11.  It'd be better to find the line
#       number of the key, then search starting at that line
#       number for the data we want, but I don't know how
#       to do that in awk or sed very well at this time
id=3279; grep "Uplay Install $id" -A 11 "$reg_file"

# Get the display name of the game
id=3279; grep "Uplay Install $id" -A 11 "$reg_file" | grep ^'"DisplayName"=' | cut -d '"' -f 4

# The display icon path (windows rooted path)
id=3279; grep "Uplay Install $id" -A 11 "$reg_file" | grep ^'"DisplayIcon"=' | cut -d '"' -f 4

# Install path (windows rooted path)
"InstallLocation"="C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games/Steep/"
```


#### Windows 'native' regedit search on Linux
Registrysearch: 
* https://wiki.winehq.org/Regedit
* https://steamcommunity.com/app/221410/discussions/0/1736589519989298578/
```
STEAM_LIBRARY = Your local default games library, usually under $HOME/.local/share/Steam/steamapps/
PROTON_BIN_PATH=$STEAM_LIBRARY/common/Proton 3.7/dist/bin/wine
env $WINEPREFIX=$STEAM_LIBRARY/compatdata/APPID/pfx $PROTON_BIN_PATH regedit

# Test
ptwine=/home/deck/.local/share/Steam/steamapps/common/Proton\ 8.0/dist/bin/wine
uplay_pfx="/home/deck/links/compatdata/UplayLauncher"
gameid=""
env $WINEPREFIX="$uplay_pfx" "$ptwine" regedit

# Search for a known ID and revolve it to a game name and it's install path
ID=410 env $WINEPREFIX=$STEAM_LIBRARY/compatdata/APPID/pfx $PROTON_BIN_PATH regedit /E /tmp/uplay.$ID.name "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\UPlay Install $ID\DisplayName"
ID=410 env $WINEPREFIX=$STEAM_LIBRARY/compatdata/APPID/pfx $PROTON_BIN_PATH regedit /E /tmp/uplay.$ID.path "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\UPlay Install $ID\InstallLocation"
ID=410 env $WINEPREFIX=$STEAM_LIBRARY/compatdata/APPID/pfx $PROTON_BIN_PATH regedit /E /tmp/uplay.$ID.ico "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\UPlay Install $ID\DisplayIcon"
```

### UPlay Shortcuts
```
"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\Uplay.exe" "uplay://launch/410/0"
```
Generic version
```
"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\Uplay.exe" "uplay://launch/APPLICATION_ID/0"
```

### Steam Shortcuts
Windows Shortcut (Child of Light):
* Target: `"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\UbisoftConnect.exe"`
* Start In: `"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher"`
* Launch Options: `%command% uplay://launch/609/0`

## GOG

### Game IDs
Game IDs are accessiable in each game's folder either in .info files OR in the name of the `goggame-GAMEID.ico` file.

* There's a problem with the .info files in that for games with DLC, the game folder will contain MULTIPLE .info files.  The DLC info files will have both a 'name' and 'rootName' key that have to be correlated to figure out which .info file is the 'main game'.

* With .ico files, there is always only ever ONE goggame-GAMEID.ico file per game, so it's simpelest to just extract the GAMEID from the filename of this ico file

Installed Directory:  `C:\Program Files (x86)\GOG Galaxy\Games\GAME`

ICO file: `C:\Program Files (x86)\GOG Galaxy\Games\GAME\goggame-GAMEID.ico`

### Game Path
The GOG launcher requires an argument that points to the folder of the game, referenced from a root drive letter (i.e. `C:\`)

By default games are installed at
````C:\Program Files (x86)\GOG Galaxy\Games\GAME````

### Steam Shortcuts
Windows Shortcut:
* Target : `"C:\Program Files (x86)\GOG Galaxy\GalaxyClient.exe"`
* Start In : `"C:\Program Files (x86)\GOG Galaxy\"`
* Launch Options : `%command% /command=runGame /gameId=1237807960 /path="C:\Program Files (x86)\GOG Galaxy\Games\Dead Cells"`
* NOTE: `/command=runGame` (not launch)  

SteamOS Shortcut
* Target: `"/home/deck/.local/shared/Steam/steamapps/compatdata/GOGGalaxy/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"`
* Start In: `"/home/deck/.local/shared/Steam/steamapps/compatdata/GOGGalaxy/pfx/drive_c/Program Files (x86)/GOG Galaxy"`
* Launch Options: `%command% /command=runGame /gameId=1237807960 /path="C:\Program Files (x86)\GOG Galaxy\Games\Dead Cells"`
* NOTE: The /path= option requies the windows-like path to the game install directory relative to drive_c in the wine prefix to work as windows exe's are chroot'd to the drive_c of the prefix

## EA App
NOTES: 
* Games appear to have launching the EA App baked into their EXE files so there's not much custom to do there

### EA App install location
`/home/deck/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe`

### Installed Game List
The Install directory for games is at
* `/home/deck/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/EA Games`

### Display Name
Three options:
1. Strip off the install directory (may not always be fully accurate, but it's at least consistent unlike the other options...)
   * /home/deck/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/EA Games/Burnout Paradise
2. Pull out of system.reg
   * `grep '[Software\Wow6432Node\EA Games' /home/deck/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/system.reg`
   * Problems: 
     - It appears that some games get MULTIPLE registry entries, so the results would need to be de-duplicated by 'Install Dir'
     - The DisplayName differs in some of the multiple registry instances
     - Not all games provide accurate data in the display name field
3. Pull from game's installerdata.xml file
   * `/home/deck/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/EA Games/Burnout Paradise/__Installer/installerdata.xml`
   * `grep "<launcher uid=\"1-3\">" installerdata.xml -A 20 | grep "<name locale=\"en_" | tr '<' '>' | cut -d '>' -f 3 | head -n 1`
   * Problems
     - It appears that the format and contents of the installer xml file vary from game to game so it's not actually a good source of data

### Game EXE
NOTE: Because the EA app does does not use a custom launch option to run games though the launcher (that functionality appears to be baked into every exe the EA store ships) we just need to launch the EXE file.  However we do need to know which EXE file is the game, and which ones are game config launchers.

The best place (again) to find this is in the __Installer/installerdata.xml file
```
grep "<launcher uid=\"1-3\">" installerdata.xml -A 20 | grep -o "\].*</filePath>" | tr ']' '<' | cut -d '<' -f 2
```

### Game IDs (unused)
NOTE: These are currently not needed, but figured I'd document them
* New EA path path-based IDs `C:\ProgramData\EA Desktop\InstallData\GAME`
  * Each GAME folder has a sub folder with the game ID in the title of the folder
* Old (defunct) Oring manifest files with IDs `C:\ProgramData\Origin\LocalContent\*.mfst`
```
# .mfst file contents example
?activerepair=0&autoresume=0&autostart=0&buildid=&contentversion=1&currentstate=kReadyToStart&ddinitialdownload=0&ddinstallalreadycompleted=0&dipInstallPath=&dipinstallpath=C%3a%5cGames%5cOrigin%5cCommand%20and%20Conquer%20Generals%20Zero%20Hour&downloaderversion=9.0.0.0&downloading=0&dynamicdownload=0&eula____installer_directx_eula_en_us_txt=2103371362&eula____installer_vc_vc2005sp1_eula_en_us_txt=602589686&eula____installer_vc_vc2010sp1_eula_en_us_rtf=774049465&eula__support_eula_en_us_eula_rtf=2269322523&eulasaccepted=1&gamemovedto=&id=OFB-EAST%3a52209&installdesktopshortcut=1&installerchanged=0&installstartmenushortcut=1&isitoflow=0&islocalsource=0&ispreload=0&isrepair=0&jobID=&jobid=%7bc1f40d67-c30a-488c-b8f5-cb5f50152aa8%7d&locale=en_US&movegameto=&moveorlocate=&optionalcomponentstoinstall=0&paused=0&previousstate=kCompleted&repairstate=&savedbytes=2290410931&stagedfilecount=0&totalbytes=3209029103&totaldownloadbytes=2290410931

Importnat part: `&id=STRING%3ASTRING` == `&id=OFB-EAST%3a52209`
```
### EA App Shortcuts

#### Steam Shortcut
Windows Shortcut (Peggle): 
* Target: `"C:\Program Files\EA Games\Peggle Deluxe\Peggle.exe"`
* Start In: `C:\Program Files\EA Games\Peggle Deluxe\`
* Launch Options: (none)

SteamOS Shortcut (Peggle):



## Amazon Games
### Windows shortcuts
#### for Amazon game launcher/store
```
Target: "C:\Users\sylverpyro\AppData\Local\Amazon Games\App\Amazon Games.exe"
Start In: ""
```

#### Shortcut for "Shotgun King"
NOTE: Amazon appears to just interprets web-handler events from the OS in their shortcuts
```
amazon-games://play/amzn1.adg.product.033d4c95-45ea-44ab-9ded-06c8e130efde
```

#### Steam shortcut for AMZ game launcher/store
```
target: "C:\Users\sylverpyro\AppData\Local\Amazon Games\App\Amazon Games.exe"
startin: "C:\Users\sylverpyro\AppData\Local\Amazon Games\App"
launch options:
```

#### Steam shortcut for AMZ "Shotgun King"
Appears to work like every other store/launcher that uses URLs - if you pass the URL as an option to the launcher it will launch the game as expected
```
target: "C:\Users\sylverpyro\AppData\Local\Amazon Games\App\Amazon Games.exe"
startin: "C:\Users\sylverpyro\AppData\Local\Amazon Games\App"
launch options: %command% amazon-games://play/amzn1.adg.product.033d4c95-45ea-44ab-9ded-06c8e130efde
```

### Game names
Two sources:
* Install folder name `C:\Amazon Games\Library\GAME_NAME`
   * GAME_NAME seems to be pretty well formatted but a more definitve source would be nice
* Can also be found in the Registry at
```
Computer\HKEY_USERS\S-1-5-21-531410201-1053027858-3794204300-1002\Software\Microsoft\Windows\CurrentVersion\Uninstall\AmazonGames/Shotgun King - The Final Checkmate
Key: DisplayNName
```
* NOTE: product_data.json does not contain the GAME_NAME

### Game IDs

Two sources:
* Can be located in the Registry at
```
Computer\HKEY_USERS\S-1-5-21-531410201-1053027858-3794204300-1002\Software\Microsoft\Windows\CurrentVersion\Uninstall\AmazonGames/Shotgun King - The Final Checkmate
Key: UninstallString
"C:\\Amazon Games\\Library\\__InstallData__\\Amazon Game Remover.exe" -m Game -p amzn1.adg.product.033d4c95-45ea-44ab-9ded-06c8e130efde
```
* Can also be located in product data json files `C:\Amazon Games\Library\__InstallData__\GAME_NAME\product_data.json`
```
  "ProductId": "amzn1.adg.product.033d4c95-45ea-44ab-9ded-06c8e130efde",

```

Extract on SteamOS with
```
jq -r .ProductId product_data.json
```


# References
Steam VDF (Valve Data File) format docs
* https://developer.valvesoftware.com/wiki/KeyValues#File_Format
* https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki/Steam-Shortcuts-Documentation

Vortext ModWiki list of locations to detect game installations:
* https://modding.wiki/en/vortex/developer/game-detection

Another tinkerer trying to do something similar with just EA App
* https://github.com/kageurufu/steamdeck-tricks/tree/main