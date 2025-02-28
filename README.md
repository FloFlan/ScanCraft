# ScanCraft

ScanCraft is a Discord bot that monitors multiple Minecraft servers, tracks player activity (including total playtime), and sends notifications when specific players join or leave a server.


## Features

### Server Monitoring
- Periodically polls Minecraft servers using the [MCStatus API](https://api.mcstatus.io/v2/status/java/<IP>) every minute.
- Displays real-time updates on each server's status, including:
  - Online/offline status
  - Current and maximum player counts
  - List of online players
  - Server version and Message of the Day (MOTD)
- Posts status updates in dedicated Discord channels for each monitored server.

### Player Tracking
- Lists the currently online players for a specific server.
- Displays a history of all players who have joined a server along with their total playtime.
- Notifies users when a specific player joins or leaves a particular server or any monitored server.

### Server Management
- **Add Server:** Easily add a new Minecraft server for monitoring.
- **Remove Server:** Remove a server from monitoring.
- **Rename Server:** Change the display name of a monitored server.
- **Reset:** Clear all tracked server data and player histories.


## Version History

### v1.0.0 - Initial Release
- Basic Minecraft server monitoring using the MCStatus API.
- Core commands:
  - **Status:** View overall server status.
  - **Player List:** Display currently online players.
  - **All Players:** Show all players who joined (with playtime).
  - **Server List:** List all monitored servers.

#### v1.1.0 - Server Management Enhancements
- Added administrative commands:
  - **Add Server:** Add a new Minecraft server.
  - **Remove Server:** Remove an existing server.
  - **Rename Server:** Rename a monitored server.
  - **Reset:** Clear all tracked data.
- Persistent storage of server data via a JSON file.

#### v1.2.0 - Player Tracking Features
- Introduced per‑server tracking to notify users when a specific player joins or leaves a server.
- Added global tracking to notify users when a specific player joins or leaves any monitored server.

#### v1.3.0 - Improvements & Bug Fixes
- Optimized background tasks to prevent iteration errors.
- Improved formatting of status updates and notifications.
- Minor bug fixes and performance enhancements.

## Roadmap

### Upcoming Features

- **Historical Data & Graphs**
  - Log server statistics (e.g., player counts, uptime) over time.
  - Generate visual graphs to display trends and peak activity.

- **Leaderboard & Statistics**
  - Display leaderboards ranking players by total playtime or session count.
  - Rank servers based on performance and activity metrics.

- **Real-Time Channel Updates**
  - Automatically update channel names or topics to reflect live server status.

- **Scheduled Reports**
  - Send daily or weekly summary reports to designated channels or via direct message.

- **Customizable Notifications**
  - Allow users to customize which events trigger notifications.
  - Provide options to mute or adjust tracking alerts.

- **Integration with Other APIs**
  - Enhance server data with additional Minecraft-related APIs (e.g., player skin, leaderboard data).
  - Display enriched content such as player avatars and detailed stats.

- **In-Game Chat Relay**
  - Bridge Minecraft in-game chat with Discord channels for real-time communication.

- **Advanced Filtering & Auto-Moderation**
  - Implement filters to notify only during certain periods or for players meeting specific criteria.
  - Introduce automated alerts for suspicious behavior with moderation tools for administrators.

- **Web Dashboard**
  - Develop a web-based dashboard for real-time monitoring and administrative control.
  - Provide historical data access and visualizations through the dashboard.

## Requirements

- Python 3.8+
- [discord.py](https://github.com/Rapptz/discord.py) (v2.0 or newer)
- [aiohttp](https://docs.aiohttp.org/)

A sample `requirements.txt` is provided:

```txt
discord.py>=2.0.0
aiohttp>=3.8.0
