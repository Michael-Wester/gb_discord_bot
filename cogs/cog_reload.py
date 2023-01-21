import discord
from discord.ext import commands
import emulator as emulator
import time
import os


class cog_reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog reloader loaded")

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


        if cmd == "reload":
            await message.channel.send("Reloading...")
            await self.bot.reload_extension("cogs.cog_reload")
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    print(f"Reloaded {filename}")
                    await self.bot.reload_extension(f"cogs.{filename[:-3]}")
            
            
            await message.channel.send("Reloaded!")
            return

        return
    
    

async def setup(bot):
    await bot.add_cog(cog_reload(bot))


