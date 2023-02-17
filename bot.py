import os
import discord
import emulator as emulator
import asyncio
from discord.ext import commands
import dotenv
import database as db


def run():
    dotenv.load_dotenv()
    
    TOKEN = os.environ['DISCORD_TOKEN']
    CONNECTION_STRING = os.environ['CONNECTION_STRING']

    bot = commands.Bot(command_prefix="", intents=discord.Intents.all())
    bot.db = db.Database(CONNECTION_STRING)
    bot.db.connect()

    async def load():
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")

    async def main():
        await load()
        await bot.start(TOKEN)
        

    asyncio.run(main())
    

