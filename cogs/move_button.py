import discord
from discord.ext import commands
import emulator as emulator
import time
import asyncio

import menu_class as m


from pyboy import WindowEvent as we
import server_properties_editor as p
import time
import image_helper as h
import os
import constants as c
from emulator import Emulator
from pyboy_instance import pyboy_gb, pyboy_gbc
import gc
import asyncio



class move_button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pyboy_gb = pyboy_gb 
        self.pyboy_gbc = pyboy_gbc

    @commands.Cog.listener()
    async def on_ready(self):
        print("move_button loaded")
        

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
            print("Server properties not found.")
        if str(message.content)[0:1] != prefix:
            return
        
        
        def save_emulator_image(emulator_img):
            if cmd in c.cmd_list:
                p.record_cmd(server_id, cmd, message.author.name)
            img_filepath = h.save_image(emulator_img, server_id)
            return img_filepath

        
        if (p.read_value(server_id, "game_type") in ["red", "blue", "yellow"]):
            self.pyboy = self.pyboy_gb
        else:
            self.pyboy = self.pyboy_gbc
            
        emulator = Emulator(server_id, self.pyboy)
        emulator.load_game()


        img = emulator.save_screenshot()
        img_filepath = save_emulator_image(img)
        emulator.save()

        if cmd == "button":
            file = discord.File(img_filepath, filename="default.png")
            embed = discord.Embed()
            embed.set_image(url="attachment://default.png")
            await message.channel.send(file=file, embed=embed, view=m.Menu())
            
async def setup(bot):
    await bot.add_cog(move_button(bot))
