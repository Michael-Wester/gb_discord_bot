from discord.ext import commands
import emulator as emulator
import os
import psutil;
import gc


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
        
        if (int(message.author.id) != int(os.environ['DEV_ID'])) and int(message.author.id) != int(os.environ['TEST_ID']):
            print("Not dev")
            return

        cmd = str(message.content)[1:]

        if cmd == "reload":
            await message.channel.send("Reloading...")
            await self.bot.reload_extension("cogs.cog_reload")
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    print(f"Reloaded {filename}")
                    await self.bot.reload_extension(f"cogs.{filename[:-3]}")           
            await message.channel.send("Reloaded!")
            return
        
        if cmd == "memory":
            await message.channel.send("Memory usage: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2) + " MB")
            return
        
        if cmd == "gc":
            gc.collect()
            await message.channel.send("Garbage collected!")
            return

        return
    
    

async def setup(bot):
    await bot.add_cog(cog_reload(bot))


