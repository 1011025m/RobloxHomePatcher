# Technical Explanation (before 9 November 2022)
When you launch Roblox from your browser, it will open a URI that launches the `RobloxPlayerLauncher.exe` first. The `RobloxPlayerLauncher.exe` handles client updates, and pass arguments it receives from your browser to the `RobloxPlayerBeta.exe`, which is the application (we call this the player client) that you use to actually play games.

The URI contains these plus-sign-separated arguments (with the corresponding flags passed onto the player client):
| URI Argument | Flag | Description |
| ------------ | ---- | ----------- |
| launchmode (`play` or `app`) | `--play` or `--app` | The gamemode (from version-b117c4c276664452 it always uses `--app`)
| gameinfo | -t | The authentication ticket to verify that you are a particular player.<br/>This can only be used once.
| launchtime | --launchtime=\<timestamp\> | The timestamp of you launching the game.
| placelauncherurl | -j | Contains the placeId of the game you're trying to play.
| browsertrackerid | -b | The tracker ID for your browser. This is for Roblox's analytics.
| robloxLocale | --rloc
| gameLocale | --gloc
| channel | | Client release channel (think of Roblox having a beta release channel, then there'll be something) |
| LaunchExp | | Modifies the registry key that you probably looked into!

Before version-b117c4c276664452, you used to be able to modify the `LaunchExp` argument to `InBrowser`, and the launcher would respect your choice and pass the `launchmode` argument as the `--play` flag when launching the player client.

Now, regardless of what you set in the `launchmode` argument, the launcher will **ALWAYS** pass the `--app` flag to the player client, resulting it to launch into the in-app homepage that you hate.

The way that this python script works is, it finds where this `app` hex is stored inside the launcher, overwrite it to something else, so when the flag is passed to the player client, the flag will be what we wrote into the launcher. 

Since the launcher size can change, we cannot tell the exact location of this hex code. The script instead looks for more than the hex code that it tries to patch to locate it relatively.

As an example, in version-b117c4c276664452 the script looks for this in the launcher binary:
```
49 6E 73 74 61 6C 6C 65 72 00 00 00 63 6C 69 65 6E 74 00 00 77 69 6E 64 6F 77 73 4C 61 75 6E 63 68 53 68 6F 72 74 63 75 74 00 00 00 4C 4F 4C
```
... which translates to `Installer���client��windowsLaunchShortcut���app` (there are null characters)

We only want to modify the `app` in the end of this hex code. However, there might be multiple `app`s in the binary, so the script looks for the content before it that is (most likely) variables and will stay together with the `app` that we want to modify in the future.

As a result, the script finds the hex code above from the launcher binary, and the offset for the start of it is `157BD0`.

The script overwrites starting from this offset with the following content:
```
49 6E 73 74 61 6C 6C 65 72 00 00 00 63 6C 69 65 6E 74 00 00 77 69 6E 64 6F 77 73 4C 61 75 6E 63 68 53 68 6F 72 74 63 75 74 00 00 00 48 34 58
```
... which translates to `Installer���client��windowsLaunchShortcut���H4X`. When the launcher pass flags to the player client, it will now pass `--H4X` instead of `--app`.

The script also patches content that worked before version-b117c4c276664452 as a failsafe, you can look into the code if you are interested.