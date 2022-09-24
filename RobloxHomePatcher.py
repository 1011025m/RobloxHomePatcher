from re import search
from sys import exit
from os import getenv,listdir

def toArbBytes(input, type):
    if type == 1: # The usual type - has have a null character before every character
        list = ["\x00"+str.strip('+') for str in input]
        return ''.join(list).encode()
    if type == 2: # The other type, doesn't have a null character before every character
        return input.replace("+", "\x00").encode()

def promptExit(code):
    input("Press Enter to quit")
    exit(code)

'''
    First item: The target bytes
    Second item: Replacement bytes
    Third item: The type used for the conversion function
'''
bytesToReplace = [
    ["InBrowser++InApp++RobloxGameUpdater", "InBrowser++H4X3D++RobloxGameUpdater", 1],
    ["LaunchExp++launchexp++PreferInApp", "LaunchExp++launchexp++PreferH4X3D", 1],
    ["Installer+++client++windowsLaunchShortcut+++app", "Installer+++client++windowsLaunchShortcut+++LOL", 2],
]

fileToPatch = None

possibleRobloxPaths = [
    getenv('LOCALAPPDATA'),
    getenv('ProgramFiles(x86)')
]

for p in possibleRobloxPaths:
    if "Roblox" in listdir(p):
        robloxPath = p + '\Roblox\Versions'

if robloxPath is None:
    print("Cannot find Roblox folder...")
    promptExit(1)

folders = [folder for folder in listdir(robloxPath) if "version" in folder]

for folder in folders:
    if 'RobloxPlayerLauncher.exe' in listdir(robloxPath+'\\'+folder):
        print('Found executable!')
        fileToPatch = robloxPath+'\\'+folder+'\\'+'RobloxPlayerLauncher.exe'
        break

if fileToPatch is not None:
    print(fileToPatch)
else:
    print("Cannot find Roblox in your system. If you haven't installed it, please do so.")
    promptExit(1)

with open(fileToPatch, 'r+b') as topatch:
    read = topatch.read()
    failures = 0

    for index, byteSet in enumerate(bytesToReplace):
        if len(byteSet[0]) != len(byteSet[1]):
                print(f"Target bytes do not match the length of replacement bytes, byte set: {index}")
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
            print(f"Target bytes set {index} of {len(bytesToReplace)} is not found.")
            failures += 1

    topatch.close()
    print("All done!") if failures == 0 else print(f"{str(failures)} failures occured when patching.")

promptExit(0)
