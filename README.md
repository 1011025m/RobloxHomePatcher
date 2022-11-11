# RobloxHomePatcher
Good ol' Roblox making unnecessary changes rather than upgrading their player client to 64-bit... C'mon you know better!

This is just a simple python script that attempts to patch Roblox so that it wouldn't launch the in-app homepage.

If you don't have python, you can grab an executable from Releases. Executable is built with PyInstaller.

## Technical Explanation
Current method is simply renaming the `Mobile.rbxl` file found inside the `./ExtraContent/places` from the Roblox installation directory. For a detailed explanation of how this worked in the past, check [here](EXPLANATION.md).

The script still provides the legacy method of patching `RobloxPlayerLauncher.exe` in case Roblox does something wacky in the future.

## Support
Join my Discord server to contact me about this project (e.g. if it breaks)

https://discord.gg/AHwMzED