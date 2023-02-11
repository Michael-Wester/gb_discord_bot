import discord
from discord.ext import commands
import emulator as emulator
from pyboy import WindowEvent as we
import server_properties_editor as p
import time
import image_helper as h
import os
import constants as c
from emulator import Emulator
from pyboy_instance import pyboy_gb, pyboy_gbc
import gc
import menu_class as m
import button_helper as bh

class movement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pyboy_gb = pyboy_gb 
        self.pyboy_gbc = pyboy_gbc

    @commands.Cog.listener()
    async def on_ready(self):
        print("movement loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        if message.author == client.user:
            return
        server_id = message.guild.id
        server_folder_path = "servers/" + str(server_id) + "/"
        cmd = str(message.content)[1:]
        time_start = time.time()
        
        if os.path.exists(server_folder_path) == False:
            return
        try:
            prefix = p.read_value(server_id, "prefix")
        except:
            print("Server properties not found.")
        if str(message.content)[0:1] != prefix:
            return
        
        if cmd not in c.cmd_list:
            return

        embed, file = bh.press_button(server_id, message.author.name, cmd)
        
        await message.channel.send(file=file)
        await message.channel.send( "Command executed in " + str(round(time.time() - time_start, 2)) + " seconds.")
        return
        

async def setup(bot):
    await bot.add_cog(movement(bot))
