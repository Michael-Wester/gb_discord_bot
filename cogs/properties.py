import discord
from discord.ext import commands
import emulator as emulator
import server_properties_editor as p
import server_list_csv_editor as serverlist
import time
import image_helper as h
import os
import asyncio
import constants as c
from PIL import Image


class properties_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("properties loaded")

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

        if os.path.exists(server_folder_path) == False:
            return

        try:
            prefix = p.read_value(server_id, "prefix")
        except:
            print("Server properties not fzzound.")

        if str(message.content)[0:1] != prefix:
            return
        def check(msg):
            return (
                msg.author == message.author
                and msg.channel == message.channel
            )

        if cmd == "help":
            cmd_list = []
            for cmd in c.cmd_list:
                cmd_list.append(prefix + cmd)
            await message.channel.send(
                "The following commands are available: " + str(cmd_list) + " Compound commands can also be used with " + c.cmd_compound_prefix
            )
            return
        if cmd == "games":
            games_list = []
            for cmd in c.list_of_games:
                games_list.append(prefix + cmd)
            embed = discord.Embed(
                title="Games list",
                url=c.games_image,
                description="Here is a list of supported Pokemon games",
                color=0x004080,
            )
            embed.add_field(name="Commands to use", value=str(games_list), inline=False)
            embed.set_image(url=c.games_gif)
            await message.channel.send(embed=embed)
            return

        if cmd == "newgame":
            await message.channel.send(
                "Please reset the game using "
                + prefix
                + "reset before starting a new game"
            )
            return
        if cmd == "info":
            await message.channel.send(
                "This bot is currently in beta. Please report any bugs to Michle#4142"
            )
        if cmd.startswith("recap"):
            cmd = cmd.split(" ")
            turn_number = int(
                p.read_value(server_id, "turn_count")
            )
            if len(cmd) == 1:
                await message.channel.send("Please enter a turn number to recap from")
                return
            if cmd[1] == "*":
                await message.channel.send("Recapping from turn 1...")
                images = []
                i = 1
                while i < turn_number:
                    image = Image.open(
                        server_folder_path
                        + "/images/"
                        + str(server_id)
                        + "_"
                        + str(i)
                        + ".png"
                    )
                    images.append(image)
                    i += 1
                h.make_gif(images, server_folder_path + "/images/recap.gif")
                await message.channel.send(
                    file=discord.File(server_folder_path + "/images/recap.gif")
                )
                return
            if not cmd[1].isdigit():
                await message.channel.send("Please enter a valid turn number")
                return
            if int(cmd[1]) > int(
                p.read_value(server_id, "turn_count")
            ):
                await message.channel.send(
                    "Please enter a turn number that is less than the current turn number"
                )
                return
            if int(cmd[1]) < 1:
                await message.channel.send(
                    "Please enter a turn number that is greater than 0"
                )
                return
            await message.channel.send("Recapping from turn " + cmd[1] + "...")
            images = []
            i = turn_number - int(cmd[1])
            while i < turn_number:
                image = Image.open(
                    server_folder_path
                    + "/images/"
                    + str(server_id)
                    + "_"
                    + str(i)
                    + ".png"
                )
                images.append(image)
                i += 1
            h.make_gif(images, server_folder_path, "/recap.gif", server_id)
            await message.channel.send(
                file=discord.File(server_folder_path + "/recap.gif")
            )
            return
        if cmd.startswith("prefix"):
            cmd = cmd.split(" ")
            if len(cmd) == 1:
                await message.channel.send("Please enter a prefix")
                return
            if len(cmd[1]) > 1:
                await message.channel.send(
                    "Please enter a prefix that is only 1 character long"
                )
                return
            p.update_server_property_value(server_id, "prefix", cmd[1])
            await message.channel.send("Prefix has been set to " + cmd[1])
            return
        if cmd.startswith("press_tick"):
            cmd = cmd.split(" ")
            if not cmd[1].isdigit():
                await message.channel.send("Please enter a number")
                return
            if int(cmd[1]) < 1:
                await message.channel.send(
                    "Please enter a tick value that is greater than 0"
                )
                return
            p.update_server_property_value(server_id, "press_tick", cmd[1])
            await message.channel.send("Press tick has been set to " + cmd[1])
            return
        if cmd.startswith("release_tick"):
            cmd = cmd.split(" ")
            if len(cmd) == 1:
                await message.channel.send("Please enter a tick value")
                return
            if not cmd[1].isdigit():
                await message.channel.send("Please enter a number")
                return
            if int(cmd[1]) < 1:
                await message.channel.send(
                    "Please enter a tick value that is greater than 0"
                )
                return
            p.update_server_property_value(server_id, "release_tick", cmd[1])
            await message.channel.send("Release tick has been set to " + cmd[1])
            return
        if cmd.startswith("cmd_set"):
            cmd = cmd.split(" ")
            if len(cmd) == 1:
                await message.channel.send("Please enter a command set")
                return
            if not cmd[1].isdigit():
                await message.channel.send("Please enter a number")
                return
            p.update_server_property_value(server_id, "cmd_set", cmd[1])
            await message.channel.send("Command set has been set to " + cmd[1])
            return
        if cmd.startswith("bar_colour"):
            cmd = cmd.split(" ")
            if cmd[1] not in [
                "red",
                "green",
                "blue",
                "yellow",
                "orange",
                "purple",
                "pink",
                "white",
                "black",
            ]:
                await message.channel.send("Please enter a valid colour")
                return
            p.update_server_property_value(server_id, "bar_colour", cmd[1])
            await message.channel.send("Bar colour has been set to " + cmd[1])
            return
        if cmd == "reinit":
            p.reinitialise_property_file(server_id)


async def setup(bot):
    await bot.add_cog(properties_cog(bot))
