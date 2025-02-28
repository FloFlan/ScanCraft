# ScanCraft

A Discord bot that monitors multiple Minecraft servers, tracks player activity (including total playtime), and notifies you when specific players join or leave a server.

## Features

- **Server Monitoring:**
  - Regularly polls Minecraft servers using the [MCStatus API](https://api.mcstatus.io/v2/status/java/<IP>) every minute.
  - Displays real-time status updates (online/offline, player count, player list, server version, and MOTD) in dedicated Discord channels.

- **Player Tracking:**
  - List currently online players on a specific server.
  - Show all players that have joined the server along with their total playtime.
  - notifies when a specific player joins or leaves a given server / any monitored server.
 
## Version History

  ### v1.0.0
- **Initial Release**
  - Basic Minecraft server monitoring using the MCStatus API.
  - Commands: `!status`, `!players`, `!allplayers`, `!list`.

  ### v1.1.0
- **Server Management Enhancements**
  - Added administrative commands: 
    - `!addserver <IP> <Server Name>`
    - `!removeserver <IP/ServerName>`
    - `!rename <IP/ServerName> <newname>`
    - `!reset`
  - Persistent storage of server data via a JSON file.

  ### v1.2.0
- **Player Tracking Features**
  - Added per‑server tracking command: `!track <playername> <IP/ServerName>`.
  - Added global tracking command: `!fulltrack <playername>`.
  - Notifies the subscriber when the tracked player joins or leaves the server.

  ### v1.3.0
- **Improvements & Bug Fixes**
  - Optimized background tasks to avoid iteration errors.
  - Improved embed formatting and notification messages.
  - Minor bug fixes and performance enhancements.


## Requirements

- Python 3.8+
- [discord.py](https://github.com/Rapptz/discord.py) (v2.0 or newer)
- [aiohttp](https://docs.aiohttp.org/)

A sample `requirements.txt` is provided:

```txt
discord.py>=2.0.0
aiohttp>=3.8.0
