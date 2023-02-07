import discord
from discord.ext import commands
import emulator as emulator
import server_properties_editor as properties
import server_list_csv_editor as serverlist
import time
import asyncio
import constants as c
import os


class newgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("newgame loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name
        server_folder_path = "servers/" + str(server_id) + "/"
        cmd = str(message.content)[1:]
        time_start = time.time()

        if os.path.exists(server_folder_path) == True:
            prefix = properties.read_value(server_id, "prefix")
            await message.channel.send(
                "Please reset the game using " + prefix + "reset before starting a new game"
            )
            return
        
        def check(msg):
                return (
                    msg.author == message.author
                    and msg.channel == message.channel
                )

        if cmd == "newgame":

            try:
                await message.channel.send(
                    "Which pokemon game would you like to play? Use "
                    + c.cmd_prefix
                    + "games to see a list of games"
                )
                games_list = []
                for cmd in c.list_of_games:
                    games_list.append(c.cmd_prefix + cmd)
                embed = discord.Embed(
                    title="Games list",
                    url=c.games_image,
                    description="Here is a list of supported Pokemon games",
                    color=0x004080,
                )
                embed.add_field(
                    name="Commands to use", value=str(games_list), inline=False
                )
                embed.set_image(url=c.games_gif)
                await message.channel.send(embed=embed)
                msg = await client.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await message.channel.send(
                    c.octagonal_sign
                    + "**Sorry "
                    + str(message.author)
                    + ", either you didn't reply in time or you didn't reply with a valid game type**"
                    + c.octagonal_sign
                )
                return
            game_type = msg.content.lower().strip(c.cmd_prefix)
            
            if game_type in c.list_of_games:
                serverlist.create_serverlist()
                serverlist.add_rows(server_id, server_name, game_type)
                properties.initialise_property_file(server_id, server_name, game_type)
                properties.copy_emulator_files(server_id, game_type)
                await message.channel.send(
                    "Game has initiated! Use "
                    + c.cmd_prefix
                    + "a to start the game and "
                    + c.cmd_prefix
                    + "help for a list of commands"
                )
                return
            else:
                await message.channel.send(
                    c.octagonal_sign
                    + "**Sorry "
                    + str(message.author)
                    + ", You didn't reply with a valid game type**"
                    + c.octagonal_sign
                )
                return
        if cmd == "reset":
            await message.channel.send(
            "Are you sure you want to reset the server? (y/n)"
            )
            try:
                msg = await client.wait_for("message", check=check, timeout=300)
            except asyncio.TimeoutError:
                await message.send("Sorry, you didn't reply in time!")
                return
            if msg.content.lower() == "y" or "!y" or "yes" or "!yes":
                serverlist.delete_server(server_id)
                properties.delete_server_folder(server_id)
                await message.channel.send(
                    "Server has been reset. Server files are held for 7 days before being permanently deleted. Contact Michle#4142 if you need to restore them"
                )
                return
            else:
                await message.channel.send(
                    c.octagonal_sign
                    + "server reset cancelled"
                    + c.octagonal_sign
                )
                return
        return



async def setup(bot):
    await bot.add_cog(newgame(bot))
