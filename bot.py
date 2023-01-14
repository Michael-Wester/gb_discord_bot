import os
import discord
import server_properties_editor as properties
import server_list_csv_editor as serverlist
import emulator as emulator
from pyboy import WindowEvent as we
import asyncio
import constants as c
import image_helper as h
import time
from PIL import Image
from discord.ext import commands


def run():
    TOKEN = os.environ["DISCORD_TOKEN"]
        
    bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

    async def load():
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")

    async def main():
        await load()
        await bot.start(TOKEN)
        
    asyncio.run(main())

