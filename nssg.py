#!/usr/bin/python3

import pathlib
import os

def defaults(): 
    # All defaults assume a stock Steamdeck config with all data stored
    # in the main steamapps library at $HOME/.local/share/Steam
    # All Storefront defaults assume they were intalled with 
    # Non-Steam-Game-Launchers on the main storage device (not sdcard)
    # https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck
    # Support for arbitrary storefront compatdata folders coming in 0.5
    # support for sdcard installed storefronts coming in 0.5


    # Epic Games Launcher paths
    egl_storefront_name = "Epic Games Store"
    # To launch the storefront in the EGL it actualy needs a special launch option
    egl_storefront_launch_opts='-com.epicgames'
    egl_comp_dir="$compdata_dir/EpicGamesLauncher"
    egl_pfx="$egl_comp_dir/pfx"
    egl_start_dir="$egl_pfx/drive_c/Program Files (x86)/Epic Games"
    egl_exe="$egl_pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
    egl_games_dir="$egl_pfx/drive_c/Program Files/Epic Games"
    ## Game Info source(s)
    # Single file containing all insalled games, but does't have the NAMES of the games :(
    #egl_game_index="$egl_pfx/drive_c/ProgramData/Epic/UnrealEngineLauncher/LauncherInstalled.dat"

    # Each directory for each game has a .mancpn file with the required ID data
    # egl_game_mancpn="drive_c/Program Files/Epic Games/*/.egstore/*.mancpn"

    # Installer manifest folder (manifests are *.item files in this folder)
    # Contains ALL extensive required info for each game
    egl_game_manifests="$egl_pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests"

    #egl_game_info_ext='.mancpn'
    egl_overlay="$egl_pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win32-Shipping.exe"
    egl_overlay_64="$egl_pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Extras/Overlay/EOSOverlayRenderer-Win64-Shipping.exe"

    # GOG
    gog_comp_dir="$compdata_dir/GogGalaxyLauncher"
    gog_pfx="$gog_comp_dir/pfx"
    gog_start_dir="$gog_pfx/drive_c/Program Files (x86)/GOG Galaxy"
    gog_exe="$gog_pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
    gog_games_dir="$gog_pfx/drive_c/Program Files (x86)/GOG Galaxy/Games"

    # EA App
    ## NOTE: EA App games currently do not use either the launcher path or dir for
    ##       generating the shortcut - it's based on the games dir and game exe only
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
    global steamapps_dir ; steamapps_dir = "$steam_root/steamapps"
    # The compatdata folder (i.e. proton/wine prefixes)
    global compdata_dir ; compatdata_dir = "$steamapps_dir/compatdata"

def find_steam_paths():


def generate_egl_data():
    print("EGL pfx")
    generate_shortcut_data(egl_storefront_name, egl_exe, egl_start_dir, egl_comp_dir, egl_storefront_launch_opts)

def generate_shortcut_data(name, target, start_dir, compat_dir, command_opts):
    print("name:        {}".format(name))
    print("target:      {}".format(target))
    print("start in:    {}".format(start_dir))
    print("launch opts: STEAM_COMPAT_DATA_PATH=\"{}\" %%command%% {}".format(compat_dir,command_opts))

def main(): 
    find_steam_paths()
    print("Steam root: {}".format(steam_paths.steam_root))
    print("User home: {}".format(steam_paths.user_home))


#if __name__ == "__main__":
#    main()

main()