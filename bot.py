import discord
from discord.ext import commands, tasks
import aiohttp
import json
import os
from datetime import datetime
import time

SERVER_FILE = "servers.json"

server_data = {}

def load_servers():
    global server_data
    if os.path.exists(SERVER_FILE):
        with open(SERVER_FILE, "r") as f:
            server_data = json.load(f)
    else:
        server_data = {}

def save_servers():
    with open(SERVER_FILE, "w") as f:
        json.dump(server_data, f, indent=4)

def get_server_ip(identifier: str) -> str | None:
    """
    Return the IP of a server based on the provided identifier,
    which can be either the IP or the server name.
    """
    if identifier in server_data:
        return identifier
    for ip, info in list(server_data.items()):
        if info.get("server_name", "").lower() == identifier.lower():
            return ip
    return None

def format_time(seconds: float) -> str:
    """Formats seconds into a string like 'X hours Y minutes'."""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0 or hours == 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    return " ".join(parts)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    load_servers()
    if not server_status_check.is_running():
        server_status_check.start()

@tasks.loop(minutes=1)
async def server_status_check():
    async with aiohttp.ClientSession() as session:
        for ip, info in server_data.items():
            url = f"https://api.mcstatus.io/v2/status/java/{ip}"
            try:
                async with session.get(url) as response:
                    data = await response.json()
            except Exception as e:
                print(f"Error fetching data for {ip}: {e}")
                data = None

            channel_id = info.get("channel_id")
            channel = bot.get_channel(channel_id)
            if not channel:
                continue

            online = False
            online_count = 0
            max_players = 0
            players_list = []
            version = "Unknown"
            motd = "No MOTD"

            if data:
                online = data.get("online", False)
                players_info = data.get("players", {})
                online_count = players_info.get("online", 0)
                max_players = players_info.get("max", 0)
                raw_players = players_info.get("list", [])
                if raw_players and isinstance(raw_players, list) and len(raw_players) > 0 and isinstance(raw_players[0], dict):
                    players_list = raw_players
                else:
                    players_list = raw_players
                version = data.get("version", {}).get("name_clean", "Unknown")
                motd = data.get("motd", {}).get("clean", "No MOTD")

            now = time.time()
            players_history = info.get("players_history", {})
            if not players_history:
                players_history = {}

            current_players = {}
            if players_list and isinstance(players_list, list) and len(players_list) > 0 and isinstance(players_list[0], dict):
                for p in players_list:
                    uuid = p.get("uuid")
                    name = p.get("name_clean", "Unknown")
                    if uuid:
                        current_players[uuid] = name

            for uuid, name in current_players.items():
                if uuid not in players_history:
                    players_history[uuid] = {"name": name, "total_seconds": 0, "last_join": now}
                else:
                    if players_history[uuid].get("last_join") is None:
                        players_history[uuid]["last_join"] = now

            for uuid, record in players_history.items():
                if uuid not in current_players and record.get("last_join") is not None:
                    session_duration = now - record["last_join"]
                    record["total_seconds"] += session_duration
                    record["last_join"] = None

            info["players_history"] = players_history

            last_status = info.get("last_status", {})
            if last_status:
                last_players = set(p.get("name_clean", "") for p in last_status.get("players_list", [])) if last_status.get("players_list") else set()
                current_players_names = set(p.get("name_clean", "") for p in players_list if isinstance(p, dict)) if players_list and isinstance(players_list[0], dict) else set(players_list)
                joined = current_players_names - last_players
                left = last_players - current_players_names
                if joined:
                    await channel.send(f"🟢 **Player Join:** {', '.join(joined)} joined the server!")
                if left:
                    await channel.send(f"🔴 **Player Leave:** {', '.join(left)} left the server!")

            info["last_status"] = {
                "online": online,
                "players": online_count,
                "max_players": max_players,
                "players_list": players_list,
                "version": version,
                "motd": motd
            }
            server_data[ip] = info
            save_servers()

            server_name = info.get("server_name", ip)
            status_emoji = "🟢" if online else "🔴"
            embed = discord.Embed(
                title=f"{status_emoji} {server_name}",
                color=5814783
            )
            embed.add_field(name="📡 Server IP", value=f"`{ip}`\n\u200E", inline=False)
            embed.add_field(name="👥 Players Online", value=f"{online_count}/{max_players}\n\u200E", inline=False)
            current_time = time.time()
            if players_list and isinstance(players_list, list):
                player_lines = []
                for p in players_list:
                    if isinstance(p, dict):
                        uuid = p.get("uuid")
                        name = p.get("name_clean", "Unknown")
                        session_time_str = ""
                        if uuid in players_history and players_history[uuid].get("last_join") is not None:
                            session_duration = current_time - players_history[uuid]["last_join"]
                            session_time_str = f" ({format_time(session_duration)})"
                        player_lines.append(f"* {name}{session_time_str}")
                    else:
                        player_lines.append(f"* {p}")
                player_names = "\n".join(player_lines)
            else:
                player_names = "None"
            embed.add_field(name="🧑‍🤝‍🧑 Player list", value=f"{player_names}\n\u200E", inline=False)
            embed.add_field(name="🕹 Server Version", value=f"{version}\n\u200E", inline=False)
            embed.add_field(name="📝 MOTD", value=f"{motd}\n\u200E", inline=False)
            timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M")
            embed.set_footer(text=timestamp)
            await channel.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    if not server_data:
        await ctx.send("No servers are currently being monitored.")
        return
    message = "**Server Status Summary**\n"
    for ip, info in server_data.items():
        last_status = info.get("last_status", {})
        online = last_status.get("online", False)
        players = last_status.get("players", 0)
        max_players = last_status.get("max_players", 0)
        version = last_status.get("version", "Unknown")
        server_name = info.get("server_name", ip)
        status_text = "Online" if online else "Offline"
        message += f"📡 **{server_name}**: {status_text} | Players: {players}/{max_players} | Version: {version}\n"
    await ctx.send(message)

@bot.command(name="players")
async def players(ctx, identifier: str):
    server_ip = get_server_ip(identifier)
    if not server_ip:
        await ctx.send(f"Server {identifier} is not being monitored.")
        return
    last_status = server_data[server_ip].get("last_status", {})
    players_list = last_status.get("players_list", [])
    embeds = []
    if players_list and isinstance(players_list, list):
        for player in players_list:
            if isinstance(player, dict):
                player_uuid = player.get("uuid", "")
                player_name = player.get("name_clean", "Unknown")
                embed = discord.Embed(color=None)
                embed.set_author(
                    name=player_name,
                    icon_url=f"https://api.mineatar.io/face/{player_uuid}?scale=12"
                )
                embeds.append(embed)
            else:
                embed = discord.Embed(description=str(player), color=None)
                embeds.append(embed)
    else:
        embed = discord.Embed(description="No players online.", color=None)
        embeds.append(embed)
    await ctx.send(content=None, embeds=embeds)

@bot.command(name="allplayers")
async def allplayers(ctx, identifier: str):
    server_ip = get_server_ip(identifier)
    if not server_ip:
        await ctx.send(f"Server {identifier} is not being monitored.")
        return
    info = server_data[server_ip]
    players_history = info.get("players_history", {})
    embeds = []
    now = time.time()
    if players_history:
        for uuid, record in players_history.items():
            total = record.get("total_seconds", 0)
            if record.get("last_join") is not None:
                total += now - record["last_join"]
            formatted_time = format_time(total)
            player_name = record.get("name", "Unknown")
            embed = discord.Embed(color=None)
            embed.set_author(
                name=f"{player_name} ({formatted_time})",
                icon_url=f"https://api.mineatar.io/face/{uuid}?scale=12"
            )
            embeds.append(embed)
    else:
        embed = discord.Embed(description="No players have joined this server yet.", color=None)
        embeds.append(embed)
    await ctx.send(content=None, embeds=embeds)

@bot.command(name="list")
async def list_servers(ctx):
    if not server_data:
        await ctx.send("No servers are being monitored.")
        return
    message = "**Monitored Servers:**\n"
    for ip, info in server_data.items():
        server_name = info.get("server_name", ip)
        message += f"- **{server_name}** (`{ip}`)\n"
    await ctx.send(message)

@bot.command(name="reset")
@commands.has_permissions(administrator=True)
async def reset(ctx):
    global server_data  
    for ip, info in list(server_data.items()):
        channel_id = info.get("channel_id")
        channel = ctx.guild.get_channel(channel_id)
        if channel:
            await channel.delete(reason="Bot memory reset")
    server_data = {}
    if os.path.exists(SERVER_FILE):
        os.remove(SERVER_FILE)
    await ctx.send("Bot memory has been reset. All tracked servers and playtimes have been removed.")

bot.remove_command("help")
@bot.command(name="help")
async def help_command(ctx):
    help_text = (
        "**Available Commands:**\n"
        "`!status` - Shows the latest status of all servers.\n"
        "`!players <IP/ServerName>` - Lists online players on a specific server.\n"
        "`!allplayers <IP/ServerName>` - Lists all players that joined the server with their total playtime.\n"
        "`!list` - Lists all monitored servers.\n"
        "`!addserver <IP> <Server Name>` - Add a server to monitor (Admin only).\n"
        "`!removeserver <IP/ServerName>` - Remove a server from monitoring (Admin only).\n"
        "`!reset` - Resets bot memory, removing all tracked servers and playtimes (Admin only).\n"
        "`!help` - Displays this help message."
    )
    await ctx.send(help_text)

@bot.command(name="addserver")
@commands.has_permissions(administrator=True)
async def addserver(ctx, server_ip: str, *, server_name: str):
    if server_ip in server_data:
        await ctx.send(f"Server {server_ip} is already being monitored.")
        return
    guild = ctx.guild
    channel = await guild.create_text_channel(name=server_name.lower().replace(" ", "-"))
    server_data[server_ip] = {
        "channel_id": channel.id,
        "server_name": server_name,
        "last_status": {},
        "players_history": {}
    }
    save_servers()
    await ctx.send(f"Server {server_ip} added as **{server_name}**. Monitoring channel {channel.mention} has been created.")

@bot.command(name="removeserver")
@commands.has_permissions(administrator=True)
async def removeserver(ctx, identifier: str):
    server_ip = get_server_ip(identifier)
    if not server_ip:
        await ctx.send(f"Server {identifier} is not in the monitoring list.")
        return
    channel_id = server_data[server_ip].get("channel_id")
    channel = ctx.guild.get_channel(channel_id)
    if channel:
        await channel.delete(reason="Server removed from monitoring")
    del server_data[server_ip]
    save_servers()
    await ctx.send(f"Server {identifier} has been removed from monitoring.")

bot.run("TOKEN")
