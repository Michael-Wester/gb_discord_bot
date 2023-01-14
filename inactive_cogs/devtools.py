import discord
from discord.ext import commands
import emulator as emulator
import time


class cog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('cog1 loaded')
        
        
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
        
        if cmd == "id":
            await message.channel.send(
            "ID: "
            + str(message.guild.id)
            + "\n Name: "
            + str(message.guild.name)
        )
        return