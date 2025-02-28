# Minecraft Server Monitor Discord Bot

A Discord bot that monitors multiple Minecraft servers, tracks player activity (including total playtime), and notifies you when specific players join or leave a server.

## Features

- **Server Monitoring:**
  - Regularly polls Minecraft servers using the [MCStatus API](https://api.mcstatus.io/v2/status/java/<IP>) every minute.
  - Displays real-time status updates (online/offline, player count, player list, server version, and MOTD) in dedicated Discord channels.

- **Player Tracking:**
  - List currently online players on a specific server.
  - Show all players that have joined the server along with their total playtime.
  - notifies when a specific player joins or leaves a given server / any monitored server.

## Requirements

- Python 3.8+
- [discord.py](https://github.com/Rapptz/discord.py) (v2.0 or newer)
- [aiohttp](https://docs.aiohttp.org/)

A sample `requirements.txt` is provided:

```txt
discord.py>=2.0.0
aiohttp>=3.8.0
