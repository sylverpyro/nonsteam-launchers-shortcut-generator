# Adding Non-Steam Games
Source: https://developer.valvesoftware.com/wiki/Add_Non-Steam_Game

Non-Steam Games are saved in the file: <<Steam Installation>>\userdata\<<User ID>>\config\shortcuts.vdf.

## Keying
* Null (NUL) characters are used to denote the end of a key.
* A key surrounded by two Null (NUL) characters denote the beginning of a set. (e.g. NULSet NameNUL)
* Start of Header (SOH) characters are used to denote that next key is actually a value to assign to this key. (e.g. |SOH|Key|NUL|Value|NUL|)
* Start of Text (STX) characters are used to denote that the next several keys are values to assign to this key. (Always four special characters - Could be one SOH and three NUL, or four NUL in a row)
  * WARNING: In testing this appears to be inaccurate - the STX key is NOT always followed by 4 special characters, and even if there are 4 special characters, they are NOT always `[|SOH||NUL|]|NUL|{3}`
* Backspace (BS) characters are used to denote the end of a set. (e.g. NULSet NameNULDefinitionBS)

## Binary equivelents
* NUL Null (NUL)
  * nul = b'\x00'
* SOH Start of Heading (SOH)
  * soh = b'\x01'
* BS Backspace (BS)
  * bs = b'\x08'
* LF Line Feed (LF)
  * lf = b'\x0a'
* STX Start of Text (STX)
  * stx = b'\x02'

## Typical structure
Typical format is as follows (New lines and indentation added for clarity; characters within two vertical separators [e.g. |NUL|] represent special characters):

**Note:** There should not be any new lines or indentation in your actual shortcuts.vdf file.

**Note:** Indentation is only a best guess attempt at determining the format of the .vdf file.

**Testing Note:** In practice it appears that the `appid` line documentation is actually inaccurate.  A hexdump of the `appid` key shows the following
```
   02 61 70 70 69 64 C0 EB F1 6C C5 | .appid...l.
|STX|  a  p  p  i  d  ?  ?  ?  l  ?
```
So it's likely safer to search for the |SOH| that follows that sets the AppName key and capture all of the STX content to re-use later


**Testing Note:** All text blocks are actually all LOWER CASE not mixed case
```
|NUL|shortcuts|NUL|
 |NUL|0|NUL|
  |STX|appid|NUL||NUL||NUL||NUL||NUL|
  |SOH|appname|NUL|APP NAME WITHOUT QUOTES|NUL|
  |SOH|exe|NUL|"PATH TO EXE"|NUL|
  |SOH|StartDir|NUL|"DIRECTORY TO START IN"|NUL|
  |SOH|icon|NUL|"PATH TO ICON"|NUL|
  |SOH|ShortcutPath|NUL||NUL|
  |SOH|LaunchOptions|NUL||NUL|
  |STX|IsHidden|NUL||NUL||NUL||NUL||NUL|
  |STX|AllowDesktopConfig|NUL||SOH||NUL||NUL||NUL|
  |STX|AllowOverlay|NUL||SOH||NUL||NUL||NUL|
  |STX|OpenVR|NUL||NUL||NUL||NUL||NUL|
  |STX|Devkit|NUL||NUL||NUL||NUL||NUL|
  |SOH|DevkitGameID|NUL||NUL|
  |STX|LastPlayTime|NUL||NUL||NUL||NUL||NUL|
  |NUL|tags|NUL|
   |SOH|0|NUL|favorite|NUL|
  |BS|
 |BS|
 |NUL|1|NUL|
  ...
 |BS|
|BS|
```

Flat (actual) format
```
|NUL|shortcuts|NUL||NUL|0|NUL||STX|appid|NUL||NUL||NUL||NUL||NUL||SOH|AppName|NUL|APP NAME ITHOUT QUOTES|NUL||SOH|Exe|NUL|"PATH TO EXE"|NUL||SOH|StartDir|NUL|"DIRECTORY TO START IN"|NUL||SOH|icon|NUL|"PATH TO ICON"|NUL||SOH|ShortcutPath|NUL||NUL||SOH|LaunchOptions|NUL||NUL||STX|IsHidden|NUL||NUL||NUL||NUL||NUL||STX|AllowDesktopConfig|NUL||SOH||NUL||NUL||NUL||STX|AllowOverlay|NUL||SOH||NUL||NUL||NUL||STX|OpenVR|NUL||NUL||NUL||NUL||NUL||STX|Devkit|NUL||NUL||NUL||NUL||NUL||SOH|DevkitGameID|NUL||NUL||STX|LastPlayTime|NUL||NUL||NUL||NUL||NUL||NUL|tags|NUL||SOH|0|NUL|favorite|NUL||BS||BS||NUL|1|NUL|...More Entries...|BS||BS|
```

## Additional format docs by Corporal Quesabilla
Source: https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki/Steam-Shortcuts-Documentation

```
# Key                # Data Type  # Internal Name       # Delimiter     # Input             # Delimiter
full_entryID        =                                      '\x00'  +  var_entryID        +  '\x00'
full_appName        =  '\x01'  +  'appname'             +  '\x00'  +  var_appName        +  '\x00'
full_quotedPath     =  '\x01'  +  'exe'                 +  '\x00'  +  var_unquotedPath   +  '\x00'
full_startDir       =  '\x01'  +  'StartDir'            +  '\x00'  +  var_startDir       +  '\x00'
full_iconPath       =  '\x01'  +  'icon'                +  '\x00'  +  var_iconPath       +  '\x00'
full_shortcutPath   =  '\x01'  +  'ShortcutPath'        +  '\x00'  +  var_shortcutPath   +  '\x00'
full_launchOptions  =  '\x01'  +  'LaunchOptions'       +  '\x00'  +  var_launchOptions  +  '\x00'
full_isHidden       =  '\x02'  +  'IsHidden'            +  '\x00'  +  var_isHidden       +  '\x00\x00\x00'
full_allowDeskConf  =  '\x02'  +  'AllowDesktopConfig'  +  '\x00'  +  var_allowDeskConf  +  '\x00\x00\x00'
full_allowOverlay   =  '\x02'  +  'AllowOverlay'        +  '\x00'  +  var_allowOverlay   +  '\x00\x00\x00'
full_openVR         =  '\x02'  +  'OpenVR'              +  '\x00'  +  var_openVR         +  '\x00\x00\x00'
full_lastPlayTime   =  '\x02'  +  'LastPlayTime'        +  '\x00'  +  var_lastPlayTime
full_tags           =  '\x00'  +  'tags'                +  '\x00'  +  var_tags           +  '\x08\x08'

newEntry = full_entryID + full_appName + full_quotedPath + full_startDir + full_iconPath + full_shortcutPath + full_launchOptions + full_isHidden + full_allowDeskConf + full_allowOverlay + full_openVR + full_tags
return newEntry
```