#!/usr/bin/python3

# We need pathlib as if we are on Linux we need the ability to manipulate wine prefix paths, which are windows-like.  os.path will only let us manipulate paths that match the underlying OS
import pathlib
# Needed to manipulate 'real' paths as the OS sees them
import os
# Needed to read various storefront manifest files
import json

def defaults(): 
    # All defaults assume a stock Steamdeck config with all data stored
    # in the main steamapps library at $HOME/.local/share/Steam
    # All Storefront defaults assume they were intalled with
    # Non-Steam-Game-Launchers on the main storage device (not sdcard)
    # https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck
    # Support for arbitrary storefront compatdata folders coming in 0.5
    # support for sdcard installed storefronts coming in 0.5

    ## Epic Games Launcher paths
    global egs ; egs = EpicGamesStore()

    #egl_storefront_name = "Epic Games Store"
    egs.name="Epic Games Store"

    # To launch the storefront in the EGL it actualy needs a special launch option
    egs.launch_opts = '-com.epicgames'
    #egl_storefront_launch_opts='-com.epicgames'

    egs.compat_path = os.path.join(steam_paths.compatdata_dir,"EpicGamesLauncher")
    #egl_comp_dir="$compdata_dir/EpicGamesLauncher"

    egs.wine_pfx=os.path.join(egs.compat_path,'pfx')
    #egl_pfx="$egl_comp_dir/pfx"

    egs.start_dir = os.path.join(egs.wine_pfx,'drive_c/Program Files (x86)/Epic Games')
    #egl_start_dir="$egl_pfx/drive_c/Program Files (x86)/Epic Games"

    egs.exe_name = 'EpicGamesLauncher.exe'
    egs.exe = os.path.join(egs.start_dir,egs.exe_name)
    #egl_exe="$egl_pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"

    egs.game_install_dir = os.path.join(egs.wine_pfx,'drive_c/Program Files/Epic Games')
    #egl_games_dir="$egl_pfx/drive_c/Program Files/Epic Games"

    ## Game Info source(s)
    # Single file containing all insalled games, but does't have the NAMES of the games :(
    #egl_game_index="$egl_pfx/drive_c/ProgramData/Epic/UnrealEngineLauncher/LauncherInstalled.dat"

    # Each directory for each game has a .mancpn file with the required ID data
    # egl_game_mancpn="drive_c/Program Files/Epic Games/*/.egstore/*.mancpn"

    # Installer manifest folder (manifests are *.item files in this folder)
    # Contains ALL extensive required info for each game
    #egl_game_manifests="$egl_pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests"
    egs.manifest_dir = os.path.join(egs.wine_pfx,'drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests')

    #egl_game_info_ext='.mancpn'
    egs.overlay = os.path.join(egs.wine_pfx,'drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win32-Shipping.exe')
    #egl_overlay="$egl_pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win32-Shipping.exe"
    egs.overlay_64 = os.path.join(egs.wine_pfx,'drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win64-Shipping.exe')
    #egl_overlay_64="$egl_pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win64-Shipping.exe"

    # GOG
    gog_comp_dir="$compdata_dir/GogGalaxyLauncher"
    gog_pfx="$gog_comp_dir/pfx"
    gog_start_dir="$gog_pfx/drive_c/Program Files (x86)/GOG Galaxy"
    gog_exe="$gog_pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
    gog_games_dir="$gog_pfx/drive_c/Program Files (x86)/GOG Galaxy/Games"

    # EA App
    ## NOTE: EA App games currently do not use either the launcher path or dir for
    ##     generating the shortcut - it's based on the games dir and game exe only
    ea_comp_dir="$compdata_dir/TheEAappLauncher"
    ea_pfx="$ea_comp_dir/pfx"
    ea_exe="$ea_pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
    ea_start_dir="$ea_pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop"
    ea_games_dir="$ea_pfx/drive_c/Program Files/EA Games"
    ea_install_manifest='__Installer/installerdata.xml'

    # Uplay/Ubisoft Connect
    uc_comp_dir="$compdata_dir/UplayLauncher"
    uc_pfx="$uc_comp_dir/pfx"
    uc_start_dir="$uc_pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher"
    uc_exe="$uc_pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"
    uc_games_dir="$uc_pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games"
    uc_data_dir="$uc_pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/data"
    uc_sys_reg="$uc_pfx/system.reg"

    # Amazon Games
    amz_comp_dir="$compdata_dir/AmazonGamesLauncher"
    amz_pfx="$amz_comp_dir/pfx"
    amz_exe="$amz_pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe"
    amz_start_dir="$amz_pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App"
    amz_games_dir="$amz_pfx/drive_c/Amazon Games/Library"
    amz_games_reg="$amz_pfx/user.reg"

class Storefront():
    def __init__(self):
        # Storefront Name to use in shortcut
        self.name = ''
        # Path to the storefront's compatdata folder inside Steam
        compat_path = ''
        # Path to the root of the wine prefix in the compatdata folder
        wine_pfx = ''
        # The 'startdir' for the shortcut
        start_dir = ''
        # Name of the exe file
        exe_name = ''
        # Full path to the storefront's exe
        self.exe = ''
        # Launch options required by the storefront
        # Get these from a windows generated shortcut file
        launch_opts = ''
        # Directory where games from the storefront are located
        game_install_dir = ''

# Epic Agmes Store specific storefront class
class EpicGamesStore(Storefront):
    def __init__(self):
        Storefront.__init__(self)
        # The name of the storefront
        self.name = "Epic Games Store"
        # The path to the main Steam compatdata directory
        self.steam_compatdata_dir = steam_paths.compatdata_dir
        # The compatdata director for THIS store
        self.compat_dir = os.path.join(self.steam_compatdata_dir,"EpicGamesLauncher")
        # The wine prefix root
        self.wine_pfx=os.path.join(self.compat_dir,'pfx')
        # Launch options required
        self.store_launch_flag = '-com.epicgames'
        self.game_launch_flag = '-com.epicgames.launcher://apps/'
        self.exe_name = 'EpicGamesLauncher.exe'
        self.start_dir = os.path.join(self.wine_pfx,'drive_c/Program Files (x86)/Epic Games')
        self.exe = os.path.join(self.start_dir,self.exe_name)

        self.game_install_dir = os.path.join(self.wine_pfx,'drive_c/Program Files/Epic Games')

        # Single file containing all insalled games, but does't have the NAMES of the games :(
        #egl_game_index="$egl_pfx/drive_c/ProgramData/Epic/UnrealEngineLauncher/LauncherInstalled.dat"

        # Each directory for each game has a .mancpn file with the required ID data
        # egl_game_mancpn="drive_c/Program Files/Epic Games/*/.egstore/*.mancpn"

        # Installer manifest folder (manifests are *.item files in this folder)
        # Contains ALL extensive required info for each game
        #egl_game_manifests="$egl_pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests"
        self.manifest_dir = os.path.join(self.wine_pfx,'drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests')

        # Overlays that we want to be able to advise if they are active or not
        self.overlay = os.path.join(self.wine_pfx,'drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win32-Shipping.exe')
        self.overlay_64 = os.path.join(self.wine_pfx,'drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win64-Shipping.exe')

        # Then find the installed games
        # This populates the game_list array
        self.game_list = []
        self.find_installed()

    # Generate the shortcut for the launcher
    def launcher_shortcut(self):
        generate_shortcut(self.name, self.exe, self.start_dir, self.store_launch_flag, self.compat_dir)

    # Check if the EGS overlays are still enabled (i.e. not renamed)
    # There's no GUI way to disable this, so it needs to be done at the FS level
    def check_overlays(self):
        if os.path.isfile(self.overlay) :
            print("Epic Games overlay enabled.  Disable by renaming {}".format(self.overlay))
        if os.path.isfile(self.overlay_64) :
            print("Epic Games overlay enabled.  Disable by renaming {}".format(self.overlay_64))

    def list_installed(self):
        # Dump the info for all games that were found
        for game in self.game_list:
            game.info()

    def list_shortcuts(self):
        # Dump the shortcut infor for all games found
        for game in self.game_list:
            game.shortcut(self.exe, self.start_dir, self.compat_dir)


    # List installed games
    def find_installed(self):
        #print("Scanning: {}".format(self.manifest_dir))
        for file in os.listdir(self.manifest_dir):
            #print("Found: {}".format(file))
            file_name, file_ext = os.path.splitext(file)
            # if the object found is a manifest ('.item' file)
            if file_ext == '.item' :
                # Derive the full path of the manifest
                full_manifest_path = os.path.join(self.manifest_dir,file)
                print("Found game manifest: {}".format(file))
                # Create a new game
                self.game_list.append(EGSgame(full_manifest_path, self.wine_pfx))
                #game.info()
                # Generate it's shortcut
                #game.shortcut(self.exe, self.start_dir, self.compat_dir)

class EGSgame():
    def __init__(self, manifest_path, prefix = ''):
        with open(manifest_path, "r") as manifest :
            self.keys = json.load(manifest)
            # The DisplayName key is the name of the game as shown by the launcher
            self.gamename = self.keys["DisplayName"]
            # NOTE: There is a CatalogNamesape AND MainGameCatalogNamespace ID in the manifest file.  If the game has DLC or expansions, the CatalogNamespace will point to the DLC or expansion, and the MainGameCatalogNamespace will point to the real game executable. To verify this manifest points at a main game and not DLC we check if these two values are the same.  If they're not then we don't want to add this entry
            self.namespaceID = self.keys["CatalogNamespace"]
            self.mainNamespaceID = self.keys["MainGameCatalogNamespace"]
            if self.namespaceID == self.mainNamespaceID :
                self.type = 'main title'
            else :
                print("This is likely DLC not a main title. Skipping")
                self.type = 'dlc'
            # NOTE: This is the non-main key in case we want to act on DLC titles
            self.itemID = self.keys["CatalogItemId"]
            # NOTE: This is the non-main key in case we want to act on DLC titles
            self.artifactID = self.keys["AppName"]
            # Get the executable and install directory so we can verify the game is actually installed still
            self.install_path = self.keys["InstallLocation"]
            self.game_exe = self.keys["LaunchExecutable"]
            # We're done extracting data, so close the file
            manifest.close()
            # Generate the exe path
            # We always want the PURE windows path representation here in case
            # we are on Linux in a wine prefix
            self.exe_path = pathlib.PureWindowsPath(self.install_path, self.game_exe)
            if prefix == '' :
                self.real_exe_path = self.exe_path
            else :
                # If there's a wine prefix, then we need to do some massaging since the self-reported exe path doesn't know it's in a wine prefix
                #drive, path = os.path.splitdrive(self.install_path)
                # print()
                # print("Split '{}' into '{}' and '{}'".format(self.exe_path, self.exe_path.anchor, self.exe_path.relative_to(self.exe_path.drive)))
                # print()
                #self.real_exe_path = os.path.join(prefix,'drive_c',path)
                # TODO / BUG: This doesn't actually result in a valid posix path
                # NEED TO FIX
                print("BROKEN Joining '{}' and '{}'".format(prefix, pathlib.PurePath.as_posix(self.exe_path.relative_to(self.exe_path.drive))))

                self.real_exe_path = pathlib.PurePath(prefix)
                self.real_exe_path.joinpath(pathlib.PurePath.as_posix(self.exe_path.relative_to(self.exe_path.drive)))
            self.game_launch_opts = "-com.epicgames.launcher://apps/{}%3A{}%3A{}?action=launch&silent=true".format(self.namespaceID, self.itemID ,self.artifactID)
    def info(self):
        print("Game name:    {} ({})".format(self.gamename,self.type))
        print("Executable:   {}".format(self.real_exe_path))
        print("Namespace ID: {}".format(self.namespaceID))
        print("Item ID:      {}".format(self.itemID))
        print("Artifact ID:  {}".format(self.artifactID))
        print()
    def shortcut(self, launcher_exe, launcher_startdir, launcher_compatdir):
        if self.type == 'main title' :
            generate_shortcut(self.gamename, launcher_exe, launcher_startdir, self.game_launch_opts, launcher_compatdir)
            print()


# Generate steam shortcuts
def generate_shortcut(name, target, start_dir, command_opts, compat_dir=''):
    # Steam shortcuts have 4 main components:
    # Name:     The name to display in the library
    # Target:   The 'command' to invoke to run the game
    # Start In: The directory to enter before invoking the command to run
    #             the game. This allows for games to provide libraries that
    #             override system libraries
    # Launch Options: Options and flags to surround the TARGET command with
    #                   This generally isn't needed except on Linux
    print("Name:        {}".format(name))
    print("Target:      \"{}\"".format(target))
    print("Start In:    \"{}\"".format(start_dir))
    if compat_dir == '' :
        print("Launch Opts: %command% \"{}\"".format(command_opts))
    else:
        print("Launch Opts: STEAM_COMPAT_DATA_PATH=\"{}\" %command% {}".format(compat_dir, command_opts))
    print()


class steam_paths():
    # grab the user home directory
    user_home = pathlib.Path.home()

    # The main steam root on the steamdeck
    # On other Linux distros this can be in SEVERAL different places
    # The 'stock' Linux installer for Steam (debian)
    #  $HOME/.steam/debian-installation
    # The flatpak install location
    #  $HOME/.var/app/valve.steam...
    #global steam_root ; steam_root = "$HOME/.local/share/Steam"
    steam_root = os.path.join(user_home, '.local/share/Steam')

    # The steamapps folder
    global steamapps_dir ; steamapps_dir = os.path.join(steam_root,"steamapps")
    # The compatdata folder (i.e. proton/wine prefixes)
    global compdata_dir ; compatdata_dir = os.path.join(steamapps_dir,"compatdata")

def main(): 
    defaults()
    #print("Steam root: {}".format(steam_paths.steam_root))
    #print("User home: {}".format(steam_paths.user_home))
    #print("EGL Name: {}".format(egs.name))
    egs.launcher_shortcut()
    egs.check_overlays()
    egs.list_installed()
    egs.list_shortcuts()
    #print("egs overlay: {}".format(egs.overlay))

if __name__ == "__main__":
    main()

#main()