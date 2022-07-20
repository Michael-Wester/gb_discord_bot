from itertools import count
import os
from unicodedata import name
import discord
from jinja2 import pass_context
from azblobstorage import download_save_state
from emulator import *
from dotenv import load_dotenv
import constants as c
from emulator import *


def run():
    
    load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']
    
    client = discord.Client()

    @client.event
    async def on_ready():
        download_save_state()
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
        if message.content == '!download':
            count1 = download_save_state()
            await message.channel.send('downloading ' + str(count1) + ' blobs')
            return
        if message.content == '!upload':
            count2 = upload_save_state()
            await message.channel.send('uploading ' + str(count2) + ' blobs')
            return
        if message.content == '!keycheck':
            AZURE_STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING'] # In Azure there needs to be quotes around the connection string in variables
            await message.channel.send('Token = ' + AZURE_STORAGE_CONNECTION_STRING)
            return
        if message.content == '!id':
            await message.channel.send("ID:" + str(message.guild.id) + "\n Name: " + str(message.guild.name))
            return
        if message.content.startswith('!'):
            await message.channel.send('Command not found. Type !help for a list of commands.')
            return

    client.run(TOKEN)





