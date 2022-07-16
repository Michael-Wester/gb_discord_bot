import os
import discord
from emulator import *
from dotenv import load_dotenv
import constants as c


def run():
    
    load_dotenv()
    #TOKEN = os.getenv('DISCORD_TOKEN')
    #print(os.environ['DISCORD_TOKEN'])
    TOKEN = "OTU3MTMzNTk3NTc0MzIwMTk5.Yj6WIA.0o76rG4R93TGu7xxVa_pS2C3OWc"
    
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content == '!help':
            await message.channel.send('Commands are: !up, !down, !left, !right, !start, !select, !a, !b, !quit, !help')
            return
        if message.content == '!quit':
            await message.channel.send('Quitting...')
            return
        if message.content == '!meme':
            await message.channel.send('Memeing...')
            return
        if message.content == '!meme2':
            await message.channel.send('Memeing2...')
            return
        if message.content == '!meme3':
            await message.channel.send('Memeing2...')
            return
        if message.content == '!a':
            a_button()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!b':
            b_button()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!up':
            up()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!down':
            down()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!left':
            left()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!right':
            right()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!start':
            start()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!select':
            select()
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content.startswith('!'):
            await message.channel.send('Command not found. Type !help for a list of commands.')
            return

    client.run(TOKEN)





