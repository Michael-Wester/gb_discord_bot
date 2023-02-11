import discord
from discord.ext import commands
import emulator as emulator
import time
import menu_class as m
import server_properties_editor as p
import time
import os
from pyboy_instance import pyboy_gb, pyboy_gbc
import button_helper as bh


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
        
        if cmd == "button":
            embed, file = bh.press_button(server_id, message.author.name, "None")
            await message.channel.send(file=file, embed=embed, view=m.Menu())
            await message.channel.send( "Command executed in " + str(round(time.time() - time_start, 2)) + " seconds.")
            return
        return
        
            

            
async def setup(bot):
    await bot.add_cog(move_button(bot))
