import json
import os
import subprocess
from datetime import datetime

import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
IP = os.getenv("IP")
SERVER_DIRECTORY = os.getenv("SERVER_DIRECTORY")


class Minecraft(commands.Cog):
    """Basic Features"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.server = None

    @app_commands.command(name="mc", description="Show status of minecraft server")
    async def minecraft(self, interaction: discord.Interaction):
        """Show status of minecraft server"""
        url = requests.get(
            f"https://minecraft-api.com/api/ping/{IP}/25565/json", timeout=100
        )
        url2 = requests.get(
            f"https://minecraft-api.com/api/ping/response/{IP}/25565/json", timeout=100
        )
        if not url.text.__contains__("players"):
            await interaction.response.send_message("Server is offline")
        else:
            text = json.loads(url.text)
            modpack_name = text["modpackData"]["name"]
            minecraft_version = text["version"]["name"]
            ping = json.loads(url2.text)["response"]
            players_online = text["players"]["online"]
            all_players = ""
            if players_online != 0:
                for player in text["players"]["sample"]:
                    all_players += f'`{player["name"]} - {player["id"]} `\n'
            if len(all_players) == 0:
                all_players = "Nobody online 🥲"
            embed = discord.Embed(title="Minecraft Server Status")
            embed.add_field(name="Modpack Name", value=modpack_name, inline=True)
            embed.add_field(
                name="Minecraft Version", value=minecraft_version, inline=True
            )
            embed.add_field(name="Ping", value=f"{ping}ms", inline=False)
            embed.add_field(
                name=f"Players Online - {players_online}",
                value=all_players,
                inline=False,
            )
            embed.timestamp = datetime.now()
            embed.set_footer(
                text=f"{interaction.user}", icon_url=interaction.user.avatar
            )
            embed.set_image(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fvignette.wikia.nocookie.net%2Fstevethetrooper%2Fimages%2F2%2F25%2FThumbnail_minecraft_zps277f5003.png%2Frevision%2Flatest%3Fcb%3D20140102163508&f=1&nofb=1"
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="start", description="Starts the minecraft server")
    async def start(self, interaction: discord.Interaction):
        # os.chdir(os.getenv("SERVER_DIRECTORY"))
        await interaction.response.defer()
        await interaction.followup.send("server starting")
        self.server = subprocess.Popen(
            f"powershell.exe -ExecutionPolicy RemoteSigned -file {SERVER_DIRECTORY}",
            shell=True,
            stdin=subprocess.PIPE,
            text=True,
        )


# async def setup(bot: commands.Bot) -> None:
#     await bot.add_cog(Minecraft(bot))
#     print("Minecraft is Loaded")
