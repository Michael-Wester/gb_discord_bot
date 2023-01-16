import os
import discord
import emulator as emulator
import asyncio
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
