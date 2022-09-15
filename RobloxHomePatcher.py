import re
import sys
import os

# The separation between the words are two null characters, in the var I just use two plus's to avoid confusion.
def toArbBytes(input):
    list = ["\x00"+str.strip('+') for str in input]
    return ''.join(list).encode()

def promptExit(code):
    input("Press Enter to quit")
    sys.exit(code)

bytesToFind = toArbBytes("InBrowser++InApp++RobloxGameUpdater")
bytesToReplace = toArbBytes("InBrowser++H4X3D++RobloxGameUpdater")

if len(bytesToFind) != len(bytesToReplace):
    print("Target bytes do not match the length of replacement bytes!")
    promptExit(1)

fileToPatch = None

robloxPath = os.getenv('LOCALAPPDATA') + '\Roblox\Versions'
folders = [folder for folder in os.listdir(robloxPath) if "version" in folder]

for folder in folders:
    if 'RobloxPlayerLauncher.exe' in os.listdir(robloxPath+'\\'+folder):
        print('Found executable!')
        fileToPatch = robloxPath+'\\'+folder+'\\'+'RobloxPlayerLauncher.exe'
        break

if fileToPatch is not None:
    print(fileToPatch)
else:
    print("Cannot find Roblox in your system. If you haven't installed it, please do so.")
    promptExit(1)

try:
    with open(fileToPatch, 'r+b') as topatch:
        read = topatch.read()
        regfind = re.search(bytesToFind, read)
        
        if regfind is not None:
            print("Found match!")
            pos = regfind.start()
            print(f'Position is: {str(pos)}')
            print("Patching...", end=" ")
            topatch.seek(pos)
            topatch.write(bytesToReplace)
            topatch.close()
            print("Patched")
        else:
            print("Cannot find target bytes - maybe the executable has already been patched?")
            promptExit(1)

except Exception as error:
    print("An error occured:")
    print(error)
    promptExit(1)

promptExit(0)