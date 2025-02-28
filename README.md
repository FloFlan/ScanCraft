# Minecraft Server Monitor Discord Bot

A Discord bot that monitors multiple Minecraft servers, tracks player activity (including total playtime), and notifies you when specific players join or leave a server.

## Features

- **Server Monitoring:**
  - Regularly polls Minecraft servers using the [MCStatus API](https://api.mcstatus.io/v2/status/java/<IP>) every minute.
  - Displays real-time status updates (online/offline, player count, player list, server version, and MOTD) in dedicated Discord channels.

- **Player Tracking:**
  - **!players `<IP/ServerName>`**: List currently online players on a specific server.
  - **!allplayers `<IP/ServerName>`**: Show all players that have joined the server along with their total playtime.
  - **!track `<playername> <IP/ServerName>`**: Get notified when a specific player joins or leaves a given server.
  - **!fulltrack `<playername>`**: Get notified when a specific player joins or leaves any monitored server.

- **Server Management:**
  - **!addserver `<IP> <Server Name>`**: Add a new Minecraft server for monitoring (Admin only).
  - **!removeserver `<IP/ServerName>`**: Remove a server from monitoring (Admin only).
  - **!rename `<IP/ServerName> <newname>`**: Rename a monitored server (Admin only).
  - **!list**: List all currently monitored servers.
  - **!reset**: Clear all tracked servers and player data (Admin only).

- **Status Summary:**
  - **!status**: Display a summary of all monitored servers.

## Requirements

- Python 3.8+
- [discord.py](https://github.com/Rapptz/discord.py) (v2.0 or newer)
- [aiohttp](https://docs.aiohttp.org/)

A sample `requirements.txt` is provided:

```txt
discord.py>=2.0.0
aiohttp>=3.8.0
