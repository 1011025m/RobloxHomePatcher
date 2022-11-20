# Imports
import sys
import os
from re import search

os.system("")

# Utility Functions
def toArbBytes(input, type):
    if type == 1: # The usual type - has have a null character before every character
        list = ["\x00"+str.strip('+') for str in input]
        return ''.join(list).encode()
    if type == 2: # The other type, doesn't have a null character before every character
        return input.replace("+", "\x00").encode()

def promptExit(code):
    input("Press Enter to quit")
    sys.exit(code)

def printColored(text: str, color: str):
    availableColors = {
        "red": "\33[91m",
        "green": "\33[92m",
        "default": "\33[0m"
    }
    print(availableColors[color] + text + availableColors["default"])

def promptYesNo(q: str):
    while True:
        promptq = input(q)
        if promptq.upper() == "Y":
            return True
        elif promptq.upper() == "N":
            return False
        else:
            printColored("Invalid input.", "red")

def permErrorPrompt(err):
    print(err)
    printColored("Permission error encountered - is Roblox currently opened?", "red")
    printColored("Close Roblox and try running this patcher as administrator.", "red")
    promptExit(1)

# Variables
'''
    First item: The target bytes
    Second item: Replacement bytes
    Third item: The type used for the conversion function
'''
bytesToReplace = [
    ["InBrowser++InApp++RobloxGameUpdater", "InBrowser++H4X3D++RobloxGameUpdater", 1],
    ["LaunchExp++launchexp++PreferInApp", "LaunchExp++launchexp++PreferH4X3D", 1],
    ["Installer+++client++windowsLaunchShortcut+++app", "Installer+++client++windowsLaunchShortcut+++H4X", 2]
]

possibleRobloxPaths = [
    os.getenv('LOCALAPPDATA'),
    os.getenv('ProgramFiles(x86)')
]

originalRblxFile = 'Mobile.rbxl'
renamedRblxFile = 'Mobile.disabled.rbxl'

# Init
foundRobloxPaths = []
fileToPatch = None
rbxlToRename = None

# The real deal!
# Apparently some users have their studio instance installed in LOCALAPPDATA
# but the player instance is not
# Check in both directories just to be safe
for p in possibleRobloxPaths:
    if "Roblox" in os.listdir(p):
        foundRobloxPaths.append(p + '\Roblox\Versions')

if not foundRobloxPaths:
    printColored("Cannot find the Roblox folder in your system.", "red")
    printColored("Currently, the patcher only supports Roblox installations in one of these locations:", "red")
    for path in possibleRobloxPaths:
        printColored(" • "+path+"\Roblox", "red")
    promptExit(1)

try:
    for robloxPath in foundRobloxPaths:
        folders = [folder for folder in os.listdir(robloxPath) if "version" in folder]

        for folder in folders:
            if 'ExtraContent' not in os.listdir(robloxPath+'\\'+folder):
                continue
            if 'places' not in os.listdir(robloxPath+'\\'+folder+'\\'+'ExtraContent'):
                continue
            
            placesFolder = robloxPath+'\\'+folder+'\\'+'ExtraContent'+'\\'+'places'
            print(placesFolder)

            if originalRblxFile in os.listdir(placesFolder):
                print('Found Roblox place file!')
                rbxlToRename = placesFolder+'\\'+originalRblxFile
                print('Renaming the Roblox place file... ', end='')
                # In case Roblox backfills the file - if there's already a renamed one we'll remove it first
                if renamedRblxFile in os.listdir(placesFolder): os.remove(placesFolder+'\\'+renamedRblxFile)
                # And then rename the actual place file
                os.rename(rbxlToRename,placesFolder+'\\'+renamedRblxFile)
                printColored('Done!', 'green')
                break
            elif renamedRblxFile in os.listdir(placesFolder):
                rbxlToRename = placesFolder+'\\'+renamedRblxFile
                print('The Roblox place file have been renamed already')
                continueUnpatch = promptYesNo('Do you want to rename it again to enable the in-app homepage? (Y/n): ')
                if continueUnpatch == True:
                    print('Renaming the Roblox place file... ', end='')
                    os.rename(rbxlToRename,placesFolder+'\\'+originalRblxFile)
                    printColored('Done!', 'green')
                else:
                    print('Skipped renaming Roblox place file.')
                break
            else:
                print(f"File not found in {folder}")
except PermissionError as e:
    permErrorPrompt(e)

if rbxlToRename is None:
    printColored("Cannot find the correct file from your Roblox installation.", "red")
    promptExit(1)

print("Would you like to patch with legacy method as well?")
printColored("As of right now, patching with the legacy method will launch Roblox into in-app homepage", "red")
printColored("or Roblox won't launch at all if you already renamed the place file. Continue with caution.", "red")
if promptYesNo("Continue? (Y/n): ") == False:
    print("Skipped legacy patching.")
    promptExit(0)

for folder in folders:
    if 'RobloxPlayerLauncher.exe' in os.listdir(robloxPath+'\\'+folder):
        print('Found executable!')
        fileToPatch = robloxPath+'\\'+folder+'\\'+'RobloxPlayerLauncher.exe'
        break

if fileToPatch is None:
    printColored("Cannot find Roblox in your system. If you haven't installed it, please do so.", "red")
    promptExit(1)
else:
    print(fileToPatch)

try:
    with open(fileToPatch, 'r+b') as topatch:
        read = topatch.read()
        failures = 0

        for index, byteSet in enumerate(bytesToReplace):
            if len(byteSet[0]) != len(byteSet[1]):
                    printColored(f"Target bytes do not match the length of replacement bytes, byte set: {index}", "red")
                    promptExit(1)

            target = search(toArbBytes(byteSet[0], byteSet[2]), read)
            
            if target is not None:
                print(f"Found matching bytes in {index+1} of {len(bytesToReplace)} set.")
                pos = target.start()
                print(f'Position is: {hex(pos)}')
                print("Patching...", end=" ")
                topatch.seek(pos)
                topatch.write(toArbBytes(byteSet[1], byteSet[2]))
                print("Patched")
                topatch.seek(0)
            else:
                print(f"Target bytes set {index+1} of {len(bytesToReplace)} is not found.")
                failures += 1

        topatch.close()
        printColored("All done!", "green") if failures == 0 else printColored(f"{str(failures)} failures occured when patching.", "red")
except PermissionError as e:
    permErrorPrompt(e)

promptExit(0)
