import discord
from discord.ext import commands
import emulator as emulator
from pyboy import WindowEvent as we
import server_properties_editor as properties
import time
import image_helper as h
import os
import constants as c


class movement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("movement loaded")

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
            prefix = properties.read_server_property_value(server_id, "prefix")
        except:
            print("Server properties not found.")
        if str(message.content)[0:1] != prefix:
            return

        def save_emulator_image(emulator_img):
            properties.increase_turn_count(server_id)
            if cmd in c.cmd_list:
                properties.add_to_command_list(
                    server_id,
                    cmd,
                    properties.read_server_property_value(server_id, "turn_count"),
                    message.author.name,
                    time.time(),
                )
            img_file_path = h.save_image(emulator_img, server_id)
            return img_file_path

        def check(msg):
            return (
                msg.author == message.author
                and msg.channel == message.channel
                and msg.content.lower() in c.list_of_games
                or msg.content.lower() in [prefix + "y", prefix + "n"]
            )

        if cmd == "a":
            img_file_path = save_emulator_image(
                emulator.command(server_id, we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A)
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "b":
            img_file_path = save_emulator_image(
                emulator.command(server_id, we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B)
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "up":
            img_file_path = save_emulator_image(
                emulator.command(server_id, we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP)
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "down":
            img_file_path = save_emulator_image(
                emulator.command(server_id, we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN)
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "left":
            img_file_path = save_emulator_image(
                emulator.command(server_id, we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT)
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "right":
            img_file_path = save_emulator_image(
                emulator.command(
                    server_id, we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT
                )
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "start":
            img_file_path = save_emulator_image(
                emulator.command(
                    server_id, we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START
                )
            )
            await message.channel.send(file=discord.File(img_file_path))
            return
        if cmd == "select":
            img_file_path = save_emulator_image(
                emulator.command(
                    server_id, we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT
                )
            )
            await message.channel.send(file=discord.File(img_file_path))
            return

        print("Unrecognised command")
        return


async def setup(bot):
    await bot.add_cog(movement(bot))
