#!/bin/bash -
set -o nounset

# Author: sylverpyro <sylverpyro@users.noreply.github.com>
# Report bugs, issues, and ideas at
#  https://github.com/sylverpyro/nonsteam-launchers-shortcut-generator/issues
# Version: pre-0.1 (alpha)

# Main supprot target is SteamDeck.  Will likely work on any other
# Linux or SteamOS device. 

defaults() {
  # All defaults assume a stock Steamdeck config with all data stored
  # in the main steamapps library at $HOME/.local/share/Steam
  # All Storefront defaults assume they were intalled with 
  # Non-Steam-Game-Launchers on the main storage device (not sdcard)
  # https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck
  # Support for arbitrary storefront compatdata folders coming in 0.5
  # support for sdcard installed storefronts coming in 0.5

  # The main steam root
  steam_root="$HOME/.local/share/Steam"
  # The steamapps folder
  steamapps_dir="$steam_root/steamapps"
  # The compatdata folder (i.e. proton/wine prefixes)
  compdata_dir="$steamapps_dir/compatdata"

  # Epic Games Launcher paths
  egl_storefront_name="Epic Games Store"
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
}

generate_egl_data() {
  # Make sure the directories are all present
  if [[ ! -d "$egl_comp_dir" ]]; then echo "  Warning: $egl_comp_dir cannot be found"; fi
  if [[ ! -d "$egl_start_dir" ]]; then echo "  Warning: $egl_start_dir cannot be found"; fi
  if [[ ! -f "$egl_exe" ]]; then echo "  Warning: $egl_exe cannot be found" ; fi
  
  # Advise if the overlay has not been disabled yet
  if [[ -f "$egl_overlay" ]]; then
    echo "NOTE: EGL Overlay enabled - disable with: mv \"$egl_overlay\" \"${egl_overlay}-disabled\""
  fi
  if [[ -f "$egl_overlay_64" ]]; then
    echo "NOTE: EGL Overlay enabled - disable with: mv \"$egl_overlay_64\" \"${egl_overlay_64}-disabled\""
  fi

  # Generate the Launcher shortcut
  generate_shortcut_data "$egl_storefront_name" "$egl_exe" "$egl_start_dir" "$egl_comp_dir" "$egl_storefront_launch_opts"

  echo "Info files: $(find "$egl_game_manifests" -mindepth 1 -maxdepth 1 -type f -name '*.info' -print0)"

  # Generate shortcuts for all installed games
  while IFS= read -r -d $'\0' item_file; do
    # Get the Name of the game
    local display_name="$(jq -r .DisplayName "$item_file")"

    # Get the NameSpace ID
    local namespaceId="$(jq -r .MainGameCatalogNamespace "$item_file")"
    #echo "name Id: $namespaceId"

    # Get the Catalog Item ID
    local itemId="$(jq -r .MainGameCatalogItemId "$item_file")"
    #echo "item ID: $itemId"

    # Get the Artifact ID
    local artifactId="$(jq -r .MainGameAppName "$item_file")"
    #echo "art  ID: $artifactId"
    
    # Generate the cmd_opts
    local cmd_opts="-com.epicgames.launcher://apps/$namespaceId%%3A$itemId%%3A$artifactId?action=launch&silent=true"

    # Generate the shortcut
    generate_shortcut_data "$display_name" "$egl_exe" "$egl_start_dir" "$egl_comp_dir" "$cmd_opts"
    
    echo ""
  done < <(find "$egl_game_manifests" -mindepth 1 -maxdepth 1 -type f -name '*.item' -print0)
}

generate_gog_data() {
  # We will need to convert some paths into windows paths relative to the
  # wine prefix so generate a handle for that now
  local trim="$gog_pfx/drive_c/"

  # Generate the storefront shortcut
  generate_shortcut_data "GoG Galaxy" "$gog_exe" "$gog_start_dir" "$gog_comp_dir" ""

  while IFS= read -r -d $'\0' game_dir; do
    #echo "game dir: $game_dir"

    # Convert the Linux game dir path to a Windows path since we need to present
    # this to a windows exe shortly inside a wine pfx so the exe will see
    # C:\ instead of .../pfx/drive_c

    # Get the full path to the game directory
    local full_install_dir="$(realpath --no-symlinks "$game_dir")"
    #echo "full dir: $full_install_dir"

    # Trim off the wine prefix and add C:/ ala-windows
    local trimmed_install_dir="C:/${full_install_dir/$trim/}"
    #echo "trimmed dir: $trimmed_install_dir"

    # Finally, swap all linux dir seperators '/' to windows dir seperators '\'
    local converted_dir="${trimmed_install_dir//\//\\}"
    #echo "Converted dir: $converted_dir"

    # Some games have MULTIPLE .info files as each DLC get's a file
    # e.g. Shovel Knight TT, Dead Cells + DLC
    # To get the MAIN game ID we need to either check the .ico file
    # OR scan for 'rootGameId' across all .info files (which in turn only
    # exists IF there are DLC .info files, otherwise it's just gameId).
    # choosing to go with the former as we only have to process a single file

    # Identify the goggame-*.ico file for the game
    local icon_file="$(find "$game_dir" -maxdepth 1 -type f -name 'goggame-*.ico')"
    #echo "icon file: $icon_file"

    # Extract the gameID from the ico file name
    local gameId="$(basename --suffix='.ico' "$icon_file" | cut -d '-' -f 2)"
    #echo "gameid: $gameId"

    # Generate a file handle for the MAIN gameIDs .info file
    local info_file="$game_dir/goggame-$gameId.info"
    #echo "info file: $info_file"

    # Extract the game name from the .info file
    local display_name="$(jq -r .name "$info_file")"
    #echo "dispaly name: $display_name"
    #echo ""

    # Generate the command options
    local cmd_opts="/command=runGame /gameID=$gameId /path=\"$converted_dir\""

    # Generate the shortcut data
    generate_shortcut_data "$display_name" "$gog_exe" "$gog_start_dir" "$gog_comp_dir" "$cmd_opts"
    echo ""
  done < <(find "$gog_games_dir" -mindepth 1 -maxdepth 1 -type d -print0)
  echo ""
}

# Ubisoft Connect/UPlay
generate_uc_data() {

  # Generate the launcher shortcut
  generate_shortcut_data "Ubisoft Connect" "$uc_exe" "$uc_start_dir" "$uc_comp_dir" ""

  #echo "data dirs: in $uc_data_dir"
  #find "$uc_data_dir" -mindepth 1 -maxdepth 1 -type d -regex '.*/[0-9]+$'

  # The definitive place to find the game IDs of installed UPlay games is in the
  # windows registry file. Luckily wine/proton store this data in text files in
  # the wine pfx directory.  So we can just grep/txt process the reg files rather
  # than resorting to launching regedit from inside a wine prefix
  # Becasue registry data is very well formatted, we can just rely on newlines rather
  # than NULLs to split up the inputs here
  while IFS= read -r uc_game_id; do
    # Extract the game name from the prefix reg file
    uc_game_name="$(grep "\\\\Uplay Install $uc_game_id]" -A 11 "$uc_sys_reg"  | grep ^'"DisplayName"=' | cut -d '"' -f 4)"
    
    # Generate the launch options
    uc_game_launch_opts="uplay://launch/$uc_game_id/0"

    # Generate the shortcut data
    generate_shortcut_data "$uc_game_name" "$uc_exe" "$uc_start_dir" "$uc_comp_dir" "$uc_game_launch_opts"
  done < <(grep -o "Uplay Install [[:digit:]]\+" "$uc_sys_reg" | cut -d ' ' -f 3)
  # Old directory-based method that is likely unreliable
  #done < <(find "$uc_data_dir" -mindepth 1 -maxdepth 1 -type d -regex '.*/[0-9]+$' -print0)

}

generate_ea_data() {
  # Generate the launcher shortcut
  generate_shortcut_data "EA App" "$ea_exe" "$ea_start_dir" "$ea_comp_dir" ""

  # read though the game install folder as that's where the critical data lies
  while IFS= read -r -d $'\0' game_dir; do
    # Check if the game is actually still installed
    # The install manifest will be gone if the game was once installed but has since
    # been removed
    if [[ -f "$game_dir/$ea_install_manifest" ]]; then
      # The display name is located in the installerdata.xml file inside
      # the game's install directory
      display_name="$(grep "<launcher uid=\"1-3\">" "$game_dir/$ea_install_manifest" -A 20 | grep "<name locale=\"en_" | tr '<' '>' | cut -d '>' -f 3 | head -n 1)"
      # fallback to the directory name
      if [[ "$display_name" == '' ]]; then
        display_name="$(basename "$game_dir")"
      fi

      # The executable file for the main game is also hidden away in the installerdata file
      game_exe="$game_dir/$(grep "<launcher uid=\"1-3\">" "$game_dir/$ea_install_manifest" -A 20 | grep -o "\].*</filePath>" | tr ']' '<' | cut -d '<' -f 2)"
      if [[ "$game_exe" == "$game_dir/" ]]; then
        # fallback to the largest exe in the game directory
        game_exe="$(find "$game_dir" -mindepth 1 -maxdepth 1 -type f -name '*.exe' | sort -n | tail -n 1)"
      fi

      # The shortcut then is just the game's dir, exe, and display name, no
      # fancy custom launch opts
      generate_shortcut_data "$display_name" "$game_exe" "$game_dir" "$ea_comp_dir" ""
    fi

  done < <(find "$ea_games_dir" -mindepth 1 -maxdepth 1 -type d -print0)
}

generate_amz_data() {
  # Generate the launcher shortcut
  generate_shortcut_data "Amazon Gaming" "$amz_exe" "$amz_start_dir" "$amz_comp_dir" ""

  # The game names are best sourced from the registry file
  reg_pattern_names='[Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmazonGames/'
  while IFS= read -r game_name; do
    display_name="$game_name"
    # Find the Game ID from the reg file as well now.  The registry data is (currently)
    # consistent and well formatted at 10 data elements per entry so if we emit the next 10
    # lines after the registy header we should be ablet o accurately find the ID from the
    # UninstallString (as that's the only element that contains it)
    # Unfortunately the structue of the uninstall string, there's a lot of slicing and 
    # dicing that needs to be done
    game_id="$(grep -A 10 --fixed-strings "${reg_pattern_names}${game_name}] " "$amz_games_reg" | grep --fixed-strings '"UninstallString"="' | rev | cut -d ' ' -f 1 | tr -d '"' | rev)"
    
    # Generate the full launch string argument that needs to be passed to the launcher
    game_launch_opts="amazon-games://play/$game_id"

    # That's all the info we need for the AMZ launcher so generate the shortcut data
    generate_shortcut_data "$display_name" "$amz_exe" "$amz_start_dir" "$amz_comp_dir" "$game_launch_opts"
  done < <(grep --fixed-strings "$reg_pattern_names" "$amz_games_reg" | cut -d '/' -f 2 | cut -d ']' -f 1)
}

# Generate shortcut data 
generate_shortcut_data() { # name target start_dir compat_dir command_opts 
  local name="$1"
  local target="$2"
  local start_dir="$3"
  local compat_dir="$4"
  local command_opts="$5"
  printf 'name       : %s\n' "$name"
  printf 'target     : "%s"\n' "$target"
  printf 'start in   : "%s"\n' "$start_dir"
  printf 'launch opts: STEAM_COMPAT_DATA_PATH="%s" %%command%% %s \n' "$compat_dir" "$command_opts"
  echo ""
}

work() {
  generate_egl_data
  generate_gog_data
  generate_uc_data
  generate_ea_data
  generate_amz_data
}

main() {
  defaults
  work
}

main
